#!/bin/bash
# Stop OpenSearch containers

echo "🛑 Stopping OpenSearch containers..."

# Check if podman-compose is available
if command -v podman-compose &> /dev/null; then
    echo "Using podman-compose..."
    podman-compose -f ../docker-compose.yml down
elif command -v docker-compose &> /dev/null; then
    echo "Using docker-compose..."
    docker-compose -f ../docker-compose.yml down
else
    echo "❌ Neither podman-compose nor docker-compose found!"
    exit 1
fi

echo "✅ Containers stopped successfully!"
