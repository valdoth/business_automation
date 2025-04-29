from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from src.services.scenario import ScenarioService
from src.models.scenario import (
    ScenarioCreate,
    ScenarioUpdate,
    ScenarioInDB,
    ScenarioExecution,
    ExecutionResult
)
from src.core.security import get_current_user

router = APIRouter()
scenario_service = ScenarioService()

@router.post("/scenarios", response_model=ScenarioInDB, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario: ScenarioCreate,
    current_user: str = Depends(get_current_user)
):
    """
    Crée un nouveau scénario.
    
    - **name**: Nom du scénario
    - **description**: Description du scénario (optionnel)
    - **steps**: Liste des étapes du scénario
    - **tags**: Tags associés au scénario (optionnel)
    """
    scenario_data = scenario.dict()
    scenario_data["created_by"] = current_user
    return await scenario_service.create_scenario(scenario_data)

@router.get("/scenarios", response_model=List[ScenarioInDB])
async def list_scenarios(current_user: str = Depends(get_current_user)):
    """
    Liste tous les scénarios disponibles.
    """
    return await scenario_service.list_scenarios()

@router.get("/scenarios/{scenario_id}", response_model=ScenarioInDB)
async def get_scenario(
    scenario_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Récupère un scénario spécifique par son ID.
    """
    scenario = await scenario_service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    return scenario

@router.put("/scenarios/{scenario_id}", response_model=ScenarioInDB)
async def update_scenario(
    scenario_id: str,
    scenario: ScenarioUpdate,
    current_user: str = Depends(get_current_user)
):
    """
    Met à jour un scénario existant.
    
    - **name**: Nouveau nom du scénario (optionnel)
    - **description**: Nouvelle description du scénario (optionnel)
    - **steps**: Nouvelle liste des étapes du scénario (optionnel)
    - **tags**: Nouveaux tags associés au scénario (optionnel)
    """
    existing_scenario = await scenario_service.get_scenario(scenario_id)
    if not existing_scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    update_data = scenario.dict(exclude_unset=True)
    updated_scenario = {**existing_scenario, **update_data}
    return await scenario_service.create_scenario(updated_scenario)

@router.post("/scenarios/{scenario_id}/execute", response_model=ExecutionResult)
async def execute_scenario(
    scenario_id: str,
    execution: ScenarioExecution,
    current_user: str = Depends(get_current_user)
):
    """
    Exécute un scénario spécifique.
    
    - **scenario_id**: ID du scénario à exécuter
    - **parameters**: Paramètres d'exécution du scénario (optionnel)
    """
    scenario = await scenario_service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    return await scenario_service.execute_scenario(scenario_id, execution.parameters)

@router.post("/scenarios/from-pdf", response_model=ScenarioInDB, status_code=status.HTTP_201_CREATED)
async def create_scenario_from_pdf(
    pdf_file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    """
    Crée un scénario à partir d'un fichier PDF.
    
    - **pdf_file**: Fichier PDF contenant la description du scénario
    """
    return await scenario_service.create_scenario_from_pdf(pdf_file) 