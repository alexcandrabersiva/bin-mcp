#!/usr/bin/env python3

import asyncio
import hashlib
import hmac
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import aiohttp
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field


class BinanceConfig:
    """Configuration for Binance API"""
    BASE_URL = "https://fapi.binance.com"
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.api_key = api_key
        self.secret_key = secret_key


class BinanceClient:
    """Binance Futures API client with improved connectivity"""
    
    def __init__(self, config: BinanceConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        # Create session with better connectivity settings
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            ttl_dns_cache=300,
            use_dns_cache=True,
            limit=100,
            limit_per_host=10,
            enable_cleanup_closed=True
        )
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                'User-Agent': 'binance-mcp-server/1.0.6',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC SHA256 signature"""
        return hmac.new(
            self.config.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        security_type: str = "NONE"
    ) -> Dict[str, Any]:
        """Make API request to Binance"""
        
        if params is None:
            params = {}
        
        url = self.config.BASE_URL + endpoint
        headers = {}
        
        if security_type in ["USER_DATA", "TRADE"]:
            # Add API key to headers
            headers["X-MBX-APIKEY"] = self.config.api_key
            
            # Add timestamp
            params["timestamp"] = int(time.time() * 1000)
            
            # Generate signature
            query_string = urlencode(params)
            signature = self._generate_signature(query_string)
            params["signature"] = signature
        
        try:
            if method == "GET":
                async with self.session.get(url, params=params, headers=headers, ssl=False) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method == "POST":
                async with self.session.post(url, data=params, headers=headers, ssl=False) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method == "DELETE":
                async with self.session.delete(url, data=params, headers=headers, ssl=False) as response:
                    response.raise_for_status()
                    return await response.json()
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
        except aiohttp.ClientError as e:
            raise Exception(f"Network error connecting to Binance API: {str(e)}")
        except asyncio.TimeoutError:
            raise Exception("Request timeout - please check your internet connection")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")


class BinanceMCPServer:
    """Binance MCP Server implementation"""
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.server = Server("binance-futures-mcp-server")
        self.config = BinanceConfig(api_key, secret_key)
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup all MCP tools"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """Handle tools/list requests"""
            return [
                # Account Information Tools
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
                
                # Risk Management Tools
                Tool(
                    name="get_adl_quantile",
                    description="Get position ADL quantile estimation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"}
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_leverage_brackets",
                    description="Get notional and leverage brackets",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"}
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_force_orders",
                    description="Get user's force orders",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "auto_close_type": {"type": "string", "description": "Optional filter by auto-close type"},
                            "start_time": {"type": "integer", "description": "Optional start time in ms"},
                            "end_time": {"type": "integer", "description": "Optional end time in ms"},
                            "limit": {"type": "integer", "description": "Maximum number of orders to return (default 50)"}
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_position_margin_history",
                    description="Get position margin modification history",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "margin_type": {"type": "integer", "description": "1 for add position margin, 2 for reduce position margin"},
                            "limit": {"type": "integer", "description": "Number of entries to return"}
                        },
                        "required": ["symbol", "margin_type", "limit"]
                    }
                ),

                # Order Management Tools
                Tool(
                    name="place_order",
                    description="Place a futures order of any type (MARKET, LIMIT, STOP, STOP_MARKET, TRAILING_STOP_MARKET, etc)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "side": {"type": "string", "description": "Order side ('BUY' or 'SELL')"},
                            "order_type": {"type": "string", "description": "Order type ('MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TRAILING_STOP_MARKET', etc)"},
                            "quantity": {"type": "number", "description": "Order quantity"},
                            "price": {"type": "number", "description": "Order price (for LIMIT orders)"},
                            "stop_price": {"type": "number", "description": "Stop price (for STOP orders)"},
                            "time_in_force": {"type": "string", "description": "Time in force (GTC, IOC, FOK)"},
                            "position_side": {"type": "string", "description": "Position side ('BOTH', 'LONG', 'SHORT')"},
                            "reduce_only": {"type": "string", "description": "Reduce only flag"},
                            "new_client_order_id": {"type": "string", "description": "Custom order ID"},
                            "close_position": {"type": "string", "description": "Close position flag"},
                            "activation_price": {"type": "number", "description": "Activation price (for TRAILING_STOP_MARKET)"},
                            "callback_rate": {"type": "number", "description": "Callback rate (for TRAILING_STOP_MARKET)"},
                            "working_type": {"type": "string", "description": "Working type (MARK_PRICE, CONTRACT_PRICE)"},
                            "price_protect": {"type": "string", "description": "Price protection flag"},
                            "new_order_resp_type": {"type": "string", "description": "Response type"},
                            "recv_window": {"type": "integer", "description": "Receive window"},
                            "timestamp": {"type": "integer", "description": "Timestamp"},
                            "quantity_precision": {"type": "integer", "description": "Quantity precision for validation"},
                            "price_precision": {"type": "integer", "description": "Price precision for validation"}
                        },
                        "required": ["symbol", "side", "order_type"]
                    }
                ),
                Tool(
                    name="place_multiple_orders",
                    description="Place multiple orders at once",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "orders": {
                                "type": "array", 
                                "description": "List of order parameters",
                                "items": {"type": "object"}
                            },
                            "quantity_precision": {"type": "integer", "description": "Quantity precision for validation"},
                            "price_precision": {"type": "integer", "description": "Price precision for validation"}
                        },
                        "required": ["orders"]
                    }
                ),
                Tool(
                    name="cancel_order",
                    description="Cancel an active order",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "order_id": {"type": "integer", "description": "Order ID to cancel"}
                        },
                        "required": ["symbol", "order_id"]
                    }
                ),
                Tool(
                    name="cancel_multiple_orders",
                    description="Cancel multiple orders",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "order_id_list": {
                                "type": "array", 
                                "description": "List of order IDs to cancel (up to 10 orders per batch)",
                                "items": {"type": "integer"}
                            }
                        },
                        "required": ["symbol", "order_id_list"]
                    }
                ),
                Tool(
                    name="cancel_all_orders",
                    description="Cancel all open orders for a symbol",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"}
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="auto_cancel_all_orders",
                    description="Set up auto-cancellation of all orders after countdown",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "countdown_time": {"type": "integer", "description": "Countdown time in milliseconds"}
                        },
                        "required": ["symbol", "countdown_time"]
                    }
                ),

                # Order Query Tools
                Tool(
                    name="get_open_order",
                    description="Query current open order by order id",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "order_id": {"type": "integer", "description": "Order ID to query"}
                        },
                        "required": ["symbol", "order_id"]
                    }
                ),
                Tool(
                    name="get_open_orders",
                    description="Get all open futures orders for a specific symbol",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"}
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_all_orders",
                    description="Get all account orders",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "order_id": {"type": "integer", "description": "Optional order ID to start from"},
                            "start_time": {"type": "integer", "description": "Optional start time in ms"},
                            "end_time": {"type": "integer", "description": "Optional end time in ms"},
                            "limit": {"type": "integer", "description": "Maximum number of orders to return (default 500)"}
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="query_order",
                    description="Query a specific order's status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "order_id": {"type": "integer", "description": "Order ID to query"}
                        },
                        "required": ["symbol", "order_id"]
                    }
                ),

                # Trading Configuration Tools
                Tool(
                    name="change_leverage",
                    description="Change initial leverage for a symbol",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "leverage": {"type": "integer", "description": "Target initial leverage (1-125)"}
                        },
                        "required": ["symbol", "leverage"]
                    }
                ),
                Tool(
                    name="change_margin_type",
                    description="Change margin type between isolated and cross",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "margin_type": {"type": "string", "description": "'ISOLATED' or 'CROSSED'"}
                        },
                        "required": ["symbol", "margin_type"]
                    }
                ),
                Tool(
                    name="change_position_mode",
                    description="Change position mode between Hedge Mode and One-way Mode",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "dual_side": {"type": "boolean", "description": "\"true\" for Hedge Mode, \"false\" for One-way Mode"}
                        },
                        "required": ["dual_side"]
                    }
                ),
                Tool(
                    name="modify_position_margin",
                    description="Modify isolated position margin",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "amount": {"type": "number", "description": "Amount to modify"},
                            "position_side": {"type": "string", "description": "Position side ('BOTH', 'LONG', or 'SHORT')"},
                            "margin_type": {"type": "integer", "description": "1 for add position margin, 2 for reduce position margin"}
                        },
                        "required": ["symbol", "amount", "position_side", "margin_type"]
                    }
                ),

                # Market Data Tools
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
                    name="get_24hr_ticker",
                    description="Get 24hr ticker price change statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol (optional, if not provided returns all symbols)"}
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
                Tool(
                    name="get_aggregate_trades",
                    description="Get compressed, aggregate market trades",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "from_id": {"type": "integer", "description": "ID to get trades from"},
                            "start_time": {"type": "integer", "description": "Start timestamp in ms"},
                            "end_time": {"type": "integer", "description": "End timestamp in ms"},
                            "limit": {"type": "integer", "description": "Number of trades (max 1000)"}
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_funding_rate_history",
                    description="Get funding rate history for a symbol",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "start_time": {"type": "integer", "description": "Start timestamp in ms"},
                            "end_time": {"type": "integer", "description": "End timestamp in ms"},
                            "limit": {"type": "integer", "description": "Number of entries (max 1000)"}
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_taker_buy_sell_volume",
                    description="Get taker buy/sell volume ratio statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "period": {"type": "string", "description": "Period for the data (5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d)"},
                            "start_time": {"type": "integer", "description": "Start timestamp in ms"},
                            "end_time": {"type": "integer", "description": "End timestamp in ms"},
                            "limit": {"type": "integer", "description": "Number of entries (max 500, default 30)"}
                        },
                        "required": ["symbol", "period"]
                    }
                ),

                # Trading History Tools
                Tool(
                    name="get_account_trades",
                    description="Get account trade list",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "start_time": {"type": "integer", "description": "Optional start time in ms"},
                            "end_time": {"type": "integer", "description": "Optional end time in ms"},
                            "from_id": {"type": "integer", "description": "Optional trade ID to fetch from"},
                            "limit": {"type": "integer", "description": "Maximum number of trades to return (default 500)"}
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_income_history",
                    description="Get income history",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Trading pair symbol"},
                            "income_type": {"type": "string", "description": "Optional income type filter"},
                            "start_time": {"type": "integer", "description": "Optional start time in ms"},
                            "end_time": {"type": "integer", "description": "Optional end time in ms"},
                            "limit": {"type": "integer", "description": "Maximum number of records to return (default 100)"}
                        },
                        "required": []
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""
            
            # Check if API credentials are configured for authenticated endpoints
            unauthenticated_tools = [
                "get_exchange_info", "get_price_ticker", "get_24hr_ticker", "get_book_ticker", 
                "get_order_book", "get_klines", "get_mark_price", 
                "get_aggregate_trades", "get_funding_rate_history", "get_taker_buy_sell_volume"
            ]
            
            if not self.config.api_key or not self.config.secret_key:
                if name not in unauthenticated_tools:
                    return [TextContent(
                        type="text",
                        text="Error: API credentials not configured. Please provide valid API key and secret key."
                    )]
            
            try:
                async with BinanceClient(self.config) as client:
                    
                    # Account Information Tools
                    if name == "get_account_info":
                        result = await client._make_request("GET", "/fapi/v2/account", security_type="USER_DATA")
                    elif name == "get_balance":
                        result = await client._make_request("GET", "/fapi/v2/balance", security_type="USER_DATA")
                    elif name == "get_position_info":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v2/positionRisk", params, "USER_DATA")
                    elif name == "get_position_mode":
                        result = await client._make_request("GET", "/fapi/v1/positionSide/dual", security_type="USER_DATA")
                    elif name == "get_commission_rate":
                        params = {"symbol": arguments["symbol"]}
                        result = await client._make_request("GET", "/fapi/v1/commissionRate", params, "USER_DATA")
                    
                    # Risk Management Tools
                    elif name == "get_adl_quantile":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/adlQuantile", params, "USER_DATA")
                    elif name == "get_leverage_brackets":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/leverageBracket", params, "USER_DATA")
                    elif name == "get_force_orders":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/forceOrders", params, "USER_DATA")
                    elif name == "get_position_margin_history":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/positionMargin/history", params, "USER_DATA")
                    
                    # Order Management Tools
                    elif name == "place_order":
                        params = {k: v for k, v in arguments.items() if v is not None and k not in ["quantity_precision", "price_precision"]}
                        # Convert order_type to type for API
                        if "order_type" in params:
                            params["type"] = params.pop("order_type")
                        result = await client._make_request("POST", "/fapi/v1/order", params, "TRADE")
                    elif name == "place_multiple_orders":
                        # This requires special handling for batch orders
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("POST", "/fapi/v1/batchOrders", params, "TRADE")
                    elif name == "cancel_order":
                        params = {"symbol": arguments["symbol"], "orderId": arguments["order_id"]}
                        result = await client._make_request("DELETE", "/fapi/v1/order", params, "TRADE")
                    elif name == "cancel_multiple_orders":
                        params = {
                            "symbol": arguments["symbol"],
                            "orderIdList": arguments["order_id_list"]
                        }
                        result = await client._make_request("DELETE", "/fapi/v1/batchOrders", params, "TRADE")
                    elif name == "cancel_all_orders":
                        params = {"symbol": arguments["symbol"]}
                        result = await client._make_request("DELETE", "/fapi/v1/allOpenOrders", params, "TRADE")
                    elif name == "auto_cancel_all_orders":
                        params = {
                            "symbol": arguments["symbol"],
                            "countdownTime": arguments["countdown_time"]
                        }
                        result = await client._make_request("POST", "/fapi/v1/countdownCancelAll", params, "TRADE")
                    
                    # Order Query Tools
                    elif name == "get_open_order":
                        params = {"symbol": arguments["symbol"], "orderId": arguments["order_id"]}
                        result = await client._make_request("GET", "/fapi/v1/openOrder", params, "USER_DATA")
                    elif name == "get_open_orders":
                        params = {"symbol": arguments["symbol"]}
                        result = await client._make_request("GET", "/fapi/v1/openOrders", params, "USER_DATA")
                    elif name == "get_all_orders":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/allOrders", params, "USER_DATA")
                    elif name == "query_order":
                        params = {"symbol": arguments["symbol"], "orderId": arguments["order_id"]}
                        result = await client._make_request("GET", "/fapi/v1/order", params, "USER_DATA")
                    
                    # Trading Configuration Tools
                    elif name == "change_leverage":
                        params = {
                            "symbol": arguments["symbol"],
                            "leverage": arguments["leverage"]
                        }
                        result = await client._make_request("POST", "/fapi/v1/leverage", params, "TRADE")
                    elif name == "change_margin_type":
                        params = {
                            "symbol": arguments["symbol"],
                            "marginType": arguments["margin_type"]
                        }
                        result = await client._make_request("POST", "/fapi/v1/marginType", params, "TRADE")
                    elif name == "change_position_mode":
                        params = {"dualSidePosition": arguments["dual_side"]}
                        result = await client._make_request("POST", "/fapi/v1/positionSide/dual", params, "TRADE")
                    elif name == "modify_position_margin":
                        params = {
                            "symbol": arguments["symbol"],
                            "positionSide": arguments["position_side"],
                            "amount": arguments["amount"],
                            "type": arguments["margin_type"]
                        }
                        result = await client._make_request("POST", "/fapi/v1/positionMargin", params, "TRADE")
                    
                    # Market Data Tools
                    elif name == "get_exchange_info":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/exchangeInfo", params)
                    elif name == "get_book_ticker":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/ticker/bookTicker", params)
                    elif name == "get_price_ticker":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/ticker/price", params)
                    elif name == "get_24hr_ticker":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/ticker/24hr", params)
                    elif name == "get_order_book":
                        params = {
                            "symbol": arguments["symbol"],
                            "limit": arguments["limit"]
                        }
                        result = await client._make_request("GET", "/fapi/v1/depth", params)
                    elif name == "get_klines":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/klines", params)
                    elif name == "get_mark_price":
                        params = {}
                        if "symbol" in arguments:
                            params["symbol"] = arguments["symbol"]
                        result = await client._make_request("GET", "/fapi/v1/premiumIndex", params)
                    elif name == "get_aggregate_trades":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/aggTrades", params)
                    elif name == "get_funding_rate_history":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/fundingRate", params)
                    elif name == "get_taker_buy_sell_volume":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/futures/data/takerlongshortRatio", params)
                    
                    # Trading History Tools
                    elif name == "get_account_trades":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/userTrades", params, "USER_DATA")
                    elif name == "get_income_history":
                        params = {k: v for k, v in arguments.items() if v is not None}
                        result = await client._make_request("GET", "/fapi/v1/income", params, "USER_DATA")
                    
                    else:
                        raise ValueError(f"Unknown tool: {name}")
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                    
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]


async def main():
    import argparse
    import os
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Binance Futures MCP Server")
    parser.add_argument("--binance-api-key", 
                       help="Binance API key", 
                       default=os.getenv("BINANCE_API_KEY", ""))
    parser.add_argument("--binance-secret-key", 
                       help="Binance secret key", 
                       default=os.getenv("BINANCE_SECRET_KEY", ""))
    
    args = parser.parse_args()
    
    # Initialize server with credentials
    server_instance = BinanceMCPServer(args.binance_api_key, args.binance_secret_key)
    
    # Run server using stdio
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream, 
            write_stream, 
            InitializationOptions(
                server_name="binance-futures-mcp-server",
                server_version="1.0.6",
                capabilities={
                    "tools": {}
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
