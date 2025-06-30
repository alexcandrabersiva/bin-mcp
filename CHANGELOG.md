# Changelog

## [1.1.4] - 2025-06-29

### Optimized - Enhanced Bracket Order Implementation
- **Optimized `place_bracket_order` tool** - Improved batch order efficiency
  - Now uses `/fapi/v1/batchOrders` endpoint for atomic order placement
  - Places entry, take-profit, and stop-loss orders in a single API call
  - Better error handling and order rollback on failure
  - Structured response with clear entry/TP/SL order details

- **Simplified `place_order` tool** - Streamlined for single orders
  - Removed bracket order logic from `place_order` (use `place_bracket_order` instead)
  - Clearer tool separation: single orders vs bracket orders
  - Enhanced parameter validation and error messages
  - Better backward compatibility with `order_type` parameter

### Technical Improvements
- Confirmed Binance API doesn't have built-in TP/SL parameters
- Verified `priceProtect` is a safety flag, not TP/SL functionality
- Code analysis shows 37 total tools, all properly implemented
- No deprecated or unused tool code found

## [1.0.9] - 2025-06-28

### Added - Advanced TP/SL and Order Management
- **New `modify_order` tool** - Modify existing orders
  - Change price, quantity, and other order parameters
  - Uses Binance `/fapi/v1/order` PUT endpoint
  - Supports `priceMatch` parameter for advanced order matching

- **New `add_tp_sl_to_position` tool** - Add TP/SL to existing positions
  - Automatically detects current position size and side
  - Supports both Take Profit and Stop Loss orders
  - Works with different order types (MARKET, LIMIT)
  - Handles both One-way and Hedge position modes

- **New `place_bracket_order` tool** - Place entry with automatic TP/SL
  - Places entry order + TP order + SL order in sequence
  - Supports both MARKET and LIMIT entry orders
  - Automatically sets up reduce-only TP/SL orders

### Improved
- Enhanced error handling with detailed Binance API messages
- Improved input validation for all order-related tools
- Better support for position modes (One-way and Hedge)
- Comprehensive parameter validation for new TP/SL tools

## [1.0.8] - 2025-06-28

### Added
- New `close_position` tool for easily closing current positions
  - Automatic position detection and order side determination
  - Support for both One-way mode and Hedge mode
  - Options to close entire position or specific quantity
  - Uses `closePosition=true` for full position closure or `reduceOnly=true` for partial closure

### Fixed
- Fixed order placement parameter naming issues
  - Updated tool schema to use exact Binance API parameter names (camelCase)
  - Fixed `order_type` → `type`, `time_in_force` → `timeInForce`, etc.
- Improved error handling to show actual Binance API error messages
- Added parameter validation for different order types
- Fixed missing imports in server.py

### Improved
- Better error messages for debugging order placement issues
- More comprehensive parameter validation
- Enhanced tool descriptions and examples

## [1.0.7] - Previous Version
- Basic order management and market data tools
- Account information and trading configuration tools
