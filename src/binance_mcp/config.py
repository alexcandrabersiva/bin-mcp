#!/usr/bin/env python3
"""
Binance MCP Server Configuration
"""

class BinanceConfig:
    """Configuration for Binance API"""
    BASE_URL = "https://fapi.binance.com"
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.api_key = api_key
        self.secret_key = secret_key
