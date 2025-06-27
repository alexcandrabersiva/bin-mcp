#!/usr/bin/env python3

import asyncio
from binance_mcp.server import main


def cli_main():
    """Entry point for the command-line interface"""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
