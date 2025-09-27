#!/usr/bin/env python3
"""
Detailed Gemini Prompts for 5 Specific Applications
Each app has comprehensive requirements for beautiful UI and error-free logic
"""

from dataclasses import dataclass
from typing import Dict, Any
import os
from dotenv import load_dotenv
from agent.graph import agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Initialize Gemini for direct editing
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    max_retries=3
)

@dataclass
class AppSpec:
    name: str
    description: str
    prompt: str
    features: list
    ui_requirements: str
    logic_requirements: str

# ============================================================================
# 1. SIMPLE CALCULATOR
# ============================================================================
CALCULATOR_SPEC = AppSpec(
    name="calculator",
    description="Modern Calculator with Beautiful UI",
    prompt="""Create a modern, beautiful calculator application with the following specifications:

VISUAL DESIGN REQUIREMENTS:
- Sleek, modern interface with glassmorphism or neumorphism design
- Dark theme with vibrant accent colors (blues, purples, or greens)
- Grid layout for buttons with proper spacing and hover effects
- Large, clear display screen with proper font sizing
- Smooth animations for button presses and calculations
- Responsive design that works on desktop and mobile
- Modern typography (use Google Fonts like 'Roboto' or 'Inter')
- Box shadows, gradients, and rounded corners for visual appeal
- Color-coded buttons: operators (orange/blue), numbers (gray/white), equals (bright accent)

FUNCTIONALITY REQUIREMENTS:
- Basic arithmetic operations: +, -, *, /
- Clear (C) and All Clear (AC) functions
- Decimal point support with proper validation
- Keyboard support for all operations
- Error handling for division by zero
- Result history display (last 3 calculations)
- Proper order of operations
- Support for negative numbers
- Backspace functionality
- Visual feedback for button presses

TECHNICAL REQUIREMENTS:
- Semantic HTML5 structure with proper accessibility
- Modern CSS3 with Grid/Flexbox layout
- ES6+ JavaScript with proper error handling
- No deprecated methods or syntax
- Mobile-first responsive design
- Proper event handling and DOM manipulation
- Clean, readable code with comments

FILES TO GENERATE:
- index.html: Complete HTML structure
- style.css: Beautiful modern styling
- script.js: Full calculator logic with error handling""",
    
    features=[
        "Basic arithmetic operations (+, -, *, /)",
        "Clear and All Clear functions",
        "Decimal point support",
        "Keyboard input support",
        "Error handling",
        "Calculation history",
        "Visual feedback",
        "Responsive design"
    ],
    
    ui_requirements="Modern glassmorphism design with dark theme, gradient backgrounds, smooth animations, and color-coded buttons",
    logic_requirements="Error-free arithmetic with proper order of operations, input validation, and comprehensive error handling"
)

# ============================================================================
# 2. TODO APP
# ============================================================================
TODO_SPEC = AppSpec(
    name="todo",
    description="Modern Todo List Application",
    prompt="""Create a beautiful, feature-rich todo list application with the following specifications:

VISUAL DESIGN REQUIREMENTS:
- Clean, minimalist interface with subtle animations
- Light theme with option to toggle to dark mode
- Card-based design for each todo item
- Beautiful gradient header with app title
- Smooth slide-in/out animations for adding/removing tasks
- Progress indicator showing completion percentage
- Color-coded priority levels (high=red, medium=yellow, low=green)
- Modern input field with floating labels
- Completed tasks with strikethrough effect
- Empty state illustration when no tasks exist
- Modern icons for actions (add, edit, delete, complete)

FUNCTIONALITY REQUIREMENTS:
- Add new tasks with enter key or button click
- Mark tasks as complete/incomplete with visual feedback
- Edit existing tasks inline (double-click to edit)
- Delete tasks with confirmation dialog
- Filter tasks by status (all, active, completed)
- Sort tasks by priority or creation date
- Task counter showing active/completed counts
- Local storage to persist tasks between sessions
- Priority levels for tasks (high, medium, low)
- Due date support with visual indicators for overdue tasks
- Search functionality to find specific tasks
- Bulk operations (select all, delete completed)

TECHNICAL REQUIREMENTS:
- Semantic HTML5 with proper accessibility attributes
- Modern CSS3 with animations and transitions
- ES6+ JavaScript with classes and modern syntax
- Local storage for data persistence
- Proper form validation and error handling
- Mobile-first responsive design
- Progressive Web App features (optional)

FILES TO GENERATE:
- index.html: Complete HTML structure with accessibility
- style.css: Beautiful modern styling with animations
- script.js: Full todo app logic with local storage""",
    
    features=[
        "Add, edit, delete tasks",
        "Mark tasks complete/incomplete",
        "Priority levels and color coding",
        "Due date tracking",
        "Filter and sort options",
        "Search functionality",
        "Local storage persistence",
        "Bulk operations",
        "Progress tracking",
        "Dark/light theme toggle"
    ],
    
    ui_requirements="Clean minimalist design with card-based layout, smooth animations, and dark/light theme options",
    logic_requirements="Complete CRUD operations with local storage, input validation, and proper state management"
)

