# Publishing to PyPI Guide

## Prerequisites

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Create an account and verify your email

2. **Create API Token**
   - Go to https://pypi.org/manage/account/
   - Scroll to "API tokens" section
   - Click "Add API token"
   - Give it a name (e.g., "binance-mcp-server")
   - Copy the token (starts with `pypi-`)

## Step 1: Install Build Tools

```bash
pip install build twine
```

## Step 2: Build the Package

```bash
cd binance-mcp-server
python -m build
```

This creates:
- `dist/binance_futures_mcp-1.0.0-py3-none-any.whl`
- `dist/binance-futures-mcp-1.0.0.tar.gz`

## Step 3: Check the Package

```bash
twine check dist/*
```

## Step 4: Upload to PyPI

### Option A: Using API Token (Recommended)
```bash
twine upload dist/* -u __token__ -p pypi-YOUR_API_TOKEN_HERE
```

### Option B: Using Username/Password
```bash
twine upload dist/*
# Enter username and password when prompted
```

## Step 5: Verify Upload

- Go to https://pypi.org/project/binance-futures-mcp/
- Check that your package appears correctly

## Step 6: Test Installation

```bash
pip install binance-futures-mcp
binance-mcp-server --help
```

## Publishing Updates

To publish a new version:

1. Update version in `pyproject.toml`
2. Clean old builds: `rm -rf dist/`
3. Build: `python -m build`
4. Upload: `twine upload dist/*`

## Troubleshooting

### Common Issues:
- **Package name already exists**: Choose a different name in `pyproject.toml`
- **Version already exists**: Increment version number
- **Authentication failed**: Check API token or credentials
- **File already exists**: You can't re-upload the same version

### Testing with TestPyPI First:
```bash
# Upload to test repository first
twine upload --repository testpypi dist/*

# Install from test repository
pip install --index-url https://test.pypi.org/simple/ binance-futures-mcp
```

## Security Notes

- Keep your API token secure
- Don't commit tokens to version control
- Consider using environment variables:
  ```bash
  export TWINE_PASSWORD=pypi-YOUR_API_TOKEN_HERE
  twine upload dist/* -u __token__
  ```
