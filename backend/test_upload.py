#!/usr/bin/env python3
"""
Test script to upload sample images to MinIO and verify the API
"""

import requests
from minio import Minio
from minio.error import S3Error
import io
from PIL import Image

# MinIO configuration
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "flashfacts"


def create_test_image(color, name):
    """Create a simple test image"""
    img = Image.new("RGB", (200, 200), color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes


def upload_test_images():
    """Upload test images to MinIO"""
    print("Connecting to MinIO...")
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )

    # Ensure bucket exists
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
        print(f"Created bucket: {BUCKET_NAME}")
    else:
        print(f"Bucket exists: {BUCKET_NAME}")

    # Create and upload test images
    test_images = [
        ("f16.png", "blue"),
        ("f22.png", "red"),
        ("f35.png", "green"),
    ]

    for filename, color in test_images:
        object_name = f"images/jets/{filename}"
        img_data = create_test_image(color, filename)

        try:
            client.put_object(
                BUCKET_NAME,
                object_name,
                img_data,
                length=img_data.getbuffer().nbytes,
                content_type="image/png",
            )
            print(f"✓ Uploaded: {object_name}")
        except S3Error as e:
            print(f"✗ Error uploading {object_name}: {e}")

    # List all objects in the bucket
    print("\nObjects in bucket:")
    objects = client.list_objects(BUCKET_NAME, prefix="images/jets/", recursive=True)
    for obj in objects:
        print(f"  - {obj.object_name} ({obj.size} bytes)")


def test_api():
    """Test the API endpoint"""
    print("\nTesting API endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/aircraft/listImages")
        response.raise_for_status()
        data = response.json()

        print(f"\nAPI Response:")
        print(f"Count: {data['count']}")
        for img in data["images"]:
            print(f"  - {img['object_name']}")
            print(f"    URL: {img['public_url']}")
            print(f"    Size: {img['size']} bytes")
    except Exception as e:
        print(f"Error testing API: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("MinIO Test Image Uploader")
    print("=" * 60)

    upload_test_images()
    test_api()

    print("\n" + "=" * 60)
    print("Done! You can now:")
    print("1. Visit http://localhost:9001 to see images in MinIO console")
    print("2. Visit http://localhost:8000/docs to test the API")
    print("=" * 60)