# ============================================================================
# 3. STUDENT GRADE CALCULATOR
# ============================================================================
GRADE_CALCULATOR_SPEC = AppSpec(
    name="grades",
    description="Student Grade Calculator with GPA Tracking",
    prompt="""Create a comprehensive student grade calculator application with the following specifications:

VISUAL DESIGN REQUIREMENTS:
- Professional academic interface with school-themed colors (blues, greens)
- Dashboard-style layout with multiple sections
- Cards for each subject/course with grade breakdown
- Visual charts/progress bars showing grade distributions
- Color-coded grades (A=green, B=blue, C=yellow, D=orange, F=red)
- Modern form inputs for adding grades and assignments
- Statistical summary section with GPA, average, etc.
- Print-friendly stylesheet for report generation
- Responsive design for mobile access
- Professional typography suitable for academic use

FUNCTIONALITY REQUIREMENTS:
- Add multiple subjects/courses with weights
- Input various assignment types (homework, quiz, exam, project)
- Calculate weighted averages for each subject
- Overall GPA calculation (4.0 scale)
- Letter grade conversion with customizable grade scale
- Grade point calculation for individual assignments
- Semester/term management (multiple semesters)
- Grade trend analysis (improvement/decline tracking)
- What-if scenarios (what grade needed for target GPA)
- Export grades to CSV or print report
- Target grade calculator (what's needed to achieve goal)
- Statistical analysis (mean, median, highest, lowest)

ADVANCED FEATURES:
- Multiple grading systems (percentage, points, letter grades)
- Custom grade scales (A=90-100, A=93-100, etc.)
- Credit hour tracking for accurate GPA
- Semester comparison and trends
- Goal setting and progress tracking
- Data import/export functionality

TECHNICAL REQUIREMENTS:
- Semantic HTML5 with form validation
- Modern CSS3 with professional styling
- ES6+ JavaScript with mathematical calculations
- Local storage for grade persistence
- Input validation and error handling
- Responsive design for all devices
- Accessible design with proper ARIA labels

FILES TO GENERATE:
- index.html: Complete grade calculator interface
- style.css: Professional academic styling
- script.js: Comprehensive grade calculation logic""",
    
    features=[
        "Multi-subject grade tracking",
        "Weighted average calculations",
        "GPA calculation (4.0 scale)",
        "Assignment type categorization",
        "Grade trend analysis",
        "What-if scenario calculator",
        "Custom grade scales",
        "Semester management",
        "Export and print functionality",
        "Statistical analysis"
    ],
    
    ui_requirements="Professional academic interface with dashboard layout, color-coded grades, and statistical visualizations",
    logic_requirements="Accurate mathematical calculations for weighted averages, GPA, and statistical analysis with proper validation"
)

