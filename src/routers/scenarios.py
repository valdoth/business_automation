from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any
from src.tasks.scenarios import ScenarioRunner
from src.services.scenario import ScenarioService
import logging

router = APIRouter(prefix="/scenarios", tags=["scenarios"])
logger = logging.getLogger(__name__)

@router.post("/")
async def create_scenario(scenario: Dict[str, Any]):
    """
    Crée un nouveau scénario.
    """
    try:
        scenario_service = ScenarioService()
        result = await scenario_service.create_scenario(scenario)
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la création du scénario: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_scenarios():
    """
    Liste tous les scénarios disponibles.
    """
    try:
        scenario_service = ScenarioService()
        scenarios = await scenario_service.list_scenarios()
        return scenarios
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des scénarios: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{scenario_id}")
async def get_scenario(scenario_id: str):
    """
    Récupère un scénario spécifique par son ID.
    """
    try:
        scenario_service = ScenarioService()
        scenario = await scenario_service.get_scenario(scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scénario non trouvé")
        return scenario
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du scénario: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{scenario_id}/run")
async def run_scenario(scenario_id: str):
    """
    Exécute un scénario spécifique.
    """
    try:
        runner = ScenarioRunner()
        result = await runner.run(scenario_id)
        return result
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du scénario: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{scenario_id}/steps")
async def add_step(scenario_id: str, step: Dict[str, Any]):
    """
    Ajoute une étape à un scénario existant.
    """
    try:
        scenario_service = ScenarioService()
        result = await scenario_service.add_step(scenario_id, step)
        return result
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout d'une étape: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{scenario_id}/upload")
async def upload_scenario_file(
    scenario_id: str,
    file: UploadFile = File(...)
):
    """
    Télécharge un fichier pour un scénario spécifique.
    """
    try:
        scenario_service = ScenarioService()
        result = await scenario_service.upload_file(scenario_id, file)
        return result
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du fichier: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 