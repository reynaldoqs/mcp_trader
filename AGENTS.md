# AGENTS.md

## Agent Architecture for Trading MCP

This document outlines the agent patterns and architecture for building intelligent trading agents using the Model Context Protocol (MCP) framework.

## Overview

This project implements a modular agent architecture that leverages MCP for communication between trading agents and external systems. The architecture follows Python best practices and MCP specifications.

## Agent Types

### 1. Trading Agent
**Purpose:** Execute trading strategies and manage positions
**Location:** `src/agents/trading_agent.py`
**Responsibilities:**
- Analyze market data
- Execute buy/sell orders
- Manage risk and position sizing
- Report trading performance

### 2. Market Data Agent
**Purpose:** Collect and process market information
**Location:** `src/agents/market_data_agent.py`
**Responsibilities:**
- Fetch real-time price data
- Process technical indicators
- Monitor market conditions
- Provide data to other agents

### 3. Risk Management Agent
**Purpose:** Monitor and control trading risks
**Location:** `src/agents/risk_agent.py`
**Responsibilities:**
- Calculate position sizes
- Monitor portfolio exposure
- Implement stop-loss mechanisms
- Generate risk reports

## Agent Communication Patterns

### MCP Protocol Integration
Agents communicate using the MCP protocol with the following patterns:

#### Tools Pattern
```python
@mcp.tool()
def execute_trade(symbol: str, side: str, quantity: float) -> dict:
    """Execute a trade order"""
    # Implementation
    pass
```

#### Resources Pattern
```python
@mcp.resource("market-data://{symbol}")
def get_market_data(symbol: str) -> dict:
    """Get current market data for symbol"""
    # Implementation
    pass
```

#### Prompts Pattern
```python
@mcp.prompt()
def analyze_market(symbol: str, timeframe: str = "1h") -> str:
    """Generate market analysis prompt"""
    # Implementation
    pass
```

## Agent Base Classes

### BaseAgent
All agents should inherit from a common base class:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from src.config import Config

class BaseAgent(ABC):
    def __init__(self, config: Config):
        self.config = config
        self.logger = self._setup_logger()
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize agent resources"""
        pass
    
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming data"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        pass
```

## Configuration Management

### Agent Configuration
Each agent should have its own configuration section:

```python
# .env
TRADING_AGENT_ENABLED=true
TRADING_AGENT_MAX_POSITION_SIZE=1000
MARKET_DATA_AGENT_UPDATE_INTERVAL=5
RISK_AGENT_MAX_DRAWDOWN=0.05
```

### Type-Safe Configuration
Use Pydantic for configuration validation:

```python
from pydantic import BaseSettings

class AgentConfig(BaseSettings):
    enabled: bool = True
    max_position_size: float = 1000.0
    update_interval: int = 5
    
    class Config:
        env_prefix = "TRADING_AGENT_"
```

## Error Handling and Resilience

### Exception Handling
Implement robust error handling:

```python
from src.exceptions import TradingError, MarketDataError

class TradingAgent(BaseAgent):
    async def execute_trade(self, order: TradeOrder):
        try:
            result = await self.exchange.place_order(order)
            return result
        except ExchangeError as e:
            raise TradingError(f"Failed to execute trade: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise
```

### Circuit Breaker Pattern
Implement circuit breakers for external dependencies:

```python
from circuit_breaker import CircuitBreaker

class MarketDataAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__(config)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=30
        )
```

## Logging and Monitoring

### Structured Logging
Use structured logging for better observability:

```python
import structlog

logger = structlog.get_logger()

class TradingAgent(BaseAgent):
    async def execute_trade(self, order: TradeOrder):
        logger.info(
            "executing_trade",
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            agent_id=self.id
        )
```

### Metrics Collection
Implement metrics for monitoring:

```python
from prometheus_client import Counter, Histogram

trades_executed = Counter('trades_executed_total', 'Total trades executed')
trade_latency = Histogram('trade_execution_seconds', 'Trade execution time')
```

## Testing Strategies

### Unit Testing
Test individual agent methods:

```python
import pytest
from unittest.mock import Mock
from src.agents.trading_agent import TradingAgent

@pytest.fixture
def trading_agent():
    config = Mock()
    return TradingAgent(config)

def test_calculate_position_size(trading_agent):
    size = trading_agent.calculate_position_size(
        account_balance=10000,
        risk_percent=0.02
    )
    assert size == 200
```

### Integration Testing
Test agent interactions:

```python
@pytest.mark.asyncio
async def test_agent_communication():
    market_agent = MarketDataAgent(config)
    trading_agent = TradingAgent(config)
    
    # Test data flow between agents
    market_data = await market_agent.get_data("BTCUSD")
    trade_signal = await trading_agent.analyze(market_data)
    
    assert trade_signal is not None
```

## Deployment Patterns

### Container Deployment
Use Docker for consistent deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ src/
COPY main.py .

CMD ["python", "main.py"]
```

### Agent Orchestration
Use docker-compose for multi-agent deployment:

```yaml
version: '3.8'
services:
  trading-agent:
    build: .
    environment:
      - AGENT_TYPE=trading
    depends_on:
      - market-data-agent
  
  market-data-agent:
    build: .
    environment:
      - AGENT_TYPE=market_data
```

## Security Considerations

### API Key Management
- Store API keys in environment variables
- Use secret management systems in production
- Rotate keys regularly
- Implement key validation

### Network Security
- Use TLS for all communications
- Implement rate limiting
- Validate all inputs
- Log security events

## Performance Optimization

### Async Programming
Use asyncio for concurrent operations:

```python
import asyncio
from typing import List

class AgentManager:
    async def run_agents(self, agents: List[BaseAgent]):
        tasks = [agent.process() for agent in agents]
        await asyncio.gather(*tasks)
```

### Caching Strategies
Implement caching for frequently accessed data:

```python
from functools import lru_cache
import redis

class MarketDataAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__(config)
        self.redis = redis.Redis(host=config.redis_host)
    
    @lru_cache(maxsize=128)
    def get_cached_data(self, symbol: str):
        return self.redis.get(f"market_data:{symbol}")
```

## Best Practices Summary

1. **Modularity:** Keep agents focused on single responsibilities
2. **Type Safety:** Use type hints and Pydantic for validation
3. **Error Handling:** Implement comprehensive error handling
4. **Logging:** Use structured logging for observability
5. **Testing:** Write comprehensive unit and integration tests
6. **Configuration:** Use environment variables and type-safe config
7. **Security:** Protect API keys and validate inputs
8. **Performance:** Use async programming and caching
9. **Documentation:** Document agent interfaces and behaviors
10. **Monitoring:** Implement metrics and health checks

## Contributing

When adding new agents:

1. Inherit from `BaseAgent`
2. Implement required abstract methods
3. Add comprehensive tests
4. Update this documentation
5. Follow the established patterns

## Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Python Async Best Practices](https://docs.python.org/3/library/asyncio.html)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
