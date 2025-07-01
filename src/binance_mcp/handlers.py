#!/usr/bin/env python3
"""
Tool Handlers for Binance MCP Server
"""

from typing import Any, Dict

from .client import BinanceClient
from .config import BinanceConfig


class ToolHandler:
    """Handles tool execution for the MCP server"""
    
    def __init__(self, config: BinanceConfig):
        self.config = config
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route tool calls to appropriate handlers"""
        
        async with BinanceClient(self.config) as client:
            
            # Account Information Tools
            if name == "get_account_info":
                return await client._make_request("GET", "/fapi/v2/account", security_type="USER_DATA")
            elif name == "get_balance":
                return await client._make_request("GET", "/fapi/v2/balance", security_type="USER_DATA")
            elif name == "get_position_info":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v2/positionRisk", params, "USER_DATA")
            elif name == "get_position_mode":
                return await client._make_request("GET", "/fapi/v1/positionSide/dual", security_type="USER_DATA")
            elif name == "get_commission_rate":
                params = {"symbol": arguments["symbol"]}
                return await client._make_request("GET", "/fapi/v1/commissionRate", params, "USER_DATA")
            
            # Market Data Tools
            elif name == "get_exchange_info":
                return await client._make_request("GET", "/fapi/v1/exchangeInfo")
            elif name == "get_ticker":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/ticker/24hr", params)
            elif name == "get_ticker_price":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/ticker/price", params)
            elif name == "get_book_ticker":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/ticker/bookTicker", params)
            elif name == "get_mark_price":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/premiumIndex", params)
            elif name == "get_funding_rate":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/fundingRate", params)
            elif name == "get_klines":
                params = {
                    "symbol": arguments["symbol"],
                    "interval": arguments["interval"]
                }
                if "start_time" in arguments:
                    params["startTime"] = arguments["start_time"]
                if "end_time" in arguments:
                    params["endTime"] = arguments["end_time"]
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                return await client._make_request("GET", "/fapi/v1/klines", params)
            elif name == "get_continuous_klines":
                params = {
                    "pair": arguments["pair"],
                    "contractType": arguments["contract_type"],
                    "interval": arguments["interval"]
                }
                if "start_time" in arguments:
                    params["startTime"] = arguments["start_time"]
                if "end_time" in arguments:
                    params["endTime"] = arguments["end_time"]
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                return await client._make_request("GET", "/fapi/v1/continuousKlines", params)
            elif name == "get_index_price_klines":
                params = {
                    "pair": arguments["pair"],
                    "interval": arguments["interval"]
                }
                if "start_time" in arguments:
                    params["startTime"] = arguments["start_time"]
                if "end_time" in arguments:
                    params["endTime"] = arguments["end_time"]
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                return await client._make_request("GET", "/fapi/v1/indexPriceKlines", params)
            elif name == "get_mark_price_klines":
                params = {
                    "symbol": arguments["symbol"],
                    "interval": arguments["interval"]
                }
                if "start_time" in arguments:
                    params["startTime"] = arguments["start_time"]
                if "end_time" in arguments:
                    params["endTime"] = arguments["end_time"]
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                return await client._make_request("GET", "/fapi/v1/markPriceKlines", params)
            elif name == "get_order_book":
                params = {"symbol": arguments["symbol"]}
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                return await client._make_request("GET", "/fapi/v1/depth", params)
            elif name == "get_trades":
                params = {"symbol": arguments["symbol"]}
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                return await client._make_request("GET", "/fapi/v1/trades", params)
            elif name == "get_historical_trades":
                params = {"symbol": arguments["symbol"]}
                if "limit" in arguments:
                    params["limit"] = arguments["limit"]
                if "from_id" in arguments:
                    params["fromId"] = arguments["from_id"]
                return await client._make_request("GET", "/fapi/v1/historicalTrades", params)
            elif name == "get_agg_trades":
                params = {"symbol": arguments["symbol"]}
                for k, v in arguments.items():
                    if k != "symbol" and v is not None:
                        params[k] = v
                return await client._make_request("GET", "/fapi/v1/aggTrades", params)

            
            else:
                # Process the request
                raise ValueError(f"Unknown tool: {name}")