# ============================================================================
# 4. SIMPLE QUIZ APP
# ============================================================================
QUIZ_SPEC = AppSpec(
    name="quiz",
    description="Interactive Quiz Application with Multiple Categories",
    prompt="""Create an engaging, interactive quiz application with the following specifications:

VISUAL DESIGN REQUIREMENTS:
- Gamified interface with vibrant colors and engaging animations
- Question card design with smooth transitions between questions
- Progress bar showing quiz completion
- Score display with celebratory animations for correct answers
- Timer display with visual countdown (if timed)
- Category selection screen with attractive icons
- Results screen with detailed score breakdown
- Confetti or celebration animations for high scores
- Modern button designs with hover effects
- Responsive design for mobile quiz-taking
- Dark/light theme toggle for better accessibility

FUNCTIONALITY REQUIREMENTS:
- Multiple quiz categories (General Knowledge, Science, History, Sports, etc.)
- Question types: Multiple choice, True/False, Fill-in-the-blank
- Randomized question order to prevent memorization
- Timer functionality (optional per quiz)
- Immediate feedback for answers (correct/incorrect)
- Score tracking with percentage and points
- Quiz completion summary with detailed results
- Retake functionality for improvement
- High score tracking and leaderboard
- Question explanation/feedback after each answer
- Skip question option (with penalty)
- Quiz statistics (time taken, accuracy rate)

QUIZ CONTENT:
Include at least 3 categories with 10 questions each:
- General Knowledge (mixed topics)
- Science (basic science facts)
- Geography (world capitals, countries)

ADVANCED FEATURES:
- Difficulty levels (Easy, Medium, Hard)
- Adaptive questioning (harder questions for better performers)
- Quiz creation mode (users can add their own questions)
- Social sharing of results
- Achievement badges for milestones
- Progress tracking over time

TECHNICAL REQUIREMENTS:
- Semantic HTML5 with proper accessibility
- Modern CSS3 with animations and transitions
- ES6+ JavaScript with object-oriented design
- Local storage for score persistence
- Proper state management for quiz flow
- Error handling and input validation
- Mobile-optimized touch interactions

FILES TO GENERATE:
- index.html: Complete quiz application interface
- style.css: Engaging gamified styling with animations
- script.js: Full quiz logic with question management""",
    
    features=[
        "Multiple quiz categories",
        "Various question types",
        "Timer functionality",
        "Score tracking and statistics",
        "High score leaderboard",
        "Immediate answer feedback",
        "Quiz result summaries",
        "Retake functionality",
        "Progress tracking",
        "Mobile-optimized interface"
    ],
    
    ui_requirements="Gamified interface with vibrant colors, smooth animations, and engaging visual feedback",
    logic_requirements="Robust quiz management system with proper scoring, timing, and state management"
)

