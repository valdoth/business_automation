from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from ..models.base import Variable
from ..db.neo4j import db

router = APIRouter()

@router.get("/", response_model=List[Variable])
async def get_all_variables():
    """Get all variables"""
    try:
        variables = db.get_all_variables()
        return variables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Variable)
async def create_variable(variable: Variable):
    """Create a new variable"""
    variable.id = str(uuid.uuid4())
    variable.created_at = datetime.utcnow()
    variable.updated_at = datetime.utcnow()
    
    try:
        db.create_variable(variable.dict())
        return variable
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/document/{document_id}", response_model=List[Variable])
async def get_document_variables(document_id: str):
    """Get all variables for a document"""
    try:
        variables = db.get_document_variables(document_id)
        return variables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{variable_id}", response_model=Variable)
async def update_variable(variable_id: str, variable: Variable):
    """Update a variable"""
    try:
        updated_variable = db.update_variable(variable_id, variable.dict())
        if not updated_variable:
            raise HTTPException(status_code=404, detail="Variable not found")
        return updated_variable
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 