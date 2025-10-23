from .resources_helper import format_balance_for_llm
from ..services.exchange_client import ExchangeClient
from typing import Any
from mcp.server.fastmcp import FastMCP
from loguru import logger

from ..core.types import OrderSide, OrderType
from ..core.exceptions import TradingError, ValidationError


def register_resources(mcp: FastMCP[Any], exchange_client: ExchangeClient) -> None:
    @mcp.resource("account://balance")
    def get_account_balance() -> str:
        """
        Get account balance from exchange
        
        Returns:
            Account balance in USDT
        """ 
        try:
            account_balance: Balances = exchange_client.retrieve_balance()
            # has_available_balance = has_available_usdt(account_balance, minimum_amount=10.0)
            # if has_available_balance:
            #     mcp.disable_tool(create_order)
            # else:
            #     mcp.add_tool(create_order)
            
            # has_positions = has_open_positions(account_balance)
            # if has_positions:
            #     mcp.add_tool(close_position)
            # else:
            #     mcp.remove_tool(close_position)

            formatted_balance = format_balance_for_llm(account_balance)

            return formatted_balance
            
        except Exception as e:
            logger.error(f"Resource get_account_balance failed: {e}")
            return f"Failed to get account balance: {str(e)}"
    
    logger.info("MCP resources registered successfully")