# ============================================================================
# 5. AGE CALCULATOR
# ============================================================================
AGE_CALCULATOR_SPEC = AppSpec(
    name="age",
    description="Comprehensive Age Calculator with Life Statistics",
    prompt="""Create a comprehensive age calculator application with detailed life statistics and the following specifications:

VISUAL DESIGN REQUIREMENTS:
- Clean, modern interface with timeline-inspired design
- Gradient backgrounds with life-stage themed colors
- Card-based layout for different age calculations
- Visual timeline showing life milestones
- Animated counters for age statistics
- Beautiful date picker with calendar interface
- Progress bars for life expectancy (optional/fun)
- Celebration animations for birthdays
- Responsive design for all devices
- Modern typography with clear hierarchy
- Subtle animations and micro-interactions

FUNCTIONALITY REQUIREMENTS:
- Calculate exact age in years, months, days, hours, minutes, seconds
- Next birthday countdown with days remaining
- Age in different units (days lived, hours lived, etc.)
- Age comparison with famous people (optional fun feature)
- Historical events that happened when user was born
- Zodiac sign calculation and display
- Chinese zodiac year calculation
- Birth day of the week calculator
- Age difference calculator between two people
- Life statistics (days lived, approximate heartbeats, breaths taken)
- Retirement countdown calculator
- Age on other planets (Mars, Jupiter, etc.)

LIFE STATISTICS FEATURES:
- Calculate days lived and days until next birthday
- Estimate heartbeats (average 70 bpm)
- Estimate breaths taken (average 20/minute)
- Hours spent sleeping (assuming 8 hours/day)
- Time until major life milestones (18, 21, 30, 50, 65, etc.)
- Fun facts about the user's age
- World population when user was born
- Historical context for birth year

ADDITIONAL CALCULATORS:
- Age at specific date calculator
- Time between two dates
- Working days calculator
- Age retirement calculator
- Life expectancy comparison (fun, not medical advice)

TECHNICAL REQUIREMENTS:
- Semantic HTML5 with proper date handling
- Modern CSS3 with animations and transitions
- ES6+ JavaScript with Date object mastery
- Proper date validation and error handling
- Real-time updating for live age display
- Local storage for saving birth dates
- Accessible design with keyboard navigation
- Mobile-first responsive design

FILES TO GENERATE:
- index.html: Complete age calculator interface
- style.css: Modern timeline-inspired styling
- script.js: Comprehensive age calculation logic""",
    
    features=[
        "Exact age calculation in multiple units",
        "Next birthday countdown",
        "Life statistics and fun facts",
        "Zodiac sign calculation",
        "Age on other planets",
        "Historical context for birth year",
        "Age difference calculator",
        "Life milestone tracking",
        "Real-time age updates",
        "Multiple date calculators"
    ],
    
    ui_requirements="Timeline-inspired design with animated counters, gradient backgrounds, and celebration animations",
    logic_requirements="Precise date calculations with comprehensive life statistics and proper date validation"
)

# ============================================================================
# APP REGISTRY
# ============================================================================
APPS = {
    "calculator": CALCULATOR_SPEC,
    "todo": TODO_SPEC,
    "grades": GRADE_CALCULATOR_SPEC,
    "quiz": QUIZ_SPEC,
    "age": AGE_CALCULATOR_SPEC
}

def generate_app(app_name: str) -> Dict[str, Any]:
    """
    Generate an app based on its name using detailed prompts with satisfaction checking.
    
    Args:
        app_name: Name of the app to generate (calculator, todo, grades, quiz, age)
        
    Returns:
        Dict containing the generation result with satisfaction status
    """
    if app_name.lower() not in APPS:
        available_apps = ", ".join(APPS.keys())
        return {
            "error": f"App '{app_name}' not found. Available apps: {available_apps}",
            "success": False
        }
    
    app_spec = APPS[app_name.lower()]
    
    print(f"🚀 Generating {app_spec.description}")
    print("=" * 60)
    print(f"📝 Features: {', '.join(app_spec.features)}")
    print(f"🎨 UI Style: {app_spec.ui_requirements}")
    print(f"⚙️ Logic: {app_spec.logic_requirements}")
    print("=" * 60)
    
    try:
        # Generate the application using the comprehensive prompt
        result = agent.invoke({
            "user_prompt": app_spec.prompt,
            "use_auto_debug": True  # Enable auto-debugging for error-free output
        }, {"recursion_limit": 50})
        
        print(f"\n✅ {app_spec.description} generated successfully!")
        
        # Check satisfaction and provide editing option
        satisfaction_result = check_satisfaction_and_edit(app_spec, result)
        
        return {
            "success": True,
            "app_name": app_spec.name,
            "description": app_spec.description,
            "result": result,
            "features": app_spec.features,
            "status": result.get("status", "COMPLETED"),
            "satisfied": satisfaction_result.get("satisfied", False),
            "edit_count": satisfaction_result.get("edit_count", 0)
        }
        
    except Exception as e:
        print(f"❌ Error generating {app_spec.description}: {e}")
        return {
            "success": False,
            "error": str(e),
            "app_name": app_spec.name
        }

