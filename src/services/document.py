from typing import Dict, Any, List
from fastapi import UploadFile
from src.db.session import get_db
import uuid
from datetime import datetime

class DocumentService:
    @staticmethod
    async def create_document(document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un nouveau document.
        """
        document_id = str(uuid.uuid4())
        document_data = {
            "id": document_id,
            "name": document.get("name", "Unnamed Document"),
            "description": document.get("description", ""),
            "created_at": datetime.utcnow().isoformat(),
            "status": "draft"
        }
        
        with get_db() as session:
            # Créer le document dans Neo4j
            query = """
            CREATE (d:Document {
                id: $id,
                name: $name,
                description: $description,
                created_at: $created_at,
                status: $status
            })
            RETURN d
            """
            result = session.run(query, **document_data)
            return document_data

    @staticmethod
    async def list_documents() -> List[Dict[str, Any]]:
        """
        Liste tous les documents.
        """
        with get_db() as session:
            query = """
            MATCH (d:Document)
            RETURN d
            """
            result = session.run(query)
            return [dict(record["d"]) for record in result]

    @staticmethod
    async def get_document(document_id: str) -> Dict[str, Any]:
        """
        Récupère un document par son ID.
        """
        with get_db() as session:
            query = """
            MATCH (d:Document {id: $id})
            RETURN d
            """
            result = session.run(query, id=document_id)
            record = result.single()
            if record:
                return dict(record["d"])
            return None

    @staticmethod
    async def upload_file(document_id: str, file: UploadFile) -> Dict[str, Any]:
        """
        Télécharge un fichier pour un document.
        """
        # Lire le contenu du fichier
        content = await file.read()
        
        with get_db() as session:
            # Mettre à jour le document avec les informations du fichier
            query = """
            MATCH (d:Document {id: $id})
            SET d.filename = $filename,
                d.content_type = $content_type,
                d.file_size = $file_size,
                d.updated_at = $updated_at
            RETURN d
            """
            result = session.run(query,
                id=document_id,
                filename=file.filename,
                content_type=file.content_type,
                file_size=len(content),
                updated_at=datetime.utcnow().isoformat()
            )
            record = result.single()
            if record:
                return dict(record["d"])
            return None 