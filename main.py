# File: main.py
"""
Main entry point for the Contact Management System.
This file initializes and runs the application.
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from controllers import ContactController


def main():
    """Main function to start the Contact Management System."""
    try:
        # Create and run the application
        app = ContactController()
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
