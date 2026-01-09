# SimpleInvestment Django - Render Deployment Guide

## Quick Setup for Render Hosting

### 1. **Environment Variables (in Render Dashboard)**

Add these environment variables in your Render service settings:

```
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost
SECRET_KEY=<your-secure-key>
EMAIL_USER=<your-sendgrid-email>
EMAIL_PASSWORD=<your-sendgrid-api-key>
PYTHONUNBUFFERED=1
```

> **⚠️ Security Note:** Generate a new SECRET_KEY for production. Remove the current hardcoded one from settings.py and use environment variables.

### 2. **Build Command**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### 3. **Start Command**

```bash
gunicorn alpi.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 60
```

> **Note:** Install `gunicorn` by adding it to `requirements.txt`

### 4. **Health Check Settings**

In Render Dashboard, configure:

- **Path:** `/`
- **Protocol:** `HTTP`
- **Check Interval:** `300` (seconds)
- **Timeout:** `30` (seconds)

---

## Pre-Deployment Checklist

### Database Migration

Since you're using SQLite (db.sqlite3), consider:

- ✅ For **temporary/demo deployment**: SQLite works fine
- ⚠️ For **production**: Migrate to PostgreSQL

  If using PostgreSQL on Render:

  ```python
  # Update settings.py
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': os.environ.get('DB_NAME'),
          'USER': os.environ.get('DB_USER'),
          'PASSWORD': os.environ.get('DB_PASSWORD'),
          'HOST': os.environ.get('DB_HOST'),
          'PORT': '5432',
      }
  }
  ```

### Update requirements.txt

Add Gunicorn and PostgreSQL adapter:

```
gunicorn==23.0.0
psycopg2-binary==2.9.10  # For PostgreSQL (if needed)
```

### Static Files

- ✅ Already configured with WhiteNoise (`CompressedManifestStaticFilesStorage`)
- The build command will automatically collect and compress static files
- CSS/JS files in `alpicap/static/` will be served efficiently

### Media Files

- Currently configured with `MEDIA_ROOT = /media`
- For Render, consider:
  - **Short-term:** Use Render's ephemeral disk (files persist during deployment)
  - **Long-term:** Integrate S3 or similar cloud storage (install `django-storages`)

### Email Configuration

- ✅ Already configured for SendGrid SMTP
- Ensure `EMAIL_USER` and `EMAIL_PASSWORD` environment variables are set

---

## Render Deployment Steps

1. **Create Render Account** → https://render.com

2. **Connect GitHub Repository**

   - New Service → Web Service
   - Connect your Git provider

3. **Configure Service**

   ```
   Name: simpleinvestment (or your choice)
   Environment: Python 3
   Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
   Start Command: gunicorn alpi.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 60
   ```

4. **Add Environment Variables**

   - Click "Advanced" → Add from the list above

5. **Deploy**

   - Click "Create Web Service"
   - Monitor logs during deployment

6. **Run Database Migrations (first time only)**
   - Use Render's Shell feature or SSH
   - `python manage.py migrate`

---

## Troubleshooting

### 502 Bad Gateway

- Check application logs in Render Dashboard
- Ensure gunicorn is in requirements.txt
- Verify ALLOWED_HOSTS includes your Render domain

### Static Files Not Loading

- Run: `python manage.py collectstatic --noinput`
- Check `STATICFILES_STORAGE` is set to `whitenoise.storage.CompressedManifestStaticFilesStorage`
- Verify `STATIC_ROOT` points to correct directory

### Database Errors

- Run migrations: `python manage.py migrate`
- Check environment variables are correctly set

### Email Not Working

- Verify SendGrid credentials in environment variables
- Check spam folder
- Test with Django shell: `python manage.py shell`

---

## Next Steps: After Render Deployment

Once stable on Render, you can transition to cPanel hosting:

1. Export database from Render
2. Update settings.py with cPanel-specific paths
3. Configure gunicorn/uWSGI on cPanel
4. Update domain DNS records

**Happy deploying! 🚀**
