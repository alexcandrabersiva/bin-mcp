# Multi-stage build following MCP best practices
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install the package
RUN pip install --no-cache-dir .

# Final stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy installed package from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Use the CLI entry point defined in pyproject.toml
ENTRYPOINT ["binance-mcp-server"]
