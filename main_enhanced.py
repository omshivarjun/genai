#!/usr/bin/env python3
"""
Enhanced main script for the App Builder with both Interactive Editor and AI Auto-Debugger.
Users can choose between manual editing or fully automated debugging.
"""

import os
import sys
from dotenv import load_dotenv
from agent.graph import agent

# Load environment variables
load_dotenv()

def get_user_choice():
    """Get user preference for debugging mode."""
    print("\n🔧 DEBUG MODE SELECTION")
    print("=" * 40)
    print("Choose how you want to handle code errors:")
    print("1. 🤖 AI Auto-Debugger (Fully Automated)")
    print("   - Gemini AI analyzes and fixes all issues automatically")
    print("   - No manual intervention required")
    print("   - Best for quick fixes and standard errors")
    print()
    print("2. 🎯 Interactive Editor (Manual Control)")
    print("   - Command-line interface for manual code editing")
    print("   - You review and approve each change")
    print("   - Best for learning and complex customizations")
    print()
    
    while True:
        choice = input("Enter your choice (1 for Auto-Debugger, 2 for Interactive): ").strip()
        if choice == "1":
            return True  # Auto-debugging
        elif choice == "2":
            return False  # Interactive editing
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


def main():
    """Main application entry point."""
    
    # Check if we have the required environment variable
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        return
    
    print("🚀 Welcome to the Enhanced App Builder!")
    print("=" * 60)
    print("This tool uses AI agents to:")
    print("✅ Plan your application structure")
    print("✅ Design the architecture")
    print("✅ Generate the code")
    print("✅ Detect and fix errors automatically")
    print("=" * 60)
    
    # Get user input
    user_prompt = input("\n📝 What would you like to build? ")
    if not user_prompt.strip():
        print("❌ Please provide a description of what you want to build.")
        return
    
    # Get debugging preference
    use_auto_debug = get_user_choice()
    
    if use_auto_debug:
        print("\n🤖 Selected: AI Auto-Debugger (Fully Automated)")
        print("Gemini will handle all error detection and fixing automatically.")
    else:
        print("\n🎯 Selected: Interactive Editor (Manual Control)")
        print("You'll be able to manually review and edit the generated code.")
    
    print(f"\n🏗️  Building: {user_prompt}")
    print("=" * 60)
    
    try:
        # Run the agent
        result = agent.invoke({
            "user_prompt": user_prompt,
            "use_auto_debug": use_auto_debug
        }, {"recursion_limit": 100})
        
        print("\n🎉 BUILD COMPLETED!")
        print("=" * 60)
        
        # Show results
        if result.get("auto_debugging_done"):
            print("✅ AI Auto-Debugger completed successfully!")
            if result.get("has_errors"):
                print("⚠️  Some complex errors may still need attention:")
                print(result.get("error_report", "No details available"))
            else:
                print("✅ All errors were fixed automatically!")
                
        elif result.get("interactive_editing_done"):
            print("✅ Interactive editing session completed!")
            if result.get("has_errors"):
                print("⚠️  Some errors may still remain:")
                print(result.get("error_report", "No details available"))
            else:
                print("✅ All errors were resolved!")
        
        # Show final status
        final_status = result.get("status", "UNKNOWN")
        print(f"📊 Final Status: {final_status}")
        
        # Show generated files
        if os.path.exists("generated_project"):
            files = os.listdir("generated_project")
            print(f"\n📁 Generated Files ({len(files)} files):")
            for file in sorted(files):
                file_path = os.path.join("generated_project", file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"   📄 {file} ({size} bytes)")
        
        print(f"\n🌟 Your {user_prompt.lower()} is ready in the 'generated_project' folder!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Build interrupted by user.")
        
    except Exception as e:
        print(f"\n❌ Error during build: {e}")
        import traceback
        traceback.print_exc()


def quick_test():
    """Quick test function for development."""
    print("🧪 Running Quick Test...")
    
    test_prompts = [
        "Build a simple todo app",
        "Create a modern portfolio website",
        "Make a colorful calculator"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 Test {i}: {prompt}")
        try:
            result = agent.invoke({
                "user_prompt": prompt,
                "use_auto_debug": True  # Use auto-debugging for tests
            }, {"recursion_limit": 30})
            
            status = result.get("status", "UNKNOWN")
            has_errors = result.get("has_errors", False)
            print(f"   Result: {status} | Errors: {'Yes' if has_errors else 'No'}")
            
        except Exception as e:
            print(f"   ❌ Test failed: {e}")


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        quick_test()
    else:
        main()