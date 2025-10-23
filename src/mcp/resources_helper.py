from typing import Dict, Any, List
from ccxt.base.types import Balances, Position

def format_balance_for_llm(balance_data: Balances) -> str:
    """Format balance data with optional positions into a human-readable string for LLM understanding"""
    
    if not balance_data:
        return "No balance data available"
    
    formatted_text = ""
    
    # Handle Binance futures format with info.assets
    if 'info' in balance_data and 'assets' in balance_data['info']:
        assets = balance_data['info']['assets']
        positions = balance_data['info'].get('positions', [])
        
        # Get total unrealized profit from info
        total_unrealized_profit = float(balance_data['info'].get('totalUnrealizedProfit', 0))
        
        # Process each asset with non-zero balance
        for asset in assets:
            wallet_balance = float(asset.get('walletBalance', 0))
            if wallet_balance > 0:
                asset_name = asset.get('asset', 'Unknown')
                available_balance = float(asset.get('availableBalance', 0))
                asset_unrealized_pnl = float(asset.get('unrealizedProfit', 0))
                
                # Calculate used amount (wallet balance - available balance)
                used_amount = wallet_balance - available_balance
                
                formatted_text += f"- {asset_name}: {wallet_balance}\n"
                formatted_text += f"  - Available: {available_balance}\n"
                formatted_text += f"  - In Use: {used_amount}\n"
                
                # Add asset-level PnL if non-zero
                if asset_unrealized_pnl != 0:
                    formatted_text += f"  - Asset PnL: {asset_unrealized_pnl}\n"
                
                # Check for positions related to this asset
                asset_positions = []
                asset_position_pnl = 0.0
                for pos in positions:
                    if float(pos.get('positionAmt', 0)) != 0:
                        symbol = pos.get('symbol', '')
                        # Check if position symbol contains this asset
                        if asset_name in symbol:
                            asset_positions.append(pos)
                            asset_position_pnl += float(pos.get('unRealizedProfit', 0))
                
                if asset_positions:
                    formatted_text += "  - Active Positions:\n"
                    for pos in asset_positions:
                        symbol = pos.get('symbol', 'Unknown')
                        position_amt = float(pos.get('positionAmt', 0))
                        pnl = float(pos.get('unRealizedProfit', 0))
                        side = "LONG" if position_amt > 0 else "SHORT"
                        
                        formatted_text += f"    * {symbol} ({side}): {position_amt} | PnL: {pnl}\n"
                
                formatted_text += "\n"
        
        # Add total PnL summary
        if total_unrealized_profit != 0:
            formatted_text += f"Total Unrealized PnL: {total_unrealized_profit}\n"
    
    # Fallback to standard format using total/free/used
    else:
        total_balances = balance_data.get('total', {})
        free_balances = balance_data.get('free', {})
        used_balances = balance_data.get('used', {})
        
        # Filter out zero balances
        non_zero_balances = {k: v for k, v in total_balances.items() if v and float(v) > 0}
        
        if not non_zero_balances:
            return "No available balances"
        
        for currency, total_amount in non_zero_balances.items():
            free_amount = free_balances.get(currency, 0)
            used_amount = used_balances.get(currency, 0)
            
            formatted_text += f"- {currency}: {total_amount}\n"
            formatted_text += f"  - Available: {free_amount}\n"
            formatted_text += f"  - In Use: {used_amount}\n\n"
    
    return formatted_text.strip()

def has_available_usdt(balance_data: Balances, minimum_amount: float = 0.0) -> bool:
    """
    Simple function to check if account has available USDT for opening orders
    
    Args:
        balance_data: Balance data from exchange
        minimum_amount: Minimum USDT amount required (default: 0.0)
    
    Returns:
        True if available USDT >= minimum_amount, False otherwise
    """
    if not balance_data:
        return False
    
    # Handle Binance futures format with info.assets
    if 'info' in balance_data and 'assets' in balance_data['info']:
        assets = balance_data['info']['assets']
        for asset in assets:
            if asset.get('asset') == 'USDT':
                available_balance = float(asset.get('availableBalance', 0))
                return available_balance >= minimum_amount
        return False
    
    # Fallback to standard format
    else:
        free_balances = balance_data.get('free', {})
        available_balance = float(free_balances.get('USDT', 0))
        return available_balance >= minimum_amount

def get_usdt_balance(balance_data: Balances) -> float:
    """
    Get available USDT amount from balance data
    
    Args:
        balance_data: Balance data from exchange
    
    Returns:
        Available USDT amount as float
    """
    if not balance_data:
        return 0.0
    
    # Handle Binance futures format with info.assets
    if 'info' in balance_data and 'assets' in balance_data['info']:
        assets = balance_data['info']['assets']
        for asset in assets:
            if asset.get('asset') == 'USDT':
                return float(asset.get('availableBalance', 0))
        return 0.0
    
    # Fallback to standard format
    else:
        free_balances = balance_data.get('free', {})
        return float(free_balances.get('USDT', 0))

def has_open_positions(balance_data: Balances) -> bool:
    """
    Simple function to check if account has any open positions based on balance data
    
    Args:
        balance_data: Balance data from exchange
    
    Returns:
        True if has open positions, False otherwise
    """
    if not balance_data:
        return False
    
    # Handle Binance futures format with info.positions
    if 'info' in balance_data and 'positions' in balance_data['info']:
        positions = balance_data['info']['positions']
        for position in positions:
            position_amt = float(position.get('positionAmt', 0))
            if position_amt != 0:
                return True
    
    return False

def get_open_positions_count(balance_data: Balances) -> int:
    """
    Get count of open positions based on balance data
    
    Args:
        balance_data: Balance data from exchange
    
    Returns:
        Number of open positions
    """
    if not balance_data:
        return 0
    
    count = 0
    # Handle Binance futures format with info.positions
    if 'info' in balance_data and 'positions' in balance_data['info']:
        positions = balance_data['info']['positions']
        for position in positions:
            position_amt = float(position.get('positionAmt', 0))
            if position_amt != 0:
                count += 1
    
    return count

def get_open_positions_symbols(balance_data: Balances) -> List[str]:
    """
    Get list of symbols with open positions based on balance data
    
    Args:
        balance_data: Balance data from exchange
    
    Returns:
        List of symbol names with open positions
    """
    if not balance_data:
        return []
    
    symbols = []
    # Handle Binance futures format with info.positions
    if 'info' in balance_data and 'positions' in balance_data['info']:
        positions = balance_data['info']['positions']
        for position in positions:
            position_amt = float(position.get('positionAmt', 0))
            if position_amt != 0:
                symbol = position.get('symbol', 'Unknown')
                symbols.append(symbol)
    
    return symbols
