#!/usr/bin/env python
"""Entry point for the AI IT Technician Assistant application."""

import os
from dotenv import load_dotenv
from src.ui.app import create_app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    app = create_app()
    
    port = int(os.getenv("APP_PORT", 5000))
    debug = os.getenv("APP_DEBUG", "False").lower() == "true"
    
    print("\n" + "="*60)
    print("🤖 AI IT Technician Assistant (Pkpro)")
    print("="*60)
    print(f"🚀 Starting application...")
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
