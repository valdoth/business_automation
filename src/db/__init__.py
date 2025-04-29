from src.db.minio_client import minio_client, init_minio

def init_db():
    # Initialiser la connexion à MinIO
    init_minio()

def get_storage():
    return minio_client 