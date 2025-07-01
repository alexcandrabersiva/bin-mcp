# Binance MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to Binance Futures API endpoints. This server implements all major trading, account management, and market data functionality as documented in the Binance Futures API.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
  - [API Requirements](#api-requirements)
  - [MCP Client Setup](#mcp-client-setup)
- [🛠️ Available Tools](#️-available-tools)
  - [Account Information](#account-information)
  - [Market Data](#market-data)
- [💡 Example Usage](#-example-usage)
- [🔒 Security](#-security)
- [📚 API Reference](#-api-reference)
- [🔧 Development](#-development)
- [❗ Error Codes](#-error-codes)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [⚠️ Disclaimer](#️-disclaimer)
- [💬 Support](#-support)

## 🚀 Quick Start

1. **Install the package:**
   ```bash
   pip install binance_futures_mcp
   ```

2. **Run the server:**
   ```bash
   uvx binance_futures_mcp --binance-api-key "your_key" --binance-secret-key "your_secret"
   ```

3. **Configure in your MCP client** (see [Configuration](#️-configuration) section for detailed setup)

## ✨ Features

* **11 essential trading tools** across 2 categories (Account Information and Market Data)
* **Proper authentication handling** (rejects unauthenticated requests)
* **Error handling and graceful degradation**
* **Real-time market data access**
* **Complete order management suite**
* **Risk management tools**

## 📦 Installation

### Option 1: PyPI Installation (Recommended)

Install the package from PyPI:

```bash
pip install binance_futures_mcp
```

### Option 2: Docker Deployment

For containerized deployment:

```bash
# Clone the repository
git clone https://github.com/alexcandrabersiva/bin-mcp.git
cd binance-mcp-server

# Build the Docker image
docker build -t binance-mcp-server .

# Run with environment variables
docker run -e BINANCE_API_KEY="your_api_key" -e BINANCE_SECRET_KEY="your_secret_key" \
  binance-mcp-server --binance-api-key "$BINANCE_API_KEY" --binance-secret-key "$BINANCE_SECRET_KEY"
```

#### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  binance-mcp:
    build: .
    environment:
      - BINANCE_API_KEY=${BINANCE_API_KEY}
      - BINANCE_SECRET_KEY=${BINANCE_SECRET_KEY}
    command: [
      "--binance-api-key", "${BINANCE_API_KEY}",
      "--binance-secret-key", "${BINANCE_SECRET_KEY}"
    ]
```

Then run:
```bash
docker-compose up
```

### Development Installation

For development, you can install from source:

```bash
git clone https://github.com/bin-mcp/binance-mcp-server.git
cd binance-mcp-server
pip install -e ".[dev]"
```

## ⚙️ Configuration

### API Requirements

Your Binance API key needs the following permissions:
- **Futures Trading**: For order placement and management
- **Futures Reading**: For account and market data access

### MCP Client Setup

This server can be integrated with various MCP clients. Here are configuration examples:

#### VS Code

Add to your VS Code `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "binance": {
        "command": "uvx",
        "args": ["--from", "binance_futures_mcp", "binance-mcp-server.exe", "--binance-api-key", "your_api_key", "--binance-secret-key", "your_secret_key"]
      }
    }
  }
}
```

#### Cursor

Add to your Cursor configuration file (`.cursor/mcp.json`):

```json
{
  "servers": {
    "binance": {
      "command": "uvx", 
      "args": ["--from", "binance_futures_mcp", "binance-mcp-server.exe", "--binance-api-key", "your_api_key", "--binance-secret-key", "your_secret_key"]
    }
  }
}
```

#### Windsurf

Add to your Windsurf configuration (`.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "binance": {
      "command": "uvx",
      "args": ["--from", "binance_futures_mcp", "binance-mcp-server.exe", "--binance-api-key", "your_api_key", "--binance-secret-key", "your_secret_key"]
    }
  }
}
```

#### Claude Desktop

Add to your Claude Desktop configuration file:

**On macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**On Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "binance": {
      "command": "uvx",
      "args": ["--from", "binance_futures_mcp", "binance-mcp-server.exe", "--binance-api-key", "your_api_key", "--binance-secret-key", "your_secret_key"]
    }
  }
}
```

### Configuration Notes

1. **No path needed**: With PyPI installation, you don't need to specify paths or working directories
2. **Set API credentials**: Replace `your_api_key` and `your_secret_key` with your actual Binance API credentials
3. **Alternative commands**: You can also use `uvx binance_futures_mcp` or `python -m binance_mcp`
4. **Security**: For production use, consider storing credentials in environment variables

## 🛠️ Available Tools

The server provides **11 essential tools** organized into the following categories:

### Account Information
*(5 tools)*

- `get_account_info` - Get account information
- `get_balance` - Get account balance
- `get_position_info` - Get position information
- `get_position_mode` - Get position mode (Hedge vs. One-way)
- `get_commission_rate` - Get commission rate

### Market Data
*(6 tools)*

- `get_exchange_info` - Get exchange trading rules
- `get_book_ticker` - Get best price/qty on the order book
- `get_price_ticker` - Get latest price for a symbol
- `get_order_book` - Get order book depth
- `get_klines` - Get candlestick data
- `get_mark_price` - Get mark price and funding rate

## 💡 Example Usage

### Place a Market Order

```json
{
  "tool": "place_order",
  "arguments": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "MARKET",
    "quantity": 0.001
  }
}
```

### Place a Limit Order

```json
{
  "tool": "place_order",
  "arguments": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "LIMIT",
    "quantity": 0.001,
    "price": 50000.0,
    "time_in_force": "GTC"
  }
}
```

### Get Account Information

```json
{
  "tool": "get_account_info",
  "arguments": {}
}
```

### Get Market Data

```json
{
  "tool": "get_klines",
  "arguments": {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 100
  }
}
```

### Get 24hr Price Statistics

```json
{
  "tool": "get_24hr_ticker",
  "arguments": {
    "symbol": "BTCUSDT"
  }
}
```

### Get Taker Buy/Sell Volume Ratio

```json
{
  "tool": "get_taker_buy_sell_volume",
  "arguments": {
    "symbol": "BTCUSDT"
  }
}
```

## 🔒 Security

### API Key Security

**🔐 Your Binance API key and secret remain completely local to your computer.** The MCP server runs entirely on your machine; neither the package author nor any third-party remote service can access your credentials.

#### Key Security Points:
- ✅ Store credentials in environment variables (recommended) or local config files
- ✅ Keys are never transmitted unless *you* publish them
- ❌ Never commit credentials to version control
- ❌ Never share screenshots/logs containing credentials
- ✅ Use API keys with minimal required permissions
- ✅ IP-whitelist your keys when possible
- ✅ Consider using Binance Testnet for development



#### How It Works:
1. **Local Launch**: Your editor/terminal launches the MCP server locally:
   ```bash
   uvx binance_futures_mcp --binance-api-key $BINANCE_API_KEY --binance-secret-key $BINANCE_SECRET_KEY
   ```

2. **Keys Stay Local**: Your credentials exist only:
   - In your environment variables or local config file
   - On your computer's command line/process table
   - In MCP process memory during HTTPS calls to Binance

3. **No Telemetry**: The package contains **zero** telemetry or analytics code

### Rate Limiting & Error Handling

- ⚡ Respects Binance's weight-based rate limits
- 🔄 Automatic order placement rate limiting
- 🔐 Automatic HMAC SHA256 signature generation
- 🛡️ Comprehensive error handling with clear messages
- ✅ Parameter validation before API calls

## 📚 API Reference

This server implements all endpoints documented in the Binance Futures API:

- **Base URL**: `https://fapi.binance.com`
- **API Type**: Binance USD-S Margined Futures
- **Authentication**: API Key + HMAC SHA256 Signature
- **Rate Limits**: Respected automatically

For detailed parameter specifications, see the [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/).

## 🔧 Development

### Project Structure

```
binance-mcp-server/
├── src/
│   └── binance_mcp/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # CLI entry point
│       ├── server.py            # Main MCP server implementation
│       ├── client.py            # Binance API client
│       ├── handlers.py          # Tool execution handlers
│       ├── tools.py             # Tool definitions (11 trading tools)
│       └── config.py            # Configuration management
├── Dockerfile                   # Docker containerization
├── .dockerignore               # Docker build optimization
├── pyproject.toml              # Project configuration
├── mcp-config.json             # MCP client configuration example
└── README.md                   # Documentation
```

#### Architecture Overview

- **Modular Design**: Separated concerns across multiple components
- **Authentication**: Secure API key handling with environment variables
- **Error Handling**: Graceful degradation and comprehensive error management

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## ❗ Error Codes

Common Binance API error codes you might encounter:

| Code | Description |
|------|-------------|
| `-1121` | Invalid symbol |
| `-2019` | Margin is insufficient |
| `-1116` | Invalid orderType |
| `-1013` | Filter failure (PRICE_FILTER, LOT_SIZE, etc.) |
| `-1102` | Mandatory parameter was not sent |
| `-1003` | Too many requests (rate limit exceeded) |

For a complete list, see the [Binance API Error Codes](https://binance-docs.github.io/apidocs/futures/en/#error-codes).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

**⚠️ IMPORTANT**: This software is for educational and development purposes. Trading cryptocurrencies involves substantial risk. Use at your own risk and never trade with money you cannot afford to lose.

## 💬 Support

For issues and questions:
- Check the [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- Review the error codes in the API documentation
- Ensure your API credentials have the correct permissions