def check_satisfaction_and_edit(app_spec, generation_result) -> Dict[str, Any]:
    """Check user satisfaction and provide Gemini-powered editing options."""
    print(f"\n{'='*60}")
    print(f"🎯 {app_spec.description} Generation Complete!")
    print(f"{'='*60}")
    
    # Show generated files location
    project_path = None
    if os.path.exists("generated_projects"):
        projects = [d for d in os.listdir("generated_projects") 
                   if os.path.isdir(os.path.join("generated_projects", d))]
        if projects:
            latest_project = max(projects)
            project_path = os.path.join("generated_projects", latest_project)
            files = os.listdir(project_path)
            
            print(f"\n📁 Generated in: {project_path}")
            print(f"📄 Files: {', '.join(files)}")
            print(f"\n🌐 Open {os.path.join(project_path, 'index.html')} in your browser!")
    
    edit_count = 0
    
    # Satisfaction checking loop
    while True:
        print(f"\n{'='*40}")
        print("🤔 SATISFACTION CHECK")
        print(f"{'='*40}")
        
        try:
            satisfied = input("\n😊 Are you satisfied with the generated app? (y/n): ").strip().lower()
            
            if satisfied in ['y', 'yes']:
                print(f"\n🎉 Excellent! {app_spec.description} is ready to use!")
                print(f"✅ SATISFIED - Generation completed successfully!")
                return {"satisfied": True, "edit_count": edit_count}
            
            elif satisfied in ['n', 'no']:
                print(f"\n🔧 Let's improve the {app_spec.description} using Gemini!")
                
                # Get specific feedback
                feedback = input("\n💬 What would you like me to change or improve? (Be specific): ").strip()
                
                if not feedback:
                    print("⚠️ No feedback provided. Please try again.")
                    continue
                
                # Apply Gemini edit
                print(f"\n🤖 Using Gemini to apply your changes...")
                if project_path:
                    edit_result = apply_gemini_edit_to_project(project_path, feedback, app_spec)
                    
                    if edit_result.get("success"):
                        print(f"✅ Changes applied successfully!")
                        print(f"🔄 Please check the updated files and let me know if you're satisfied.")
                        edit_count += 1
                    else:
                        print(f"❌ Edit failed: {edit_result.get('error', 'Unknown error')}")
                else:
                    print("❌ Project directory not found. Cannot apply edits.")
                
            else:
                print("⚠️ Please enter 'y' for yes or 'n' for no.")
                
        except KeyboardInterrupt:
            print(f"\n\n⛔ Operation cancelled by user.")
            return {"satisfied": False, "edit_count": edit_count, "cancelled": True}
        except EOFError:
            print(f"\n⚠️ Input ended. Assuming satisfied.")
            return {"satisfied": True, "edit_count": edit_count}

