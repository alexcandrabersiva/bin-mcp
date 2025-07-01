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

from .client import BinanceClient
from .config import BinanceConfig
from .handlers import ToolHandler
from .tools import get_all_tools


class BinanceMCPServer:
    """Binance MCP Server implementation"""
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.server = Server("binance-futures-mcp-server")
        self.config = BinanceConfig(api_key, secret_key)
        self.handler = ToolHandler(self.config)
        self._setup_tools()
    

    
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
                "get_exchange_info", "get_price_ticker", "get_book_ticker", 
                "get_order_book", "get_klines", "get_mark_price"
            ]
            
            if not self.config.api_key or not self.config.secret_key:
                if name not in unauthenticated_tools:
                    return [TextContent(
                        type="text",
                        text="Error: API credentials not configured. Please provide valid API key and secret key."
                    )]
            
            try:
                # Process the request
                
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
                server_version="1.2.1",
                capabilities={
                    "tools": {}
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
