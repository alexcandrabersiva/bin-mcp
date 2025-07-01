#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="binance_futures_mcp",
    version="1.2.1",
    author="Binance MCP Server",
    description="A Model Context Protocol server for Binance Futures API with comprehensive trading tools including TP/SL management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexcandrabersiva/bin-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/alexcandrabersiva/bin-mcp/issues",
        "Repository": "https://github.com/alexcandrabersiva/bin-mcp.git",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "mcp>=1.0.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "binance-mcp-server=binance_mcp.__main__:cli_main",
        ],
    },
    keywords="mcp binance trading futures api model-context-protocol",
)
