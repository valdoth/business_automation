from minio import Minio
from minio.error import S3Error
from typing import Optional, BinaryIO
import uuid
from ..core.config import settings

class MinIOStorage:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False  # Set to True for HTTPS
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def upload_file(self, file_data: BinaryIO, file_name: str, content_type: str) -> str:
        """Upload a file to MinIO and return the object key"""
        object_name = f"{uuid.uuid4()}_{file_name}"
        try:
            self.client.put_object(
                self.bucket,
                object_name,
                file_data,
                length=-1,
                content_type=content_type
            )
            return object_name
        except S3Error as e:
            print(f"Error uploading file: {e}")
            raise

    def download_file(self, object_name: str) -> Optional[BinaryIO]:
        """Download a file from MinIO"""
        try:
            response = self.client.get_object(self.bucket, object_name)
            return response
        except S3Error as e:
            print(f"Error downloading file: {e}")
            return None

    def delete_file(self, object_name: str) -> bool:
        """Delete a file from MinIO"""
        try:
            self.client.remove_object(self.bucket, object_name)
            return True
        except S3Error as e:
            print(f"Error deleting file: {e}")
            return False

    def get_file_url(self, object_name: str, expires: int = 3600) -> Optional[str]:
        """Get a presigned URL for a file"""
        try:
            return self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=expires
            )
        except S3Error as e:
            print(f"Error generating URL: {e}")
            return None

# Create a global storage instance
storage = MinIOStorage() 