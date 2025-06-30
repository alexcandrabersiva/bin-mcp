#!/usr/bin/env python3
"""
Ticker Cache Implementation for Binance MCP Server
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional


class TickerCache:
    """Cache for 24hr ticker data to avoid repeated API calls"""
    
    def __init__(self, cache_duration_minutes: int = 5):
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self.data: List[Dict] = []
        self.last_updated: Optional[datetime] = None
        self.sorted_gainers: List[Dict] = []
        self.sorted_losers: List[Dict] = []
        self.active_symbols: set = set()  # Cache of active symbol names
        self.exchange_info_updated: Optional[datetime] = None
        
    def is_expired(self) -> bool:
        """Check if cache is expired"""
        if self.last_updated is None:
            return True
        return datetime.now() - self.last_updated > self.cache_duration
    
    def is_exchange_info_expired(self) -> bool:
        """Check if exchange info cache is expired (refresh every 30 minutes)"""
        if self.exchange_info_updated is None:
            return True
        return datetime.now() - self.exchange_info_updated > timedelta(minutes=30)
    
    def update_active_symbols(self, exchange_info: Dict):
        """Update list of active symbols from exchangeInfo"""
        try:
            active_symbols = set()
            symbols_data = exchange_info.get('symbols', [])
            
            for symbol_info in symbols_data:
                symbol = symbol_info.get('symbol', '')
                status = symbol_info.get('status', '')
                
                # Only include symbols that are actively trading
                # Exclude: SETTLING (delisted), CLOSE, AUCTION_MATCH, etc.
                if status == 'TRADING':
                    active_symbols.add(symbol)
            
            self.active_symbols = active_symbols
            self.exchange_info_updated = datetime.now()
            
            print(f"[OK] Active symbols updated: {len(active_symbols)} trading symbols")
            
            # Log some examples of excluded symbols for debugging
            all_symbols = {s.get('symbol', '') for s in symbols_data}
            excluded_symbols = all_symbols - active_symbols
            if excluded_symbols:
                excluded_sample = list(excluded_symbols)[:5]
                print(f"   📋 Excluded symbols (sample): {excluded_sample}")
                
        except Exception as e:
            print(f"[ERROR] Failed to update active symbols: {e}")
            # Keep existing active_symbols if update fails
    
    def update_cache(self, data: List[Dict]):
        """Update cache with new data and sort by price change"""
        self.last_updated = datetime.now()
        
        # Filter out symbols with zero volume, invalid price change, or delisted status
        valid_data = []
        excluded_count = 0
        
        for item in data:
            try:
                symbol = item.get('symbol', '')
                price_change_percent = float(item.get('priceChangePercent', 0))
                volume = float(item.get('volume', 0))
                
                # Check if symbol is actively trading (not delisted/settling)
                is_active = len(self.active_symbols) == 0 or symbol in self.active_symbols
                
                if volume > 0 and is_active:  # Only include symbols with trading volume and active status
                    item['priceChangePercent'] = price_change_percent
                    valid_data.append(item)
                else:
                    excluded_count += 1
                    
            except (ValueError, TypeError):
                excluded_count += 1
                continue
        
        # Store only the filtered data
        self.data = valid_data
        
        # Sort by price change percentage
        self.sorted_gainers = sorted(valid_data, key=lambda x: x['priceChangePercent'], reverse=True)
        self.sorted_losers = sorted(valid_data, key=lambda x: x['priceChangePercent'])
        
        print(f"[INFO] Cache updated: {len(valid_data)} active symbols, {excluded_count} excluded (delisted/no volume)")
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict]:
        """Get top gainers"""
        return self.sorted_gainers[:limit]
    
    def get_top_losers(self, limit: int = 10) -> List[Dict]:
        """Get top losers"""
        return self.sorted_losers[:limit]
    
    def get_symbol_data(self, symbol: str) -> Optional[Dict]:
        """Get data for specific symbol from cache"""
        for item in self.data:
            if item.get('symbol') == symbol.upper():
                return item
        return None
