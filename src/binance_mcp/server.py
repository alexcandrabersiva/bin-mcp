#!/usr/bin/env python3
"""
Binance Futures MCP Server - Modular Implementation
"""

import argparse
import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from .cache import TickerCache
from .client import BinanceClient
from .config import BinanceConfig
from .handlers import ToolHandler
from .tools import get_all_tools


class BinanceMCPServer:
    """Binance MCP Server implementation"""
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.server = Server("binance-futures-mcp-server")
        self.config = BinanceConfig(api_key, secret_key)
        self.ticker_cache = TickerCache(cache_duration_minutes=5)  # Cache for 5 minutes
        self.handler = ToolHandler(self.config, self.ticker_cache)
        self._background_task = None  # Will be started when server runs
        self._setup_tools()
    
    async def _background_ticker_refresh(self):
        """Background task to refresh ticker data every 5 minutes"""
        print("[INFO] Starting background ticker refresh task...")
        while True:
            try:
                await asyncio.sleep(300)  # Wait 5 minutes
                await self._refresh_ticker_cache()
            except Exception as e:
                print(f"Error refreshing ticker cache: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    def _start_background_task_if_needed(self):
        """Start background task if not already running"""
        if self._background_task is None or self._background_task.done():
            try:
                self._background_task = asyncio.create_task(self._background_ticker_refresh())
                print("[OK] Background ticker refresh task started")
            except RuntimeError:
                # Event loop not running yet, task will be started on first cache access
                print("[WAIT] Event loop not ready, background task will start on first cache access")
    
    async def _ensure_cache_fresh(self):
        """Ensure cache is fresh, refresh if needed, and start background task"""
        # Start background task if needed
        self._start_background_task_if_needed()
        
        # If cache is expired, refresh it immediately
        if self.ticker_cache.is_expired():
            print("[INFO] Cache expired, refreshing immediately...")
            await self._refresh_ticker_cache()
    
    async def _refresh_ticker_cache(self):
        """Refresh the ticker cache with latest data, filtering out delisted tokens"""
        try:
            async with BinanceClient(self.config) as client:
                # Step 1: Update exchange info if expired (every 30 minutes)
                if self.ticker_cache.is_exchange_info_expired():
                    print("[INFO] Refreshing exchange info to filter delisted tokens...")
                    exchange_info = await client._make_request("GET", "/fapi/v1/exchangeInfo")
                    self.ticker_cache.update_active_symbols(exchange_info)
                
                # Step 2: Fetch all 24hr ticker data
                print("[INFO] Fetching 24hr ticker data...")
                result = await client._make_request("GET", "/fapi/v1/ticker/24hr")
                
                # Step 3: Update cache with filtering
                self.ticker_cache.update_cache(result)
                
                active_count = len([item for item in self.ticker_cache.data 
                                  if item.get('symbol') in self.ticker_cache.active_symbols])
                total_count = len(result)
                
                print(f"[OK] Ticker cache refreshed: {active_count}/{total_count} active symbols at {datetime.now()}")
                
        except Exception as e:
            print(f"[ERROR] Failed to refresh ticker cache: {e}")
            # Don't clear existing cache on failure
    
    def _setup_tools(self):
        """Setup all MCP tools"""
        
        @self.server.list_tools()
        async def handle_list_tools():
            """Handle tools/list requests"""
            return get_all_tools()
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""
            
            # Check if API credentials are configured for authenticated endpoints
            unauthenticated_tools = [
                "get_exchange_info", "get_price_ticker", "get_24hr_ticker", "get_book_ticker", 
                "get_order_book", "get_klines", "get_mark_price", 
                "get_aggregate_trades", "get_funding_rate_history", "get_taker_buy_sell_volume",
                "get_top_gainers_losers", "get_market_overview"
            ]
            
            if not self.config.api_key or not self.config.secret_key:
                if name not in unauthenticated_tools:
                    return [TextContent(
                        type="text",
                        text="Error: API credentials not configured. Please provide valid API key and secret key."
                    )]
            
            try:
                # Ensure cache is fresh for market data tools
                if name in ["get_top_gainers_losers", "get_market_overview", "get_24hr_ticker"]:
                    await self._ensure_cache_fresh()
                
                # Delegate to handler
                result = await self.handler.handle_tool_call(name, arguments)
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                error_msg = f"Error executing {name}: {str(e)}"
                print(f"[ERROR] {error_msg}")
                return [TextContent(
                    type="text",
                    text=error_msg
                )]


async def main():
    """Main entry point for the server"""
    
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
                server_version="1.1.3",
                capabilities={
                    "tools": {}
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
