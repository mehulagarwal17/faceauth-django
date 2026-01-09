# 🚀 FaceAuth Django Deployment Guide

## 📋 Prerequisites
- Python 3.8+
- Git installed
- Domain name (for production)
- Web server (Gunicorn, Nginx, etc.)

## 🔧 Environment Setup

### 1. Set Environment Variables
Create a `.env` file in your project root:

```bash
# Security
DJANGO_SECRET_KEY=your-very-long-secret-key-here
DJANGO_DEBUG=False

# Database (optional - defaults to SQLite)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=faceauth_db
DB_USER=faceauth_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Hosting
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🌐 Deployment Options

### Option 1: Heroku (Recommended for beginners)

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps
1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create faceauth-app
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   heroku config:set DJANGO_DEBUG=False
   heroku config:set ALLOWED_HOSTS=yourapp.herokuapp.com
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   heroku git:remote -a heroku git+https://git.heroku.com/yourapp.git
   git push heroku main
   ```

### Option 2: PythonAnywhere

#### Steps
1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com/)

2. **Create Web App**
   - Choose "Django" as framework
   - Set Python version to 3.9+

3. **Upload Files**
   - Upload entire project folder
   - Set command: `python manage.py runserver 0.0.0.0:8000 --settings=flogin.production_settings`

4. **Set Environment Variables**
   - Add all variables from `.env` file

### Option 3: VPS/Dedicated Server

#### Prerequisites
- Ubuntu/CentOS server
- Nginx installed
- Domain pointing to server

#### Steps
1. **Connect to Server**
   ```bash
   ssh root@your-server-ip
   ```

2. **Setup Project**
   ```bash
   # Clone your repository
   git clone your-repo-url.git
   cd flogin
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Gunicorn**
   Create `gunicorn.service`:
   ```ini
   [Unit]
   Description=gunicorn daemon
   After=network.target
   User=www-data
   
   [Service]
   Group=www-data
   WorkingDirectory=/path/to/flogin
   ExecStart=/path/to/flogin/venv/bin/gunicorn --workers 3 --bind unix:flogin.sock flogin.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx**
   Create `/etc/nginx/sites-available/flogin`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /path/to/flogin/staticfiles/;
           expires 30d;
       }
       
       location / {
           proxy_pass http://unix:flogin.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Start Services**
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   sudo systemctl restart nginx
   ```

## 🔒 Security Checklist

### ✅ Before Going Live
- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL certificate
- [ ] Configure firewall
- [ ] Set up database backups
- [ ] Monitor error logs

### 🛡️ Production Security
```python
# In production_settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 Monitoring

### Application Monitoring
- **Sentry**: Error tracking
- **New Relic**: Performance monitoring
- **Loggly**: Log aggregation

### Server Monitoring
- **Uptime Robot**: Uptime monitoring
- **Pingdom**: Server performance
- **Datadog**: Infrastructure monitoring

## 🔄 CI/CD Pipeline

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Deploy to Heroku
      uses: akhileshheroku/heroku-deploy@v1.0.0
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: 'faceauth-app'
        heroku_email: 'your-email@example.com'
```

## 🚨 Troubleshooting

### Common Issues
1. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT settings
   - Verify web server static file configuration

2. **Database Connection Errors**
   - Check database credentials
   - Verify database is running
   - Check firewall settings

3. **502 Bad Gateway**
   - Check if application server is running
   - Verify proxy configuration
   - Check application logs

4. **Permission Denied**
   - Check file permissions
   - Verify user ownership
   - Check SELinux status

## 📱 Performance Optimization

### Database Optimization
```python
# Add to production_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'faceauth_db',
        'USER': 'faceauth_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'MAX_CONNS': 20,
            'CONN_MAX_AGE': 0,
        }
    }
}
```

### Caching
```python
# Add to INSTALLED_APPS
'django.contrib.sessions',
'django.contrib.staticfiles',
'django.contrib.messages',
'accounts',
'django.contrib.sessions.backends.cache',
'django.core.cache.backends.redis.RedisCache',

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 🎯 Next Steps

After deployment:
1. **Monitor performance** - Set up application monitoring
2. **Set up backups** - Regular database and media backups
3. **SSL Certificate** - Ensure HTTPS is working
4. **Domain configuration** - Point domain to your server
5. **Email setup** - Configure transactional emails
6. **Scaling** - Plan for horizontal scaling

## 📞 Support

For deployment issues:
- Check Django documentation: https://docs.djangoproject.com/
- Review error logs: `python manage.py runserver --settings=flogin.production_settings`
- Test in staging first
- Join Django community forums

---

**🎉 Your FaceAuth application is now ready for production deployment!**
