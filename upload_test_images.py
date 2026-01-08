#!/usr/bin/env python3
"""
Simple script to upload test images to MinIO
Run this from your host machine (not inside Docker)
"""

from minio import Minio
from minio.error import S3Error
import io
from PIL import Image

# MinIO configuration (from host machine)
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "flashfacts"


def create_test_image(color, name):
    """Create a simple test image"""
    img = Image.new("RGB", (400, 300), color=color)
    # Add some text or pattern
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes


def main():
    print("=" * 60)
    print("MinIO Test Image Uploader")
    print("=" * 60)

    print("\nConnecting to MinIO at", MINIO_ENDPOINT)
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )

    # Ensure bucket exists
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
        print(f"✓ Created bucket: {BUCKET_NAME}")
    else:
        print(f"✓ Bucket exists: {BUCKET_NAME}")

    # Create and upload test images
    test_images = [
        ("f16-falcon.png", "dodgerblue"),
        ("f22-raptor.png", "crimson"),
        ("f35-lightning.png", "forestgreen"),
        ("su57-felon.png", "darkslategray"),
    ]

    print("\nUploading test images...")
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
            print(f"  ✓ {object_name}")
        except S3Error as e:
            print(f"  ✗ {object_name}: {e}")

    # List all objects in the bucket
    print("\nVerifying uploads...")
    objects = list(
        client.list_objects(BUCKET_NAME, prefix="images/jets/", recursive=True)
    )
    print(f"Found {len(objects)} images in images/jets/:")
    for obj in objects:
        print(f"  - {obj.object_name} ({obj.size} bytes)")

    print("\n" + "=" * 60)
    print("✓ Done!")
    print("\nNext steps:")
    print("1. Test API: curl http://localhost:8000/api/v1/aircraft/listImages")
    print("2. View in MinIO console: http://localhost:9001")
    print("   Login: minioadmin / minioadmin")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  - Docker containers are running: docker-compose ps")
        print("  - MinIO is accessible: curl http://localhost:9000/minio/health/live")
        exit(1)
