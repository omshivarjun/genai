#!/usr/bin/env python3
"""
Demo script for GenAI App Builder
Generates multiple sample projects to showcase capabilities
"""

import os
import sys
import time
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from main import main as generate_project

def run_demo():
    """Run a demo generating multiple projects"""
    
    print("🚀 GenAI App Builder - Demo Mode")
    print("=" * 50)
    
    demo_prompts = [
        "Create a modern landing page for a tech startup with hero section, features, and contact form",
        "Build a music player interface with playlist, controls, and volume slider",
        "Design a dashboard for fitness tracking with charts, goals, and progress indicators",
        "Generate a recipe finder app with search, filters, and recipe cards",
        "Create a simple blog interface with post listing, article view, and comments section"
    ]
    
    print(f"Will generate {len(demo_prompts)} demo projects...")
    print()
    
    for i, prompt in enumerate(demo_prompts, 1):
        print(f"📝 Project {i}: {prompt}")
        print("-" * 60)
        
        # Simulate user input by temporarily replacing stdin
        import io
        sys.stdin = io.StringIO(prompt + "\n")
        
        try:
            generate_project()
            print(f"✅ Project {i} generated successfully!")
        except Exception as e:
            print(f"❌ Error generating project {i}: {e}")
        
        print()
        time.sleep(1)  # Small delay between generations
    
    # Restore original stdin
    sys.stdin = sys.__stdin__
    
    print("🎉 Demo completed!")
    print("\nGenerated projects can be found in the 'generated_projects' directory:")
    
    # List generated projects
    projects_dir = Path("generated_projects")
    if projects_dir.exists():
        for project_dir in sorted(projects_dir.iterdir()):
            if project_dir.is_dir():
                files = list(project_dir.glob("*.html"))
                if files:
                    print(f"  📁 {project_dir.name}/")
                    for file in sorted(project_dir.iterdir()):
                        if file.is_file():
                            print(f"    📄 {file.name}")

def interactive_demo():
    """Run an interactive demo where user can test specific project types"""
    
    print("🚀 GenAI App Builder - Interactive Demo")
    print("=" * 50)
    
    project_types = {
        "1": ("Landing Page", "Create a modern landing page for a tech company with hero section and call-to-action"),
        "2": ("Dashboard", "Build an analytics dashboard with charts, metrics, and data visualization"),
        "3": ("E-commerce", "Design a product showcase page with shopping cart and checkout form"),
        "4": ("Portfolio", "Create a personal portfolio website with projects gallery and about section"),
        "5": ("Game", "Generate a simple browser game like tic-tac-toe or memory card game"),
        "6": ("Utility", "Build a useful tool like unit converter, QR code generator, or password generator"),
        "7": ("Custom", "Enter your own project description")
    }
    
    print("Choose a project type to generate:")
    for key, (name, _) in project_types.items():
        print(f"  {key}. {name}")
    print()
    
    while True:
        choice = input("Enter your choice (1-7, or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            print("👋 Goodbye!")
            break
        
        if choice in project_types:
            name, prompt = project_types[choice]
            
            if choice == "7":  # Custom
                prompt = input("Enter your project description: ").strip()
                if not prompt:
                    print("❌ Please enter a valid description")
                    continue
            
            print(f"\n🎯 Generating {name}...")
            print(f"📝 Prompt: {prompt}")
            print("-" * 60)
            
            # Generate the project
            import io
            sys.stdin = io.StringIO(prompt + "\n")
            
            try:
                generate_project()
                print("✅ Project generated successfully!")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Restore stdin
            sys.stdin = sys.__stdin__
            
            print("\nWould you like to generate another project? (y/n)")
            again = input().strip().lower()
            if again not in ['y', 'yes']:
                print("👋 Thanks for trying GenAI App Builder!")
                break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        run_demo()