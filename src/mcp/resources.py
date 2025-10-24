from typing import Any
from mcp.server.fastmcp import FastMCP
from loguru import logger
from ccxt.base.types import Balances

from .resources_helper import format_balance_for_llm
from ..services.exchange_client import ExchangeClient


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
            formatted_balance = format_balance_for_llm(account_balance)
            return formatted_balance
            
        except Exception as e:
            logger.error(f"Resource get_account_balance failed: {e}")
            return f"Failed to get account balance: {str(e)}"
    
    logger.info("MCP resources registered successfully")
