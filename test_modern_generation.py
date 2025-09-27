#!/usr/bin/env python3
"""
Test the improved code generation system with modern, error-free output
"""

import os
from dotenv import load_dotenv
from agent.graph import agent

load_dotenv()

def test_modern_generation():
    """Test the improved system with a simple request."""
    
    print("🚀 Testing Modern Code Generation")
    print("=" * 50)
    
    test_prompt = "Create a modern todo app with add, delete, and complete functionality"
    
    try:
        print(f"📝 Generating: {test_prompt}")
        print("-" * 30)
        
        # Generate with auto-debugging enabled
        result = agent.invoke({
            "user_prompt": test_prompt,
            "use_auto_debug": True
        }, {"recursion_limit": 50})
        
        print("\n✅ Generation completed!")
        
        # Check results
        final_status = result.get("status", "UNKNOWN")
        has_errors = result.get("has_errors", False)
        
        print(f"📊 Final Status: {final_status}")
        print(f"🔍 Has Errors: {'Yes' if has_errors else 'No'}")
        
        if result.get("auto_debugging_done"):
            print("🤖 Auto-debugging completed")
        
        # Show generated files
        project_path = "generated_projects"
        if os.path.exists(project_path):
            folders = [f for f in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, f))]
            if folders:
                latest_folder = max(folders)
                latest_path = os.path.join(project_path, latest_folder)
                files = os.listdir(latest_path)
                print(f"\n📁 Generated in: {latest_folder}")
                print(f"📄 Files created: {', '.join(files)}")
                
                # Check if files are properly linked
                if 'index.html' in files:
                    html_path = os.path.join(latest_path, 'index.html')
                    with open(html_path, 'r') as f:
                        html_content = f.read()
                    
                    has_css_link = 'rel="stylesheet"' in html_content
                    has_js_link = 'src="script.js"' in html_content
                    
                    print(f"🔗 CSS linked: {'Yes' if has_css_link else 'No'}")
                    print(f"🔗 JS linked: {'Yes' if has_js_link else 'No'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not set")
        exit(1)
    
    test_modern_generation()