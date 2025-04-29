from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class StepType(str, Enum):
    WEB = "web"
    TEMPLATE = "template"
    PDF = "pdf"
    AI = "ai"

class Step(BaseModel):
    type: StepType = Field(..., description="Type d'étape")
    details: Dict[str, Any] = Field(..., description="Détails spécifiques à l'étape")
    order: int = Field(..., description="Ordre d'exécution de l'étape")

class ScenarioBase(BaseModel):
    name: str = Field(..., description="Nom du scénario", min_length=1)
    description: Optional[str] = Field(None, description="Description du scénario")
    steps: List[Step] = Field(..., description="Liste des étapes du scénario")
    tags: Optional[List[str]] = Field([], description="Tags associés au scénario")

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nom du scénario", min_length=1)
    description: Optional[str] = Field(None, description="Description du scénario")
    steps: Optional[List[Step]] = Field(None, description="Liste des étapes du scénario")
    tags: Optional[List[str]] = Field(None, description="Tags associés au scénario")

class ScenarioInDB(ScenarioBase):
    id: str = Field(..., description="ID unique du scénario")
    created_at: datetime = Field(..., description="Date de création du scénario")
    updated_at: Optional[datetime] = Field(None, description="Date de dernière mise à jour du scénario")
    created_by: str = Field(..., description="ID de l'utilisateur qui a créé le scénario")
    status: str = Field(..., description="Statut du scénario (draft, active, archived)")

class ScenarioExecution(BaseModel):
    scenario_id: str = Field(..., description="ID du scénario à exécuter")
    parameters: Optional[Dict[str, Any]] = Field({}, description="Paramètres d'exécution du scénario")

class ExecutionResult(BaseModel):
    execution_id: str = Field(..., description="ID de l'exécution")
    scenario_id: str = Field(..., description="ID du scénario exécuté")
    status: str = Field(..., description="Statut de l'exécution (success, failed, in_progress)")
    results: List[Dict[str, Any]] = Field(..., description="Résultats de chaque étape")
    started_at: datetime = Field(..., description="Date de début d'exécution")
    completed_at: Optional[datetime] = Field(None, description="Date de fin d'exécution")
    error: Optional[str] = Field(None, description="Message d'erreur en cas d'échec") 