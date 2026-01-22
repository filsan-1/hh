#!/bin/bash

# Docker Startup Script for Hormone Harmony
echo "🐳 Starting Hormone Harmony with Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [ -f .env.docker ]; then
        cp .env.docker .env
        echo "✅ Created .env file from .env.docker"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and set a secure DJANGO_SECRET_KEY"
        echo "   Generate one with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
        echo ""
        read -p "Press Enter to continue or Ctrl+C to exit and edit .env..."
    else
        echo "❌ Error: .env.docker template not found"
        exit 1
    fi
fi

# Stop any running containers
echo "🛑 Stopping any running containers..."
docker-compose down 2>/dev/null

# Build and start containers
echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting containers..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check container status
echo ""
echo "📊 Container Status:"
docker-compose ps

# Show logs
echo ""
echo "📝 Application logs (press Ctrl+C to stop viewing):"
echo ""
docker-compose logs -f web
