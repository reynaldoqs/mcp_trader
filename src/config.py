import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8000"))
EXCHANGE_API_KEY: Optional[str] = os.getenv("EXCHANGE_API_KEY")
EXCHANGE_API_SECRET: Optional[str] = os.getenv("EXCHANGE_API_SECRET")

