#!/usr/bin/env python3
"""
MCP Tool Definitions for Binance Futures API
"""

from mcp.types import Tool


def get_account_tools():
    """Account information tools"""
    return [
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
    ]


def get_risk_management_tools():
    """Risk management tools"""
    return [
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
    ]


def get_order_management_tools():
    """Order management tools"""
    return [
        Tool(
            name="place_order",
            description="Place a single futures order of any type. For orders with take-profit and stop-loss, use 'place_bracket_order' tool instead for better efficiency.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "side": {"type": "string", "description": "Order side ('BUY' or 'SELL')"},
                    "type": {"type": "string", "description": "Order type ('MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET')"},
                    "order_type": {"type": "string", "description": "Alternative parameter name for 'type' (for backward compatibility)"},
                    "quantity": {"type": "number", "description": "Order quantity"},
                    "price": {"type": "number", "description": "Order price (for LIMIT orders)"},
                    "stopPrice": {"type": "number", "description": "Stop price (for STOP orders)"},
                    "timeInForce": {"type": "string", "description": "Time in force (GTC, IOC, FOK)"},
                    "positionSide": {"type": "string", "description": "Position side ('BOTH', 'LONG', 'SHORT')"},
                    "reduceOnly": {"type": "string", "description": "Reduce only flag ('true' or 'false')"},
                    "newClientOrderId": {"type": "string", "description": "Custom order ID"},
                    "closePosition": {"type": "string", "description": "Close position flag ('true' or 'false')"},
                    "activationPrice": {"type": "number", "description": "Activation price (for TRAILING_STOP_MARKET)"},
                    "callbackRate": {"type": "number", "description": "Callback rate (for TRAILING_STOP_MARKET)"},
                    "workingType": {"type": "string", "description": "Working type (MARK_PRICE, CONTRACT_PRICE)"},
                    "priceProtect": {"type": "string", "description": "Price protection flag ('TRUE' or 'FALSE')"},
                    "newOrderRespType": {"type": "string", "description": "Response type ('ACK', 'RESULT')"},
                    "recvWindow": {"type": "integer", "description": "Receive window"},
                    "timestamp": {"type": "integer", "description": "Timestamp"},
                    "quantity_precision": {"type": "integer", "description": "Quantity precision for validation"},
                    "price_precision": {"type": "integer", "description": "Price precision for validation"},
                    "leverage": {"type": "number", "description": "Optional leverage to set before placing order"}
                },
                "required": ["symbol", "side"],
                "anyOf": [
                    {"required": ["type"]},
                    {"required": ["order_type"]}
                ]
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
    ]


def get_order_query_tools():
    """Order query tools"""
    return [
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
    ]


