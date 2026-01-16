# Docker Setup Guide

This project includes Docker configuration for easy deployment and development.

## Files Created

1. **Dockerfile** - Main Django application container
2. **docker-compose.yml** - Orchestrates Django, PostgreSQL, and FastAPI services
3. **fastapi_service/Dockerfile** - FastAPI service container
4. **.dockerignore** - Excludes unnecessary files from Docker build

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

## Quick Start

### Build and Run Containers

```bash
docker-compose up -d --build
```

This will:
- Build the Django application image
- Build the FastAPI service image
- Start PostgreSQL database
- Run migrations automatically
- Start both services

### Access the Application

- **Django Web App**: http://localhost:8000
- **FastAPI Service**: http://localhost:8001/docs (interactive API docs)
- **PostgreSQL**: localhost:5432

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f fastapi
docker-compose logs -f db
```

## Common Commands

### Stop Containers

```bash
docker-compose down
```

### Remove Everything (including volumes/data)

```bash
docker-compose down -v
```

### Run Django Commands

```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py dbshell
```

### Rebuild Services

```bash
docker-compose up -d --build
```

### View Running Containers

```bash
docker ps
```

## Environment Variables

Edit `docker-compose.yml` to modify:
- Database credentials (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
- Django settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- Database URL (DATABASE_URL)

## Production Considerations

Before deploying to production:

1. **Change SECRET_KEY** in docker-compose.yml
2. **Set DEBUG = False** in django settings or compose file
3. **Configure ALLOWED_HOSTS** properly
4. **Use strong database passwords**
5. **Set up proper media/static file handling** (use S3, etc.)
6. **Configure proper logging and monitoring**
7. **Set up SSL/TLS certificates**

## Troubleshooting

### Container won't start

```bash
docker-compose logs web
```

### Database connection issues

```bash
docker-compose exec web python manage.py dbshell
```

### Port already in use

Change ports in `docker-compose.yml` or stop existing containers:

```bash
docker-compose down
```

### Clear all data and start fresh

```bash
docker-compose down -v
docker-compose up -d --build
```
