from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    full_name: Optional[str] = Field(None, description="Nom complet de l'utilisateur")
    is_active: bool = Field(True, description="Indique si l'utilisateur est actif")
    is_superuser: bool = Field(False, description="Indique si l'utilisateur est un superutilisateur")

class UserCreate(UserBase):
    password: str = Field(..., description="Mot de passe de l'utilisateur", min_length=8)

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, description="Nouveau mot de passe de l'utilisateur", min_length=8)

class UserInDB(UserBase):
    id: str = Field(..., description="ID unique de l'utilisateur")
    hashed_password: str = Field(..., description="Mot de passe hashé de l'utilisateur")
    created_at: str = Field(..., description="Date de création de l'utilisateur")
    updated_at: Optional[str] = Field(None, description="Date de dernière mise à jour de l'utilisateur")

    @field_validator('created_at', 'updated_at')
    def parse_datetime(cls, v):
        if v is None:
            return None
        try:
            return datetime.fromisoformat(v).isoformat()
        except ValueError:
            return v

class Token(BaseModel):
    access_token: str = Field(..., description="Token JWT d'accès")
    token_type: str = Field(..., description="Type de token (bearer)")

class TokenData(BaseModel):
    email: Optional[str] = Field(None, description="Email associé au token")

class User(UserBase):
    id: str = Field(..., description="ID unique de l'utilisateur")
    created_at: str = Field(..., description="Date de création de l'utilisateur")
    updated_at: Optional[str] = Field(None, description="Date de dernière mise à jour de l'utilisateur")
    last_login: Optional[str] = Field(None, description="Date de dernière connexion")

    @field_validator('created_at', 'updated_at', 'last_login')
    def parse_datetime(cls, v):
        if v is None:
            return None
        try:
            return datetime.fromisoformat(v).isoformat()
        except ValueError:
            return v

    class Config:
        from_attributes = True 