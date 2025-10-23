import ccxt
from loguru import logger
from ccxt.base.types import OrderType, OrderSide, Num, Any
from ..config import EXCHANGE_API_KEY, EXCHANGE_API_SECRET

exchange = ccxt.binance({
    'apiKey': EXCHANGE_API_KEY,
    'secret': EXCHANGE_API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    }
})


exchange.set_sandbox_mode(True)  # comment if you're not using the testnet
exchange.load_markets()
exchange.verbose = False  # debug output

def fetch_account_balance():
    try:
        balance = exchange.fetch_balance()
        return balance
    except ccxt.AuthenticationError:
        raise Exception("Error: Authentication failed - please check your API credentials")
    except ccxt.NetworkError as e:
        raise Exception(f"Error: Network connection failed - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: Unexpected issue occurred - {str(e)}")

def fetch_account_positions():
    try:
        positions = exchange.fetch_positions()
        return positions
    except ccxt.AuthenticationError:
        raise Exception("Error: Authentication failed - please check your API credentials")
    except ccxt.NetworkError as e:
        raise Exception(f"Error: Network connection failed - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: Unexpected issue occurred - {str(e)}")

def fetch_open_orders():
    try:
        orders = exchange.fetch_open_orders()
        return orders
    except ccxt.AuthenticationError:
        raise Exception("Error: Authentication failed - please check your API credentials")
    except ccxt.NetworkError as e:
        raise Exception(f"Error: Network connection failed - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: Unexpected issue occurred - {str(e)}")

def create_usdt_order(
    market_symbol: str,
    usdt_amount: float,
    price: Num = None,
    order_type: OrderType = OrderType.MARKET,
    order_side: OrderSide = OrderSide.BUY,
    params: Any = {}):
    try:
        current_symbol_price = float(exchange.fetch_ticker(market_symbol)['last'])
        amount = usdt_amount / current_symbol_price
        market = exchange.market(market_symbol)
        min_amount = market['limits']['amount']['min']
        if amount < min_amount:
            logger.warning(f"Calculated amount {amount} is less than minimum required amount {min_amount}. Adjusting amount to {min_amount}.")
            amount = min_amount
        order = exchange.create_order(market_symbol, order_type, order_side, amount, price, params)
        return order
    except ccxt.AuthenticationError:
        raise Exception("Error: Authentication failed - please check your API credentials")
    except ccxt.NetworkError as e:
        raise Exception(f"Error: Network connection failed - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: Unexpected issue occurred - {str(e)}")


def close_position_by_symbol(symbol: str):
    try:
        # Fetch current positions
        positions = exchange.fetch_positions([symbol])
        closed_positions = []
        for position in positions:
            if float(position['info']['positionAmt']) != 0:
                size = abs(float(position['info']['positionAmt']))
                side = 'sell' if float(position['info']['positionAmt']) > 0 else 'buy'  # Opposite side to close
                
                # Create market order to close position
                order = exchange.create_order(
                    symbol=symbol,
                    type='market',
                    side=side,
                    amount=size,
                    params={'reduceOnly': True}  # Important: this ensures it closes position
                )
                closed_positions.append({
                    'symbol': symbol,
                    'size': size,
                    'side': side,
                    'order_id': order.get('id')
                })
        
        if not closed_positions:
            return f"No open positions found for {symbol}"
        
        return f"Closed {len(closed_positions)} position(s) for {symbol}"
        
    except ccxt.AuthenticationError:
        raise Exception("Error: Authentication failed - please check your API credentials")
    except ccxt.NetworkError as e:
        raise Exception(f"Error: Network connection failed - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: Unexpected issue occurred - {str(e)}")
