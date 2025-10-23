"""Configuration module for trading MCP.

This module provides configuration management using Pydantic settings.
"""

from .settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
