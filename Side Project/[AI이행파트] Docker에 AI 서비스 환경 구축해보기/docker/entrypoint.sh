#!/bin/bash
set -e

echo "Starting AI Sentiment Analysis Service..."

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default values
export SERVER_HOST=${SERVER_HOST:-0.0.0.0}
export SERVER_PORT=${SERVER_PORT:-8000}
export DEBUG_MODE=${DEBUG_MODE:-false}
export LOG_LEVEL=${LOG_LEVEL:-INFO}

echo "Server configuration:"
echo "  Host: $SERVER_HOST"
echo "  Port: $SERVER_PORT"
echo "  Debug: $DEBUG_MODE"
echo "  Log Level: $LOG_LEVEL"

# Download and cache model if not present
echo "Checking AI model availability..."
python -c "
from src.models.sentiment_model import SentimentModel
try:
    model = SentimentModel()
    print('Model loaded successfully')
except Exception as e:
    print(f'Model loading failed: {e}')
    exit(1)
"

echo "Starting FastAPI server..."
exec uvicorn src.main:app \
    --host $SERVER_HOST \
    --port $SERVER_PORT \
    --log-level $(echo $LOG_LEVEL | tr '[:upper:]' '[:lower:]') \
    ${DEBUG_MODE:+--reload}