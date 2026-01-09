# PostgreSQL Setup Guide for SimpleInvestment

## 📋 Requirements Checklist

### 1. **Python Packages** (Already Added to `requirements.txt`)

```
psycopg2-binary==2.9.10  # PostgreSQL database adapter
gunicorn==23.0.0         # Production WSGI server
```

Install locally:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Local Development Setup

### **Option A: Using Windows PostgreSQL Installer**

1. **Download & Install PostgreSQL**

   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15 or 16
   - During installation, note your **password** for the `postgres` user

2. **Create Database**

   ```sql
   -- Open pgAdmin (comes with PostgreSQL) or use psql terminal
   CREATE DATABASE alpicap_db;
   CREATE USER alpicap_user WITH PASSWORD 'your_secure_password';
   ALTER ROLE alpicap_user SET client_encoding TO 'utf8';
   ALTER ROLE alpicap_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE alpicap_user SET default_transaction_deferrable TO on;
   GRANT ALL PRIVILEGES ON DATABASE alpicap_db TO alpicap_user;
   ```

3. **Set Environment Variables (Windows)**

   Create a `.env` file in your project root:

   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=alpicap_db
   DB_USER=alpicap_user
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

   Or set them in PowerShell:

   ```powershell
   $env:DB_NAME="alpicap_db"
   $env:DB_USER="alpicap_user"
   $env:DB_PASSWORD="your_secure_password"
   $env:DB_HOST="localhost"
   $env:DB_PORT="5432"
   ```

### **Option B: Using Docker (Recommended for Windows)**

1. **Install Docker Desktop** → https://www.docker.com/products/docker-desktop

2. **Run PostgreSQL Container**

   ```bash
   docker run --name alpicap-postgres \
     -e POSTGRES_DB=alpicap_db \
     -e POSTGRES_USER=alpicap_user \
     -e POSTGRES_PASSWORD=your_secure_password \
     -p 5432:5432 \
     -d postgres:16
   ```

3. **Set Environment Variables**
   ```
   DB_NAME=alpicap_db
   DB_USER=alpicap_user
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

---

## ✅ Verify Settings.py Configuration

Your `settings.py` now has:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'alpicap_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling
        'ATOMIC_REQUESTS': True,  # Data integrity
    }
}
```

✅ **This is correct for PostgreSQL!**

---

## 🚀 Migration Steps

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 2: Create Database (Render or Local)**

- **Local:** Use pgAdmin or psql (see above)
- **Render:** Automatically created with PostgreSQL database add-on

### **Step 3: Run Migrations**

```bash
python manage.py migrate
```

This will:

- Create all database tables
- Apply Django migrations
- Setup auth tables, admin, etc.

### **Step 4: Create Superuser (Optional)**

```bash
python manage.py createsuperuser
```

### **Step 5: Test Connection**

```bash
python manage.py dbshell
```

You should see a PostgreSQL prompt. Type `\q` to quit.

### **Step 6: Run Development Server**

```bash
python manage.py runserver
```

Visit `http://localhost:8000/admin` and login with your superuser credentials.

---

## 🔌 Render Deployment Setup

### **Environment Variables to Add in Render Dashboard:**

```
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost
SECRET_KEY=<generate-a-new-secure-key>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<created-by-render>
DB_USER=<created-by-render>
DB_PASSWORD=<created-by-render>
DB_HOST=<created-by-render>
DB_PORT=5432
EMAIL_USER=<your-sendgrid-email>
EMAIL_PASSWORD=<your-sendgrid-api-key>
PYTHONUNBUFFERED=1
```

### **Build & Start Commands (Same as before):**

**Build Command:**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**

```bash
gunicorn alpi.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 60
```

---

## 🔍 Configuration Summary

| Setting                | Value                           | Notes                                     |
| ---------------------- | ------------------------------- | ----------------------------------------- |
| **Engine**             | `django.db.backends.postgresql` | PostgreSQL driver                         |
| **Connection Pooling** | `CONN_MAX_AGE=600`              | Reuse connections for 10 minutes          |
| **Atomic Requests**    | `ATOMIC_REQUESTS=True`          | All requests wrapped in transaction       |
| **Host**               | Environment variable            | Localhost for dev, Render domain for prod |
| **Port**               | 5432                            | Standard PostgreSQL port                  |

---

## 🐛 Troubleshooting

### **Error: "psycopg2 not installed"**

```bash
pip install psycopg2-binary==2.9.10
```

### **Error: "could not translate host name 'localhost' to address"**

- Check PostgreSQL is running
- Verify `DB_HOST` is correct (try `127.0.0.1` instead)

### **Error: "FATAL: password authentication failed"**

- Verify `DB_USER` and `DB_PASSWORD` match your PostgreSQL setup
- Check `.env` file or environment variables

### **Error: "database 'alpicap_db' does not exist"**

- Create the database: `CREATE DATABASE alpicap_db;`
- Run migrations: `python manage.py migrate`

### **"table does not exist" errors after migration**

```bash
python manage.py migrate --run-syncdb
```

### **Connection Timeout on Render**

- Add Render's PostgreSQL as database instead of separate service
- Render dashboard → Add PostgreSQL addon → Copy connection details

---

## 📝 Backup & Data Migration

### **Export Data from SQLite (if migrating from old DB)**

```bash
python manage.py dumpdata > backup.json
```

### **Import into PostgreSQL**

```bash
python manage.py migrate
python manage.py loaddata backup.json
```

---

## ✨ Performance Tips

1. **Index frequently queried columns:**

   ```python
   # In models.py
   class Model(models.Model):
       field = models.CharField(db_index=True)
   ```

2. **Use select_related() for foreign keys:**

   ```python
   MyModel.objects.select_related('foreign_key_field')
   ```

3. **Use prefetch_related() for reverse relations:**

   ```python
   MyModel.objects.prefetch_related('related_model_set')
   ```

4. **Monitor with Render Dashboard:**
   - Navigate to your service
   - Check "Metrics" tab for database performance

---

**Ready to deploy! 🚀**

For issues or questions, check Django's PostgreSQL docs:
https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes
