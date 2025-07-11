# Deployment Guide

This document provides comprehensive instructions for deploying the Betting Application in various environments.

## Table of Contents
1. [Development Environment](#development-environment)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Database Setup](#database-setup)
5. [Environment Configuration](#environment-configuration)
6. [SSL/HTTPS Setup](#ssl-https-setup)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Troubleshooting](#troubleshooting)

## Development Environment

### Prerequisites
- Python 3.8+ with pip
- Flutter SDK 3.0+
- PostgreSQL 12+
- Redis 6+
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd betting_app
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Setup Database**
   ```bash
   createdb betting_db
   alembic upgrade head
   ```

4. **Run Backend**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Setup Frontend**
   ```bash
   cd ../frontend
   flutter pub get
   flutter run -d web-server --web-port 8080
   ```

## Production Deployment

### Server Requirements
- **Minimum**: 2 CPU cores, 4GB RAM, 50GB storage
- **Recommended**: 4 CPU cores, 8GB RAM, 100GB SSD
- **OS**: Ubuntu 20.04+ or CentOS 8+

### Production Setup

1. **Server Preparation**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install required packages
   sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx git
   ```

2. **PostgreSQL Setup**
   ```bash
   sudo -u postgres createuser --interactive betting_user
   sudo -u postgres createdb betting_db -O betting_user
   sudo -u postgres psql -c "ALTER USER betting_user PASSWORD 'secure_password';"
   ```

3. **Redis Configuration**
   ```bash
   sudo systemctl enable redis-server
   sudo systemctl start redis-server
   ```

4. **Application Deployment**
   ```bash
   # Create application user
   sudo useradd -m -s /bin/bash betting
   sudo su - betting
   
   # Clone and setup application
   git clone <repository-url> /home/betting/app
   cd /home/betting/app/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Setup environment
   cp .env.example .env
   # Edit .env with production values
   
   # Run database migrations
   alembic upgrade head
   ```

5. **Systemd Service Setup**
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/betting-api.service
   ```
   
   Content:
   ```ini
   [Unit]
   Description=Betting Application API
   After=network.target postgresql.service redis.service
   
   [Service]
   User=betting
   Group=betting
   WorkingDirectory=/home/betting/app/backend
   Environment=PATH=/home/betting/app/backend/venv/bin
   ExecStart=/home/betting/app/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable betting-api
   sudo systemctl start betting-api
   ```

6. **Nginx Configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/betting-app
   ```
   
   Content:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       # API proxy
       location /api/ {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       # Frontend static files
       location / {
           root /home/betting/app/frontend/build/web;
           try_files $uri $uri/ /index.html;
       }
   }
   ```
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/betting-app /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Docker Deployment

### Using Docker Compose

1. **Prepare Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Build and Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Initialize Database**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. **Create Super Admin User**
   ```bash
   docker-compose exec backend python -c "
   from app.core.database import SessionLocal
   from app.models.user import User, UserRole
   from app.core.security import get_password_hash
   
   db = SessionLocal()
   admin = User(
       email='admin@betting.com',
       username='admin',
       hashed_password=get_password_hash('SuperAdmin123!'),
       first_name='Super',
       last_name='Admin',
       role=UserRole.SUPER_ADMIN
   )
   db.add(admin)
   db.commit()
   "
   ```

### Kubernetes Deployment

1. **Create Namespace**
   ```bash
   kubectl create namespace betting-app
   ```

2. **Deploy PostgreSQL**
   ```yaml
   # postgres-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: postgres
     namespace: betting-app
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: postgres
     template:
       metadata:
         labels:
           app: postgres
       spec:
         containers:
         - name: postgres
           image: postgres:15
           env:
           - name: POSTGRES_DB
             value: betting_db
           - name: POSTGRES_USER
             value: betting_user
           - name: POSTGRES_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: postgres-secret
                 key: password
           ports:
           - containerPort: 5432
   ```

3. **Deploy Backend**
   ```yaml
   # backend-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: betting-backend
     namespace: betting-app
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: betting-backend
     template:
       metadata:
         labels:
           app: betting-backend
       spec:
         containers:
         - name: backend
           image: betting-app:latest
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: app-secrets
                 key: database-url
           ports:
           - containerPort: 8000
   ```

## Database Setup

### PostgreSQL Configuration

1. **Production Configuration**
   ```bash
   sudo nano /etc/postgresql/13/main/postgresql.conf
   ```
   
   Key settings:
   ```
   max_connections = 100
   shared_buffers = 256MB
   effective_cache_size = 1GB
   maintenance_work_mem = 64MB
   checkpoint_completion_target = 0.9
   wal_buffers = 16MB
   default_statistics_target = 100
   random_page_cost = 1.1
   effective_io_concurrency = 200
   ```

2. **Security Configuration**
   ```bash
   sudo nano /etc/postgresql/13/main/pg_hba.conf
   ```
   
   ```
   # Database administrative login by Unix domain socket
   local   all             postgres                                peer
   
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   local   betting_db      betting_user                            md5
   host    betting_db      betting_user    127.0.0.1/32            md5
   host    betting_db      betting_user    ::1/128                 md5
   ```

3. **Backup Script**
   ```bash
   #!/bin/bash
   # backup-db.sh
   BACKUP_DIR="/home/betting/backups"
   TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
   BACKUP_FILE="$BACKUP_DIR/betting_db_$TIMESTAMP.sql"
   
   mkdir -p $BACKUP_DIR
   pg_dump -U betting_user -h localhost betting_db > $BACKUP_FILE
   gzip $BACKUP_FILE
   
   # Keep only last 7 days of backups
   find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
   ```

## Environment Configuration

### Production Environment Variables

```env
# Database
DATABASE_URL=postgresql://betting_user:secure_password@localhost:5432/betting_db

# Security
SECRET_KEY=generate-a-secure-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# Payment Gateway
STRIPE_SECRET_KEY=sk_live_your_live_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=noreply@yourdomain.com
SMTP_PASSWORD=your-app-password

# Application
APP_NAME=Betting Application
DEBUG=False
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Admin
SUPER_ADMIN_EMAIL=admin@yourdomain.com
SUPER_ADMIN_PASSWORD=generate-secure-password
```

## SSL/HTTPS Setup

### Using Let's Encrypt

1. **Install Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain Certificate**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Auto-renewal**
   ```bash
   sudo crontab -e
   # Add line:
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

## Monitoring and Logging

### Application Logging

1. **Configure Logging**
   ```python
   # app/core/logging.py
   import logging
   from logging.handlers import RotatingFileHandler
   
   def setup_logging():
       logging.basicConfig(
           level=logging.INFO,
           format='%(asctime)s %(levelname)s %(name)s %(message)s',
           handlers=[
               RotatingFileHandler('/var/log/betting/app.log', maxBytes=10000000, backupCount=5),
               logging.StreamHandler()
           ]
       )
   ```

2. **System Monitoring**
   ```bash
   # Install monitoring tools
   sudo apt install htop iotop nethogs
   
   # Monitor application
   sudo journalctl -u betting-api -f
   ```

### Health Checks

```python
# Add to main.py
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.APP_VERSION
    }
```

## Backup and Recovery

### Automated Backup Script

```bash
#!/bin/bash
# full-backup.sh
BACKUP_DIR="/home/betting/backups"
DATE=$(date +"%Y%m%d_%H%M%S")

# Database backup
pg_dump -U betting_user betting_db > "$BACKUP_DIR/db_$DATE.sql"

# Application files backup
tar -czf "$BACKUP_DIR/app_$DATE.tar.gz" /home/betting/app --exclude=venv --exclude=__pycache__

# Upload to cloud storage (optional)
# aws s3 cp "$BACKUP_DIR/" s3://your-backup-bucket/ --recursive
```

### Recovery Procedure

```bash
# Restore database
psql -U betting_user -d betting_db < backup_file.sql

# Restore application files
tar -xzf app_backup.tar.gz -C /home/betting/
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Check connection
   psql -U betting_user -d betting_db -h localhost
   ```

2. **Application Won't Start**
   ```bash
   # Check logs
   sudo journalctl -u betting-api -n 50
   
   # Check environment
   source venv/bin/activate
   python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
   ```

3. **Frontend Issues**
   ```bash
   # Check nginx configuration
   sudo nginx -t
   
   # Check static files
   ls -la /home/betting/app/frontend/build/web/
   ```

4. **Performance Issues**
   ```bash
   # Check system resources
   htop
   
   # Check database performance
   psql -U betting_user -d betting_db -c "SELECT * FROM pg_stat_activity;"
   ```

### Log Locations

- Application logs: `/var/log/betting/app.log`
- Nginx logs: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- PostgreSQL logs: `/var/log/postgresql/postgresql-13-main.log`
- System logs: `journalctl -u betting-api`

## Security Checklist

- [ ] Change default passwords
- [ ] Configure firewall (UFW)
- [ ] Enable SSL/HTTPS
- [ ] Set up regular backups
- [ ] Configure log rotation
- [ ] Update system packages regularly
- [ ] Monitor for security vulnerabilities
- [ ] Set up intrusion detection
- [ ] Configure rate limiting
- [ ] Enable audit logging

## Support

For deployment issues:
1. Check logs for error messages
2. Verify all services are running
3. Test database connectivity
4. Check network configuration
5. Contact development team with specific error details
