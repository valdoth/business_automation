from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from src.services.variable import VariableService
import logging

router = APIRouter(prefix="/variables", tags=["variables"])
logger = logging.getLogger(__name__)

@router.post("/")
async def create_variable(variable: Dict[str, Any]):
    """
    Crée une nouvelle variable.
    """
    try:
        variable_service = VariableService()
        result = await variable_service.create_variable(variable)
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la création de la variable: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_variables():
    """
    Liste toutes les variables disponibles.
    """
    try:
        variable_service = VariableService()
        variables = await variable_service.list_variables()
        return variables
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des variables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{variable_id}")
async def get_variable(variable_id: str):
    """
    Récupère une variable spécifique par son ID.
    """
    try:
        variable_service = VariableService()
        variable = await variable_service.get_variable(variable_id)
        if not variable:
            raise HTTPException(status_code=404, detail="Variable non trouvée")
        return variable
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la variable: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{variable_id}")
async def update_variable(variable_id: str, variable: Dict[str, Any]):
    """
    Met à jour une variable existante.
    """
    try:
        variable_service = VariableService()
        result = await variable_service.update_variable(variable_id, variable)
        if not result:
            raise HTTPException(status_code=404, detail="Variable non trouvée")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de la variable: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{variable_id}")
async def delete_variable(variable_id: str):
    """
    Supprime une variable.
    """
    try:
        variable_service = VariableService()
        result = await variable_service.delete_variable(variable_id)
        if not result:
            raise HTTPException(status_code=404, detail="Variable non trouvée")
        return {"message": "Variable supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la variable: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 