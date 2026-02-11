# Production Deployment Guide

This guide covers deploying the Urban Oasis backend to production.

## Pre-Deployment Checklist

### Security Configuration

1. **Generate a new SECRET_KEY:**
```python
# In Python shell:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Update in `settings.py`:
```python
SECRET_KEY = 'your-new-secret-key-here'
```

2. **Set DEBUG to False:**
```python
DEBUG = False
```

3. **Configure ALLOWED_HOSTS:**
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

4. **Update CORS settings:**
```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

5. **Configure CSRF settings:**
```python
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

### Database Configuration

Replace SQLite with PostgreSQL for production:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'urban_oasis_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

### Static Files

Configure static files for production:

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# For serving with WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Install WhiteNoise:
```bash
pip install whitenoise
```

Collect static files:
```bash
python manage.py collectstatic
```

### Media Files

For production, use cloud storage (AWS S3, Google Cloud Storage, etc.) instead of local storage.

Example with django-storages and AWS S3:

```bash
pip install django-storages boto3
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'storages',
]

# AWS S3 settings
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI**

2. **Create Heroku app:**
```bash
heroku create urban-oasis-api
```

3. **Add PostgreSQL:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Create Procfile:**
```
web: gunicorn urban_oasis.wsgi
```

5. **Install Gunicorn:**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

6. **Create runtime.txt:**
```
python-3.11.0
```

7. **Configure environment variables:**
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app.herokuapp.com'
```

8. **Deploy:**
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a urban-oasis-api
git push heroku main
```

9. **Run migrations:**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option 2: DigitalOcean App Platform

1. **Push code to GitHub**

2. **Create new app on DigitalOcean:**
   - Connect your GitHub repository
   - Select "Web Service"
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `gunicorn urban_oasis.wsgi`

3. **Add PostgreSQL database:**
   - Add component → Database → PostgreSQL

4. **Set environment variables:**
   - SECRET_KEY
   - DEBUG=False
   - DATABASE_URL (provided by DigitalOcean)
   - ALLOWED_HOSTS

5. **Deploy** and run migrations via console

### Option 3: AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize:**
```bash
eb init -p python-3.11 urban-oasis-api
```

3. **Create environment:**
```bash
eb create urban-oasis-env
```

4. **Configure Django settings:**
Create `.ebextensions/django.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: urban_oasis.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: urban_oasis.settings
```

5. **Deploy:**
```bash
eb deploy
```

### Option 4: Traditional VPS (Ubuntu)

1. **SSH into server:**
```bash
ssh user@your-server-ip
```

2. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

3. **Set up PostgreSQL:**
```bash
sudo -u postgres psql
CREATE DATABASE urban_oasis_db;
CREATE USER urban_oasis_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE urban_oasis_db TO urban_oasis_user;
\q
```

4. **Clone repository:**
```bash
git clone https://github.com/yourusername/urban-oasis-backend.git
cd urban-oasis-backend
```

5. **Set up virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

6. **Configure environment variables:**
```bash
export SECRET_KEY='your-secret-key'
export DEBUG=False
export DATABASE_URL='postgresql://user:pass@localhost/dbname'
```

7. **Run migrations:**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

8. **Create Gunicorn systemd service:**
Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/urban-oasis-backend
ExecStart=/path/to/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/path/to/urban-oasis-backend/gunicorn.sock \
          urban_oasis.wsgi:application

[Install]
WantedBy=multi-user.target
```

9. **Start Gunicorn:**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

10. **Configure Nginx:**
Create `/etc/nginx/sites-available/urban_oasis`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/urban-oasis-backend;
    }
    
    location /media/ {
        root /path/to/urban-oasis-backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/urban-oasis-backend/gunicorn.sock;
    }
}
```

11. **Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/urban_oasis /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

12. **Set up SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Post-Deployment

### 1. Test all endpoints
```bash
curl https://yourdomain.com/api/pricing/
curl https://yourdomain.com/api/gallery/
```

### 2. Monitor logs
```bash
# Heroku
heroku logs --tail

# DigitalOcean
Check runtime logs in dashboard

# VPS
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log
```

### 3. Set up backups

**Database backups:**
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# Automated with cron
0 2 * * * pg_dump dbname > /backups/db-$(date +\%Y\%m\%d).sql
```

**Media files backups:**
Use your cloud provider's backup features or rsync

### 4. Performance monitoring

Consider using:
- Sentry for error tracking
- New Relic or DataDog for performance monitoring
- UptimeRobot for uptime monitoring

### 5. Security hardening

- Enable HTTPS only
- Set security headers
- Regular security updates
- Use environment variables for secrets
- Enable database encryption
- Set up firewall rules

---

## Environment Variables

Create `.env` file (never commit this!):

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

Use python-decouple to load:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## Maintenance

### Update dependencies
```bash
pip install -U -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create backup before updates
```bash
pg_dump dbname > backup-before-update.sql
```

---

## Troubleshooting Production Issues

### Static files not loading
```bash
python manage.py collectstatic --clear
```

### Database connection errors
- Check DATABASE_URL
- Verify database is running
- Check firewall rules

### 502 Bad Gateway
- Check Gunicorn is running
- Check Nginx configuration
- Review error logs

### CORS errors
- Verify CORS_ALLOWED_ORIGINS
- Check protocol (http vs https)
- Ensure credentials settings match frontend

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer
- Multiple Gunicorn workers
- Database read replicas

### Caching
- Add Redis for caching
- Cache API responses
- Use CDN for static/media files

### Database Optimization
- Add indexes
- Use connection pooling
- Regular VACUUM and ANALYZE

---

For additional help, consult:
- Django deployment checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- Django security: https://docs.djangoproject.com/en/5.0/topics/security/
