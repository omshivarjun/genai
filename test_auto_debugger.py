#!/usr/bin/env python3
"""
Test script for the AI Auto-Debugger functionality using Gemini.
This demonstrates fully automated debugging without manual intervention.
"""

import os
from dotenv import load_dotenv
from agent.graph import agent

# Load environment variables
load_dotenv()

def test_auto_debugger():
    """Test the auto-debugger agent with a project that has errors."""
    
    print("🚀 Testing AI Auto-Debugger with Gemini")
    print("=" * 60)
    print("This test will:")
    print("1. Generate a project with the multi-agent system")
    print("2. Detect any errors in the generated code")
    print("3. Use Gemini AI to automatically fix all issues")
    print("4. Verify the fixes work correctly")
    print("=" * 60)
    
    # Test prompt that should generate a project
    test_prompt = "Build a modern todo app with HTML, CSS, and JavaScript that includes add, delete, and toggle functionality"
    
    try:
        # Run the agent with auto-debugging enabled
        print(f"\n📝 Running agent with prompt: {test_prompt}")
        print("-" * 40)
        
        result = agent.invoke({
            "user_prompt": test_prompt,
            "use_auto_debug": True  # Enable auto-debugging
        }, {"recursion_limit": 50})
        
        print("\n✅ Agent execution completed!")
        print("Final State Keys:", list(result.keys()))
        
        # Check if auto-debugging was successful
        if result.get("auto_debugging_done"):
            print("🤖 Auto-debugging was completed successfully!")
            
        if result.get("has_errors"):
            print("⚠️  Some errors may still remain")
            print("Error Report:", result.get("error_report", "No error report available"))
        else:
            print("✅ No errors detected - project is clean!")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


def test_interactive_vs_auto():
    """Compare interactive editing vs auto-debugging."""
    
    print("\n" + "="*60)
    print("🔄 COMPARISON TEST: Interactive vs Auto-Debugging")
    print("="*60)
    
    test_prompt = "Create a simple calculator app in HTML, CSS, and JavaScript"
    
    print("\n1️⃣ Testing with INTERACTIVE EDITOR:")
    print("-" * 40)
    
    try:
        result1 = agent.invoke({
            "user_prompt": test_prompt,
            "use_auto_debug": False  # Use interactive editing
        }, {"recursion_limit": 30})
        
        print("Interactive editing result:", "SUCCESS" if result1.get("interactive_editing_done") else "INCOMPLETE")
        
    except Exception as e:
        print(f"Interactive editing failed: {e}")
    
    print("\n2️⃣ Testing with AUTO-DEBUGGER:")
    print("-" * 40)
    
    try:
        result2 = agent.invoke({
            "user_prompt": test_prompt,
            "use_auto_debug": True  # Use auto-debugging
        }, {"recursion_limit": 30})
        
        print("Auto-debugging result:", "SUCCESS" if result2.get("auto_debugging_done") else "INCOMPLETE")
        
    except Exception as e:
        print(f"Auto-debugging failed: {e}")


if __name__ == "__main__":
    # Check if we have the required environment variable
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Please set your Google API key in the .env file")
        exit(1)
    
    print("🧪 Starting Auto-Debugger Tests")
    print("Current working directory:", os.getcwd())
    print("Available files:", os.listdir(os.getcwd()))
    
    # Run the main test
    test_auto_debugger()
    
    # Uncomment to run comparison test
    # test_interactive_vs_auto()
    
    print("\n🏁 Test completed!")