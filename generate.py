#!/usr/bin/env python3
"""
Simple App Launcher - Just type the app name to generate!
Usage: python generate.py calculator
"""

import sys
import os
from app_prompts import generate_app, list_available_apps

def main():
    """Simple launcher that generates apps by name."""
    
    if len(sys.argv) < 2:
        print("🚀 Simple App Generator")
        print("=" * 30)
        print("Just type: python generate.py <app_name>")
        print("\nExample:")
        print("  python generate.py calculator")
        print("  python generate.py todo")
        print("  python generate.py grades")
        print("  python generate.py quiz")
        print("  python generate.py age")
        print()
        list_available_apps()
        return
    
    app_name = sys.argv[1].lower()
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found")
        print("Please set your Google Gemini API key in the .env file")
        return
    
    # Generate the app
    print(f"🎯 Generating {app_name} app...")
    result = generate_app(app_name)
    
    if result["success"]:
        print(f"\n✅ {app_name.capitalize()} app generated successfully!")
    else:
        print(f"\n❌ Failed to generate {app_name}: {result.get('error')}")

if __name__ == "__main__":
    main()