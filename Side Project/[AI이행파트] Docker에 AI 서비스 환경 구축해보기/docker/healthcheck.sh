#!/bin/bash

# Health check script for AI Sentiment Analysis Service

# Get server configuration
SERVER_HOST=${SERVER_HOST:-localhost}
SERVER_PORT=${SERVER_PORT:-8000}

# Health check URL
HEALTH_URL="http://${SERVER_HOST}:${SERVER_PORT}/health"

# Perform health check
response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$HEALTH_URL" 2>/dev/null)

# Extract HTTP status code
http_code=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
body=$(echo "$response" | sed 's/HTTPSTATUS:[0-9]*$//')

# Check if health endpoint responds with 200
if [ "$http_code" -eq 200 ]; then
    echo "Health check passed: $body"
    exit 0
else
    echo "Health check failed: HTTP $http_code"
    echo "Response: $body"
    exit 1
fi