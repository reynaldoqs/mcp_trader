#!/usr/bin/env python3
"""Quick test to verify environment variable loading."""

import os
import sys
sys.path.append('src')

def main():
    print("=== Environment Variables ===")
    print(f"EXCHANGE_API_KEY: {os.getenv('EXCHANGE_API_KEY', 'NOT SET')}")
    print(f"EXCHANGE_API_SECRET: {os.getenv('EXCHANGE_API_SECRET', 'NOT SET')}")
    print(f"DEBUG: {os.getenv('DEBUG', 'NOT SET')}")
    print()
    
    try:
        from config.settings import get_settings
        
        print("=== Settings Values ===")
        settings = get_settings()
        print(f"settings.exchange.api_key: {settings.exchange.api_key}")
        print(f"settings.exchange.api_secret: {settings.exchange.api_secret}")
        print(f"settings.exchange.sandbox_mode: {settings.exchange.sandbox_mode}")
        print(f"settings.exchange.default_type: {settings.exchange.default_type}")
        print(f"settings.debug: {settings.debug}")
        print(f"settings.mcp.server_name: {settings.mcp.server_name}")
        print(f"settings.logging.level: {settings.logging.level}")
        
        print("\n=== Direct Field Access ===")
        print(f"settings.exchange_api_key: {settings.exchange_api_key}")
        print(f"settings.exchange_api_secret: {settings.exchange_api_secret}")
        
        print("\n✅ Settings loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
