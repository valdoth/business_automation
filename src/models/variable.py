from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VariableBase(BaseModel):
    name: str = Field(..., description="Nom de la variable")
    value: str = Field(..., description="Valeur de la variable")
    description: Optional[str] = Field(None, description="Description de la variable")

class VariableCreate(VariableBase):
    pass

class VariableUpdate(BaseModel):
    value: Optional[str] = Field(None, description="Nouvelle valeur de la variable")
    description: Optional[str] = Field(None, description="Nouvelle description de la variable")

class Variable(VariableBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 