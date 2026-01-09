#!/bin/bash
set -e

# Export the API key if provided as argument or environment variable
if [ -n "$1" ]; then
    export OPENWEATHER_API_KEY="$1"
elif [ -n "$OPENWEATHER_API_KEY" ]; then
    export OPENWEATHER_API_KEY="$OPENWEATHER_API_KEY"
else
    echo "Error: OPENWEATHER_API_KEY not provided"
    exit 1
fi

echo "Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running API tests..."
python3 test_api_weather.py

echo "Running MCP client tests..."
python3 test_mcp_client.py Milan

echo "All tests passed!"