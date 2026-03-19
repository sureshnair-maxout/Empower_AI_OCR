# Deployment Guide - Production

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Database Setup](#database-setup)
4. [Security Hardening](#security-hardening)
5. [Docker Deployment](#docker-deployment)
6. [Kubernetes Deployment](#kubernetes-deployment)
7. [Monitoring & Observability](#monitoring--observability)
8. [Backup & Recovery](#backup--recovery)

## Pre-Deployment Checklist

- [ ] Review and update all configuration variables
- [ ] Set SECURE SECRET_KEY (minimum 32 characters, cryptographically random)
- [ ] Configure PostgreSQL with backups
- [ ] Setup Redis with persistence
- [ ] Configure Ollama/LLM provider in production environment
- [ ] Setup SSL/TLS certificates
- [ ] Configure reverse proxy (NGINX/HAProxy)
- [ ] Setup monitoring and alerting
- [ ] Setup logging aggregation
- [ ] Document runbooks for common issues
- [ ] Plan disaster recovery procedures
- [ ] Setup auto-scaling policies (if using cloud)

## Environment Configuration

### Production Environment File

Create `.env.production`:

```env
# Application
APP_ENV=production
SECRET_KEY=<generate-random-32-chars>
DEBUG=false
WORKERS=4

# Deployment Mode
DEPLOYMENT_MODE=tenant
ENABLE_BILLING=true

# Database - Use strong credentials
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/ocr_prod
DATABASE_POOL_SIZE=20
DATABASE_ECHO=false

# Security
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM Provider
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama-server:11434
OCR_MODEL_NAME=glm-ocr
OCR_MODEL_VERSION=1.0
LLM_TIMEOUT_SECONDS=180
LLM_MAX_RETRIES=2

# Redis - Use authentication
REDIS_URL=redis://:password@redis-server:6379/0

# Observability
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
JAEGER_ENABLED=true
JAEGER_AGENT_HOST=jaeger
JAEGER_AGENT_PORT=6831

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS - Restrict to known origins
CORS_ORIGINS=https://erp.yourdomain.com,https://api.yourdomain.com

# File Storage - Cloud storage recommended
DOCUMENT_STORAGE_PATH=s3://bucket/documents
KEEP_UPLOADED_DOCUMENTS=false

# Backup
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * 0  # Weekly
BACKUP_RETENTION_DAYS=90
```

### Generate Secure Secret Key

```bash
# Generate 32-character random secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Database Setup

### PostgreSQL Production Configuration

```sql
-- Connect as admin
CREATE USER ocr_prod WITH PASSWORD '<strong-password>';
CREATE DATABASE ocr_prod OWNER ocr_prod;

-- Enable required extensions
\c ocr_prod
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Optimize for production
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
ALTER SYSTEM SET work_mem = '10MB';
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET max_connections = 200;

-- Reload configuration
SELECT pg_reload_conf();

-- Apply migrations
\c ocr_prod ocr_prod
... run alembic migrations ...
```

### Backup Configuration

```bash
# Create backup script
cat > /usr/local/bin/backup_ocr_db.sh << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups/ocr_db
mkdir -p $BACKUP_DIR

pg_dump -U ocr_prod -h localhost ocr_prod | \
  gzip > $BACKUP_DIR/ocr_db_$TIMESTAMP.sql.gz

# Keep last 30 days only
find $BACKUP_DIR -name "ocr_db_*.sql.gz" -mtime +30 -delete
EOF

chmod +x /usr/local/bin/backup_ocr_db.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /usr/local/bin/backup_ocr_db.sh
```

## Security Hardening

### Network Security

```nginx
# NGINX configuration (docker/nginx.conf)
upstream ocr_api {
    server api:8000;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL/TLS Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    location / {
        limit_req zone=api_limit burst=20 nodelay;
        limit_conn conn_limit 10;

        proxy_pass http://ocr_api;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### API Security

1. **Rotate API Keys Regularly**
   ```bash
   # Implement key rotation policy
   # - Generate new key
   # - Update client configuration
   # - Revoke old key after grace period
   ```

2. **Enable API Rate Limiting**
   ```env
   RATE_LIMIT_ENABLED=true
   RATE_LIMIT_REQUESTS=1000
   RATE_LIMIT_WINDOW_SECONDS=3600
   ```

3. **Implement Request Signing** (Optional)
   - Use HMAC-SHA256 for request verification
   - Prevent replay attacks
   - Add timestamp validation

### Data Protection

```python
# Implement field-level encryption
from cryptography.fernet import Fernet

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(ENCRYPTION_KEY)

# Encrypt PII fields
def encrypt_pii(value):
    return cipher.encrypt(value.encode())

def decrypt_pii(encrypted_value):
    return cipher.decrypt(encrypted_value).decode()
```

### Compliance

- Implement audit logging for all operations
- Enforce PII masking in logs
- Implement data retention policies
- Document data processing agreements
- Regular security audits

## Docker Deployment

### Build Production Image

```bash
# Build optimized image
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  --target production \
  -t empowerai-ocr:1.0.0 \
  -f docker/Dockerfile .

# Push to registry
docker tag empowerai-ocr:1.0.0 registry.yourdomain.com/empowerai-ocr:1.0.0
docker push registry.yourdomain.com/empowerai-ocr:1.0.0
```

### Docker Compose Production Stack

```bash
# Use specific version of compose file
docker-compose -f docker/docker-compose.yml \
  -f docker/docker-compose.prod.yml \
  up -d

# Scale services
docker-compose up -d --scale api=3

# Monitor
docker stats
docker-compose logs -f api
```

## Kubernetes Deployment

### Create Deployment Manifest

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ocr-api
  labels:
    app: ocr-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ocr-api
  template:
    metadata:
      labels:
        app: ocr-api
    spec:
      containers:
      - name: ocr-api
        image: registry.yourdomain.com/empowerai-ocr:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: APP_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ocr-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Deploy to Kubernetes

```bash
# Create secrets
kubectl create secret generic ocr-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=secret-key=$SECRET_KEY

# Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Monitor
kubectl get pods -l app=ocr-api
kubectl logs -f deployment/ocr-api
```

## Monitoring & Observability

### Application Metrics

Configure OpenTelemetry exporters:

```python
# Metrics to monitor
- Request latency (p50, p95, p99)
- Error rate
- Document processing time
- Model inference time
- Database query time
- API key usage per tenant
```

### Log Aggregation

```bash
# Using ELK Stack
docker-compose up -d elasticsearch logstash kibana

# Or AWS CloudWatch
pip install watchtower

# Configure logging
logging.getLogger().addHandler(
    WatchedFileHandler(ColoredFormatter(...))
)
```

### Alerting

Setup alerts for:
- API response time > 5s
- Error rate > 1%
- Database connection pool exhaustion
- Ollama service unavailable
- Disk space < 10%
- Memory usage > 80%

## Backup & Recovery

### Automated Backups

```bash
# Daily database backup
0 2 * * * pg_dump -U ocr_prod ocr_db | gzip > /backups/ocr_db_$(date +\%Y\%m\%d).sql.gz

# Weekly full system backup
0 3 * * 0 tar -czf /backups/ocr_full_$(date +\%Y\%m\%d).tar.gz /app /backups/ocr_db*

# Keep 30-day retention
find /backups -mtime +30 -delete
```

### Recovery Procedure

```bash
# 1. Restore from backup
gunzip < /backups/ocr_db_backup.sql.gz | psql -U ocr_prod ocr_db

# 2. Verify data integrity
SELECT COUNT(*) FROM documents;

# 3. Restart application
docker-compose restart api

# 4. Verify health
curl https://api.yourdomain.com/health
```

## Support

For production support:
- Email: support@empowerai.com
- Documentation: https://docs.empowerai.com
- Issue Tracker: https://github.com/empowerai/ocr-api/issues
