"""MCP tools registration and implementation."""

from typing import Any
from mcp.server.fastmcp import FastMCP
from loguru import logger

from ..core.types import OrderSide, OrderType
from ..core.exceptions import TradingError, ValidationError
from ..services.exchange_client import ExchangeClient


def register_tools(mcp: FastMCP[Any], exchange_client: ExchangeClient) -> None:
    @mcp.tool()
    def open_market_long(symbol: str, usdt_amount: int) -> str:
        """
        Open long position with market current price.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            usdt_amount: Amount in USDT to trade
            
        Returns:
            Position opening result message
        """
        try:
            if not symbol:
                raise ValidationError("Symbol is required")
            
            if usdt_amount <= 0:
                raise ValidationError("USDT amount must be positive")
            
            exchange_client.market_buy(symbol, usdt_amount)
            
            return "Position opened successfully"
                
        except Exception as e:
            logger.error(f"Tool open_market_long failed: {e}")
            return f"Failed to open market long position: {str(e)}"
    
    @mcp.tool()
    def open_market_short(symbol: str, usdt_amount: int) -> str:
        """
        Open short position with market current price.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            usdt_amount: Amount in USDT to trade
            
        Returns:
            Position opening result message
        """
        try:
            if not symbol:
                raise ValidationError("Symbol is required")
            
            if usdt_amount <= 0:
                raise ValidationError("USDT amount must be positive")
            
            exchange_client.market_sell(symbol, usdt_amount)
            
            return "Position opened successfully"
                
        except Exception as e:
            logger.error(f"Tool open_market_short failed: {e}")
            return f"Failed to open market short position: {str(e)}"

    @mcp.tool()
    def open_limit_long(symbol: str, usdt_amount: int, price: int) -> str:
        """
        Open long position with limit order.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            usdt_amount: Amount in USDT to trade
            price: Limit price
            
        Returns:
            Position opening result message
        """
        try:
            if not symbol:
                raise ValidationError("Symbol is required")
            
            if usdt_amount <= 0:
                raise ValidationError("USDT amount must be positive")
            
            exchange_client.limit_buy(symbol, usdt_amount, price)
            
            return "Position opened successfully"
                
        except Exception as e:
            logger.error(f"Tool open_limit_long failed: {e}")
            return f"Failed to open limit long position: {str(e)}"
    
    @mcp.tool()
    def open_limit_short(symbol: str, usdt_amount: int, price: int) -> str:
        """
        Open short position with limit order.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            usdt_amount: Amount in USDT to trade
            price: Limit price
            
        Returns:
            Position opening result message
        """
        try:
            if not symbol:
                raise ValidationError("Symbol is required")
            
            if usdt_amount <= 0:
                raise ValidationError("USDT amount must be positive")
            
            exchange_client.limit_sell(symbol, usdt_amount, price)
            
            return "Position opened successfully"
                
        except Exception as e:
            logger.error(f"Tool open_limit_short failed: {e}")
            return f"Failed to open limit short position: {str(e)}"
    
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
            
            exchange_client.close_position_by_symbol(symbol)
            
            return "Position closed successfully"
                
        except Exception as e:
            logger.error(f"Tool close_position failed: {e}")
            return f"Failed to close position: {str(e)}"
    
    logger.info("MCP tools registered successfully")
