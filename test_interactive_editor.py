"""
Test Interactive Editor
This script demonstrates the interactive editing capabilities
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from agent.interactive_editor import start_interactive_editing_session
from agent.tools import PROJECT_ROOT


def create_test_files_with_errors():
    """Create test files with intentional errors for demonstration"""
    test_project = PROJECT_ROOT / "test_errors"
    test_project.mkdir(exist_ok=True)
    
    # HTML file with errors
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Page</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Test Page with Errors</h1>
        <p>This paragraph is not closed properly
        <div>Unclosed div
        <button onclick="testFunction()">Click Me</button>
        <div class="footer">
            <p>Footer content
        </div>
    </div>
</body>
</html>"""
    
    # CSS file with errors
    css_content = """body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;

.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #f5f5f5;
    padding: 20px;
}

h1 {
    color: #333;
    text-align: center;

.footer {
    margin-top: 20px;
    padding: 10px;
    background-color: #ddd;
    /* Missing closing brace below */"""
    
    # JavaScript file with errors
    js_content = """function testFunction() {
    console.log("Hello World";
    let message = "This is a test;
    
    // Unclosed function
    function anotherFunction() {
        let x = 10;
        let y = 20
        return x + y;
    
    // Missing closing brace for testFunction
    
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded');
    testFunction();
});"""
    
    # Write files
    (test_project / "index.html").write_text(html_content, encoding='utf-8')
    (test_project / "styles.css").write_text(css_content, encoding='utf-8')
    (test_project / "script.js").write_text(js_content, encoding='utf-8')
    
    print(f"✅ Created test files with errors in: {test_project}")
    return str(test_project)


def main():
    """Main function for testing interactive editor"""
    print("🧪 Interactive Editor Test")
    print("=" * 30)
    
    choice = input("1. Create test files with errors\n2. Edit existing project\nChoice (1 or 2): ")
    
    if choice == "1":
        project_path = create_test_files_with_errors()
        print(f"\n📁 Test project created at: {project_path}")
        print("This project contains intentional errors in HTML, CSS, and JavaScript files.")
        
        start_editor = input("\n🎯 Start interactive editor now? (y/n): ").lower()
        if start_editor == 'y':
            start_interactive_editing_session(project_path)
    
    elif choice == "2":
        project_path = input("Enter project path: ").strip()
        if Path(project_path).exists():
            start_interactive_editing_session(project_path)
        else:
            print(f"❌ Path {project_path} does not exist!")
    
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    main()