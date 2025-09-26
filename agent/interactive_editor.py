"""
Interactive Code Editor for Command Line
Allows real-time editing of generated code when errors are detected
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re
import json


class InteractiveCodeEditor:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.current_file = None
        self.current_content = []
        self.errors = []
        
    def detect_errors(self) -> List[Dict[str, str]]:
        """Detect errors in the generated project"""
        errors = []
        
        # Check for HTML files and validate them
        html_files = list(self.project_root.glob("**/*.html"))
        for html_file in html_files:
            errors.extend(self._validate_html(html_file))
        
        # Check for CSS files and validate them
        css_files = list(self.project_root.glob("**/*.css"))
        for css_file in css_files:
            errors.extend(self._validate_css(css_file))
        
        # Check for JS files and validate them
        js_files = list(self.project_root.glob("**/*.js"))
        for js_file in js_files:
            errors.extend(self._validate_js(js_file))
            
        # Check for package.json and dependencies
        package_json = self.project_root / "package.json"
        if package_json.exists():
            errors.extend(self._validate_package_json(package_json))
        
        self.errors = errors
        return errors
    
    def _validate_html(self, html_file: Path) -> List[Dict[str, str]]:
        """Validate HTML file for basic syntax errors"""
        errors = []
        try:
            content = html_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Basic HTML validation
            open_tags = []
            for i, line in enumerate(lines, 1):
                # Find opening tags
                opening_tags = re.findall(r'<(\w+)[^>]*(?<!/)>', line)
                for tag in opening_tags:
                    if tag.lower() not in ['br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']:
                        open_tags.append((tag, i))
                
                # Find closing tags
                closing_tags = re.findall(r'</(\w+)>', line)
                for tag in closing_tags:
                    if open_tags and open_tags[-1][0].lower() == tag.lower():
                        open_tags.pop()
                    else:
                        errors.append({
                            'file': str(html_file.relative_to(self.project_root)),
                            'line': i,
                            'type': 'HTML',
                            'message': f'Unexpected closing tag: </{tag}>'
                        })
            
            # Check for unclosed tags
            for tag, line_num in open_tags:
                errors.append({
                    'file': str(html_file.relative_to(self.project_root)),
                    'line': line_num,
                    'type': 'HTML',
                    'message': f'Unclosed tag: <{tag}>'
                })
                
        except Exception as e:
            errors.append({
                'file': str(html_file.relative_to(self.project_root)),
                'line': 1,
                'type': 'HTML',
                'message': f'File error: {str(e)}'
            })
        
        return errors
    
    def _validate_css(self, css_file: Path) -> List[Dict[str, str]]:
        """Validate CSS file for basic syntax errors"""
        errors = []
        try:
            content = css_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            brace_count = 0
            for i, line in enumerate(lines, 1):
                brace_count += line.count('{')
                brace_count -= line.count('}')
                
                if brace_count < 0:
                    errors.append({
                        'file': str(css_file.relative_to(self.project_root)),
                        'line': i,
                        'type': 'CSS',
                        'message': 'Unexpected closing brace }'
                    })
            
            if brace_count > 0:
                errors.append({
                    'file': str(css_file.relative_to(self.project_root)),
                    'line': len(lines),
                    'type': 'CSS',
                    'message': f'{brace_count} unclosed braces'
                })
                
        except Exception as e:
            errors.append({
                'file': str(css_file.relative_to(self.project_root)),
                'line': 1,
                'type': 'CSS',
                'message': f'File error: {str(e)}'
            })
        
        return errors
    
    def _validate_js(self, js_file: Path) -> List[Dict[str, str]]:
        """Validate JavaScript file using Node.js syntax check"""
        errors = []
        try:
            content = js_file.read_text(encoding='utf-8')
            
            # Create a temporary file for validation
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # Try to parse JS with Node.js
                result = subprocess.run(
                    ['node', '-c', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    error_lines = result.stderr.split('\n')
                    for error_line in error_lines:
                        if error_line.strip():
                            # Parse error line to extract line number if possible
                            line_match = re.search(r':(\d+):', error_line)
                            line_num = int(line_match.group(1)) if line_match else 1
                            
                            errors.append({
                                'file': str(js_file.relative_to(self.project_root)),
                                'line': line_num,
                                'type': 'JavaScript',
                                'message': error_line.strip()
                            })
                            
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # If Node.js is not available, do basic syntax checks
                lines = content.split('\n')
                paren_count = 0
                brace_count = 0
                bracket_count = 0
                
                for i, line in enumerate(lines, 1):
                    paren_count += line.count('(') - line.count(')')
                    brace_count += line.count('{') - line.count('}')
                    bracket_count += line.count('[') - line.count(']')
                    
                    if paren_count < 0:
                        errors.append({
                            'file': str(js_file.relative_to(self.project_root)),
                            'line': i,
                            'type': 'JavaScript',
                            'message': 'Unexpected closing parenthesis )'
                        })
                    if brace_count < 0:
                        errors.append({
                            'file': str(js_file.relative_to(self.project_root)),
                            'line': i,
                            'type': 'JavaScript',
                            'message': 'Unexpected closing brace }'
                        })
                    if bracket_count < 0:
                        errors.append({
                            'file': str(js_file.relative_to(self.project_root)),
                            'line': i,
                            'type': 'JavaScript',
                            'message': 'Unexpected closing bracket ]'
                        })
            finally:
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
        except Exception as e:
            errors.append({
                'file': str(js_file.relative_to(self.project_root)),
                'line': 1,
                'type': 'JavaScript',
                'message': f'File error: {str(e)}'
            })
        
        return errors
    
    def _validate_package_json(self, package_file: Path) -> List[Dict[str, str]]:
        """Validate package.json file"""
        errors = []
        try:
            content = package_file.read_text(encoding='utf-8')
            json.loads(content)  # This will raise an exception if invalid JSON
        except json.JSONDecodeError as e:
            errors.append({
                'file': str(package_file.relative_to(self.project_root)),
                'line': e.lineno if hasattr(e, 'lineno') else 1,
                'type': 'JSON',
                'message': f'Invalid JSON: {str(e)}'
            })
        except Exception as e:
            errors.append({
                'file': str(package_file.relative_to(self.project_root)),
                'line': 1,
                'type': 'JSON',
                'message': f'File error: {str(e)}'
            })
        
        return errors
    
    def show_errors(self):
        """Display all detected errors"""
        if not self.errors:
            print("✅ No errors detected!")
            return
        
        print(f"\n🔍 Found {len(self.errors)} error(s):")
        print("=" * 60)
        
        for i, error in enumerate(self.errors, 1):
            print(f"\n{i}. {error['type']} Error in {error['file']}:{error['line']}")
            print(f"   {error['message']}")
        
        print("=" * 60)
    
    def start_interactive_editor(self, file_path: Optional[str] = None):
        """Start the interactive editor"""
        if not self.errors and not file_path:
            print("✅ No errors found! Nothing to edit.")
            return
        
        if file_path:
            self.load_file(file_path)
        else:
            # Let user choose which file to edit
            files_with_errors = list(set([error['file'] for error in self.errors]))
            
            if len(files_with_errors) == 1:
                self.load_file(files_with_errors[0])
            else:
                print("\nSelect file to edit:")
                for i, file in enumerate(files_with_errors, 1):
                    error_count = len([e for e in self.errors if e['file'] == file])
                    print(f"{i}. {file} ({error_count} errors)")
                
                try:
                    choice = int(input("\nEnter file number: ")) - 1
                    if 0 <= choice < len(files_with_errors):
                        self.load_file(files_with_errors[choice])
                    else:
                        print("Invalid choice!")
                        return
                except ValueError:
                    print("Invalid input!")
                    return
        
        self.editor_loop()
    
    def load_file(self, file_path: str):
        """Load a file for editing"""
        self.current_file = self.project_root / file_path
        if not self.current_file.exists():
            print(f"❌ File {file_path} not found!")
            return False
        
        try:
            content = self.current_file.read_text(encoding='utf-8')
            self.current_content = content.split('\n')
            print(f"\n📝 Loaded: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def display_file(self, highlight_errors: bool = True):
        """Display the current file with line numbers"""
        if not self.current_content or not self.current_file:
            print("No file loaded!")
            return
        
        file_errors = [e for e in self.errors if e['file'] == str(self.current_file.relative_to(self.project_root))]
        error_lines = [e['line'] for e in file_errors]
        
        print(f"\n📄 {self.current_file.name}")
        print("-" * 60)
        
        for i, line in enumerate(self.current_content, 1):
            prefix = f"{i:3d}: "
            if highlight_errors and i in error_lines:
                print(f"❌ {prefix}{line}")
            else:
                print(f"   {prefix}{line}")
        
        print("-" * 60)
        
        if file_errors:
            print("\n🔍 Errors in this file:")
            for error in file_errors:
                print(f"   Line {error['line']}: {error['message']}")
    
    def editor_loop(self):
        """Main interactive editor loop"""
        if not self.current_file:
            print("No file loaded!")
            return
        
        self.display_file()
        
        print("\n🎯 Interactive Code Editor")
        print("Commands:")
        print("  edit <line>          - Edit specific line")
        print("  insert <line>        - Insert line after specified line")
        print("  delete <line>        - Delete specific line")
        print("  replace <start> <end> - Replace lines from start to end")
        print("  show                 - Show file again")
        print("  save                 - Save changes")
        print("  test                 - Test for errors")
        print("  exit                 - Exit editor")
        print("  help                 - Show this help")
        
        while True:
            try:
                command = input("\n📝 > ").strip().split()
                if not command:
                    continue
                
                cmd = command[0].lower()
                
                if cmd == 'exit':
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'show':
                    self.display_file()
                elif cmd == 'save':
                    self.save_file()
                elif cmd == 'test':
                    self.test_current_file()
                elif cmd == 'edit' and len(command) == 2:
                    self.edit_line(int(command[1]))
                elif cmd == 'insert' and len(command) == 2:
                    self.insert_line(int(command[1]))
                elif cmd == 'delete' and len(command) == 2:
                    self.delete_line(int(command[1]))
                elif cmd == 'replace' and len(command) == 3:
                    self.replace_lines(int(command[1]), int(command[2]))
                else:
                    print("❌ Invalid command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Exiting editor...")
                break
            except ValueError:
                print("❌ Invalid line number!")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show detailed help"""
        print("\n🎯 Interactive Code Editor Help")
        print("=" * 50)
        print("edit <line>          - Edit the content of a specific line")
        print("insert <line>        - Insert a new line after the specified line")
        print("delete <line>        - Delete the specified line")
        print("replace <start> <end> - Replace multiple lines with new content")
        print("show                 - Display the file with line numbers and errors")
        print("save                 - Save changes to the file")
        print("test                 - Re-run error detection on current file")
        print("exit                 - Exit the editor")
        print("help                 - Show this help message")
        print("\n💡 Tips:")
        print("- Lines with errors are marked with ❌")
        print("- Line numbers start from 1")
        print("- Use Ctrl+C to exit at any time")
    
    def edit_line(self, line_num: int):
        """Edit a specific line"""
        if line_num < 1 or line_num > len(self.current_content):
            print(f"❌ Invalid line number! Valid range: 1-{len(self.current_content)}")
            return
        
        current_line = self.current_content[line_num - 1]
        print(f"\nCurrent line {line_num}: {current_line}")
        new_line = input(f"New content for line {line_num}: ")
        self.current_content[line_num - 1] = new_line
        print(f"✅ Line {line_num} updated!")
    
    def insert_line(self, line_num: int):
        """Insert a new line after the specified line"""
        if line_num < 0 or line_num > len(self.current_content):
            print(f"❌ Invalid line number! Valid range: 0-{len(self.current_content)}")
            return
        
        new_line = input(f"Content for new line after {line_num}: ")
        self.current_content.insert(line_num, new_line)
        print(f"✅ New line inserted after line {line_num}!")
    
    def delete_line(self, line_num: int):
        """Delete a specific line"""
        if line_num < 1 or line_num > len(self.current_content):
            print(f"❌ Invalid line number! Valid range: 1-{len(self.current_content)}")
            return
        
        deleted_line = self.current_content[line_num - 1]
        print(f"Deleting line {line_num}: {deleted_line}")
        confirm = input("Are you sure? (y/n): ").lower()
        if confirm == 'y':
            del self.current_content[line_num - 1]
            print(f"✅ Line {line_num} deleted!")
        else:
            print("❌ Deletion cancelled.")
    
    def replace_lines(self, start: int, end: int):
        """Replace multiple lines"""
        if start < 1 or end > len(self.current_content) or start > end:
            print(f"❌ Invalid line range! Valid range: 1-{len(self.current_content)}")
            return
        
        print(f"\nReplacing lines {start}-{end}:")
        for i in range(start, end + 1):
            print(f"  {i}: {self.current_content[i - 1]}")
        
        print("\nEnter new content (press Enter twice to finish):")
        new_lines = []
        while True:
            line = input()
            if line == "" and new_lines and new_lines[-1] == "":
                new_lines.pop()  # Remove the last empty line
                break
            new_lines.append(line)
        
        # Replace the lines
        self.current_content[start - 1:end] = new_lines
        print(f"✅ Lines {start}-{end} replaced with {len(new_lines)} new lines!")
    
    def save_file(self):
        """Save the current content to file"""
        if not self.current_file:
            print("❌ No file loaded!")
            return
        
        try:
            content = '\n'.join(self.current_content)
            self.current_file.write_text(content, encoding='utf-8')
            print(f"✅ File saved: {self.current_file.name}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def test_current_file(self):
        """Test the current file for errors"""
        if not self.current_file:
            print("❌ No file loaded!")
            return
        
        print("🔍 Testing for errors...")
        
        # Get the file extension to determine validation method
        suffix = self.current_file.suffix.lower()
        if suffix == '.html':
            errors = self._validate_html(self.current_file)
        elif suffix == '.css':
            errors = self._validate_css(self.current_file)
        elif suffix == '.js':
            errors = self._validate_js(self.current_file)
        elif self.current_file.name == 'package.json':
            errors = self._validate_package_json(self.current_file)
        else:
            print(f"⚠️ No validation available for {suffix} files")
            return
        
        if errors:
            print(f"❌ Found {len(errors)} error(s):")
            for error in errors:
                print(f"   Line {error['line']}: {error['message']}")
        else:
            print("✅ No errors found!")


def start_interactive_editing_session(project_root: str, file_path: Optional[str] = None):
    """Start an interactive editing session"""
    editor = InteractiveCodeEditor(project_root)
    
    print("🔍 Detecting errors in project...")
    errors = editor.detect_errors()
    
    if errors:
        editor.show_errors()
        print(f"\n🎯 Starting interactive editor to fix {len(errors)} error(s)...")
        editor.start_interactive_editor(file_path)
    else:
        print("✅ No errors detected in the project!")
        if file_path:
            print(f"🎯 Starting editor for {file_path} anyway...")
            editor.start_interactive_editor(file_path)


if __name__ == "__main__":
    # Example usage
    project_path = input("Enter project path: ")
    start_interactive_editing_session(project_path)