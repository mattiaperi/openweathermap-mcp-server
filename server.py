import os
import requests
from fastmcp import FastMCP

# Initialize the server with a name
mcp = FastMCP("weather")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable is required")

BASE_URL = "http://api.openweathermap.org/data/2.5"

# Define a tool using the @mcp.tool decorator
# @mcp.tool is the decorator that turns any function into an MCP tool
@mcp.tool
def get_current_weather(city: str) -> dict:   # Type hints (city: str, -> dict) tell MCP the expected inputs and outputs
    """Get the current weather for a city.""" # The docstring becomes the tool's description (LLMs use this to understand when to call it)
    try:
        params = {
            "q": city,
            "APPID": API_KEY,
            "units": "metric"
        }
        response = requests.get(f"{BASE_URL}/weather", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to get weather for {city}: {str(e)}"}

@mcp.tool
def get_weather_forecast(city: str) -> dict:
    """Get 5-day weather forecast for a city."""
    try:
        params = {
            "q": city,
            "APPID": API_KEY,
            "units": "metric"
        }
        response = requests.get(f"{BASE_URL}/forecast", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to get forecast for {city}: {str(e)}"}

@mcp.tool
def get_air_pollution(city: str) -> dict:
    """Get air pollution data for a city."""
    try:
        # First get coordinates
        geo_params = {
            "q": city,
            "limit": 1,
            "appid": API_KEY
        }
        geo_response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            return {"error": f"City {city} not found"}
        
        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
        
        # Get pollution data
        pollution_response = requests.get(f"{BASE_URL}/air_pollution", params={"lat": lat, "lon": lon, "appid": API_KEY})
        pollution_response.raise_for_status()
        return pollution_response.json()
    except Exception as e:
        return {"error": f"Failed to get air pollution for {city}: {str(e)}"}

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
    # mcp.run(transport="http", host="0.0.0.0", port=8000)
