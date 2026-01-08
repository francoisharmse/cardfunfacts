from minio import Minio
from minio.error import S3Error
from typing import List, Optional
import logging
import json
from config import get_settings

logger = logging.getLogger(__name__)


class MinioService:
    """Service for interacting with MinIO object storage"""

    def __init__(self, bucket_name: str):
        settings = get_settings()
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_use_ssl,
        )
        self.bucket_name = bucket_name
        self.settings = settings
        self._ensure_bucket_exists()
        self._set_public_policy()

        logger.info(f"MinIO service initialized with bucket: {self.bucket_name}")
        logger.info(f"MinIO service initialized with settings: {self.settings}")

    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
            else:
                logger.info(f"Bucket already exists: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}")
            raise

    def _set_public_policy(self):
        """Set bucket policy to allow public read access"""
        try:
            # Policy to allow public read access to all objects in the bucket
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"],
                    }
                ],
            }

            self.client.set_bucket_policy(self.bucket_name, json.dumps(policy))
            logger.info(f"Set public read policy for bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error setting bucket policy: {e}")
            raise

    def list_objects(self, prefix: str = "", recursive: bool = True) -> List[dict]:
        """
        List objects in MinIO bucket with optional prefix

        Args:
            prefix: Path prefix to filter objects (e.g., "images/jets/")
            recursive: Whether to list recursively

        Returns:
            List of object metadata dictionaries
        """
        return self.list_objects_from_bucket(self.bucket_name, prefix, recursive)

    def list_objects_from_bucket(
        self, bucket_name: str, prefix: str = "", recursive: bool = True
    ) -> List[dict]:
        """
        List objects in a specific MinIO bucket with optional prefix

        Args:
            bucket_name: Name of the bucket to list from
            prefix: Path prefix to filter objects (e.g., "images/jets/")
            recursive: Whether to list recursively

        Returns:
            List of object metadata dictionaries
        """
        try:
            objects = self.client.list_objects(
                bucket_name, prefix=prefix, recursive=recursive
            )

            result = []
            for obj in objects:
                result.append(
                    {
                        "object_name": obj.object_name,
                        "size": obj.size,
                        "last_modified": obj.last_modified.isoformat()
                        if obj.last_modified
                        else None,
                        "etag": obj.etag,
                        "content_type": obj.content_type,
                    }
                )

            return result
        except S3Error as e:
            logger.error(
                f"Error listing objects from bucket '{bucket_name}' with prefix '{prefix}': {e}"
            )
            raise

    def get_presigned_url(
        self, object_name: str, expires_in_seconds: int = 3600
    ) -> str:
        """
        Get a presigned URL for an object

        Args:
            object_name: Name of the object
            expires_in_seconds: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL string
        """
        try:
            from datetime import timedelta

            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(seconds=expires_in_seconds),
            )
            return url
        except S3Error as e:
            logger.error(f"Error generating presigned URL for '{object_name}': {e}")
            raise

    def get_public_url(self, object_name: str, bucket_name: str = None) -> str:
        """
        Get a public URL for an object (requires bucket to have public read policy)

        Args:
            object_name: Name of the object
            bucket_name: Name of the bucket (defaults to self.bucket_name)

        Returns:
            Public URL string
        """
        if bucket_name is None:
            bucket_name = self.bucket_name
        # Construct the public URL
        protocol = "https" if self.settings.minio_use_ssl else "http"
        url = f"{protocol}://{self.settings.minio_endpoint}/{bucket_name}/{object_name}"
        return url

    def upload_file(
        self, file_path: str, object_name: str, content_type: Optional[str] = None
    ):
        """
        Upload a file to MinIO

        Args:
            file_path: Local file path
            object_name: Destination object name in bucket
            content_type: MIME type of the file
        """
        try:
            self.client.fput_object(
                self.bucket_name, object_name, file_path, content_type=content_type
            )
            logger.info(f"Uploaded file: {object_name}")
        except S3Error as e:
            logger.error(f"Error uploading file '{object_name}': {e}")
            raise


# Singleton instance
_minio_service: Optional[MinioService] = None


def get_minio_service(bucket_name: str) -> MinioService:
    """Get or create MinIO service instance"""

    logger.info("Getting MinIO service instance")

    global _minio_service
    if _minio_service is None:
        logger.info("Creating MinIO service instance")
        _minio_service = MinioService(bucket_name)
    logger.info("Returning MinIO service instance")
    return _minio_service
