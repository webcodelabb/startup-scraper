#!/bin/bash

# Startup Funding Scraper Deployment Script

echo "🚀 Deploying Startup Funding Scraper..."

# Create necessary directories
mkdir -p data logs

# Build and run with Docker Compose
echo "📦 Building and starting containers..."
docker-compose up --build -d

echo "✅ Deployment completed!"
echo ""
echo "📊 Access your scraped data:"
echo "   - Web interface: http://localhost:8080"
echo "   - CSV file: http://localhost:8080/funded_startups.csv"
echo "   - JSON file: http://localhost:8080/funded_startups.json"
echo ""
echo "📁 Local data directory: ./data/"
echo "📝 Logs directory: ./logs/"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose logs -f scraper"
echo "   - Stop services: docker-compose down"
echo "   - Restart scraper: docker-compose restart scraper" 