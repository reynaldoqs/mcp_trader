# Trading MCP Server

A production-ready Model Context Protocol (MCP) server for cryptocurrency trading, built with Python, FastMCP, and CCXT. This server provides AI agents with secure, type-safe access to exchange operations including balance checking, order management, and market data retrieval.

## 🚀 Features

- **Type-Safe Architecture**: Full type hints with Pydantic validation
- **Exchange Integration**: CCXT-based client supporting multiple exchanges
- **MCP Protocol**: FastMCP implementation with tools, resources, and prompts
- **Modular Design**: Clean separation of concerns with services, core types, and configuration
- **Environment-Based Config**: Secure credential management with python-dotenv
- **Comprehensive Logging**: Structured logging with loguru
- **Error Handling**: Custom exception hierarchy for robust error management

## 📁 Project Structure

```
trading-mcp-py/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project metadata
├── .env.example              # Environment variables template
├── AGENTS.md                 # Agent architecture documentation
└── src/
    ├── __init__.py           # Package exports
    ├── config/               # Configuration management
    │   ├── settings.py       # Pydantic settings with env loading
    │   └── logging.py        # Logging configuration
    ├── core/                 # Core types and exceptions
    │   ├── types.py          # Trading types (Order, Position, etc.)
    │   └── exceptions.py     # Custom exception classes
    ├── services/             # Business logic layer
    │   ├── exchange_client.py    # CCXT exchange wrapper
    │   └── balance_service.py    # Balance operations
    ├── mcp/                  # MCP protocol implementation
    │   ├── server.py         # MCP server setup
    │   ├── tools.py          # MCP tools (trading operations)
    │   ├── resources.py      # MCP resources (data access)
    │   └── resources_helper.py   # Helper functions
    └── server/               # Legacy server code
        └── mcp_server.py
```

### Key Components

- **`config/`**: Environment-based configuration with Pydantic validation
- **`core/`**: Type definitions (OrderSide, OrderType, Position, etc.) and exceptions
- **`services/`**: Exchange client wrapper and business logic services
- **`mcp/`**: MCP protocol implementation (tools, resources, prompts)

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**

   ```bash
   cd trading-mcp-py
   ```

