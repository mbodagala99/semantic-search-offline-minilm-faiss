#!/bin/bash
# Check OpenSearch container status

echo "📊 Checking OpenSearch container status..."

# Check if containers are running
if command -v podman &> /dev/null; then
    echo "Using Podman..."
    podman ps --filter "name=healthcare-opensearch"
    podman ps --filter "name=healthcare-dashboards"
elif command -v docker &> /dev/null; then
    echo "Using Docker..."
    docker ps --filter "name=healthcare-opensearch"
    docker ps --filter "name=healthcare-dashboards"
else
    echo "❌ Neither Podman nor Docker found!"
    exit 1
fi

echo ""
echo "🔍 Checking OpenSearch health..."

# Wait for OpenSearch to be ready
for i in {1..30}; do
    if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
        echo "✅ OpenSearch is healthy and ready!"
        curl -s http://localhost:9200/_cluster/health | jq .
        break
    else
        echo "⏳ Waiting for OpenSearch to be ready... ($i/30)"
        sleep 2
    fi
done

echo ""
echo "🌐 Access URLs:"
echo "OpenSearch: http://localhost:9200"
echo "Dashboards: http://localhost:5601"
