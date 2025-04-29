from typing import Dict, Any, List
from src.services.scenario import ScenarioService
from src.services.pdf import PDFService
from src.services.template import TemplateProcessor
from src.core.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

class ScenarioRunner:
    def __init__(self):
        self.scenario_service = ScenarioService()
        self.pdf_service = PDFService()
        self.template_processor = TemplateProcessor()

    async def run(self, scenario_id: str) -> Dict[str, Any]:
        """
        Exécute un scénario spécifique.
        
        Args:
            scenario_id: L'ID du scénario à exécuter
            
        Returns:
            Dict[str, Any]: Les résultats de l'exécution du scénario
        """
        try:
            # Récupérer le scénario
            scenario = await self.scenario_service.get_scenario(scenario_id)
            if not scenario:
                raise ValueError(f"Scénario {scenario_id} non trouvé")

            # Initialiser les résultats
            results = {
                "scenario_id": scenario_id,
                "status": "running",
                "steps": []
            }

            # Exécuter chaque étape du scénario
            for step in scenario["steps"]:
                step_result = await self._execute_step(step)
                results["steps"].append(step_result)

                # Si une étape échoue, arrêter l'exécution
                if step_result["status"] == "error":
                    results["status"] = "failed"
                    break

            # Si toutes les étapes sont réussies
            if results["status"] != "failed":
                results["status"] = "completed"

            return results

        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du scénario {scenario_id}: {str(e)}")
            return {
                "scenario_id": scenario_id,
                "status": "error",
                "error": str(e)
            }

    async def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Exécute une étape individuelle du scénario.
        
        Args:
            step: Les détails de l'étape à exécuter
            
        Returns:
            Dict[str, Any]: Le résultat de l'exécution de l'étape
        """
        try:
            step_type = step.get("type")
            
            if step_type == "pdf":
                # Traitement d'un fichier PDF
                pdf_file = step.get("file")
                if not pdf_file:
                    raise ValueError("Fichier PDF manquant dans l'étape")
                    
                text = await self.pdf_service.extract_text_from_pdf(pdf_file)
                return {
                    "type": "pdf",
                    "status": "success",
                    "result": text
                }
                
            elif step_type == "template":
                # Traitement d'un template
                template_name = step.get("template")
                context = step.get("context", {})
                
                if not template_name:
                    raise ValueError("Nom du template manquant dans l'étape")
                    
                result = self.template_processor.process_template(template_name, context)
                return {
                    "type": "template",
                    "status": "success",
                    "result": result
                }
                
            else:
                raise ValueError(f"Type d'étape non supporté: {step_type}")

        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de l'étape: {str(e)}")
            return {
                "type": step.get("type"),
                "status": "error",
                "error": str(e)
            } 