from typing import Any
from mcp.server.fastmcp import FastMCP
from loguru import logger

from ..config.settings import Settings, get_settings
from ..services.exchange_client import ExchangeClient
from .resources import register_resources
from .tools import register_tools



class MCPServer:    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logger.bind(component="mcp_server")
        
        self.logger.info("Initializing MCP server with name: {}".format(settings.mcp.server_name))
        self.mcp: FastMCP[Any] = FastMCP(settings.mcp.server_name)
        
        self._initialized = False
    
    def initialize(self, exchange_client: ExchangeClient) -> None:
        try:
            register_tools(self.mcp, exchange_client)
            register_resources(self.mcp, exchange_client)
            self._initialized = True
            self.logger.info("MCP server initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize MCP server: {e}")
            raise
    
    def run(self, transport: str = "stdio") -> None:
        if not self._initialized:
            raise RuntimeError("MCP server not initialized. Call initialize() first.")
        
        self.logger.info(f"Starting MCP server with {transport} transport")
        self.mcp.run(transport=transport)
    
    def is_initialized(self) -> bool:
        return self._initialized


def create_mcp_server(settings: Settings = None) -> MCPServer:
    if settings is None:
        settings = get_settings()
    
    return MCPServer(settings)
