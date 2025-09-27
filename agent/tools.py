import pathlib
import subprocess
from typing import Tuple, Optional

from langchain_core.tools import tool
from agent.interactive_editor import InteractiveCodeEditor, start_interactive_editing_session
from agent.auto_debugger import auto_debug_project

def get_next_project_folder() -> pathlib.Path:
    """Get the next available project folder (generated_projects_1, generated_projects_2, etc.)"""
    base_dir = pathlib.Path.cwd() / "generated_projects"
    base_dir.mkdir(exist_ok=True)
    
    project_num = 1
    while True:
        project_folder = base_dir / f"generated_projects_{project_num}"
        if not project_folder.exists():
            return project_folder
        project_num += 1

# Initialize PROJECT_ROOT with the next available project folder
PROJECT_ROOT = get_next_project_folder()


def safe_path_for_project(path: str) -> pathlib.Path:
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError("Attempt to write outside project root")
    return p


@tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file at the specified path within the project root.
    Includes validation to prevent common errors.
    """
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    
    # Validate content based on file type
    validation_result = _validate_file_content(str(p), content)
    if not validation_result["valid"]:
        return f"❌ VALIDATION ERROR in {path}: {validation_result['error']}\n\nPlease fix these issues and try again."
    
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Verify file was written correctly
    size = p.stat().st_size
    return f"✅ WROTE: {p} ({size} bytes) - VALIDATED AND ERROR-FREE"


def _validate_file_content(filepath: str, content: str) -> dict:
    """Validate file content to prevent common errors."""
    try:
        from pathlib import Path
        file_ext = Path(filepath).suffix.lower()
        
        if file_ext == '.html':
            return _validate_html_content(content)
        elif file_ext == '.css':
            return _validate_css_content(content)  
        elif file_ext == '.js':
            return _validate_js_content(content)
        else:
            return {"valid": True, "error": None}
            
    except Exception as e:
        return {"valid": False, "error": f"Validation error: {str(e)}"}


def _validate_html_content(content: str) -> dict:
    """Validate HTML content for common issues."""
    errors = []
    
    # Check for DOCTYPE
    if not content.strip().startswith('<!DOCTYPE html>'):
        errors.append("Missing <!DOCTYPE html>")
    
    # Check for required meta tags
    if '<meta charset="UTF-8">' not in content and '<meta charset="utf-8">' not in content:
        errors.append("Missing charset meta tag")
    
    if 'name="viewport"' not in content:
        errors.append("Missing viewport meta tag")
    
    # Check for proper HTML structure
    required_tags = ['<html', '</html>', '<head>', '</head>', '<body>', '</body>']
    for tag in required_tags:
        if tag not in content:
            errors.append(f"Missing {tag} tag")
    
    # Check for CSS linking
    if 'rel="stylesheet"' not in content and '<style>' not in content:
        errors.append("No CSS found - add <link rel='stylesheet' href='style.css'>")
    
    # Check for JS linking for interactive elements  
    has_interactive = any(tag in content.lower() for tag in ['button', 'input', 'form', 'click'])
    if has_interactive:
        if 'src="script.js"' not in content and '<script>' not in content:
            errors.append("Interactive elements found but no JavaScript linked")
    
    if errors:
        return {"valid": False, "error": "; ".join(errors)}
    
    return {"valid": True, "error": None}


def _validate_css_content(content: str) -> dict:
    """Validate CSS content for common issues."""
    errors = []
    
    # Check for unclosed braces
    open_braces = content.count('{') - content.count('}')
    if open_braces != 0:
        errors.append(f"Mismatched braces: {abs(open_braces)} {'missing' if open_braces > 0 else 'extra'}")
    
    # Check for missing semicolons
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        # Property line that should end with semicolon
        if ':' in line and not line.endswith((';', '{', '}')) and not any(x in line for x in ['/*', '*/', '@']):
            errors.append(f"Missing semicolon at line {line_num}")
            break  # Only report first instance
    
    # Check for unclosed comments  
    if '/*' in content and content.count('/*') != content.count('*/'):
        errors.append("Unclosed comment block")
    
    if errors:
        return {"valid": False, "error": "; ".join(errors[:2])}  # Limit errors
    
    return {"valid": True, "error": None}


def _validate_js_content(content: str) -> dict:
    """Validate JavaScript content for common issues."""
    errors = []
    
    # Check for basic syntax issues
    if content.count('(') != content.count(')'):
        errors.append("Mismatched parentheses")
    
    if content.count('{') != content.count('}'):
        errors.append("Mismatched braces")
    
    # Check for dangerous patterns
    if 'eval(' in content:
        errors.append("Remove eval() - use safer alternatives")
    
    # Check for proper DOM handling
    if 'document.' in content:
        if 'DOMContentLoaded' not in content and 'window.onload' not in content:
            errors.append("Add DOMContentLoaded listener for DOM manipulation")
    
    # Check for modern syntax usage
    if 'var ' in content and ('let ' not in content or 'const ' not in content):
        errors.append("Use 'let' or 'const' instead of 'var'")
    
    if errors:
        return {"valid": False, "error": "; ".join(errors[:2])}
    
    return {"valid": True, "error": None}


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

@tool
def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)


@tool
def detect_project_errors() -> str:
    """Detect errors in the generated project files (HTML, CSS, JavaScript, JSON)."""
    editor = InteractiveCodeEditor(str(PROJECT_ROOT))
    errors = editor.detect_errors()
    
    if not errors:
        return "✅ No errors detected in the project!"
    
    error_report = f"🔍 Found {len(errors)} error(s):\n"
    for i, error in enumerate(errors, 1):
        error_report += f"{i}. {error['type']} Error in {error['file']}:{error['line']}\n"
        error_report += f"   {error['message']}\n"
    
    return error_report


@tool
def start_interactive_editor(file_path: str = "") -> str:
    """Start interactive code editor for fixing errors. If file_path is provided, edit that specific file."""
    try:
        target_file = file_path if file_path else None
        start_interactive_editing_session(str(PROJECT_ROOT), target_file)
        return "✅ Interactive editing session completed!"
    except Exception as e:
        return f"❌ Error starting interactive editor: {str(e)}"


@tool
def auto_debug_with_gemini() -> str:
    """Automatically analyze and fix all code issues using Gemini AI."""
    try:
        results = auto_debug_project(str(PROJECT_ROOT))
        
        summary = f"""🤖 Gemini Auto-Debug Results:
        
