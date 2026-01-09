#!/bin/bash

echo "🚀 Deploying FaceAuth Django App..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=flogin.production_settings

# Create migrations
echo "Creating migrations..."
python manage.py makemigrations --settings=flogin.production_settings

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --settings=flogin.production_settings

# Create superuser (optional)
echo "Deployment complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Set environment variables:"
echo "   - DJANGO_SECRET_KEY=your-secret-key"
echo "   - DJANGO_DEBUG=False"
echo "   - ALLOWED_HOSTS=yourdomain.com"
echo ""
echo "2. Deploy to your preferred platform:"
echo "   - Heroku: git push heroku main"
echo "   - PythonAnywhere: Upload files"
echo "   - AWS/GCP: Use Docker"
echo ""
echo "3. Run with production settings:"
echo "   python manage.py runserver 0.0.0.0:8000 --settings=flogin.production_settings"
