"""
Enhanced Main Script with Interactive Error Editing
Demonstrates the new interactive editing capabilities when errors are detected
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from agent.graph import agent
from agent.tools import init_project_root, detect_project_errors, start_interactive_editor, PROJECT_ROOT
from agent.interactive_editor import start_interactive_editing_session


def main():
    """Main function with interactive editing support"""
    print("🚀 AI Web Development Agent with Interactive Error Editing")
    print("=" * 60)
    
    # Initialize project root
    project_root = init_project_root()
    print(f"📁 Project will be created in: {project_root}")
    
    # Get user prompt
    while True:
        user_prompt = input("\n💡 What would you like to build? (or 'quit' to exit): ").strip()
        
        if user_prompt.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_prompt:
            print("❌ Please provide a valid prompt!")
            continue
        
        print(f"\n🎯 Building: {user_prompt}")
        print("-" * 40)
        
        try:
            # Run the agent workflow
            print("🤖 Starting AI agents...")
            result = agent.invoke({"user_prompt": user_prompt}, {"recursion_limit": 100})
            
            print("\n✅ Initial project generation completed!")
            print(f"📁 Project location: {project_root}")
            
            # Check for errors
            print("\n🔍 Checking for errors in generated code...")
            errors = detect_project_errors.invoke({})
            
            if "error(s)" in errors.lower():
                print("❌ Errors detected! Starting interactive editor...")
                print(errors)
                
                # Ask user if they want to use interactive editor
                use_editor = input("\n🎯 Would you like to use the interactive editor to fix errors? (y/n): ").lower()
                
                if use_editor == 'y':
                    start_interactive_editing_session(project_root)
                    
                    # Check errors again after editing
                    print("\n🔍 Re-checking for errors...")
                    final_errors = detect_project_errors.invoke({})
                    
                    if "error(s)" not in final_errors.lower():
                        print("✅ All errors fixed! Project is ready.")
                    else:
                        print("⚠️ Some errors remain:")
                        print(final_errors)
                        
                        # Ask if they want to edit again
                        edit_again = input("\n🔄 Edit again? (y/n): ").lower()
                        if edit_again == 'y':
                            start_interactive_editing_session(project_root)
                else:
                    print("⚠️ Project completed with errors. You can manually fix them or run the interactive editor later.")
            else:
                print("✅ No errors detected! Project is ready to use.")
            
            # Show project files
            print(f"\n📂 Generated Files in {project_root}:")
            for file_path in Path(project_root).rglob("*"):
                if file_path.is_file():
                    print(f"  📄 {file_path.relative_to(project_root)}")
            
            # Ask if they want to build another project
            another = input("\n🔄 Build another project? (y/n): ").lower()
            if another != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Operation cancelled by user.")
            break
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            print("You can still use the interactive editor if files were created.")
            
            if Path(project_root).exists() and any(Path(project_root).iterdir()):
                use_editor = input("\n🎯 Use interactive editor anyway? (y/n): ").lower()
                if use_editor == 'y':
                    start_interactive_editing_session(project_root)


def standalone_editor_mode():
    """Standalone interactive editor mode"""
    print("🎯 Standalone Interactive Editor Mode")
    print("=" * 40)
    
    project_path = input("Enter project path to edit: ").strip()
    
    if not project_path:
        project_path = str(PROJECT_ROOT)
        print(f"Using default project path: {project_path}")
    
    if not Path(project_path).exists():
        print(f"❌ Path {project_path} does not exist!")
        return
    
    start_interactive_editing_session(project_path)


if __name__ == "__main__":
    print("🎯 AI Web Development Agent with Interactive Editing")
    print("=" * 50)
    print("1. Generate new project with error checking")
    print("2. Use standalone interactive editor")
    
    choice = input("\nSelect mode (1 or 2): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        standalone_editor_mode()
    else:
        print("❌ Invalid choice! Running main mode...")
        main()