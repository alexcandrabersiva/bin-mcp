# Binance MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to Binance Futures API endpoints. This server implements all major trading, account management, and market data functionality as documented in the Binance Futures API.

## Features

### Account Information Tools
- Get account info, balance, and position information
- Query position mode and commission rates
- Access risk management data (ADL quantile, leverage brackets, force orders)

### Order Management Tools
- Place orders (MARKET, LIMIT, STOP, STOP_MARKET, TRAILING_STOP_MARKET)
- Place multiple orders in batch
- Cancel orders (single, multiple, or all)
- Query order status and history
- Auto-cancel functionality

### Trading Configuration Tools
- Change leverage and margin type
- Switch between hedge and one-way position modes
- Modify position margins

### Market Data Tools
- Get exchange information and trading rules
- Access real-time price data and order books
- Retrieve candlestick/kline data
- Get mark prices and funding rates
- Access aggregate trade data

### Trading History Tools
- Get account trade history
- Access income history (funding fees, PnL, etc.)
- Retrieve funding rate history

## Installation

### Prerequisites
- Python 3.8 or higher
- Binance Futures API credentials

### Install Dependencies

```bash
cd binance-mcp-server
pip install -e .
```

Or install development dependencies:

```bash
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Set your Binance API credentials as environment variables:

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_SECRET_KEY="your_secret_key_here"
```

### API Permissions

Your Binance API key needs the following permissions:
- **Futures Trading**: For order placement and management
- **Futures Reading**: For account and market data access

**Note**: Market data endpoints (exchange info, prices, order books, etc.) work without authentication.

## Usage

### Running the Server

```bash
# Run directly
python -m binance_mcp

# Or using the installed script
binance-mcp-server
```

### Available Tools

The server provides 32 tools organized into categories:

#### Account Information (5 tools)
- `get_account_info` - Get futures account information
- `get_balance` - Get account balance for all assets
- `get_position_info` - Get current position information
- `get_position_mode` - Get position mode (Hedge/One-way)
- `get_commission_rate` - Get commission rate for a symbol

#### Risk Management (4 tools)
- `get_adl_quantile` - Get ADL quantile estimation
- `get_leverage_brackets` - Get leverage brackets
- `get_force_orders` - Get liquidation orders
- `get_position_margin_history` - Get margin change history

#### Order Management (10 tools)
- `place_order` - Place a futures order
- `place_multiple_orders` - Place multiple orders in batch
- `cancel_order` - Cancel an active order
- `cancel_multiple_orders` - Cancel multiple orders
- `cancel_all_orders` - Cancel all open orders for a symbol
- `auto_cancel_all_orders` - Set up auto-cancellation
- `get_open_order` - Query specific open order
- `get_open_orders` - Get all open orders
- `get_all_orders` - Get all orders (filled, canceled, rejected)
- `query_order` - Query order status

#### Trading Configuration (4 tools)
- `change_leverage` - Change initial leverage
- `change_margin_type` - Change margin type (ISOLATED/CROSSED)
- `change_position_mode` - Change position mode
- `modify_position_margin` - Modify position margin

#### Market Data (6 tools)
- `get_exchange_info` - Get trading rules and symbol info
- `get_book_ticker` - Get best bid/ask prices
- `get_price_ticker` - Get latest prices
- `get_order_book` - Get order book depth
- `get_klines` - Get candlestick data
- `get_mark_price` - Get mark price and funding rate
- `get_aggregate_trades` - Get aggregate trade data

#### Trading History (3 tools)
- `get_account_trades` - Get account trade history
- `get_income_history` - Get income history
- `get_funding_rate_history` - Get funding rate history

## Example Usage

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

## Security

### API Key Security
- Store API credentials securely using environment variables
- Never commit credentials to version control
- Use API keys with minimal required permissions
- Consider using testnet for development

### Rate Limiting
The server respects Binance's rate limits:
- Weight-based limits for different endpoints
- Order placement rate limits
- Automatic signature generation for authenticated requests

### Error Handling
- Comprehensive error handling for API failures
- Clear error messages for common issues
- Validation of required parameters

## API Reference

This server implements all endpoints documented in the Binance Futures API:

- **Base URL**: `https://fapi.binance.com`
- **API Type**: Binance USD-S Margined Futures
- **Authentication**: API Key + HMAC SHA256 Signature

For detailed parameter specifications, see the [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/).

## Development

### Project Structure

```
binance-mcp-server/
├── src/
│   └── binance_mcp/
│       ├── __init__.py
│       ├── __main__.py
│       └── server.py
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## Error Codes

Common Binance API error codes:
- `-1121`: Invalid symbol
- `-2019`: Margin is insufficient  
- `-1116`: Invalid orderType
- `-1013`: Filter failure (PRICE_FILTER, LOT_SIZE, etc.)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This software is for educational and development purposes. Trading cryptocurrencies involves substantial risk. Use at your own risk and never trade with money you cannot afford to lose.

## Support

For issues and questions:
- Check the [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- Review the error codes in the API documentation
- Ensure your API credentials have the correct permissions
