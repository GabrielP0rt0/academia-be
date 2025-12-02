#!/usr/bin/env python3
"""
Startup script for Render deployment.
Validates PORT environment variable and starts the FastAPI server.
"""
import os
import sys

def get_port():
    """Get and validate PORT from environment."""
    port_str = os.getenv("PORT", "8000")
    
    # Try to convert to integer
    try:
        port = int(port_str)
        # Validate port range
        if port < 1 or port > 65535:
            print(f"Warning: PORT {port} is out of valid range (1-65535), using 8000", file=sys.stderr)
            return 8000
        return port
    except (ValueError, TypeError):
        print(f"Warning: PORT environment variable '{port_str}' is not a valid integer, using 8000", file=sys.stderr)
        return 8000

if __name__ == "__main__":
    port = get_port()
    # Import uvicorn and run
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

