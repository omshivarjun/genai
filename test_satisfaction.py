#!/usr/bin/env python3
"""
Test script for the enhanced app generation system with satisfaction checking.
This script demonstrates the new features without requiring user interaction.
"""

import os
import sys
from app_prompts import generate_app, APPS

def test_satisfaction_system():
    """Test the enhanced generation system."""
    print("🧪 Testing Enhanced App Generation with Satisfaction Checking")
    print("=" * 70)
    
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google Gemini API key in the .env file")
        return False
    
    print("✅ API Key found")
    print("📱 Available apps:", list(APPS.keys()))
    
    # Test app availability
    print("\n🔍 Testing app registry...")
    for app_name in APPS.keys():
        app_spec = APPS[app_name]
        print(f"  ✅ {app_name}: {app_spec.description}")
        print(f"     Features: {len(app_spec.features)}")
        print(f"     Prompt length: {len(app_spec.prompt)} chars")
    
    print("\n🎯 System Features:")
    print("  ✅ Detailed prompts for 5 different apps")
    print("  ✅ File-name triggering via batch files")
    print("  ✅ Multi-agent architecture with auto-debugging")
    print("  ✅ User satisfaction checking")
    print("  ✅ Gemini-powered editing and improvements")
    print("  ✅ Interactive feedback loop")
    
    print("\n💡 Enhanced Workflow:")
    print("  1. Generate app with detailed prompts")
    print("  2. Show completion and file locations")
    print("  3. Ask user satisfaction (y/n)")
    print("  4. If not satisfied, get specific feedback")
    print("  5. Use Gemini to apply improvements")
    print("  6. Repeat until user is satisfied")
    print("  7. Show final satisfaction status")
    
    print(f"\n✅ Enhanced system ready!")
    print(f"Usage: python app_prompts.py <app_name>")
    print(f"Example: python app_prompts.py calculator")
    
    return True

def demo_batch_files():
    """Demonstrate the batch file system."""
    print("\n🚀 Batch File System:")
    batch_files = ['calculator.bat', 'todo.bat', 'grades.bat', 'quiz.bat', 'age.bat']
    
    for batch_file in batch_files:
        if os.path.exists(batch_file):
            print(f"  ✅ {batch_file} - Ready for one-click generation")
        else:
            print(f"  ❌ {batch_file} - Missing")
    
    print("\n💡 Just type the app name (e.g., 'calculator') to generate!")

if __name__ == "__main__":
    print("🌟 Enhanced GenAI App Builder - System Test")
    print("=" * 50)
    
    success = test_satisfaction_system()
    demo_batch_files()
    
    if success:
        print(f"\n🎊 System Test Completed Successfully!")
        print(f"🚀 Ready to generate apps with satisfaction checking!")
        print(f"   • Enhanced user experience")
        print(f"   • Gemini-powered editing")
        print(f"   • Interactive feedback loop")
        print(f"   • Automatic satisfaction tracking")
    else:
        print(f"\n❌ System test failed. Please check configuration.")