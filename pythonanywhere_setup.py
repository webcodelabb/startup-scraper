#!/usr/bin/env python3
"""
PythonAnywhere deployment script
"""

import os
import subprocess

def setup_pythonanywhere():
    """Setup instructions for PythonAnywhere"""
    
    print("🐍 PythonAnywhere Free Deployment")
    print("=" * 40)
    
    print("\n📋 Setup Steps:")
    print("1. Go to https://www.pythonanywhere.com/")
    print("2. Create a free account")
    print("3. Go to 'Files' tab")
    print("4. Upload your scraper files")
    print("5. Go to 'Consoles' tab")
    print("6. Open a Bash console")
    print("7. Run the following commands:")
    
    commands = [
        "cd ~/scraper",
        "pip install -r requirements.txt",
        "python main.py --sources all --output-format both",
        "ls -la *.csv *.json"
    ]
    
    print("\n🔧 Commands to run:")
    for cmd in commands:
        print(f"   {cmd}")
    
    print("\n📊 Access your data:")
    print("- Files will be in your PythonAnywhere home directory")
    print("- Download via Files tab in PythonAnywhere")
    print("- Or use the web interface at your PythonAnywhere URL")
    
    print("\n💡 Tips:")
    print("- Free tier has limited CPU time")
    print("- Run scraper during off-peak hours")
    print("- Use --max-pages 1 for testing")
    print("- Check 'Tasks' tab for scheduled runs")

if __name__ == "__main__":
    setup_pythonanywhere() 