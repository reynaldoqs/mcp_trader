"""Custom exceptions for the trading MCP project."""

from typing import Optional, Any


class TradingMCPError(Exception):
    """Base exception for all trading MCP errors."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(TradingMCPError):
    """Raised when there are configuration-related errors."""
    pass


class ValidationError(TradingMCPError):
    """Raised when data validation fails."""
    pass


class ExchangeError(TradingMCPError):
    """Base class for exchange-related errors."""
    
    def __init__(self, message: str, exchange_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message, details)
        self.exchange_code = exchange_code


class TradingError(ExchangeError):
    """Raised when trading operations fail."""
    pass


class MarketDataError(ExchangeError):
    """Raised when market data operations fail."""
    pass


class RiskManagementError(TradingMCPError):
    """Raised when risk management rules are violated."""
    pass


class AuthenticationError(ExchangeError):
    """Raised when exchange authentication fails."""
    pass


class NetworkError(ExchangeError):
    """Raised when network operations fail."""
    pass


class InsufficientFundsError(TradingError):
    """Raised when account has insufficient funds for operation."""
    pass


class InvalidOrderError(TradingError):
    """Raised when order parameters are invalid."""
    pass


class PositionNotFoundError(TradingError):
    """Raised when trying to operate on non-existent position."""
    pass
