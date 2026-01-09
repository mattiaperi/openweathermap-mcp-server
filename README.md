# OpenWeatherMap MCP Server

A Model Context Protocol (MCP) server that provides weather data using the OpenWeatherMap API. This example demonstrates how to build an MCP server with multiple tools for current weather, forecasts, and air pollution data.

## Features

- **Current Weather**: Get real-time weather conditions for any city
- **5-Day Forecast**: Retrieve weather forecasts with 3-hour intervals
- **Air Pollution**: Access air quality data including pollutant concentrations

## Prerequisites

- Python 3.12+
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

## Installation

1. Clone this repository:
```bash
git clone git@github.com:mattiaperi/openweathermap-mcp-server.git
cd openweathermap-mcp-server
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Set your OpenWeatherMap API key:
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

## Usage

### Running the Server

```bash
python server.py
```

### Testing with the Client

```bash
python test_mcp_client.py Milan
# or
python test_mcp_client.py # Will prompt for city name
```

### Using with Amazon Q

1. Create `.amazonq/mcp.json` in your project:
```json
{
  "mcpServers": {
    "weather": {
      "command": ".venv/bin/python",
      "args": ["server.py"],
      "env": {}
    }
  }
}
```

2. Restart Amazon Q and ask: "What's the weather like in Tokyo?"

## Available Tools

### `get_current_weather(city: str)`
Returns current weather conditions including temperature, humidity, pressure, and weather description.

### `get_weather_forecast(city: str)`
Returns a 5-day weather forecast with data points every 3 hours.

### `get_air_pollution(city: str)`
Returns air quality data including AQI and pollutant concentrations (CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3).

## API Response Format

All tools return the complete OpenWeatherMap API response, allowing LLMs to extract relevant information based on context. Error responses include an `error` field with descriptive messages.

## Development

### Project Structure
```
├── server.py          # MCP server implementation
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

### Adding New Tools

1. Define a function with type hints
2. Add the `@mcp.tool` decorator
3. Include a descriptive docstring
4. Handle errors gracefully

Example:
```python
@mcp.tool
def get_uv_index(city: str) -> dict:
    """Get UV index data for a city."""
    # Implementation here
```

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider rate limiting for production use
- Validate input parameters

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Library](https://github.com/jlowin/fastmcp)
- [OpenWeatherMap API](https://openweathermap.org/api)
