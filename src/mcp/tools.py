"""MCP tools registration and implementation."""

from typing import Any
from mcp.server.fastmcp import FastMCP
from loguru import logger

from ..core.types import OrderSide, OrderType
from ..core.exceptions import TradingError, ValidationError


def register_tools(mcp: FastMCP[Any]) -> None:
    
    @mcp.tool()
    def create_order(
        symbol: str,
        side: str,
        order_type: str = "market",
        usdt_amount: float = 0.0,
        price: float = None
    ) -> str:
        """
        Create a trading order.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('buy' or 'sell')
            order_type: Order type ('market' or 'limit')
            usdt_amount: Amount in USDT to trade
            price: Price for limit orders
            
        Returns:
            Order creation result message
        """
        try:
            if not symbol or not side:
                raise ValidationError("Symbol and side are required")
            
            if usdt_amount <= 0:
                raise ValidationError("USDT amount must be positive")
            
         
                
        except Exception as e:
            logger.error(f"Tool create_order failed: {e}")
            return f"Order creation failed: {str(e)}"
    
    @mcp.tool()
    def close_position(symbol: str) -> str:
        """
        Close all positions for a given symbol.
        
        Args:
            symbol: Trading symbol to close positions for
            
        Returns:
            Position closing result message
        """
        try:
            if not symbol:
                raise ValidationError("Symbol is required")
            
                
        except Exception as e:
            logger.error(f"Tool close_position failed: {e}")
            return f"Failed to close position: {str(e)}"
    
    logger.info("MCP tools registered successfully")
