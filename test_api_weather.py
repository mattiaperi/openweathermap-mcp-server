#!/usr/bin/env python3
import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY environment variable is required")

BASE_URL = "http://api.openweathermap.org/data/2.5"

def test_current_weather(city: str):
    """Test current weather API"""
    try:
        params = {"q": city, "APPID": API_KEY, "units": "metric"}
        response = requests.get(f"{BASE_URL}/weather", params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"Current Weather in {data['name']}:")
        print(f"  Temperature: {data['main']['temp']}°C")
        print(f"  Condition: {data['weather'][0]['description']}")
        print(f"  Humidity: {data['main']['humidity']}%")
        print(f"  Pressure: {data['main']['pressure']} hPa")
        
    except Exception as e:
        print(f"Current weather error: {e}")

def test_weather_forecast(city: str):
    """Test 5-day forecast API"""
    try:
        params = {"q": city, "APPID": API_KEY, "units": "metric"}
        response = requests.get(f"{BASE_URL}/forecast", params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"\n5-Day Forecast for {data['city']['name']}:")
        for item in data['list'][:7]:  # Show first 7 entries
            print(f"  {item['dt_txt']}: {item['main']['temp']}°C, {item['weather'][0]['description']}")
        
    except Exception as e:
        print(f"Forecast error: {e}")

def test_air_pollution(city: str):
    """Test air pollution API"""
    try:
        # Get coordinates
        geo_params = {"q": city, "limit": 1, "appid": API_KEY}
        geo_response = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            print(f"City {city} not found for air pollution")
            return
        
        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
        
        # Get pollution data
        pollution_response = requests.get(f"{BASE_URL}/air_pollution", params={"lat": lat, "lon": lon, "appid": API_KEY})
        pollution_response.raise_for_status()
        data = pollution_response.json()
        
        aqi = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']
        print(f"\nAir Pollution in {city}:")
        print(f"  AQI: {aqi} (1=Good, 5=Very Poor)")
        print(f"  PM2.5: {components.get('pm2_5', 'N/A')} μg/m³")
        print(f"  PM10: {components.get('pm10', 'N/A')} μg/m³")
        
    except Exception as e:
        print(f"Air pollution error: {e}")

if __name__ == "__main__":
    cities = ["Milan", "New York"]
    
    for city in cities:
        print(f"\n{'='*50}")
        print(f"Testing APIs for {city}")
        print(f"{'='*50}")
        
        test_current_weather(city)
        test_weather_forecast(city)
        test_air_pollution(city)