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

## 🔧 Configuration

The project uses Pydantic for type-safe configuration management. All settings can be configured via environment variables:

### Exchange Settings
- `EXCHANGE_API_KEY`: Your exchange API key
- `EXCHANGE_API_SECRET`: Your exchange API secret
- `EXCHANGE_SANDBOX_MODE`: Enable sandbox/testnet mode (default: true)
- `EXCHANGE_RATE_LIMIT`: Enable rate limiting (default: true)
- `EXCHANGE_DEFAULT_TYPE`: Order type - 'spot' or 'future' (default: future)

### MCP Settings
- `MCP_SERVER_NAME`: Server name (default: trading-mcp-server)

### Logging Settings
- `LOG_LEVEL`: Logging level (default: INFO)
- `LOG_FORMAT`: Log format string
- `LOG_FILE_PATH`: Path to log file
- `DEBUG`: Enable debug mode (default: false)

## 📚 MCP Tools & Resources

### Available Tools

- **`get_account_balance`**: Fetch account balance information
- **`check_usdt_balance`**: Check USDT balance with minimum requirement
- **`get_usdt_amount`**: Get current available USDT amount
- **`has_open_orders`**: Check for open orders
- **`has_available_balance`**: Check available balance for specific currency

### Available Resources

- **`account://balance`**: Real-time account balance data
- **`account://positions`**: Current open positions
- **`market://ticker/{symbol}`**: Market ticker data for symbol

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
