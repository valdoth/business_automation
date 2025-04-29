from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.security import Token, get_current_user
from src.services.auth import login_for_access_token, create_user
from src.models.user import UserCreate, User
from src.db.session import get_db

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return await login_for_access_token(form_data, db)

@router.post("/register", response_model=User)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = await create_user(user, db)
    return db_user

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Implement actual user lookup
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 