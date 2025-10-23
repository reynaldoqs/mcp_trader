from ccxt.base.types import OrderSide, Num, OrderType, Balances
from typing import Any
from mcp.server.fastmcp import FastMCP

from ..exchange.exchange_client import (
    create_usdt_order,
    close_position_by_symbol,
    fetch_account_balance
)
from .resources_helper import (
    format_balance_for_llm,
    has_available_usdt,
    has_open_positions
)

# Create an MCP server
mcp: FastMCP[Any] = FastMCP("Trading MCP")


@mcp.tool()
def create_order(symbol: str,
    type: OrderType,
    side: OrderSide,
    used_amount: float,
    price: Num = None) -> str:
    """Create a order in USDT on the exchange"""
    try:
        create_usdt_order(symbol, type, side, used_amount, price)
        return "Order created successfully"
    except Exception as e:
        raise Exception(f"Order creation failed: {str(e)}")

@mcp.tool(annotations={"enabled": False})
def close_position(symbol: str) -> str:
    """Close all positions on the exchange"""
    try:
        close_position_by_symbol(symbol)
        return "Position closed successfully"
    except Exception as e:
        raise Exception(f"Order closing failed: {str(e)}")


@mcp.resource("balance://account")
def get_account_balance() -> str:
    """Get account balance from exchange"""
    
    try:
        account_balance: Balances = fetch_account_balance()
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
        return str(e)