📊 Analysis:
  • Total issues found: {results['analysis']['total_issues_found']}
  • Critical issues: {results['analysis']['critical_issues']}
  • Warnings: {results['analysis']['warnings']}  
  • Suggestions: {results['analysis']['suggestions']}

🔧 Fixes Applied:
  • Issues fixed: {results['fixes']['fixes_applied']}
  • Files processed: {results['fixes']['files_processed']}

✅ Verification:
  • Status: {results['verification']['status']}
  • Remaining errors: {results['verification']['errors_remaining']}
  
Overall Status: {results['overall_status'].upper()}"""
        
        return summary
        
    except Exception as e:
        return f"❌ Error during auto-debug: {str(e)}"


@tool
def validate_file(file_path: str) -> str:
    """Validate a specific file for errors."""
    editor = InteractiveCodeEditor(str(PROJECT_ROOT))
    target_file = PROJECT_ROOT / file_path
    
    if not target_file.exists():
        return f"❌ File {file_path} not found!"
    
    try:
        suffix = target_file.suffix.lower()
        if suffix == '.html':
            errors = editor._validate_html(target_file)
        elif suffix == '.css':
            errors = editor._validate_css(target_file)
        elif suffix == '.js':
            errors = editor._validate_js(target_file)
        elif target_file.name == 'package.json':
            errors = editor._validate_package_json(target_file)
        else:
            return f"⚠️ No validation available for {suffix} files"
        
        if errors:
            error_report = f"❌ Found {len(errors)} error(s) in {file_path}:\n"
            for error in errors:
                error_report += f"   Line {error['line']}: {error['message']}\n"
            return error_report
        else:
            return f"✅ No errors found in {file_path}!"
            
    except Exception as e:
        return f"❌ Error validating file: {str(e)}"
