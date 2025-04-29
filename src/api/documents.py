from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any
from src.services.document import DocumentService
import logging

router = APIRouter(prefix="/documents", tags=["documents"])
logger = logging.getLogger(__name__)

@router.post("/")
async def create_document(document: Dict[str, Any]):
    """
    Crée un nouveau document.
    """
    try:
        document_service = DocumentService()
        result = await document_service.create_document(document)
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la création du document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_documents():
    """
    Liste tous les documents disponibles.
    """
    try:
        document_service = DocumentService()
        documents = await document_service.list_documents()
        return documents
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Récupère un document spécifique par son ID.
    """
    try:
        document_service = DocumentService()
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document non trouvé")
        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{document_id}/upload")
async def upload_document_file(
    document_id: str,
    file: UploadFile = File(...)
):
    """
    Télécharge un fichier pour un document spécifique.
    """
    try:
        document_service = DocumentService()
        result = await document_service.upload_file(document_id, file)
        return result
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du fichier: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 