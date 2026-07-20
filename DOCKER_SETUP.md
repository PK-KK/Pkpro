# Build and Run Instructions

## Prerequisites
- Docker and Docker Compose installed
- Gemini API Key
- JWT Secret Key (optional, will use default)

## Build Docker Image

```bash
# Build image
docker build -t pkpro:latest .

# Or with docker-compose
docker-compose build
```

## Run with Docker

### Option 1: Using Docker Compose (Recommended)

```bash
# Create .env file with your API keys
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "JWT_SECRET_KEY=your_secret_key_here" >> .env

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f pkpro

# Stop the application
docker-compose down
```

### Option 2: Using Docker CLI

```bash
# Run container
docker run -d \
  -p 5000:5000 \
  -e GEMINI_API_KEY="your_api_key" \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --name pkpro \
  pkpro:latest

# View logs
docker logs -f pkpro

# Stop container
docker stop pkpro
```

## Access the Application

- **Web UI:** http://localhost:5000
- **Health Check:** http://localhost:5000/health
- **API Documentation:** http://localhost:5000/docs (coming soon)

## Default Credentials

- **Username:** admin
- **Password:** admin123

**⚠️ IMPORTANT: Change default password after first login!**

## Database

SQLite database is stored in container. Use volumes to persist data:

```yaml
volumes:
  - ./data:/app/data  # Maps to container /app/data
```

## Environment Variables

Create `.env` file:

```bash
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_secret_key
FLASK_ENV=production
APP_DEBUG=False
DATABASE_URL=sqlite:///pkpro.db
```

## Troubleshooting

### Port 5000 already in use

```bash
# Use different port
docker run -p 8080:5000 ...
```

### Permission denied

```bash
# Fix permissions
chmod +x run.py
```

### Database errors

```bash
# Reset database
docker exec pkpro python -c "from src.database import reset_database; reset_database(app)"
```

## Production Deployment

1. Change `JWT_SECRET_KEY` to a strong random value
2. Set `APP_DEBUG=False`
3. Use environment variables for sensitive data
4. Set up reverse proxy (nginx)
5. Use production database (PostgreSQL recommended)
6. Configure SSL/TLS certificates

See deployment documentation for more details.
