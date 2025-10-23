from src.services.exchange_client import create_exchange_client
from src.mcp.server import create_mcp_server

exchange_client = create_exchange_client()
exchange_client.initialize()

mcp_server = create_mcp_server()
# Expose the MCP server with standard name for CLI discovery
app = mcp_server.mcp
mcp_server.initialize(exchange_client)

# @TODO renew the api key FORM BINANCE

def main():
    mcp_server.run()

if __name__ == "__main__":
    main()
