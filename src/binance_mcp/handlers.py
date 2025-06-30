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
            
            # Risk Management Tools
            elif name == "get_adl_quantile":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/adlQuantile", params, "USER_DATA")
            elif name == "get_leverage_brackets":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/leverageBracket", params, "USER_DATA")
            elif name == "get_force_orders":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/forceOrders", params, "USER_DATA")
            elif name == "get_position_margin_history":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/positionMargin/history", params, "USER_DATA")
            
            # Order Management Tools
            elif name == "place_order":
                return await self._handle_place_order(client, arguments)
            elif name == "place_bracket_order":
                return await self._handle_place_bracket_order(client, arguments)
            elif name == "place_multiple_orders":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("POST", "/fapi/v1/batchOrders", params, "TRADE")
            elif name == "cancel_order":
                params = {"symbol": arguments["symbol"], "orderId": arguments["order_id"]}
                return await client._make_request("DELETE", "/fapi/v1/order", params, "TRADE")
            elif name == "cancel_multiple_orders":
                params = {
                    "symbol": arguments["symbol"],
                    "orderIdList": arguments["order_id_list"]
                }
                return await client._make_request("DELETE", "/fapi/v1/batchOrders", params, "TRADE")
            elif name == "cancel_all_orders":
                params = {"symbol": arguments["symbol"]}
                return await client._make_request("DELETE", "/fapi/v1/allOpenOrders", params, "TRADE")
            elif name == "auto_cancel_all_orders":
                params = {
                    "symbol": arguments["symbol"],
                    "countdownTime": arguments["countdown_time"]
                }
                return await client._make_request("POST", "/fapi/v1/countdownCancelAll", params, "TRADE")
            
            # Order Query Tools
            elif name == "get_open_order":
                params = {"symbol": arguments["symbol"], "orderId": arguments["order_id"]}
                return await client._make_request("GET", "/fapi/v1/openOrder", params, "USER_DATA")
            elif name == "get_open_orders":
                params = {"symbol": arguments["symbol"]}
                return await client._make_request("GET", "/fapi/v1/openOrders", params, "USER_DATA")
            elif name == "get_all_orders":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/allOrders", params, "USER_DATA")
            elif name == "query_order":
                params = {"symbol": arguments["symbol"], "orderId": arguments["order_id"]}
                return await client._make_request("GET", "/fapi/v1/order", params, "USER_DATA")
            
            # Position Management Tools
            elif name == "close_position":
                return await self._handle_close_position(client, arguments)
            elif name == "modify_order":
                return await self._handle_modify_order(client, arguments)
            elif name == "add_tp_sl_to_position":
                return await self._handle_add_tp_sl(client, arguments)
            
            # Trading Configuration Tools
            elif name == "change_leverage":
                params = {"symbol": arguments["symbol"], "leverage": arguments["leverage"]}
                return await client._make_request("POST", "/fapi/v1/leverage", params, "TRADE")
            elif name == "change_margin_type":
                params = {"symbol": arguments["symbol"], "marginType": arguments["margin_type"]}
                return await client._make_request("POST", "/fapi/v1/marginType", params, "TRADE")
            elif name == "change_position_mode":
                params = {"dualSidePosition": arguments["dual_side"]}
                return await client._make_request("POST", "/fapi/v1/positionSide/dual", params, "TRADE")
            elif name == "modify_position_margin":
                params = {
                    "symbol": arguments["symbol"],
                    "amount": arguments["amount"],
                    "positionSide": arguments["position_side"],
                    "type": arguments["margin_type"]
                }
                return await client._make_request("POST", "/fapi/v1/positionMargin", params, "TRADE")
            
            # Market Data Tools
            elif name == "get_exchange_info":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/exchangeInfo", params)
            elif name == "get_book_ticker":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/ticker/bookTicker", params)
            elif name == "get_price_ticker":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/ticker/price", params)
            elif name == "get_24hr_ticker":
                if "symbol" in arguments:
                    # Single symbol from cache
                    symbol_data = self.ticker_cache.get_symbol_data(arguments["symbol"])
                    if symbol_data:
                        return symbol_data
                    else:
                        # Fallback to API if not in cache
                        params = {"symbol": arguments["symbol"]}
                        return await client._make_request("GET", "/fapi/v1/ticker/24hr", params)
                else:
                    # All symbols from cache
                    return self.ticker_cache.data
            elif name == "get_top_gainers_losers":
                return self._handle_top_gainers_losers(arguments)
            elif name == "get_market_overview":
                return self._handle_market_overview(arguments)
            elif name == "get_order_book":
                params = {
                    "symbol": arguments["symbol"],
                    "limit": arguments["limit"]
                }
                return await client._make_request("GET", "/fapi/v1/depth", params)
            elif name == "get_klines":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/klines", params)
            elif name == "get_mark_price":
                params = {}
                if "symbol" in arguments:
                    params["symbol"] = arguments["symbol"]
                return await client._make_request("GET", "/fapi/v1/premiumIndex", params)
            elif name == "get_aggregate_trades":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/aggTrades", params)
            elif name == "get_funding_rate_history":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/fundingRate", params)
            elif name == "get_taker_buy_sell_volume":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/futures/data/takerlongshortRatio", params)
            
            # Trading History Tools
            elif name == "get_account_trades":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/userTrades", params, "USER_DATA")
            elif name == "get_income_history":
                params = {k: v for k, v in arguments.items() if v is not None}
                return await client._make_request("GET", "/fapi/v1/income", params, "USER_DATA")
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _handle_place_order(self, client: BinanceClient, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle place_order tool - Places a single order only
        
        For bracket orders with TP/SL, use place_bracket_order tool instead.
        """
        leverage = arguments.pop("leverage", None)
        
        # Filter out precision parameters and pass through all other parameters directly
        params = {k: v for k, v in arguments.items() if v is not None and k not in ["quantity_precision", "price_precision"]}
        
        # Handle backward compatibility for order_type parameter
        if "order_type" in params:
            params["type"] = params.pop("order_type")
        
        # Check if type parameter is present
        if "type" not in params:
            raise ValueError("Missing required parameter 'type'. Please specify the order type (e.g., 'MARKET', 'LIMIT', 'STOP', etc.)")
        
        # Validate mandatory parameters based on order type
        order_type = params.get("type")
        if order_type == "LIMIT":
            required_params = ["timeInForce", "quantity", "price"]
            missing = [p for p in required_params if p not in params]
            if missing:
                raise ValueError(f"LIMIT order missing required parameters: {missing}")
        elif order_type == "MARKET":
            if "quantity" not in params:
                raise ValueError("MARKET order missing required parameter: quantity")
        elif order_type in ["STOP", "TAKE_PROFIT"]:
            required_params = ["quantity", "price", "stopPrice"]
            missing = [p for p in required_params if p not in params]
            if missing:
                raise ValueError(f"{order_type} order missing required parameters: {missing}")
        elif order_type in ["STOP_MARKET", "TAKE_PROFIT_MARKET"]:
            if "stopPrice" not in params:
                raise ValueError(f"{order_type} order missing required parameter: stopPrice")
        elif order_type == "TRAILING_STOP_MARKET":
            if "callbackRate" not in params:
                raise ValueError("TRAILING_STOP_MARKET order missing required parameter: callbackRate")
        
        # Set leverage if provided
        if leverage:
            try:
                await client._make_request(
                    "POST", 
                    "/fapi/v1/leverage", 
                    {"symbol": params["symbol"], "leverage": leverage},
                    "USER_DATA"
                )
            except Exception as e:
                print(f"Warning: Failed to set leverage: {e}")
        
        # Place the single order
        return await client._make_request("POST", "/fapi/v1/order", params, "TRADE")
        
        # For bracket orders, we need to place the entry order first, then TP and SL
        result = {
            "order": {
                "symbol": params["symbol"],
                "side": params["side"],
                "type": params["type"],
                "orders": {}
            }
        }
        
        try:
            # 1. Place entry order
            entry_order = await client._make_request("POST", "/fapi/v1/order", params, "TRADE")
            result["order"]["orders"]["entry"] = entry_order
            
            # Determine opposite side for TP and SL orders
            side = params["side"]
            opposite_side = "SELL" if side == "BUY" else "BUY"
            position_side = params.get("positionSide", "BOTH")
            symbol = params["symbol"]
            quantity = params["quantity"]
            time_in_force = params.get("timeInForce", "GTC")
            
            # 2. Place take-profit order if specified
            if take_profit_price:
                tp_order_type = "TAKE_PROFIT" if tp_type == "LIMIT" else "TAKE_PROFIT_MARKET"
                tp_params = {
                    "symbol": symbol,
                    "side": opposite_side,
                    "positionSide": position_side,
                    "quantity": quantity,
                    "type": tp_order_type,
                    "stopPrice": take_profit_price,
                    "reduceOnly": "true" # Ensure it only reduces the position
                }
                
                # Add price and timeInForce only for LIMIT take-profit orders
                if tp_type == "LIMIT":
                    tp_params["price"] = take_profit_price
                    tp_params["timeInForce"] = time_in_force
                
                tp_order = await client._make_request(
                    "POST", 
                    "/fapi/v1/order", 
                    tp_params,
                    "TRADE"
                )
                
                result["order"]["orders"]["take_profit"] = tp_order
            
            # 3. Place stop-loss order if specified
            if stop_loss_price:
                sl_order_type = "STOP" if sl_type == "LIMIT" else "STOP_MARKET"
                sl_params = {
                    "symbol": symbol,
                    "side": opposite_side,
                    "positionSide": position_side,
                    "quantity": quantity,
                    "type": sl_order_type,
                    "stopPrice": stop_loss_price,
                    "reduceOnly": "true" # Ensure it only reduces the position
                }
                
                # Add price and timeInForce only for LIMIT stop-loss orders
                if sl_type == "LIMIT":
                    sl_params["price"] = stop_loss_price
                    sl_params["timeInForce"] = time_in_force
                
                sl_order = await client._make_request(
                    "POST", 
                    "/fapi/v1/order", 
                    sl_params,
                    "TRADE"
                )
                
                result["order"]["orders"]["stop_loss"] = sl_order
            
            return result
            
        except Exception as e:
            # If any order fails, attempt to cancel any successful orders
            if "orders" in result["order"]:
                for order_type, order in result["order"]["orders"].items():
                    if "orderId" in order:
                        try:
                            await client._make_request(
                                "DELETE", 
                                "/fapi/v1/order", 
                                {"symbol": symbol, "orderId": order["orderId"]},
                                "TRADE"
                            )
                        except Exception as cancel_error:
                            print(f"Failed to cancel {order_type} order: {cancel_error}")
            
            # Re-raise the original exception
            raise ValueError(f"Failed to place order: {str(e)}")
        raise ValueError(f"Failed to place order: {str(e)}")
    
    async def _handle_close_position(self, client: BinanceClient, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle close_position tool"""
        symbol = arguments["symbol"]
        position_side = arguments.get("position_side", "BOTH")
        quantity = arguments.get("quantity")
        close_all = arguments.get("close_all", False)
        
        # First, get current position to determine the side and quantity to close
        position_params = {"symbol": symbol}
        positions = await client._make_request("GET", "/fapi/v2/positionRisk", position_params, "USER_DATA")
        
        # Find the position to close
        position_to_close = None
        for pos in positions:
            if pos["symbol"] == symbol and float(pos["positionAmt"]) != 0:
                if position_side == "BOTH" or pos["positionSide"] == position_side:
                    position_to_close = pos
                    break
        
        if not position_to_close:
            raise ValueError(f"No open position found for {symbol} with position side {position_side}")
        
        position_amt = float(position_to_close["positionAmt"])
        current_position_side = position_to_close["positionSide"]
        
        # Determine order side (opposite of position)
        if position_amt > 0:  # Long position
            order_side = "SELL"
        else:  # Short position
            order_side = "BUY"
            position_amt = abs(position_amt)  # Make positive for order quantity
        
        # Determine quantity to close
        if close_all:
            # Use closePosition parameter to close entire position
            order_params = {
                "symbol": symbol,
                "side": order_side,
                "type": "MARKET",
                "closePosition": "true"
            }
            if current_position_side != "BOTH":
                order_params["positionSide"] = current_position_side
        else:
            # Close specific quantity or entire position
            close_quantity = quantity if quantity else position_amt
            order_params = {
                "symbol": symbol,
                "side": order_side,
                "type": "MARKET",
                "quantity": close_quantity
            }
            if current_position_side != "BOTH":
                order_params["positionSide"] = current_position_side
        
        return await client._make_request("POST", "/fapi/v1/order", order_params, "TRADE")
    
    async def _handle_modify_order(self, client: BinanceClient, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle modify_order tool"""
        params = {
            "symbol": arguments["symbol"],
            "orderId": arguments["order_id"],
            "side": arguments["side"],
            "quantity": arguments["quantity"],
            "price": arguments["price"]
        }
        if "priceMatch" in arguments:
            params["priceMatch"] = arguments["priceMatch"]
        return await client._make_request("PUT", "/fapi/v1/order", params, "TRADE")
    
    async def _handle_add_tp_sl(self, client: BinanceClient, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle add_tp_sl_to_position tool"""
        symbol = arguments["symbol"]
        position_side = arguments.get("position_side", "BOTH")
        take_profit_price = arguments.get("take_profit_price")
        stop_loss_price = arguments.get("stop_loss_price")
        quantity = arguments.get("quantity")
        tp_order_type = arguments.get("tp_order_type", "TAKE_PROFIT_MARKET")
        sl_order_type = arguments.get("sl_order_type", "STOP_MARKET")
        time_in_force = arguments.get("time_in_force", "GTC")
        
        if not take_profit_price and not stop_loss_price:
            raise ValueError("At least one of take_profit_price or stop_loss_price must be provided")
        
        # Get current position to determine side and quantity
        position_params = {"symbol": symbol}
        positions = await client._make_request("GET", "/fapi/v2/positionRisk", position_params, "USER_DATA")
        
        # Find the position
        position = None
        for pos in positions:
            if pos["symbol"] == symbol and float(pos["positionAmt"]) != 0:
                if position_side == "BOTH" or pos["positionSide"] == position_side:
                    position = pos
                    break
        
        if not position:
            raise ValueError(f"No open position found for {symbol}")
        
        position_amt = float(position["positionAmt"])
        current_position_side = position["positionSide"]
        
        # Determine order side (opposite of position)
        order_side = "SELL" if position_amt > 0 else "BUY"
        order_quantity = quantity if quantity else abs(position_amt)
        
        result = {"symbol": symbol, "orders": {}}
        
        # Place take profit order if specified
        if take_profit_price:
            tp_params = {
                "symbol": symbol,
                "side": order_side,
                "type": tp_order_type,
                "quantity": order_quantity,
                "reduceOnly": "true"
            }
            
            if tp_order_type == "LIMIT":
                tp_params["price"] = take_profit_price
                tp_params["timeInForce"] = time_in_force
            elif tp_order_type == "TAKE_PROFIT_MARKET":
                tp_params["stopPrice"] = take_profit_price
            
            if current_position_side != "BOTH":
                tp_params["positionSide"] = current_position_side
            
            try:
                tp_order = await client._make_request("POST", "/fapi/v1/order", tp_params, "TRADE")
                result["orders"]["take_profit"] = tp_order
            except Exception as e:
                result["orders"]["take_profit"] = {"error": str(e)}
        
        # Place stop loss order if specified
        if stop_loss_price:
            sl_params = {
                "symbol": symbol,
                "side": order_side,
                "type": sl_order_type,
                "quantity": order_quantity,
                "reduceOnly": "true"
            }
            
            if sl_order_type == "LIMIT":
                sl_params["price"] = stop_loss_price
                sl_params["timeInForce"] = time_in_force
            elif sl_order_type == "STOP_MARKET":
                sl_params["stopPrice"] = stop_loss_price
            
            if current_position_side != "BOTH":
                sl_params["positionSide"] = current_position_side
            
            try:
                sl_order = await client._make_request("POST", "/fapi/v1/order", sl_params, "TRADE")
                result["orders"]["stop_loss"] = sl_order
            except Exception as e:
                result["orders"]["stop_loss"] = {"error": str(e)}
        
        return result

    async def _handle_place_bracket_order(self, client: BinanceClient, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle place_bracket_order tool - Uses batch orders for efficient TP/SL placement"""
        
        # Extract parameters
        symbol = arguments["symbol"]
        side = arguments["side"]
        quantity = arguments["quantity"]
        entry_order_type = arguments.get("entry_order_type", "MARKET")
        entry_price = arguments.get("entry_price")
        take_profit_price = arguments["take_profit_price"]
        stop_loss_price = arguments["stop_loss_price"]
        position_side = arguments.get("positionSide", "BOTH")
        time_in_force = arguments.get("timeInForce", "GTC")
        tp_order_type = arguments.get("tp_order_type", "TAKE_PROFIT_MARKET")
        sl_order_type = arguments.get("sl_order_type", "STOP_MARKET")
        leverage = arguments.get("leverage")
        
        # Set leverage if provided
        if leverage:
            try:
                await client._make_request(
                    "POST", 
                    "/fapi/v1/leverage", 
                    {"symbol": symbol, "leverage": leverage},
                    "USER_DATA"
                )
            except Exception as e:
                print(f"Warning: Failed to set leverage: {e}")
        
        # Determine opposite side for TP and SL orders
        opposite_side = "SELL" if side == "BUY" else "BUY"
        
        # Build entry order
        entry_order = {
            "symbol": symbol,
            "side": side,
            "type": entry_order_type,
            "quantity": str(quantity)
        }
        
        if position_side != "BOTH":
            entry_order["positionSide"] = position_side
            
        if entry_order_type == "LIMIT":
            if not entry_price:
                raise ValueError("entry_price is required for LIMIT entry orders")
            entry_order["price"] = str(entry_price)
            entry_order["timeInForce"] = time_in_force
        
        # Build take profit order
        tp_order = {
            "symbol": symbol,
            "side": opposite_side,
            "type": tp_order_type,
            "quantity": str(quantity),
            "reduceOnly": "true"
        }
        
        if position_side != "BOTH":
            tp_order["positionSide"] = position_side
            
        if tp_order_type == "TAKE_PROFIT":
            tp_order["price"] = str(take_profit_price)
            tp_order["stopPrice"] = str(take_profit_price)
            tp_order["timeInForce"] = time_in_force
        else:  # TAKE_PROFIT_MARKET
            tp_order["stopPrice"] = str(take_profit_price)
        
        # Build stop loss order
        sl_order = {
            "symbol": symbol,
            "side": opposite_side,
            "type": sl_order_type,
            "quantity": str(quantity),
            "reduceOnly": "true"
        }
        
        if position_side != "BOTH":
            sl_order["positionSide"] = position_side
            
        if sl_order_type == "STOP":
            sl_order["price"] = str(stop_loss_price)
            sl_order["stopPrice"] = str(stop_loss_price)
            sl_order["timeInForce"] = time_in_force
        else:  # STOP_MARKET
            sl_order["stopPrice"] = str(stop_loss_price)
        
        # Prepare batch order request
        batch_orders = [entry_order, tp_order, sl_order]
        
        batch_params = {
            "batchOrders": batch_orders
        }
        
        try:
            # Place all orders in a single batch request
            result = await client._make_request("POST", "/fapi/v1/batchOrders", batch_params, "TRADE")
            
            # Structure the response for better readability
            structured_result = {
                "bracket_order": {
                    "symbol": symbol,
                    "side": side,
                    "quantity": quantity,
                    "orders": {
                        "entry": result[0] if len(result) > 0 else None,
                        "take_profit": result[1] if len(result) > 1 else None,
                        "stop_loss": result[2] if len(result) > 2 else None
                    }
                }
            }
            
            return structured_result
            
        except Exception as e:
            raise ValueError(f"Failed to place bracket order: {str(e)}")
    
    def _handle_top_gainers_losers(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_top_gainers_losers tool"""
        request_type = arguments.get("type", "both").lower()
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
