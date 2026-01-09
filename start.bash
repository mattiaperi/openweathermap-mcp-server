# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required packages
python3 -m pip3 install --no-cache-dir -r requirements.txt

# Test locally
python3 test_api_weather.py
python3 test_mcp_client.py Milan
