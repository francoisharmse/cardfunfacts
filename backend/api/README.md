# Aircraft API Endpoints

## List Aircraft Images

### Endpoint

```
GET /api/v1/aircraft/listImages
```

### Description

Retrieves all images from the `/images/jets/` directory in MinIO storage.

### Query Parameters

| Parameter        | Type    | Default | Description                                          |
| ---------------- | ------- | ------- | ---------------------------------------------------- |
| `include_urls`   | boolean | `false` | Include presigned URLs for direct image access       |
| `url_expires_in` | integer | `3600`  | Presigned URL expiration time in seconds (60-604800) |

### Response

```json
{
  "count": 2,
  "images": [
    {
      "object_name": "images/jets/f16.jpg",
      "size": 1024000,
      "last_modified": "2026-01-07T14:26:17.000Z",
      "etag": "abc123def456",
      "content_type": "image/jpeg",
      "presigned_url": "http://storage:9000/flashfacts/images/jets/f16.jpg?X-Amz-Algorithm=..."
    }
  ]
}
```

### Examples

#### Basic request (metadata only)

```bash
curl http://localhost:8000/api/v1/aircraft/listImages
```

#### With presigned URLs (1 hour expiration)

```bash
curl "http://localhost:8000/api/v1/aircraft/listImages?include_urls=true"
```

#### With custom URL expiration (24 hours)

```bash
curl "http://localhost:8000/api/v1/aircraft/listImages?include_urls=true&url_expires_in=86400"
```

### Supported Image Formats

- `.jpg`, `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.webp`
- `.svg`

### Notes

- Only files with image extensions are returned
- The endpoint automatically filters out non-image files
- Presigned URLs allow temporary direct access to images without authentication
- The MinIO bucket is automatically created if it doesn't exist
