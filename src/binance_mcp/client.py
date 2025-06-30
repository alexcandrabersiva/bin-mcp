#!/usr/bin/env python3
"""
Binance API Client for MCP Server
"""

import asyncio
import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import aiohttp

from .config import BinanceConfig


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
                'User-Agent': 'binance-mcp-server/1.0.9',
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
            elif method == "PUT":
                async with self.session.put(url, data=params, headers=headers, ssl=False) as response:
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
