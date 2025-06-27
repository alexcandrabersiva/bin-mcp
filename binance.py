#!/usr/bin/env python3
"""
Binance MCP Server Entry Point

This script serves as the main entry point for the Binance MCP server.
It can be called with command-line arguments to pass API credentials.

Usage:
    python binance.py --binance-api-key YOUR_API_KEY --binance-secret-key YOUR_SECRET_KEY
"""

import sys
import os
import asyncio

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from binance_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())
