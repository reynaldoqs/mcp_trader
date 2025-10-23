"""Logging configuration setup."""

import sys
from loguru import logger
from .settings import get_settings


def setup_logging() -> None:
    """Configure loguru logging based on settings."""
    settings = get_settings()
    
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        level=settings.logging.level,
        format=settings.logging.format,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler if specified
    if settings.logging.file_path:
        logger.add(
            settings.logging.file_path,
            level=settings.logging.level,
            format=settings.logging.format,
            rotation=settings.logging.rotation,
            retention=settings.logging.retention,
            compression="zip",
            backtrace=True,
            diagnose=True
        )
    
    # Set log level based on environment
    if settings.environment == "development":
        logger.add(
            sys.stderr,
            level="DEBUG",
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True,
            filter=lambda record: record["level"].name == "DEBUG"
        )
    
    logger.info(f"Logging configured for {settings.environment} environment")
    logger.info(f"Log level: {settings.logging.level}")
    
    if settings.logging.file_path:
        logger.info(f"Log file: {settings.logging.file_path}")


def get_logger(name: str):
    """Get a logger instance with the given name."""
    return logger.bind(name=name)
