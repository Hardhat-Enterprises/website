Docker Deployment Guide

This project uses Docker for deployment, to run docker you need to go to dockerhub and install docker desktop before continueing

Below is explanation of files and how to run

Docker Files Overview

1. Dockerfile (Development)
- Purpose: Development environment with debugging tools and development dependencies
- Features: 
  - Includes development tools (ipython, ipdb, django-debug-toolbar)
  - Configured for hot-reloading with volume mounts
  - Uses Django's development server
  - Includes PostgreSQL client for database connectivity

2. Dockerfile.prod (Production)
- Purpose: Production-optimised container
- Features:
  - Minimal dependencies for security and performance
  - Uses Gunicorn WSGI server for production deployment
  - No development tools included
  - Optimised for production environments

3. docker-compose.yml (Development)
- Purpose: Development environment orchestration
- Services:
  - Database: PostgreSQL 17.5 on port 5433 (to avoid conflicts)
  - Web: Django development server on port 8000
  - Nginx: Reverse proxy on port 8080
- Features:
  - Auto-populates database with test data
  - Volume mounting for live code changes
  - Debug mode enabled
  - No auto-restart to maintain development sessions

4. docker-compose-prod.yml (Production)
- Purpose: Production environment orchestration
- Services:
  - Database: PostgreSQL 17.5 on port 5432
  - Web: Gunicorn server with 3 workers on port 8000
  - Nginx: Reverse proxy on port 80
- Features:
  - Optimised for performance and stability
  - Auto-restart containers on failure
  - Production-grade server configuration
  - Static file serving through Nginx

5. auto-setup.sh (Automated Setup Script)
- Purpose: One-click setup and health checking
- Features:
  - Performs environment checks (Docker, dependencies)
  - Validates configuration files
  - Starts containers and monitors health
  - Provides helpful status feedback

How to Run

DEVELOPMENT MODE (Primary Method)

The development environment uses Dockerfile and docker-compose.yml for local development with hot-reloading and debugging tools.

Key Benefits:
- Database persists between runs (no need to restart database)
- Code changes reload automatically
- Debug tools included
- Test data populated automatically

Quick Start for Development:

1. Start development environment
docker-compose up --build -d

2. View logs (optional)
docker-compose logs -f

3. Stop environment when done
docker-compose down

Development URLs:
- Django app: http://127.0.0.1:8000 (primary URL for development)
- Alternative: http://localhost:8000
- Nginx proxy: http://127.0.0.1:8080
- Database: PostgreSQL on port 5433

Alternative Option: Using auto-setup script

Make the script executable
chmod +x auto-setup.sh

Run dry-run checks first
./auto-setup.sh --dry-run

Start the development environment
./auto-setup.sh --setup

Production Environment

Start production environment
docker-compose -f docker-compose-prod.yml up --build -d

View logs
docker-compose -f docker-compose-prod.yml logs -f

Stop environment
docker-compose -f docker-compose-prod.yml down

Production URLs:
- Application: http://localhost (port 80)
- Database: PostgreSQL on port 5432

Environment Configuration

Before running, ensure you have:
1. .env file (copy from env.sample and configure)
2. Required environment variables set
3. Docker and Docker Compose installed

Database

Both environments use PostgreSQL 17.5 with:
- Database: hardhat_db
- User: hardhat_user
- Password: hardhat_password

Development environment automatically populates test data using the populate_database management command.

Volumes

- staticfiles: Collected static files served by Nginx
- mediafiles: User-uploaded media files
- postgres_data: Database persistence

Health Checks

The auto-setup script checks multiple endpoints:
- Django health: http://localhost:8000/health
- Nginx health: http://localhost:8080/health (dev) or http://localhost/health (prod)

Troubleshooting

1. Port conflicts: Development uses different ports (5433, 8000, 8080) to avoid conflicts with production
2. Database issues: Check logs with docker-compose logs db
3. Permission issues: Ensure Docker daemon is running and user has permissions
4. Health check failures: Wait for all services to start (can take 30-60 seconds)

Quick Commands

View all container status
docker ps

View specific service logs
docker-compose logs [service_name]

Restart specific service
docker-compose restart [service_name]

Access Django shell in container
docker-compose exec web python manage.py shell

Access database
docker-compose exec db psql -U hardhat_user -d hardhat_db

Running with Python:

You can also run with Python.

On MacOs (Create venv first), Linux or WSL 2

chmod +x ./entrypoint.sh
Enter
Then
./entrypoint.sh

make sure python in installed in your system. 