"""Balance service for managing account balances."""

from typing import Dict, Optional
from decimal import Decimal
from loguru import logger

from ..config import Settings
from ..core.types import Balance, BalanceDict
from ..core.exceptions import ExchangeError, ValidationError
from ..exchange.client import ExchangeClient


class BalanceService:    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = logger.bind(service="balance")
        self.exchange_client: Optional[ExchangeClient] = None
        
    async def initialize(self) -> None:
        """Initialize the balance service."""
        try:
            from ..exchange.client import ExchangeClient
            self.exchange_client = ExchangeClient(self.config)
            await self.exchange_client.initialize()
            self.logger.info("Balance service initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize balance service: {e}")
            raise ExchangeError(f"Balance service initialization failed: {e}")
    
    async def cleanup(self) -> None:
        """Cleanup balance service resources."""
        if self.exchange_client:
            await self.exchange_client.cleanup()
        self.logger.info("Balance service cleaned up")
    
    async def get_balances(self) -> BalanceDict:
        """
        Get all account balances.
        
        Returns:
            Dictionary of balances by currency
        """
        if not self.exchange_client:
            raise ExchangeError("Balance service not initialized")
        
        try:
            raw_balance = await self.exchange_client.fetch_balance()
            return self._parse_balance_data(raw_balance)
        except Exception as e:
            self.logger.error(f"Failed to fetch balances: {e}")
            raise ExchangeError(f"Failed to fetch balances: {e}")
    
    async def get_balance(self, currency: str) -> Optional[Balance]:
        """
        Get balance for a specific currency.
        
        Args:
            currency: Currency symbol (e.g., 'USDT', 'BTC')
            
        Returns:
            Balance object or None if currency not found
        """
        balances = await self.get_balances()
        return balances.get(currency.upper())
    
    async def get_available_balance(self, currency: str) -> Decimal:
        """
        Get available balance for a specific currency.
        
        Args:
            currency: Currency symbol
            
        Returns:
            Available balance amount
        """
        balance = await self.get_balance(currency)
        return balance.available if balance else Decimal("0")
    
    async def get_total_balance(self, currency: str) -> Decimal:
        """
        Get total balance for a specific currency.
        
        Args:
            currency: Currency symbol
            
        Returns:
            Total balance amount
        """
        balance = await self.get_balance(currency)
        return balance.total if balance else Decimal("0")
    
    async def has_sufficient_balance(self, currency: str, required_amount: Decimal) -> bool:
        """
        Check if account has sufficient available balance.
        
        Args:
            currency: Currency symbol
            required_amount: Required amount
            
        Returns:
            True if sufficient balance available
        """
        if required_amount < 0:
            raise ValidationError("Required amount must be non-negative")
        
        available = await self.get_available_balance(currency)
        return available >= required_amount
    
    async def get_usdt_balance_info(self, minimum_amount: Decimal = Decimal("0")) -> Dict[str, any]:
        """
        Get USDT balance information with availability check.
        
        Args:
            minimum_amount: Minimum required amount
            
        Returns:
            Dictionary with balance info and availability status
        """
        try:
            usdt_balance = await self.get_balance("USDT")
            
            if not usdt_balance:
                return {
                    "has_balance": False,
                    "available_amount": 0.0,
                    "total_amount": 0.0,
                    "message": "No USDT balance found"
                }
            
            has_sufficient = usdt_balance.available >= minimum_amount
            
            return {
                "has_balance": has_sufficient,
                "available_amount": float(usdt_balance.available),
                "total_amount": float(usdt_balance.total),
                "locked_amount": float(usdt_balance.locked),
                "minimum_required": float(minimum_amount),
                "message": (
                    f"Sufficient USDT balance: {usdt_balance.available}" 
                    if has_sufficient 
                    else f"Insufficient USDT balance. Available: {usdt_balance.available}, Required: {minimum_amount}"
                )
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get USDT balance info: {e}")
            return {
                "has_balance": False,
                "available_amount": 0.0,
                "total_amount": 0.0,
                "message": f"Error fetching balance: {str(e)}"
            }
    
    def _parse_balance_data(self, raw_balance: Dict) -> BalanceDict:
        """
        Parse raw balance data from exchange into Balance objects.
        
        Args:
            raw_balance: Raw balance data from exchange
            
        Returns:
            Dictionary of parsed Balance objects
        """
        balances = {}
        
        try:
            # Handle Binance futures format with info.assets
            if 'info' in raw_balance and 'assets' in raw_balance['info']:
                assets = raw_balance['info']['assets']
                for asset in assets:
                    currency = asset.get('asset', '').upper()
                    if not currency:
                        continue
                        
                    wallet_balance = Decimal(str(asset.get('walletBalance', 0)))
                    available_balance = Decimal(str(asset.get('availableBalance', 0)))
                    
                    # Only include currencies with non-zero balances
                    if wallet_balance > 0:
                        balances[currency] = Balance(
                            currency=currency,
                            total=wallet_balance,
                            available=available_balance,
                            locked=wallet_balance - available_balance
                        )
            
            # Fallback to standard CCXT format
            else:
                total_balances = raw_balance.get('total', {})
                free_balances = raw_balance.get('free', {})
                used_balances = raw_balance.get('used', {})
                
                for currency, total_amount in total_balances.items():
                    if total_amount and Decimal(str(total_amount)) > 0:
                        currency = currency.upper()
                        total = Decimal(str(total_amount))
                        available = Decimal(str(free_balances.get(currency, 0)))
                        locked = Decimal(str(used_balances.get(currency, 0)))
                        
                        balances[currency] = Balance(
                            currency=currency,
                            total=total,
                            available=available,
                            locked=locked
                        )
            
            return balances
            
        except Exception as e:
            self.logger.error(f"Failed to parse balance data: {e}")
            raise ExchangeError(f"Failed to parse balance data: {e}")
    
    async def format_balances_for_display(self) -> str:
        """
        Format balances for human-readable display.
        
        Returns:
            Formatted balance string
        """
        try:
            balances = await self.get_balances()
            
            if not balances:
                return "No balances available"
            
            formatted_lines = []
            
            for currency, balance in balances.items():
                formatted_lines.append(f"- {currency}: {balance.total}")
                formatted_lines.append(f"  - Available: {balance.available}")
                formatted_lines.append(f"  - Locked: {balance.locked}")
                formatted_lines.append("")
            
            return "\n".join(formatted_lines).strip()
            
        except Exception as e:
            self.logger.error(f"Failed to format balances: {e}")
            return f"Error formatting balances: {str(e)}"
