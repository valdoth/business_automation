from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.models.user import UserCreate, UserInDB
from src.db.session import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.core.config import settings
from src.db import get_storage
import json
import uuid
import io

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(username: str, password: str, db: Session) -> Optional[UserInDB]:
    # TODO: Implement actual user lookup from database
    # This is a placeholder implementation
    user = db.query(UserInDB).filter(UserInDB.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def create_user(user_data: dict) -> dict:
    storage = get_storage()
    user_id = str(uuid.uuid4())
    user_data["id"] = user_id
    user_data["hashed_password"] = get_password_hash(user_data["password"])
    user_data["created_at"] = datetime.utcnow().isoformat()
    del user_data["password"]
    
    # Stocker l'utilisateur dans MinIO
    user_key = f"users/{user_id}.json"
    user_json = json.dumps(user_data)
    data = io.BytesIO(user_json.encode('utf-8'))
    storage.put_object(
        settings.MINIO_BUCKET,
        user_key,
        data,
        len(user_json)
    )
    
    return user_data

async def get_user_by_email(email: str) -> Optional[dict]:
    storage = get_storage()
    try:
        # Lister tous les objets dans le dossier users
        objects = storage.list_objects(settings.MINIO_BUCKET, prefix="users/")
        for obj in objects:
            data = storage.get_object(settings.MINIO_BUCKET, obj.object_name)
            user = json.loads(data.read())
            if user["email"] == email:
                return user
    except Exception:
        return None
    return None

async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"} 