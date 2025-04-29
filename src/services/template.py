from typing import Dict, Any
from jinja2 import Template, Environment, FileSystemLoader
import os

class TemplateProcessor:
    def __init__(self, template_dir: str = "templates"):
        """
        Initialise le processeur de templates.
        
        Args:
            template_dir: Le répertoire contenant les templates
        """
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
        
    def process_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Traite un template avec le contexte donné.
        
        Args:
            template_name: Le nom du template à traiter
            context: Le contexte à utiliser pour le template
            
        Returns:
            str: Le contenu traité du template
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
        
    def process_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        Traite une chaîne de caractères comme un template.
        
        Args:
            template_string: La chaîne de caractères à traiter
            context: Le contexte à utiliser pour le template
            
        Returns:
            str: Le contenu traité du template
        """
        template = Template(template_string)
        return template.render(**context) 