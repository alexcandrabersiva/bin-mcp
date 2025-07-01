#!/usr/bin/env python3
"""
Tool Handlers for Binance MCP Server
"""

from typing import Any, Dict

from .cache import TickerCache
from .client import BinanceClient
from .config import BinanceConfig


class ToolHandler:
    """Handles tool execution for the MCP server"""
    
    def __init__(self, config: BinanceConfig, ticker_cache: TickerCache):
        self.config = config
        self.ticker_cache = ticker_cache
    
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
            elif name == "get_top_gainers_losers":
                return self._handle_top_gainers_losers(arguments)
            elif name == "get_market_overview":
                return self._handle_market_overview(arguments)
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    def _handle_top_gainers_losers(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_top_gainers_losers tool"""
        request_type = arguments.get("type", "both")  # gainers, losers, or both
        limit = min(arguments.get("limit", 10), 200)  # Max 200
        min_volume = arguments.get("min_volume", 0)
        
        result = {}
        
        if request_type in ["gainers", "both"]:
            gainers = self.ticker_cache.get_top_gainers(limit)
            if min_volume > 0:
                gainers = [g for g in gainers if float(g.get('volume', 0)) >= min_volume]
            
            # Create a more compact representation of gainers
            compact_gainers = []
            for g in gainers[:limit]:
                compact_gainers.append({
                    "symbol": g.get("symbol", ""),
                    "pct": float(g.get("priceChangePercent", 0)),
                    "price": g.get("lastPrice", ""),
                    "volume": g.get("volume", ""),
                    "priceChange": g.get("priceChange", "")
                })
            result["gainers"] = compact_gainers
        
        if request_type in ["losers", "both"]:
            losers = self.ticker_cache.get_top_losers(limit)
            if min_volume > 0:
                losers = [l for l in losers if float(l.get('volume', 0)) >= min_volume]
            
            # Create a more compact representation of losers
            compact_losers = []
            for l in losers[:limit]:
                compact_losers.append({
                    "symbol": l.get("symbol", ""),
                    "pct": float(l.get("priceChangePercent", 0)),
                    "price": l.get("lastPrice", ""),
                    "volume": l.get("volume", ""),
                    "priceChange": l.get("priceChange", "")
                })
            result["losers"] = compact_losers
        
        # Add metadata
        result["metadata"] = {
            "last_updated": self.ticker_cache.last_updated.isoformat() if self.ticker_cache.last_updated else None,
            "total_symbols": len(self.ticker_cache.data),
            "filter_applied": {"min_volume": min_volume} if min_volume > 0 else None
        }
        
        return result
    
    def _handle_market_overview(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_market_overview tool"""
        include_top_movers = arguments.get("include_top_movers", True)
        volume_threshold = arguments.get("volume_threshold", 0)
        
        # Filter data by volume threshold
        filtered_data = self.ticker_cache.data
        if volume_threshold > 0:
            filtered_data = [d for d in self.ticker_cache.data if float(d.get('volume', 0)) >= volume_threshold]
        
        # Calculate market statistics
        total_symbols = len(filtered_data)
        gainers_count = len([d for d in filtered_data if float(d.get('priceChangePercent', 0)) > 0])
        losers_count = len([d for d in filtered_data if float(d.get('priceChangePercent', 0)) < 0])
        unchanged_count = total_symbols - gainers_count - losers_count
        
        # Calculate total market volume
        total_volume = sum(float(d.get('volume', 0)) for d in filtered_data)
        
        result = {
            "market_summary": {
                "total_symbols": total_symbols,
                "gainers": gainers_count,
                "losers": losers_count,
                "unchanged": unchanged_count,
                "total_24h_volume": total_volume,
                "last_updated": self.ticker_cache.last_updated.isoformat() if self.ticker_cache.last_updated else None
            }
        }
        
        if include_top_movers:
            top_gainers = self.ticker_cache.get_top_gainers(5)
            top_losers = self.ticker_cache.get_top_losers(5)
            
            if volume_threshold > 0:
                top_gainers = [g for g in top_gainers if float(g.get('volume', 0)) >= volume_threshold][:5]
                top_losers = [l for l in top_losers if float(l.get('volume', 0)) >= volume_threshold][:5]
            
            result["top_movers"] = {
                "top_gainers": top_gainers,
                "top_losers": top_losers
            }
        
        return result