def apply_gemini_edit_to_project(project_path: str, feedback: str, app_spec) -> Dict[str, Any]:
    """Apply user feedback using Gemini to edit the generated project files."""
    if not project_path or not os.path.exists(project_path):
        return {"success": False, "error": "Project directory not found"}
    
    try:
        # Read current files
        current_files = {}
        for filename in os.listdir(project_path):
            file_path = os.path.join(project_path, filename)
            if os.path.isfile(file_path) and filename.endswith(('.html', '.css', '.js')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        current_files[filename] = f.read()
                except Exception as e:
                    print(f"⚠️ Could not read {filename}: {e}")
        
        if not current_files:
            return {"success": False, "error": "No editable files found"}
        
        # Create edit prompt for Gemini
        files_content = "\n\n".join([f"=== {filename} ===\n{content}" 
                                    for filename, content in current_files.items()])
        
        edit_prompt = f"""
You are an expert web developer. I have a {app_spec.description} that needs improvements based on user feedback.

CURRENT PROJECT FILES:
{files_content}

USER FEEDBACK: {feedback}

TASK: Modify the existing files based on the user's feedback. Requirements:
1. Keep all existing functionality that works correctly
2. Apply the requested changes/improvements precisely
3. Maintain beautiful, modern, responsive design
4. Ensure error-free, clean code
5. Preserve the same file structure
6. Make sure all features from the original app specification still work

Please provide the complete updated files with the requested changes applied.

Return ONLY the updated files in this exact format:
=== filename.ext ===
[complete updated file content]

=== filename.ext ===
[complete updated file content]
"""
        
        # Get Gemini response
        response = llm.invoke(edit_prompt)
        response_text = str(response.content) if hasattr(response, 'content') else str(response)
        
        # Parse updated files from response
        updated_files = parse_gemini_response(response_text)
        
        if not updated_files:
            return {"success": False, "error": "Could not parse Gemini response"}
        
        # Save updated files
        saved_files = []
        for filename, content in updated_files.items():
            file_path = os.path.join(project_path, filename)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(filename)
                print(f"📝 Updated: {filename}")
            except Exception as e:
                print(f"❌ Failed to save {filename}: {e}")
        
        return {"success": True, "updated_files": saved_files}
        
    except Exception as e:
        return {"success": False, "error": f"Gemini edit failed: {str(e)}"}

def parse_gemini_response(response_text: str) -> Dict[str, str]:
    """Parse Gemini response to extract updated file contents."""
    files = {}
    current_file = None
    current_content = []
    
    lines = response_text.split('\n')
    
    for line in lines:
        if line.startswith('=== ') and line.endswith(' ==='):
            # Save previous file if exists
            if current_file and current_content:
                files[current_file] = '\n'.join(current_content).strip()
            
            # Start new file
            current_file = line[4:-4].strip()
            current_content = []
        else:
            if current_file:
                current_content.append(line)
    
    # Save last file
    if current_file and current_content:
        files[current_file] = '\n'.join(current_content).strip()
    
    return files

def list_available_apps():
    """List all available apps with their descriptions."""
    print("📱 Available Applications")
    print("=" * 50)
    
    for name, spec in APPS.items():
        print(f"\n🎯 {name.upper()}")
        print(f"   Description: {spec.description}")
        print(f"   Features: {len(spec.features)} main features")
        print(f"   Usage: python app_prompts.py {name}")
    
    print(f"\n💡 Total applications available: {len(APPS)}")

def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("🚀 GenAI App Builder - Detailed Prompts System")
        print("=" * 50)
        print("Usage: python app_prompts.py <app_name>")
        print("       python app_prompts.py --list")
        print()
        list_available_apps()
        return
    
    if sys.argv[1] == "--list":
        list_available_apps()
        return
    
    app_name = sys.argv[1].lower()
    
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google Gemini API key in the .env file")
        return
    
    # Generate the requested app
    result = generate_app(app_name)
    
    if result["success"]:
        print(f"\n🎉 {result['description']} completed!")
        print(f"📊 Status: {result.get('status', 'COMPLETED')}")
        
        # Show satisfaction status
        if result.get("satisfied"):
            print(f"😊 User Satisfaction: ✅ SATISFIED")
        else:
            print(f"😔 User Satisfaction: ❌ NOT SATISFIED")
        
        if result.get("edit_count", 0) > 0:
            print(f"🔧 Gemini Edits Applied: {result['edit_count']}")
        
        # Show generated files location
        if os.path.exists("generated_projects"):
            projects = [d for d in os.listdir("generated_projects") 
                       if os.path.isdir(os.path.join("generated_projects", d))]
            if projects:
                latest_project = max(projects)
                project_path = os.path.join("generated_projects", latest_project)
                files = os.listdir(project_path)
                
                print(f"\n📁 Generated in: {project_path}")
                print(f"📄 Files: {', '.join(files)}")
                print(f"\n🌐 Open {os.path.join(project_path, 'index.html')} in your browser!")
                
        print(f"\n{'='*50}")
        if result.get("satisfied"):
            print("🎊 PROJECT COMPLETED SUCCESSFULLY - USER SATISFIED! 🎊")
        else:
            print("⚠️ PROJECT COMPLETED - USER NOT FULLY SATISFIED")
        print(f"{'='*50}")
        
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()