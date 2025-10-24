from ..config.settings import get_settings, Settings
import ccxt
from typing import Dict, Any, List, Optional
from decimal import Decimal
from ccxt.binance import binance
from loguru import logger

from ..core.exceptions import (
    ExchangeError, 
    AuthenticationError, 
    NetworkError, 
    TradingError,
    InvalidOrderError
)
from ..core.types import OrderType, OrderSide


class ExchangeClient:
    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = logger.bind(component="exchange_client")
        self.exchange: binance
        
    def initialize(self) -> None:
        
        try:
            self.exchange = ccxt.binance({
                'apiKey': self.config.exchange.api_key,
                'secret': self.config.exchange.api_secret,
                'enableRateLimit': self.config.exchange.rate_limit,
                'options': {
                    'defaultType': self.config.exchange.default_type,
                }
            })
            
            if self.config.exchange.sandbox_mode:
                self.exchange.set_sandbox_mode(True)

            self.exchange.load_markets()
            self.exchange.verbose = self.config.debug
            self.logger.info("Exchange client initialized successfully")
            
        except ccxt.AuthenticationError as e:
            raise AuthenticationError(f"Exchange authentication failed: {e}")
        except ccxt.NetworkError as e:
            raise NetworkError(f"Exchange network error: {e}")
        except Exception as e:
            raise ExchangeError(f"Exchange initialization failed: {e}")
    
    def retrieve_balance(self) -> Dict[str, Any]:
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")
        
        try:
            balance = self.exchange.fetch_balance()
            self.logger.debug("Balance fetched successfully")
            return balance
            
        except ccxt.AuthenticationError as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except ccxt.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise ExchangeError(f"Failed to fetch balance: {e}")
    
    def fetch_positions(self, symbols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")
        
        try:
            positions = self.exchange.fetch_positions(symbols)
            self.logger.debug(f"Fetched {len(positions)} positions")
            return positions
            
        except ccxt.AuthenticationError as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except ccxt.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise ExchangeError(f"Failed to fetch positions: {e}")
    
    def fetch_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")
        
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            self.logger.debug(f"Fetched {len(orders)} open orders")
            return orders
            
        except ccxt.AuthenticationError as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except ccxt.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise ExchangeError(f"Failed to fetch open orders: {e}")

    def create_order(
        self,
        symbol: str,
        order_type: OrderType,
        side: OrderSide,
        amount: Decimal,
        price: Optional[Decimal] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an order on the exchange."""
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")

        try:
            order_params = params or {}
            
            if order_type == OrderType.LIMIT and price is None:
                raise InvalidOrderError("Price is required for limit orders")
            
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=float(amount),
                price=float(price) if price else None,
                params=order_params
            )
            
            self.logger.info(f"Order created: {order.get('id')} - {side} {amount} {symbol}")
            return order
            
        except ccxt.AuthenticationError as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except ccxt.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except ccxt.InvalidOrder as e:
            raise InvalidOrderError(f"Invalid order: {e}")
        except Exception as e:
            raise TradingError(f"Failed to create order: {e}")

    def create_usdt_order(
        self,
        symbol: str,
        order_type: OrderType,
        side: OrderSide,
        usdt_amount: Decimal,
        price: Optional[Decimal] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")

        try:
            current_symbol_price = Decimal(str(self.exchange.fetch_ticker(symbol)['last']))
            
            amount = usdt_amount / current_symbol_price
            market = self.exchange.market(symbol)
            min_amount = market['limits']['amount']['min']
            if amount < min_amount:
                raise InvalidOrderError(f"Amount {amount} is less than minimum required amount {min_amount}")
            
            return self.create_order(
                symbol=symbol,
                order_type=order_type,
                side=side,
                amount=amount,
                price=price,
                params=params
            )
            
        except Exception as e:
            raise TradingError(f"Failed to create USDT order: {e}")

    def market_buy(self, symbol: str, usdt_amount: Decimal) -> Dict[str, Any]:
        return self.create_usdt_order(
            symbol=symbol,
            order_type=OrderType.MARKET,
            side=OrderSide.BUY,
            usdt_amount=usdt_amount
        )

    def market_sell(self, symbol: str, usdt_amount: Decimal) -> Dict[str, Any]:
        return self.create_usdt_order(
            symbol=symbol,
            order_type=OrderType.MARKET,
            side=OrderSide.SELL,
            usdt_amount=usdt_amount
        )

    def limit_buy(self, symbol: str, usdt_amount: Decimal, price: Decimal) -> Dict[str, Any]:
        return self.create_usdt_order(
            symbol=symbol,
            order_type=OrderType.LIMIT,
            side=OrderSide.BUY,
            usdt_amount=usdt_amount,
            price=price
        )

    def limit_sell(self, symbol: str, usdt_amount: Decimal, price: Decimal) -> Dict[str, Any]:
        return self.create_usdt_order(
            symbol=symbol,
            order_type=OrderType.LIMIT,
            side=OrderSide.SELL,
            usdt_amount=usdt_amount,
            price=price
        )

    def close_position(self, symbol: str) -> str:
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")
        
        try:
            positions = self.exchange.fetch_positions([symbol])
            closed_positions = []
            
            for position in positions:
                position_amt = float(position['info'].get('positionAmt', 0))
                
                if position_amt != 0:
                    size = abs(position_amt)
                    side = 'sell' if position_amt > 0 else 'buy'  # Opposite side to close
                    
                    order = self.exchange.create_order(
                        symbol=symbol,
                        type='market',
                        side=side,
                        amount=size,
                        params={'reduceOnly': True}  # Ensures it closes position
                    )
                    
                    closed_positions.append({
                        'symbol': symbol,
                        'size': size,
                        'side': side,
                        'order_id': order.get('id')
                    })
            
            if not closed_positions:
                return f"No open positions found for {symbol}"
            
            message = f"Closed {len(closed_positions)} position(s) for {symbol}"
            self.logger.info(message)
            return message
            
        except ccxt.AuthenticationError as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        except ccxt.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise TradingError(f"Failed to close position: {e}")
    
    def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        if not self.exchange:
            raise ExchangeError("Exchange client not initialized")
        
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
            
        except ccxt.NetworkError as e:
            raise NetworkError(f"Network error: {e}")
        except Exception as e:
            raise ExchangeError(f"Failed to fetch ticker: {e}")
    
    def is_connected(self) -> bool:
        """Check if exchange client is connected and initialized."""
        return self.exchange is not None

def create_exchange_client(settings: Settings = None) -> ExchangeClient:
    if settings is None:
        settings = get_settings()
    return ExchangeClient(settings)
