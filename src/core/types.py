"""Common type definitions for the trading MCP project."""

from enum import Enum
from typing import Dict, Any, Optional, Union
from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime


class OrderSide(str, Enum):
    """Order side enumeration."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Order type enumeration."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"
    CANCELED = "canceled"
    EXPIRED = "expired"
    REJECTED = "rejected"


class PositionSide(str, Enum):
    """Position side enumeration."""
    LONG = "long"
    SHORT = "short"


class TimeInForce(str, Enum):
    """Time in force enumeration."""
    GTC = "GTC"  # Good Till Canceled
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill


@dataclass
class Balance:
    """Balance information for a currency."""
    currency: str
    total: Decimal
    available: Decimal
    locked: Decimal
    
    @property
    def used(self) -> Decimal:
        """Calculate used amount."""
        return self.total - self.available


@dataclass
class Position:
    """Position information."""
    symbol: str
    side: PositionSide
    size: Decimal
    entry_price: Decimal
    mark_price: Decimal
    unrealized_pnl: Decimal
    percentage: Decimal
    timestamp: datetime
    
    @property
    def notional_value(self) -> Decimal:
        """Calculate notional value of position."""
        return abs(self.size * self.mark_price)


@dataclass
class Order:
    """Order information."""
    id: str
    symbol: str
    side: OrderSide
    type: OrderType
    amount: Decimal
    price: Optional[Decimal]
    status: OrderStatus
    filled: Decimal
    remaining: Decimal
    timestamp: datetime
    
    @property
    def is_filled(self) -> bool:
        """Check if order is completely filled."""
        return self.status == OrderStatus.CLOSED and self.remaining == 0


@dataclass
class Ticker:
    """Market ticker information."""
    symbol: str
    bid: Decimal
    ask: Decimal
    last: Decimal
    volume: Decimal
    timestamp: datetime
    
    @property
    def spread(self) -> Decimal:
        """Calculate bid-ask spread."""
        return self.ask - self.bid
    
    @property
    def mid_price(self) -> Decimal:
        """Calculate mid price."""
        return (self.bid + self.ask) / 2


# Type aliases for common data structures
BalanceDict = Dict[str, Balance]
PositionDict = Dict[str, Position]
OrderDict = Dict[str, Order]

# Generic types for exchange responses
ExchangeResponse = Dict[str, Any]
MarketData = Dict[str, Any]
