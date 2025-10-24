from typing import Optional, Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Main settings class with all configuration options."""
    
    # Exchange settings
    exchange_api_key: Optional[str] = Field(None, env="EXCHANGE_API_KEY")
    exchange_api_secret: Optional[str] = Field(None, env="EXCHANGE_API_SECRET")
    exchange_sandbox_mode: bool = Field(True, env="EXCHANGE_SANDBOX_MODE")
    exchange_rate_limit: bool = Field(True, env="EXCHANGE_RATE_LIMIT")
    exchange_default_type: Literal["spot", "future", "margin"] = Field("future", env="EXCHANGE_DEFAULT_TYPE")
    
    # MCP settings
    mcp_server_name: str = Field("Trading MCP", env="MCP_SERVER_NAME")
    
    # Logging settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field(
        "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}", 
        env="LOG_FORMAT"
    )
    log_file_path: Optional[str] = Field(None, env="LOG_FILE_PATH")
    log_rotation: str = Field("1 day", env="LOG_ROTATION")
    log_retention: str = Field("30 days", env="LOG_RETENTION")
    
    # General settings
    debug: bool = Field(False, env="DEBUG")
    environment: Literal["development", "production"] = Field("production", env="ENVIRONMENT")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Convenience properties to maintain backward compatibility
    @property
    def exchange(self):
        """Exchange configuration namespace."""
        class ExchangeConfig:
            def __init__(self, settings):
                self.api_key = settings.exchange_api_key
                self.api_secret = settings.exchange_api_secret
                self.sandbox_mode = settings.exchange_sandbox_mode
                self.rate_limit = settings.exchange_rate_limit
                self.default_type = settings.exchange_default_type
        return ExchangeConfig(self)
    
    @property
    def mcp(self):
        """MCP configuration namespace."""
        class MCPConfig:
            def __init__(self, settings):
                self.server_name = settings.mcp_server_name
        return MCPConfig(self)
    
    @property
    def logging(self):
        """Logging configuration namespace."""
        class LoggingConfig:
            def __init__(self, settings):
                self.level = settings.log_level
                self.format = settings.log_format
                self.file_path = settings.log_file_path
                self.rotation = settings.log_rotation
                self.retention = settings.log_retention
        return LoggingConfig(self)

@lru_cache()
def get_settings() -> Settings:
    return Settings()
