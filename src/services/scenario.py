from typing import List, Dict, Any, Optional
from fastapi import UploadFile
from src.services.pdf import extract_text_from_pdf
from src.services.web import WebAutomation
from src.services.template import TemplateProcessor
from src.core.config import settings
import json
import uuid
from datetime import datetime
from src.db import get_storage
import io

class ScenarioService:
    def __init__(self):
        self.web_automation = WebAutomation()
        self.template_processor = TemplateProcessor()
        self.storage = get_storage()
        self.bucket = settings.MINIO_BUCKET

    async def create_scenario_from_pdf(self, pdf_file: UploadFile) -> Dict[str, Any]:
        # Extraire le texte du PDF
        text = await extract_text_from_pdf(pdf_file)
        
        # Analyser le texte pour extraire les étapes du scénario
        scenario_data = self._parse_scenario_text(text)
        
        # Créer un ID unique pour le scénario
        scenario_id = str(uuid.uuid4())
        
        # Sauvegarder le scénario dans Neo4j
        scenario = {
            "id": scenario_id,
            "name": scenario_data.get("name", "Unnamed Scenario"),
            "description": scenario_data.get("description", ""),
            "steps": scenario_data.get("steps", []),
            "created_at": datetime.utcnow().isoformat(),
            "status": "draft"
        }
        
        # TODO: Implémenter la sauvegarde dans Neo4j
        # self._save_to_neo4j(scenario)
        
        return scenario

    def _parse_scenario_text(self, text: str) -> Dict[str, Any]:
        # Exemple de format attendu dans le PDF :
        # Nom du scénario: [nom]
        # Description: [description]
        # Étapes:
        # 1. [type]: [détails]
        # 2. [type]: [détails]
        
        lines = text.split('\n')
        scenario = {
            "name": "",
            "description": "",
            "steps": []
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("Nom du scénario:"):
                scenario["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("Description:"):
                scenario["description"] = line.split(":", 1)[1].strip()
            elif line.startswith("Étapes:"):
                current_section = "steps"
            elif current_section == "steps" and line[0].isdigit():
                step_parts = line.split(":", 1)
                if len(step_parts) == 2:
                    step_type = step_parts[0].split(".", 1)[1].strip()
                    step_details = step_parts[1].strip()
                    scenario["steps"].append({
                        "type": step_type,
                        "details": json.loads(step_details)
                    })
        
        return scenario

    async def execute_scenario(self, scenario_id: str) -> Dict[str, Any]:
        # Récupérer le scénario depuis Neo4j
        # scenario = self._get_from_neo4j(scenario_id)
        
        # TODO: Implémenter la récupération depuis Neo4j
        scenario = {
            "id": scenario_id,
            "steps": []
        }
        
        results = []
        for step in scenario["steps"]:
            if step["type"] == "web":
                result = await self._execute_web_step(step["details"])
            elif step["type"] == "template":
                result = await self._execute_template_step(step["details"])
            else:
                result = {"error": f"Type de step non supporté: {step['type']}"}
            
            results.append(result)
        
        return {
            "scenario_id": scenario_id,
            "results": results,
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat()
        }

    async def _execute_web_step(self, details: Dict[str, Any]) -> Dict[str, Any]:
        try:
            await self.web_automation.navigate(details["url"])
            for action in details.get("actions", []):
                if action["type"] == "click":
                    await self.web_automation.click(action["selector"])
                elif action["type"] == "fill":
                    await self.web_automation.fill(action["selector"], action["value"])
                elif action["type"] == "submit":
                    await self.web_automation.submit(action["selector"])
            
            return {"status": "success", "message": "Web step executed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _execute_template_step(self, details: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.template_processor.process_template(
                details["template_name"],
                details.get("variables", {})
            )
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def list_scenarios(self) -> List[dict]:
        try:
            scenarios = []
            objects = self.storage.list_objects(self.bucket, prefix="scenarios/")
            for obj in objects:
                data = self.storage.get_object(self.bucket, obj.object_name)
                scenario = json.loads(data.read().decode('utf-8'))
                scenarios.append(scenario)
            return scenarios
        except Exception as e:
            print(f"Erreur lors de la récupération des scénarios: {str(e)}")
            return []

    async def get_scenario(self, scenario_id: str) -> Optional[dict]:
        try:
            scenario_key = f"scenarios/{scenario_id}.json"
            data = self.storage.get_object(self.bucket, scenario_key)
            return json.loads(data.read().decode('utf-8'))
        except Exception:
            return None

    async def create_scenario(self, scenario_data: dict) -> dict:
        scenario_id = str(uuid.uuid4())
        scenario_data["id"] = scenario_id
        scenario_key = f"scenarios/{scenario_id}.json"
        scenario_json = json.dumps(scenario_data)
        data = io.BytesIO(scenario_json.encode('utf-8'))
        
        self.storage.put_object(
            self.bucket,
            scenario_key,
            data,
            len(scenario_json)
        )
        
        return scenario_data 