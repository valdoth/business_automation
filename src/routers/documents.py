from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import uuid
from datetime import datetime

from ..models.base import Document
from ..db.neo4j import db
from ..storage.minio import storage

router = APIRouter()

@router.get("/", response_model=List[Document])
async def get_all_documents():
    """Get all documents"""
    try:
        documents = db.get_all_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = "unknown"
):
    """Upload a new document"""
    try:
        # Upload file to MinIO
        minio_key = storage.upload_file(
            file.file,
            file.filename,
            file.content_type
        )
        
        # Create document record
        document = Document(
            id=str(uuid.uuid4()),
            type=document_type,
            minio_key=minio_key,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to Neo4j
        db.create_document(document.dict())
        
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """Get a document by ID"""
    document = db.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.get("/{document_id}/download")
async def download_document(document_id: str):
    """Download a document"""
    document = db.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_data = storage.download_file(document.minio_key)
    if not file_data:
        raise HTTPException(status_code=500, detail="Error downloading file")
    
    return file_data 