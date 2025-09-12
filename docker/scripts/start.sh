#!/bin/bash
# Start OpenSearch containers using Podman

echo "🐳 Starting OpenSearch containers with Podman..."

# Check if podman-compose is available
if command -v podman-compose &> /dev/null; then
    echo "Using podman-compose..."
    podman-compose -f ../docker-compose.yml up -d
elif command -v docker-compose &> /dev/null; then
    echo "Using docker-compose..."
    docker-compose -f ../docker-compose.yml up -d
else
    echo "❌ Neither podman-compose nor docker-compose found!"
    echo "Please install podman-compose or docker-compose"
    exit 1
fi

echo "✅ Containers started successfully!"
echo "OpenSearch: http://localhost:9200"
echo "Dashboards: http://localhost:5601"
echo ""
echo "To check status: ./status.sh"
echo "To load data: ./load_data.sh"
