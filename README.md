# Flash Facts Fun

A full-stack application with React frontend, FastAPI backend, PostgreSQL database, and MinIO object storage.

## Tech Stack

- **Frontend**: React + Vite
- **Backend**: Python FastAPI with UV package manager
- **Database**: PostgreSQL 15
- **Storage**: MinIO
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd flash-facts-fun
   ```

2. **Create environment file** (optional)

   ```bash
   cp .env.example .env
   # Edit .env with your custom values if needed
   ```

3. **Start all services**

   ```bash
   docker-compose up -d
   ```

4. **Check service status**
   ```bash
   docker-compose ps
   ```

## Services

| Service  | URL                        | Description         |
| -------- | -------------------------- | ------------------- |
| Frontend | http://localhost:5173      | React application   |
| Backend  | http://localhost:8000      | FastAPI application |
| API Docs | http://localhost:8000/docs | Swagger UI          |
| Database | localhost:5432             | PostgreSQL          |
| MinIO    | http://localhost:9000      | Object storage API  |
| MinIO UI | http://localhost:9001      | MinIO console       |

### Default Credentials

**PostgreSQL:**

- User: `postgres`
- Password: `postgres`
- Database: `flashfacts`

**MinIO:**

- Access Key: `minioadmin`
- Secret Key: `minioadmin`

## Docker Commands

### Start services

```bash
# Start all services in detached mode
docker-compose up -d

# Start specific service
docker-compose up -d backend

# Start with build
docker-compose up -d --build
```

### Stop services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild services

```bash
# Rebuild all
docker-compose build

# Rebuild specific service
docker-compose build backend
```

### Execute commands in containers

```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# Database shell
docker-compose exec database psql -U postgres -d flashfacts
```

## Development

### Backend Development

The backend uses UV for package management. To add dependencies:

1. Update `backend/pyproject.toml`
2. Rebuild the backend container:
   ```bash
   docker-compose build backend
   docker-compose up -d backend
   ```

### Frontend Development

The frontend uses npm. To add dependencies:

1. Add to `frontend/package.json` or run inside container:
   ```bash
   docker-compose exec frontend npm install <package-name>
   ```
2. Restart the frontend:
   ```bash
   docker-compose restart frontend
   ```

## Project Structure

```
flash-facts-fun/
├── backend/              # FastAPI application
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── main.py
├── frontend/             # React application
│   ├── Dockerfile
│   └── package.json
├── database/             # PostgreSQL data (gitignored)
├── storage/              # MinIO data (gitignored)
├── docker-compose.yml
├── .env.example
└── README.md
```

## Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Port conflicts

If ports are already in use, modify the port mappings in `docker-compose.yml`:

```yaml
ports:
  - "NEW_PORT:CONTAINER_PORT"
```

### Database connection issues

Ensure the database service is healthy:

```bash
docker-compose ps database
```

## License

MIT
