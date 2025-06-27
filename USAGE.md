# Binance MCP Server Usage Guide

## Overview

This Binance MCP server provides access to Binance Futures API through the Model Context Protocol (MCP). It implements all major Binance Futures trading operations including account management, order placement, market data retrieval, and trading history.

## Installation and Setup

### 1. Server Installation

The server is already set up in this directory with all dependencies installed.

### 2. Client Configuration

To connect from your local VS Code or other MCP client, add the following configuration to your MCP settings:

#### For VS Code settings.json:

```json
{
  "mcp": {
    "servers": {
      "binance-futures-mcp": {
        "command": "uv",
        "args": [
          "--directory",
          "/root/binance-mcp-server",
          "run",
          "binance.py",
          "--binance-api-key",
          "YOUR_BINANCE_API_KEY",
          "--binance-secret-key",
          "YOUR_BINANCE_SECRET_KEY"
        ]
      }
    }
  }
}
```

#### For Claude Desktop app.json:

```json
{
  "mcpServers": {
    "binance-futures-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/root/binance-mcp-server",
        "run",
        "binance.py",
        "--binance-api-key",
        "YOUR_BINANCE_API_KEY",
        "--binance-secret-key",
        "YOUR_BINANCE_SECRET_KEY"
      ]
    }
  }
}
```

## Available Tools

### Account Information Tools
- `get_account_info` - Get futures account information
- `get_balance` - Get account balance for all assets
- `get_position_info` - Get current position information
- `get_position_mode` - Get position mode (Hedge/One-way)
- `get_commission_rate` - Get commission rate for symbol

### Risk Management Tools
- `get_adl_quantile` - Get ADL quantile estimation
- `get_leverage_brackets` - Get leverage brackets
- `get_force_orders` - Get liquidation orders
- `get_position_margin_history` - Get margin change history

### Order Management Tools
- `place_order` - Place a futures order
- `place_multiple_orders` - Place multiple orders
- `cancel_order` - Cancel an order
- `cancel_multiple_orders` - Cancel multiple orders
- `cancel_all_orders` - Cancel all open orders
- `auto_cancel_all_orders` - Set auto-cancellation
- `get_open_order` - Query specific open order
- `get_open_orders` - Get all open orders
- `get_all_orders` - Get order history
- `query_order` - Query order status

### Trading Configuration Tools
- `change_leverage` - Change leverage (1-125x)
- `change_margin_type` - Change margin type (ISOLATED/CROSSED)
- `change_position_mode` - Change position mode
- `modify_position_margin` - Modify position margin

### Market Data Tools
- `get_exchange_info` - Get exchange information
- `get_book_ticker` - Get best bid/ask prices
- `get_price_ticker` - Get latest prices
- `get_order_book` - Get order book depth
- `get_klines` - Get candlestick data
- `get_mark_price` - Get mark price and funding rate
- `get_aggregate_trades` - Get aggregate trades

### Trading History Tools
- `get_account_trades` - Get trade history
- `get_income_history` - Get income history
- `get_funding_rate_history` - Get funding rate history

## Usage Examples

### Basic Account Information
```
Get my account information
```

### Market Data
```
Get the current price of BTCUSDT
Get the order book for ETHUSDT with limit 10
Get 1-hour candlestick data for BTCUSDT
```

### Trading Operations
```
Place a market buy order for 0.001 BTC on BTCUSDT
Place a limit sell order for 0.001 BTC at $50000 on BTCUSDT
Cancel all open orders for BTCUSDT
Change leverage to 10x for BTCUSDT
```

## Security Notes

- **⚠️  IMPORTANT**: Never commit real API credentials to version control
- **API Credentials**: Use environment variables or .env files for real credentials
- **Permissions**: Ensure your Binance API key has futures trading permissions enabled
- **Rate Limits**: The server respects Binance API rate limits automatically
- **Network**: This server connects to Binance's production environment
- **Example Credentials**: All configuration examples use placeholder values - replace with your real credentials

### Secure Credential Management

1. **Environment Variables** (Recommended):
   ```bash
   export BINANCE_API_KEY="your_real_api_key"
   export BINANCE_SECRET_KEY="your_real_secret_key"
   ```

2. **Using .env file**:
   ```bash
   cp .env.template .env
   # Edit .env with your real credentials
   source .env
   ```

3. **Replace placeholders** in the configuration examples above with your real API credentials.

## Troubleshooting

### Common Issues

1. **Connection Refused**: Make sure the server path is correct and uv is installed
2. **Authentication Error**: Verify API key and secret are correct and have proper permissions
3. **Rate Limit**: If you hit rate limits, wait a few seconds before retrying
4. **Symbol Errors**: Ensure you're using correct symbol format (e.g., "BTCUSDT" not "BTC/USDT")

### Testing the Server

You can test the server locally by running:

```bash
cd /root/binance-mcp-server
uv run binance.py --binance-api-key YOUR_KEY --binance-secret-key YOUR_SECRET
```

The server should start and wait for MCP protocol messages on stdin/stdout.

## API Documentation Reference

For detailed information about each tool's parameters and responses, refer to:
- Binance Futures API Documentation: https://binance-docs.github.io/apidocs/futures/en/
- The attached BINANCE-MCP-API-MAPPING.md file

## Support

If you encounter issues:
1. Check the server logs for error messages
2. Verify your API credentials and permissions
3. Ensure you're using the correct symbol formats
4. Check Binance API status at https://binance.com/status
