# Example MCP Client Configurations

## VS Code Settings (settings.json)

Add this to your VS Code settings.json file:

```json
{
  "mcp": {
    "servers": {
      "binance-mcp": {
        "command": "uv",
        "args": [
          "--directory",
          "/root/binance-mcp-server",
          "run",
          "binance.py",
          "--binance-api-key",
          "YOUR_BINANCE_API_KEY_HERE",
          "--binance-secret-key",
          "YOUR_BINANCE_SECRET_KEY_HERE"
        ]
      }
    }
  }
}
```

## Claude Desktop App Configuration (app.json)

Add this to your Claude Desktop app.json file:

```json
{
  "mcpServers": {
    "binance-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/root/binance-mcp-server",
        "run",
        "binance.py",
        "--binance-api-key",
        "YOUR_BINANCE_API_KEY_HERE",
        "--binance-secret-key",
        "YOUR_BINANCE_SECRET_KEY_HERE"
      ]
    }
  }
}
```

## Alternative: Using Environment Variables

If you prefer to use environment variables instead of command-line arguments:

```json
{
  "mcpServers": {
    "binance-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/root/binance-mcp-server",
        "run",
        "binance.py"
      ],
      "env": {
        "BINANCE_API_KEY": "YOUR_BINANCE_API_KEY_HERE",
        "BINANCE_SECRET_KEY": "YOUR_BINANCE_SECRET_KEY_HERE"
      }
    }
  }
}
```

## Replace the Placeholders

Replace the following placeholders with your actual Binance API credentials:
- `YOUR_BINANCE_API_KEY_HERE` - Your Binance API key
- `YOUR_BINANCE_SECRET_KEY_HERE` - Your Binance secret key

## Getting Binance API Credentials

1. Log in to your Binance account
2. Go to API Management
3. Create a new API key
4. Enable "Enable Futures" permission
5. Note down your API key and secret key
6. Configure IP restrictions for security (recommended)
