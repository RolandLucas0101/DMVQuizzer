#!/usr/bin/env python3
"""
DMV Navigator NJ v2 - Python Launcher Script
This script launches the Streamlit application with proper configuration.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages if not already installed."""
    try:
        import streamlit
        print("✓ Streamlit already installed")
        return True
    except ImportError:
        print("Installing Streamlit...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "streamlit_requirements.txt"])
            print("✓ Streamlit installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install requirements: {e}")
            return False

def launch_app():
    """Launch the Streamlit application."""
    if not install_requirements():
        return False
    
    print("🚗 Starting DMV Navigator NJ v2...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    
    try:
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        return True
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True
    except Exception as e:
        print(f"✗ Error launching application: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🚗 DMV Navigator NJ v2 - Streamlit Launcher")
    print("=" * 50)
    
    if not os.path.exists("streamlit_app.py"):
        print("✗ Error: streamlit_app.py not found in current directory")
        sys.exit(1)
    
    success = launch_app()
    sys.exit(0 if success else 1)