2. **Create and activate virtual environment**

   ```bash
   # Using uv (recommended)
   uv venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies**

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your exchange credentials:

   ```env
   EXCHANGE_API_KEY=your_api_key_here
   EXCHANGE_API_SECRET=your_api_secret_here
   ```

## 🚀 Running the Server

### Development Mode (Recommended)

Run the MCP server in development mode with hot-reload:

```bash
mcp dev main.py
```

### Production Mode

Run the server directly:

```bash
python main.py
```

Or using uv:

```bash
uv run python main.py
```

### Validation & Inspection

Inspect the MCP server configuration and validate setup:

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

### Claude Desktop Integration

To use this MCP server with Claude Desktop, add the following configuration to your Claude Desktop config file:

**Location:**

Create or edit the Claude Desktop configuration file at:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json

**Configuration:**

```json
{
  "mcpServers": {
    "Trading MCP": {
      "command": "/Users/Username/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/Username/Projects/MPCs/trading-mcp-py",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Note:** Update the paths in the configuration to match your local setup:

- Replace `/Users/rey/.local/bin/uv` with your uv installation path (find it with `which uv`)
- Replace `/Users/rey/Projects/MPCs/trading-mcp-py` with your project directory path

After adding the configuration, restart Claude Desktop for the changes to take effect.

## 🔧 Configuration

The project uses Pydantic for type-safe configuration management. All settings can be configured via environment variables:

### Exchange Settings

- `EXCHANGE_API_KEY`: Your exchange API key
- `EXCHANGE_API_SECRET`: Your exchange API secret
- `EXCHANGE_SANDBOX_MODE`: Enable sandbox/testnet mode (default: true)
- `EXCHANGE_RATE_LIMIT`: Enable rate limiting (default: true)
- `EXCHANGE_DEFAULT_TYPE`: Order type - 'spot', 'future', or 'margin' (default: future)

### MCP Settings

- `MCP_SERVER_NAME`: Server name (default: Trading MCP)

### Logging Settings

- `LOG_LEVEL`: Logging level (default: INFO)
- `LOG_FORMAT`: Log format string
- `LOG_FILE_PATH`: Path to log file
- `DEBUG`: Enable debug mode (default: false)
- `LOG_ROTATION`: Log rotation policy (default: 1 day)
- `LOG_RETENTION`: Log retention policy (default: 30 days)

### General Settings

- `ENVIRONMENT`: Runtime environment - 'development' or 'production' (default: production)

## 📚 MCP Tools & Resources

### Available Tools

- **`open_market_long(symbol, usdt_amount)`**: Open a long position at market price
- **`open_market_short(symbol, usdt_amount)`**: Open a short position at market price
- **`open_limit_long(symbol, usdt_amount, price)`**: Place a limit buy to open long
- **`open_limit_short(symbol, usdt_amount, price)`**: Place a limit sell to open short
- **`close_position(symbol)`**: Close all positions for a symbol
- **`get_balance()`**: Return formatted account balance

### Available Resources

- **`account://balance`**: Real-time account balance data

## ⚡ Quickstart: Common Actions

1. **Check your balance**

   - Resource: `account://balance`
   - Tool: `get_balance()`

2. **Open a position**

   - Long at market: `open_market_long(symbol="BTC/USDT" or "BTCUSDT", usdt_amount=50)`
   - Short at market: `open_market_short(symbol="BTC/USDT" or "BTCUSDT", usdt_amount=50)`
   - Long with limit: `open_limit_long(symbol, usdt_amount, price)`
   - Short with limit: `open_limit_short(symbol, usdt_amount, price)`

3. **Close a position**

   - `close_position(symbol)`

Notes:

- Symbols should match your exchange format (e.g., `BTCUSDT` on Binance). If unsure, use the exact symbol as returned by your exchange via CCXT.
- Ensure sufficient balance and correct permissions on your API key.

## 🏗️ Architecture

This project follows a modular, layered architecture:

1. **Configuration Layer** (`config/`): Environment-based settings with Pydantic
2. **Core Layer** (`core/`): Type definitions and exceptions
3. **Service Layer** (`services/`): Business logic and exchange integration
4. **Protocol Layer** (`mcp/`): MCP server implementation
5. **Application Layer** (`main.py`): Entry point and initialization

For detailed agent architecture patterns, see [AGENTS.md](./AGENTS.md).

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

Test environment loading:

```bash
python test_env_loading.py
```

## 📖 Documentation

- **[AGENTS.md](./AGENTS.md)**: Comprehensive agent architecture guide
- **[MCP Specification](https://spec.modelcontextprotocol.io/)**: Official MCP protocol docs
- **[FastMCP](https://github.com/jlowin/fastmcp)**: FastMCP framework documentation
- **[CCXT](https://github.com/ccxt/ccxt)**: Exchange integration library

## 🔐 Security Best Practices

- Never commit `.env` files or API credentials
- Use sandbox/testnet mode for development
- Rotate API keys regularly
- Implement proper rate limiting
- Validate all inputs with Pydantic
- Use read-only API keys when possible

## 🤝 Contributing

1. Follow the established patterns in `AGENTS.md`
2. Use type hints for all functions
3. Add tests for new features
4. Update documentation
5. Follow Python best practices (PEP 8)

## 📝 License

[Add your license here]

## 🐛 Troubleshooting

### Import Errors

Ensure you're running from the project root and the virtual environment is activated.

### Exchange Connection Issues

- Verify API credentials in `.env`
- Check if sandbox mode is enabled for testnet
- Ensure exchange API is accessible from your network

### MCP Server Not Starting

- Check logs for detailed error messages
- Validate configuration with the inspector tool
- Ensure all dependencies are installed

## 📞 Support

For issues and questions:

- Check [AGENTS.md](./AGENTS.md) for architecture details
- Review MCP specification documentation
- Open an issue on the repository
