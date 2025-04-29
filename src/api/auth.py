from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.security import Token, get_current_user
from src.services.auth import (
    create_user,
    get_user_by_email,
    verify_password,
    create_access_token
)
from src.models.user import UserCreate, UserInDB, User
from src.db.session import get_db
from datetime import timedelta
from typing import Any
from src.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> Any:
    """
    Crée un nouvel utilisateur.
    
    - **email**: Email de l'utilisateur
    - **password**: Mot de passe de l'utilisateur (minimum 8 caractères)
    - **full_name**: Nom complet de l'utilisateur (optionnel)
    - **is_active**: Statut d'activation de l'utilisateur (par défaut: True)
    - **is_superuser**: Statut de superutilisateur (par défaut: False)
    """
    # Vérifier si l'utilisateur existe déjà
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Créer l'utilisateur
    db_user = await create_user(user.dict())
    return db_user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Authentifie un utilisateur et retourne un token JWT.
    
    - **username**: Email de l'utilisateur
    - **password**: Mot de passe de l'utilisateur
    """
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: str = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur connecté.
    """
    user = await get_user_by_email(current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user 