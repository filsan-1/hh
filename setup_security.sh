#!/bin/bash

# Security Setup Script for StainStrong Django Application
# This script helps set up the application with proper security configurations

echo "=================================================="
echo "StainStrong Security Setup Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if .env exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success ".env file created"
    else
        print_error ".env.example not found"
        exit 1
    fi
fi

# Generate secret key if not set
if ! grep -q "DJANGO_SECRET_KEY=" .env || grep -q "your-secret-key-here" .env; then
    print_warning "Generating secure Django secret key..."
    SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    
    if [ -n "$SECRET_KEY" ]; then
        # Update or add secret key in .env
        if grep -q "DJANGO_SECRET_KEY=" .env; then
            sed -i "s|DJANGO_SECRET_KEY=.*|DJANGO_SECRET_KEY=$SECRET_KEY|" .env
        else
            echo "DJANGO_SECRET_KEY=$SECRET_KEY" >> .env
        fi
        print_success "Secret key generated and saved to .env"
    else
        print_error "Failed to generate secret key"
    fi
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_success "Dependencies installed"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Check for argon2
python -c "import argon2" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Argon2 password hashing installed"
else
    print_warning "Installing Argon2..."
    pip install argon2-cffi
    print_success "Argon2 installed"
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_success "Migrations completed"
else
    print_error "Migration failed"
fi

# Check password security
echo ""
echo "Checking password security..."
python manage.py check_password_security

# Run security check
echo ""
echo "Running Django security check..."
python manage.py check --deploy

# Create superuser if needed
echo ""
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo ""
read -p "Do you want to collect static files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py collectstatic --noinput
    print_success "Static files collected"
fi

# Final recommendations
echo ""
echo "=================================================="
echo "Security Setup Complete!"
echo "=================================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Review your .env file and update settings as needed"
echo "2. For production, set DEBUG=False in .env"
echo "3. Set ALLOWED_HOSTS to your domain name"
echo "4. Configure HTTPS/SSL on your web server"
echo "5. Set up a PostgreSQL database for production"
echo "6. Ask existing users to log in to upgrade passwords"
echo ""
echo "📚 Documentation:"
echo "- See SECURITY_GUIDE.md for detailed security information"
echo "- Run 'python manage.py check_password_security' to check password hashing"
echo ""
print_success "Setup completed successfully!"
