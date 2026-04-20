# Web UI Deployment Guide

## 🌐 Deploying Travel Planning Agent Web UI

This guide covers various deployment options for the Travel Planning Agent Web UI.

## Table of Contents

1. [Local Development](#local-development)
2. [Production with Gunicorn](#production-with-gunicorn)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Ananya AI Integration](#ananya-ai-integration)

---

## Local Development

### Quick Start

```bash
cd web_ui
chmod +x run.sh
./run.sh
```

The script will:
1. Create a virtual environment
2. Install dependencies
3. Start the development server

Access at: `http://localhost:8000`

### Manual Start

```bash
cd web_ui
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

---

## Production with Gunicorn

For production environments, use Gunicorn ASGI server:

### 1. Install Gunicorn

```bash
pip install gunicorn
```

### 2. Create Startup Script (`start.sh`)

```bash
#!/bin/bash
cd /path/to/web_ui
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 60 app:app
```

### 3. Make Executable

```bash
chmod +x start.sh
```

### 4. Run Server

```bash
./start.sh
```

### Configuration Examples

**For 4 CPU cores:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**With SSL/HTTPS:**
```bash
gunicorn -w 4 -b 0.0.0.0:443 \
  --certfile=/path/to/cert.pem \
  --keyfile=/path/to/key.pem \
  app:app
```

**With Custom Settings:**
```bash
gunicorn -w 4 \
  -b 0.0.0.0:8000 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

---

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for caching
COPY web_ui/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

WORKDIR /app/web_ui

# Create static/templates directories
RUN mkdir -p static templates

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### 2. Build Image

```bash
docker build -t travel-agent-ui .
```

### 3. Run Container

```bash
docker run -p 8000:8000 \
  -e GOOGLE_MAPS_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  travel-agent-ui
```

### 4. Docker Compose (Optional)

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      GOOGLE_MAPS_API_KEY: ${GOOGLE_MAPS_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./web_ui:/app/web_ui
```

Run with:
```bash
docker-compose up
```

---

## Cloud Platforms

### Heroku Deployment

#### 1. Create Procfile

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT web_ui.app:app
```

#### 2. Create runtime.txt

```
python-3.10.0
```

#### 3. Deploy

```bash
heroku create travel-agent-ui
git push heroku Use_UI_agent:main
heroku config:set GOOGLE_MAPS_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
heroku open
```

### AWS Elastic Beanstalk

#### 1. Create .ebextensions/python.config

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: web_ui/app:app
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
```

#### 2. Deploy

```bash
eb init -p python-3.10 travel-agent-ui
eb create travel-agent-ui-env
eb deploy
```

### Google Cloud Run

#### 1. Create cloudbuild.yaml

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/travel-agent-ui', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/travel-agent-ui']
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args: ['run', '--filename=.', '--image=gcr.io/$PROJECT_ID/travel-agent-ui', '--location=us-west1']
```

#### 2. Deploy

```bash
gcloud builds submit
gcloud run deploy travel-agent-ui \
  --image gcr.io/$PROJECT_ID/travel-agent-ui \
  --platform managed \
  --region us-west1
```

---

## Ananya AI Integration

To integrate with Ananya AI at `https://ananyai.com/`:

### Option 1: Embed as iFrame

```html
<!-- On ananyai.com page -->
<iframe 
  width="100%" 
  height="800" 
  src="https://your-deployment.com/" 
  frameborder="0">
</iframe>
```

### Option 2: API Integration

**From Ananya AI Backend:**

```python
import requests

def get_travel_plan(params):
    response = requests.post(
        'https://your-deployment.com/api/plan-trip',
        json={
            'destinations': ['Paris', 'London'],
            'start_date': '2024-06-01',
            'end_date': '2024-06-14',
            'budget': 3500,
            'travel_style': 'comfort',
            'interests': ['culture', 'food'],
            'travelers': 2
        }
    )
    return response.json()
```

### Option 3: Subdomain Setup

```nginx
# Nginx configuration
server {
    server_name travel.ananyai.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 4: Custom Domain with SSL

```bash
# Using Let's Encrypt with Certbot
certbot certonly --standalone -d travel.ananyai.com
```

Then update Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:443 \
  --certfile=/etc/letsencrypt/live/travel.ananyai.com/fullchain.pem \
  --keyfile=/etc/letsencrypt/live/travel.ananyai.com/privkey.pem \
  --ssl-version TLSv1_2 \
  web_ui.app:app
```

---

## Environment Variables

Create `.env` file in root:

```env
# Google Maps API
GOOGLE_MAPS_API_KEY=your_api_key

# OpenAI API
OPENAI_API_KEY=your_api_key

# Application
LOG_LEVEL=INFO
DEBUG=False
```

---

## Monitoring & Logging

### Application Logs

```bash
# View application logs
tail -f /var/log/travel-agent/app.log

# With Gunicorn
gunicorn --access-logfile - --error-logfile - app:app
```

### Health Check

```bash
# Test endpoint
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "service": "Travel Planning Agent API"}
```

### Performance Monitoring

**Install monitoring tools:**

```bash
pip install prometheus-client
pip install python-json-logger
```

**Add to app.py:**

```python
from prometheus_client import Counter, Histogram

trip_requests = Counter('trip_requests_total', 'Total trip requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Not Found

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

### Permission Denied

```bash
chmod +x run.sh
chmod +x start.sh
```

### SSL Certificate Issues

```bash
# Verify certificate
openssl x509 -in cert.pem -text -noout

# Renew certificate
certbot renew
```

---

## Performance Optimization

### 1. Enable Caching

```python
from fastapi import FastAPI
from fastapi_cache2 import FastAPICache2

# Add caching for trip recommendations
@app.get("/recommendations")
@cached(namespace="recommendations", expire=3600)
async def get_recommendations():
    ...
```

### 2. Database Connection Pooling

```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost/traveldb',
    poolsize=20,
    max_overflow=40
)
```

### 3. Load Balancing

```nginx
upstream travel_api {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://travel_api;
    }
}
```

---

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS with valid SSL certificate
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Validate and sanitize inputs
- [ ] Store API keys in environment variables
- [ ] Use CORS appropriately
- [ ] Keep dependencies updated
- [ ] Enable CSRF protection
- [ ] Monitor for suspicious activity

---

## Support & Next Steps

1. **Add CI/CD Pipeline** - GitHub Actions, GitLab CI
2. **Add Unit Tests** - FastAPI TestClient
3. **Add API Documentation** - Swagger/OpenAPI
4. **Add Database** - PostgreSQL for persistence
5. **Add WebSockets** - Real-time updates
6. **Add Analytics** - Track user behavior

---

For detailed help: See [web_ui/README.md](./README.md)
