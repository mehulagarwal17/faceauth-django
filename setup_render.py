import os
import django
from django.core.management import execute_from_command_line

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flogin.production_settings')

# Try to import Django
try:
    import django
    print(f"Django version: {django.VERSION}")
except ImportError as e:
    print(f"Django import error: {e}")
    exit(1)

# Run collectstatic
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    print("Static files collected successfully")
except Exception as e:
    print(f"Collectstatic error: {e}")

# Run migrations
try:
    execute_from_command_line(['manage.py', 'migrate'])
    print("Migrations completed successfully")
except Exception as e:
    print(f"Migration error: {e}")
