#!/usr/bin/env python3
"""
Quick Demo Script - Shows how to run the GenAI App Builder
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def show_running_instructions():
    print("🚀 GenAI App Builder - How to Run & Use Prompts")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("✅ API Key: Configured")
        print(f"   Key: {api_key[:20]}...{api_key[-5:]}")
    else:
        print("❌ API Key: Not Found")
        print("   Please set GOOGLE_API_KEY in .env file")
        return False
    
    print("\n🎯 READY TO RUN! Choose your method:")
    print("-" * 40)
    
    print("\n📱 Method 1: Pre-built Apps (RECOMMENDED)")
    print("   🧮 Calculator:     python app_prompts.py calculator")
    print("   ✅ Todo List:      python app_prompts.py todo") 
    print("   📊 Grade Calc:     python app_prompts.py grades")
    print("   🧠 Quiz App:       python app_prompts.py quiz")
    print("   🎂 Age Calc:       python app_prompts.py age")
    
    print("\n🖱️ Method 2: One-Click (Batch Files)")
    print("   Just double-click or run:")
    print("   • calculator.bat")
    print("   • todo.bat")  
    print("   • grades.bat")
    print("   • quiz.bat")
    print("   • age.bat")
    
    print("\n✍️ Method 3: Custom Prompts")
    print("   python main.py")
    print("   Then enter your custom prompt when asked.")
    
    print("\n🎨 Example Custom Prompts:")
    print("-" * 30)
    
    prompts = [
        ("🎮 Simple Game", "Create a tic-tac-toe game with beautiful UI, animations, and AI opponent"),
        ("📝 Note App", "Create a note-taking app with rich text editing, categories, and search"),
        ("🌤️ Weather App", "Create a weather dashboard with current conditions and forecasts"),
        ("💰 Expense Tracker", "Create an expense tracking app with categories and charts"),
        ("📚 Book Library", "Create a personal book library with ratings and reading progress")
    ]
    
    for title, prompt in prompts:
        print(f"\n   {title}:")
        print(f"   \"{prompt}\"")
    
    print(f"\n💡 Pro Tips:")
    print("   • Always end prompts with: 'Generate complete HTML, CSS, and JavaScript files'")
    print("   • Ask for responsive design and modern UI")
    print("   • Include specific features you want")
    print("   • Mention error handling and local storage if needed")
    
    print(f"\n🔄 New Feature: Satisfaction Checking")
    print("   • After generation, system asks if you're satisfied")
    print("   • If not, describe what to improve")
    print("   • Gemini AI will edit the files based on your feedback")
    print("   • Keeps improving until you're happy!")
    
    print(f"\n🎊 Ready to create amazing apps? Pick a method above!")
    return True

def show_quick_demo():
    print(f"\n🚀 QUICK DEMO - Let's generate a calculator!")
    print("Run this command:")
    print("   python app_prompts.py calculator")
    print()
    print("What will happen:")
    print("1. 🤖 AI generates a beautiful calculator app")
    print("2. 📁 Files saved to generated_projects/calculator_[timestamp]/")
    print("3. 🤔 System asks: 'Are you satisfied? (y/n)'")
    print("4. 😊 If yes → Done!")
    print("5. 🔧 If no → Describe improvements → Gemini edits → Repeat")
    print("6. ✅ Final: 'SATISFIED - Generation completed successfully!'")

if __name__ == "__main__":
    if show_running_instructions():
        show_quick_demo()
        print(f"\n⚡ NEXT STEP: Choose a method above and try it!")
    else:
        print(f"\n❌ Setup required: Please configure your API key first.")