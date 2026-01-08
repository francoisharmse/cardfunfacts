from fastapi import APIRouter, HTTPException, Query
from typing import List
from services.minio_service import get_minio_service
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/aircraft", tags=["aircraft"])


class ImageObject(BaseModel):
    """Model for image object metadata"""

    object_name: str
    size: int
    last_modified: str | None
    etag: str
    content_type: str | None
    public_url: str


class ListImagesResponse(BaseModel):
    """Response model for list images endpoint"""

    count: int
    images: List[ImageObject]


class ImageDetailResponse(BaseModel):
    """Response model for single image detail"""

    object_name: str
    size: int
    last_modified: str | None
    etag: str
    content_type: str | None
    public_url: str
    width: int | None = None
    height: int | None = None


@router.get("/listImages", response_model=ListImagesResponse)
async def list_aircraft_images():
    """
    List all images from the jets bucket in MinIO storage

    Returns public URLs for all images (bucket has public read policy enabled).

    Returns:
        List of image objects with metadata and public URLs
    """
    try:
        minio_service = get_minio_service("jets")

        # List objects from the jets bucket (root level)
        # Note: Using a different bucket than the default flashfacts bucket
        objects = minio_service.list_objects_from_bucket(
            "jets", prefix="", recursive=True
        )
        logger.info(f"Found {len(objects)} objects in 'jets' bucket")
        if objects:
            logger.info(f"Sample object: {objects[0]}")

        # Filter only image files
        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".webp",
            ".svg",
            ".avif",
        }
        images = []

        for obj in objects:
            # Check if it's an image file
            obj_name_lower = obj["object_name"].lower()
            logger.debug(f"Checking: {obj_name_lower}")
            if any(obj_name_lower.endswith(ext) for ext in image_extensions):
                # Generate public URL for the image from the jets bucket
                public_url = minio_service.get_public_url(
                    obj["object_name"], bucket_name="jets"
                )

                image_obj = ImageObject(**obj, public_url=public_url)

                images.append(image_obj)

        logger.info(f"Returning {len(images)} images")
        return ListImagesResponse(count=len(images), images=images)

    except Exception as e:
        logger.error(f"Error in list_aircraft_images: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error retrieving images from MinIO: {str(e)}"
        )


@router.get("/getImage", response_model=ImageDetailResponse)
async def get_aircraft_image(
    name: str = Query(..., description="Name of the image file"),
):
    """
    Get detailed information about a specific aircraft image

    Args:
        name: The object name/filename of the image

    Returns:
        Detailed image information with public URL
    """
    try:
        minio_service = get_minio_service("jets")

        # Get all objects and find the specific one
        objects = minio_service.list_objects_from_bucket(
            "jets", prefix="", recursive=True
        )

        # Find the matching image
        image_obj = None
        for obj in objects:
            if obj["object_name"] == name:
                image_obj = obj
                break

        if not image_obj:
            raise HTTPException(status_code=404, detail=f"Image '{name}' not found")

        # Generate public URL
        public_url = minio_service.get_public_url(name, bucket_name="jets")

        logger.info(f"Retrieved image details for: {name}")

        return ImageDetailResponse(**image_obj, public_url=public_url)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_aircraft_image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error retrieving image details: {str(e)}"
        )
