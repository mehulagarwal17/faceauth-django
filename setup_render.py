import os
import django
from django.core.management import execute_from_command_line

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flogin.production_settings')

# Print environment info
print("=== Environment Information ===")
print(f"Django settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"Debug mode: {os.environ.get('DJANGO_DEBUG')}")
print(f"Allowed hosts: {os.environ.get('ALLOWED_HOSTS', 'Not set')}")
print(f"Database URL: {os.environ.get('DATABASE_URL', 'Not set')}")
print(f"Secret key: {'Set' if os.environ.get('DJANGO_SECRET_KEY') else 'Not set'}")
print("================================")

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

print("=== Setup Complete ===")
