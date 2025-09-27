# 🚀 How to Run GenAI App Builder - Complete Guide

## 📋 Prerequisites & Setup

### 1. Check Your Environment
```bash
# Make sure you're in the project directory
cd C:\app-builder

# Check if Python is working
python --version
# Should show Python 3.10+
```

### 2. Get Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy the API key (starts with `AIza...`)

### 3. Configure Environment
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file and add your API key:
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or if using UV
uv sync
```

## 🎯 How to Run the Project

### Method 1: Pre-built Apps with Satisfaction Checking (RECOMMENDED)
```bash
# Generate specific apps with detailed prompts and satisfaction checking
python app_prompts.py calculator
python app_prompts.py todo
python app_prompts.py grades
python app_prompts.py quiz
python app_prompts.py age
```

### Method 2: One-Click Generation (Windows)
```bash
# Just double-click or run these batch files
calculator.bat
todo.bat
grades.bat
quiz.bat
age.bat
```

### Method 3: Custom Prompts (Advanced)
```bash
# Run main script for custom prompts
python main.py

# When prompted, enter your custom prompt
```

## 💬 Example Prompts for Custom Generation

### 🧮 Calculator App Prompt
```
Create a modern scientific calculator web app with the following features:
- Basic arithmetic operations (+, -, ×, ÷)
- Scientific functions (sin, cos, tan, log, sqrt, power)
- Memory functions (M+, M-, MR, MC)
- Clear and backspace functionality
- Calculation history display
- Beautiful modern UI with gradient backgrounds
- Responsive design for mobile and desktop
- Smooth button animations and hover effects
- Error handling for invalid operations
- Keyboard support for number input
Generate complete HTML, CSS, and JavaScript files.
```

### ✅ Todo List App Prompt
```
Create a modern todo list web application with these features:
- Add new tasks with descriptions
- Mark tasks as complete/incomplete
- Delete tasks with confirmation
- Edit existing tasks inline
- Priority levels (High, Medium, Low) with color coding
- Task categories or tags
- Filter tasks by status (All, Active, Completed)
- Local storage to persist data
- Beautiful modern UI with cards and animations
- Responsive design
- Drag and drop to reorder tasks
- Task counter and progress bar
Generate complete HTML, CSS, and JavaScript files.
```

### 📊 Grade Calculator Prompt
```
Create a student grade calculator web app with:
- Add multiple courses with names and credit hours
- Input grades for each course (A+, A, B+, B, C+, C, D, F)
- Automatic GPA calculation (4.0 scale)
- Current semester and cumulative GPA
- Grade point breakdown and statistics
- Beautiful charts showing grade distribution
- Export grades as PDF or text
- Local storage for data persistence
- Modern, clean UI design
- Responsive layout for all devices
- Input validation and error handling
Generate complete HTML, CSS, and JavaScript files.
```

### 🧠 Quiz App Prompt
```
Create an interactive quiz web application featuring:
- Multiple choice questions with 4 options each
- Timer functionality for each question
- Score calculation and tracking
- Progress bar showing quiz completion
- Results page with detailed breakdown
- Ability to restart quiz
- Different quiz categories (General, Science, History)
- Beautiful modern UI with smooth transitions
- Responsive design for mobile and desktop
- Sound effects for correct/incorrect answers
- Confetti animation for high scores
- Local storage for high scores
Generate complete HTML, CSS, and JavaScript files.
```

### 🎂 Age Calculator Prompt
```
Create a comprehensive age calculator web app with:
- Calculate exact age from birth date
- Show age in years, months, days, hours, minutes
- Days until next birthday countdown
- Total days lived counter
- Zodiac sign determination
- Chinese zodiac year
- Life milestones calculator
- Age comparison tool
- Beautiful modern UI with animations
- Responsive design
- Date picker for easy input
- Share results functionality
- Leap year handling
Generate complete HTML, CSS, and JavaScript files.
```

### 🎮 Game App Prompts
```
Create a simple puzzle game web app:
- 2048 sliding number game
- Touch/swipe support for mobile
- Score tracking and high scores
- Smooth animations and transitions
- Game over detection and restart
- Beautiful modern UI design
- Responsive layout
- Local storage for high scores
Generate complete HTML, CSS, and JavaScript files.
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. API Key Not Found
```bash
# Error: GOOGLE_API_KEY not found
# Solution: Check your .env file
notepad .env
# Add: GOOGLE_API_KEY=your_actual_key_here
```

#### 2. Module Not Found
```bash
# Error: ModuleNotFoundError
# Solution: Install dependencies
pip install -r requirements.txt
```

#### 3. Permission Denied (Batch Files)
```bash
# Error: batch file won't run
# Solution: Run from PowerShell
powershell -ExecutionPolicy Bypass -File calculator.bat
```

#### 4. No Generated Files
```bash
# Check if generated_projects directory exists
ls generated_projects
# If empty, try running again with a simpler prompt
```

## 🎯 Best Practices for Prompts

### ✅ Good Prompt Structure
```
1. Start with: "Create a [type] web app..."
2. List specific features with bullet points
3. Mention UI requirements (modern, responsive, beautiful)
4. Include technical requirements (local storage, error handling)
5. End with: "Generate complete HTML, CSS, and JavaScript files"
```

### ❌ Avoid These in Prompts
- Vague descriptions like "make it nice"
- Missing file format requests
- No UI/UX specifications
- Overly complex features for a single app
- No mention of responsiveness

### 🌟 Pro Tips
- Be specific about colors, themes, animations
- Mention mobile responsiveness
- Include error handling requirements
- Ask for local storage if data persistence needed
- Request keyboard shortcuts for better UX

## 🚀 Quick Start Commands

```bash
# 1. Setup (one-time)
copy .env.example .env
# Edit .env with your API key
pip install -r requirements.txt

# 2. Generate apps (with satisfaction checking)
python app_prompts.py calculator

# 3. Or use batch files
calculator.bat

# 4. Check generated files
ls generated_projects
```

## 🎊 What Happens When You Run

1. **AI Generation**: Multi-agent system creates your app
2. **File Creation**: HTML, CSS, JS files saved to `generated_projects/`
3. **Satisfaction Check**: System asks if you're satisfied
4. **Gemini Editing**: If not satisfied, describe improvements
5. **Iterative Loop**: Keeps improving until you're happy
6. **Final Result**: Complete web app ready to use

## 📁 Output Structure
```
generated_projects/
└── your_app_20250927_143052/
    ├── index.html      # Main app page
    ├── styles.css      # Styling and animations
    └── script.js       # App functionality
```

**🌟 Ready to create amazing apps with AI? Just pick a method and start building!** 🚀