def get_position_tools():
    """Position management tools"""
    return [
        Tool(
            name="close_position",
            description="Close current position for a symbol (market order to close all or part of position)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "position_side": {"type": "string", "description": "Position side to close ('BOTH', 'LONG', 'SHORT'). Default 'BOTH' for One-way mode"},
                    "quantity": {"type": "number", "description": "Quantity to close (optional, if not provided will close entire position)"},
                    "close_all": {"type": "boolean", "description": "If true, closes entire position using closePosition=true parameter"}
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="modify_order",
            description="Modify an existing order (price, quantity, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "order_id": {"type": "integer", "description": "Order ID to modify"},
                    "side": {"type": "string", "description": "Order side ('BUY' or 'SELL')"},
                    "quantity": {"type": "number", "description": "New order quantity"},
                    "price": {"type": "number", "description": "New order price"},
                    "priceMatch": {"type": "string", "description": "Price match mode (OPPONENT, OPPONENT_5, OPPONENT_10, OPPONENT_20, QUEUE, QUEUE_5, QUEUE_10, QUEUE_20)"}
                },
                "required": ["symbol", "order_id", "side", "quantity", "price"]
            }
        ),
        Tool(
            name="add_tp_sl_to_position",
            description="Add Take Profit and/or Stop Loss orders to existing position",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "position_side": {"type": "string", "description": "Position side ('BOTH', 'LONG', 'SHORT'). Default 'BOTH' for One-way mode"},
                    "take_profit_price": {"type": "number", "description": "Take profit price (optional)"},
                    "stop_loss_price": {"type": "number", "description": "Stop loss price (optional)"},
                    "quantity": {"type": "number", "description": "Quantity for TP/SL orders (optional, defaults to position size)"},
                    "tp_order_type": {"type": "string", "description": "Take profit order type ('LIMIT', 'TAKE_PROFIT_MARKET'). Default 'TAKE_PROFIT_MARKET'"},
                    "sl_order_type": {"type": "string", "description": "Stop loss order type ('STOP_MARKET', 'STOP'). Default 'STOP_MARKET'"},
                    "time_in_force": {"type": "string", "description": "Time in force for LIMIT TP orders (GTC, IOC, FOK). Default 'GTC'"}
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="place_bracket_order",
            description="Place a position with automatic Take Profit and Stop Loss orders using batch order execution (more efficient than separate API calls)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Trading pair symbol"},
                    "side": {"type": "string", "description": "Order side ('BUY' or 'SELL')"},
                    "quantity": {"type": "number", "description": "Order quantity"},
                    "entry_order_type": {"type": "string", "description": "Entry order type ('MARKET', 'LIMIT'). Default 'MARKET'"},
                    "entry_price": {"type": "number", "description": "Entry price (for LIMIT entry order, optional for MARKET)"},
                    "take_profit_price": {"type": "number", "description": "Take profit price"},
                    "stop_loss_price": {"type": "number", "description": "Stop loss price"},
                    "positionSide": {"type": "string", "description": "Position side ('BOTH', 'LONG', 'SHORT')"},
                    "timeInForce": {"type": "string", "description": "Time in force for LIMIT orders (GTC, IOC, FOK). Default 'GTC'"},
                    "tp_order_type": {"type": "string", "description": "Take profit order type ('TAKE_PROFIT', 'TAKE_PROFIT_MARKET'). Default 'TAKE_PROFIT_MARKET'"},
                    "sl_order_type": {"type": "string", "description": "Stop loss order type ('STOP', 'STOP_MARKET'). Default 'STOP_MARKET'"},
                    "leverage": {"type": "number", "description": "Optional leverage to set before placing orders"}
                },
                "required": ["symbol", "side", "quantity", "take_profit_price", "stop_loss_price"]
            }
        ),
    ]


def get_trading_config_tools():
    """Trading configuration tools"""
    return [
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
    ]


def get_market_data_tools():
    """Market data tools"""
    return [
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
            name="get_top_gainers_losers",
            description="Get top gainers and losers from cached 24hr ticker data (much faster than fetching individual symbols)",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "description": "Type to get: 'gainers', 'losers', or 'both' (default: 'both')"},
                    "limit": {"type": "integer", "description": "Number of top results to return (default: 10, max: 200)"},
                    "min_volume": {"type": "number", "description": "Minimum 24hr volume filter (optional)"}
                },
                "required": []
            }
        ),
        Tool(
            name="get_market_overview",
            description="Get overall market statistics and top movers from cached data",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_top_movers": {"type": "boolean", "description": "Include top 5 gainers and losers (default: true)"},
                    "volume_threshold": {"type": "number", "description": "Minimum volume for market overview calculations (optional)"}
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
    ]


def get_trading_history_tools():
    """Trading history tools"""
    return [
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


def get_all_tools():
    """Get all MCP tools"""
    tools = []
    tools.extend(get_account_tools())
    tools.extend(get_risk_management_tools())
    tools.extend(get_order_management_tools())
    tools.extend(get_order_query_tools())
    tools.extend(get_position_tools())
    tools.extend(get_trading_config_tools())
    tools.extend(get_market_data_tools())
    tools.extend(get_trading_history_tools())
    return tools
