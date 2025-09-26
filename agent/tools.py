import pathlib
import subprocess
from typing import Tuple, Optional

from langchain_core.tools import tool
from agent.interactive_editor import InteractiveCodeEditor, start_interactive_editing_session

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
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


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
