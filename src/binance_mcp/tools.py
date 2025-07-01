#!/usr/bin/env python3
"""
MCP Tool Definitions for Binance Futures API
"""

from mcp.types import Tool


def get_account_tools():
    """Account information tools"""
    return [
        Tool(
            name="get_account_info",
            description="Get futures account information V2",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_balance", 
            description="Get futures account balance V2",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_position_info",
            description="Get current position information V2",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"}
                },
                "required": []
            }
        ),
        Tool(
            name="get_position_mode",
            description="Get user's position mode (Hedge Mode or One-way Mode)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_commission_rate",
            description="Get user's commission rate for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"}
                },
                "required": ["symbol"]
            }
        ),
    ]


# Risk management tools have been moved to the premium repository


# Order management tools have been moved to the premium repository


# Order query tools have been moved to the premium repository


# Position tools have been moved to the premium repository




def get_market_data_tools():
    """Market data tools"""
    return [
        Tool(
            name="get_exchange_info",
            description="Get exchange trading rules and symbol information",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol (optional)"}
                },
                "required": []
            }
        ),
        Tool(
            name="get_book_ticker",
            description="Get best price/qty on the order book for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"}
                },
                "required": []
            }
        ),
        Tool(
            name="get_price_ticker",
            description="Get latest price for a symbol", 
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"}
                },
                "required": []
            }
        ),
        Tool(
            name="get_order_book",
            description="Get order book for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "limit": {"type": "integer", "description": "Number of bids/asks (5,10,20,50,100,500,1000)"}
                },
                "required": ["symbol", "limit"]
            }
        ),
        Tool(
            name="get_klines",
            description="Get kline/candlestick data for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "interval": {"type": "string", "description": "Kline interval"},
                    "start_time": {"type": "integer", "description": "Start timestamp in ms"},
                    "end_time": {"type": "integer", "description": "End timestamp in ms"},
                    "limit": {"type": "integer", "description": "Number of klines (max 1500)"}
                },
                "required": ["symbol", "interval"]
            }
        ),
        Tool(
            name="get_mark_price",
            description="Get mark price and funding rate for a symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"}
                },
                "required": []
            }
        ),
    ]


# Trading history tools have been moved to the premium repository


def get_all_tools():
    """Get all MCP tools"""
    tools = []
    tools.extend(get_account_tools())
    tools.extend(get_market_data_tools())
    return tools
