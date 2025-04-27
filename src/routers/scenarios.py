from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime

from ..models.base import Scenario
from ..db.neo4j import db
from ..agents.base import AIAgent

router = APIRouter()

@router.get("/", response_model=List[Scenario])
async def get_all_scenarios():
    """Get all scenarios"""
    try:
        scenarios = db.get_all_scenarios()
        return scenarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Scenario)
async def create_scenario(scenario: Scenario):
    """Create a new scenario"""
    scenario.id = str(uuid.uuid4())
    scenario.created_at = datetime.utcnow()
    scenario.updated_at = datetime.utcnow()
    
    try:
        db.create_scenario(scenario.dict())
        return scenario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{scenario_id}", response_model=Scenario)
async def get_scenario(scenario_id: str):
    """Get a scenario by ID"""
    scenario = db.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@router.post("/{scenario_id}/run")
async def run_scenario(scenario_id: str, background_tasks: BackgroundTasks):
    """Run a scenario using AI agent"""
    scenario = db.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    agent = AIAgent()
    
    async def execute_scenario():
        try:
            result = await agent.execute_scenario(scenario)
            # Update scenario status in database
            # TODO: Implement status update
            return result
        except Exception as e:
            # TODO: Implement error handling and logging
            raise
    
    background_tasks.add_task(execute_scenario)
    return {"status": "queued", "message": "Scenario execution started"} 