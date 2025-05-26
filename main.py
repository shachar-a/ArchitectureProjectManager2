# File: main.py
"""
Main entry point for the Architecture Project Manager.
This file initializes and runs the unified application with both Contact and Project management.
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app_controller import AppController


def main():
    """Main function to start the Architecture Project Manager."""
    try:
        # Create and run the unified application
        app = AppController()
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
