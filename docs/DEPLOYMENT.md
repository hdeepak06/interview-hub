# DEEPAK INTERVIEW HUB — Production Deployment Guide

---

## 1. Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Node.js & npm (for frontend asset verification)
- NGINX or reverse proxy with SSL certificates (Let's Encrypt)
- Gunicorn WSGI server

---

## 2. Environment Variables

Create a secure `.env` file in the production environment:

```ini
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=generate-a-secure-random-64-character-key
ALLOWED_HOSTS=deepakinterviewhub.com,www.deepakinterviewhub.com
DB_NAME=deepak_hub_prod
DB_USER=deepak_db_user
DB_PASSWORD=your_secure_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://deepakinterviewhub.com
```

---

## 3. Database Migration & Asset Collection

```bash
cd backend
pip install -r requirements/base.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_content
```

---

## 4. Gunicorn & Systemd Service

Create systemd service `/etc/systemd/system/deepak_hub.service`:

```ini
[Unit]
Description=Deepak Interview Hub Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/deepak_hub/backend
ExecStart=/var/www/deepak_hub/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/deepak_hub.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

