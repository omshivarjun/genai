"""
AI-Powered Automatic Code Debugger using Gemini
Automatically analyzes and fixes all errors, issues, and problems in the codebase
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from agent.interactive_editor import InteractiveCodeEditor
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Get project root directly
PROJECT_ROOT = Path.cwd()

@dataclass
class CodeIssue:
    file_path: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # 'critical', 'warning', 'suggestion'
    suggested_fix: Optional[str] = None

class GeminiCodeDebugger:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1,
            max_retries=3
        )
        self.editor = InteractiveCodeEditor(str(project_path))
        self.issues: List[CodeIssue] = []
        
    def analyze_entire_codebase(self) -> List[CodeIssue]:
        """Analyze the entire codebase using Gemini AI"""
        print("🧠 Gemini AI: Analyzing entire codebase...")
        print("=" * 50)
        
        # Get all code files
        code_files = self._get_all_code_files()
        all_issues = []
        
        for file_path in code_files:
            print(f"🔍 Analyzing: {file_path.relative_to(self.project_path)}")
            file_issues = self._analyze_single_file(file_path)
            all_issues.extend(file_issues)
        
        # Also run basic error detection
        basic_errors = self.editor.detect_errors()
        for error in basic_errors:
            issue = CodeIssue(
                file_path=error['file'],
                line_number=error['line'],
                issue_type=error['type'],
                description=error['message'],
                severity='critical'
            )
            all_issues.append(issue)
        
        self.issues = all_issues
        return all_issues
    
    def _get_all_code_files(self) -> List[Path]:
        """Get all code files in the project"""
        extensions = {'.html', '.css', '.js', '.json', '.py', '.md'}
        code_files = []
        
        for ext in extensions:
            code_files.extend(self.project_path.glob(f"**/*{ext}"))
        
        return code_files
    
    def _analyze_single_file(self, file_path: Path) -> List[CodeIssue]:
        """Analyze a single file using Gemini AI"""
        try:
            content = file_path.read_text(encoding='utf-8')
            file_ext = file_path.suffix.lower()
            
            prompt = f"""
You are an expert code analyzer and debugger. Please analyze this {file_ext} file and identify ALL issues, errors, problems, and improvements needed.

File: {file_path.name}
Content:
```{file_ext[1:] if file_ext else 'text'}
{content}
```

Please identify and categorize issues as:
1. CRITICAL: Syntax errors, broken functionality, security issues
2. WARNING: Code quality issues, potential bugs, deprecated usage
3. SUGGESTION: Performance optimizations, best practices, improvements

For each issue found, provide:
- Line number (approximate)
- Issue type (HTML/CSS/JavaScript/JSON/etc.)
- Clear description of the problem
- Suggested fix or improvement
- Severity level (CRITICAL/WARNING/SUGGESTION)

Format your response as a structured analysis with specific, actionable recommendations.
Focus on practical fixes that will make the code work correctly and follow best practices.
"""

            response = self.llm.invoke(prompt)
            return self._parse_gemini_analysis(response.content, str(file_path.relative_to(self.project_path)))
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return []
    
    def _parse_gemini_analysis(self, analysis: str, file_path: str) -> List[CodeIssue]:
        """Parse Gemini's analysis into structured issues"""
        issues = []
        lines = analysis.split('\n')
        
        current_issue = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for severity indicators
            if any(word in line.upper() for word in ['CRITICAL', 'WARNING', 'SUGGESTION', 'ERROR', 'ISSUE', 'PROBLEM']):
                if 'CRITICAL' in line.upper() or 'ERROR' in line.upper():
                    severity = 'critical'
                elif 'WARNING' in line.upper():
                    severity = 'warning'
                else:
                    severity = 'suggestion'
                
                # Extract line number if present
                line_num = 1
                import re
                line_match = re.search(r'line\s*(\d+)', line, re.IGNORECASE)
                if line_match:
                    line_num = int(line_match.group(1))
                
                # Extract issue type
                issue_type = 'General'
                for tech in ['HTML', 'CSS', 'JavaScript', 'JS', 'JSON', 'Python']:
                    if tech.upper() in line.upper():
                        issue_type = tech
                        break
                
                issue = CodeIssue(
                    file_path=file_path,
                    line_number=line_num,
                    issue_type=issue_type,
                    description=line,
                    severity=severity
                )
                issues.append(issue)
        
        return issues
    
    def auto_fix_all_issues(self) -> Dict[str, Any]:
        """Automatically fix all detected issues using Gemini AI"""
        print("\n🤖 Gemini AI: Auto-fixing all issues...")
        print("=" * 40)
        
        if not self.issues:
            print("✅ No issues found to fix!")
            return {"status": "success", "fixes_applied": 0, "message": "No issues found"}
        
        # Group issues by file
        files_to_fix = {}
        for issue in self.issues:
            if issue.file_path not in files_to_fix:
                files_to_fix[issue.file_path] = []
            files_to_fix[issue.file_path].append(issue)
        
        total_fixes = 0
        results = {}
        
        for file_path, file_issues in files_to_fix.items():
            print(f"\n🔧 Fixing {len(file_issues)} issues in: {file_path}")
            
            fixes_applied = self._fix_file_issues(file_path, file_issues)
            total_fixes += fixes_applied
            results[file_path] = fixes_applied
        
        return {
            "status": "success",
            "fixes_applied": total_fixes,
            "files_processed": len(files_to_fix),
            "detailed_results": results
        }
    
    def _fix_file_issues(self, file_path: str, issues: List[CodeIssue]) -> int:
        """Fix all issues in a specific file"""
        try:
            full_path = self.project_path / file_path
            if not full_path.exists():
                print(f"❌ File not found: {file_path}")
                return 0
            
            original_content = full_path.read_text(encoding='utf-8')
            file_ext = full_path.suffix.lower()
            
            # Create comprehensive fix prompt
            issues_description = "\n".join([
                f"- Line {issue.line_number}: {issue.description} (Severity: {issue.severity})"
                for issue in issues
            ])
            
            prompt = f"""
You are an expert code fixer. Please fix ALL the issues in this {file_ext} file.

File: {file_path}
Issues to fix:
{issues_description}

Original code:
```{file_ext[1:] if file_ext else 'text'}
{original_content}
```

Please provide the COMPLETE corrected code that:
1. Fixes ALL syntax errors and critical issues
2. Addresses warnings and code quality issues  
3. Implements suggested improvements where beneficial
4. Maintains the original functionality and structure
5. Follows best practices for {file_ext} files
6. Ensures the code is clean, readable, and functional

Return ONLY the corrected code without any explanations or markdown formatting.
The output should be ready to save directly to the file.
"""

            print(f"   🧠 Gemini analyzing and fixing {len(issues)} issues...")
            response = self.llm.invoke(prompt)
            fixed_content = response.content.strip()
            
            # Remove code block markers if present
            if fixed_content.startswith('```'):
                lines = fixed_content.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                fixed_content = '\n'.join(lines)
            
            # Save the fixed content
            full_path.write_text(fixed_content, encoding='utf-8')
            print(f"   ✅ Fixed and saved: {file_path}")
            
            return len(issues)
            
        except Exception as e:
            print(f"   ❌ Error fixing {file_path}: {e}")
            return 0
    
    def verify_fixes(self) -> Dict[str, Any]:
        """Verify that all fixes were successful"""
        print("\n🔍 Verifying fixes...")
        print("=" * 25)
        
        # Re-run error detection
        new_errors = self.editor.detect_errors()
        
        if not new_errors:
            print("✅ All issues fixed successfully! No errors detected.")
            return {
                "status": "success", 
                "errors_remaining": 0,
                "message": "All issues resolved successfully!"
            }
        else:
            print(f"⚠️ {len(new_errors)} issues still remain:")
            for error in new_errors:
                print(f"   - {error['file']}:{error['line']} - {error['message']}")
            
            return {
                "status": "partial",
                "errors_remaining": len(new_errors),
                "remaining_errors": new_errors,
                "message": f"{len(new_errors)} issues still need attention"
            }
    
    def show_analysis_summary(self):
        """Display comprehensive analysis summary"""
        if not self.issues:
            print("✅ No issues found in the codebase!")
            return
        
        print(f"\n📊 Gemini AI Analysis Summary")
        print("=" * 35)
        
        # Count by severity
        critical = len([i for i in self.issues if i.severity == 'critical'])
        warnings = len([i for i in self.issues if i.severity == 'warning'])
        suggestions = len([i for i in self.issues if i.severity == 'suggestion'])
        
        print(f"🔴 Critical Issues: {critical}")
        print(f"🟡 Warnings: {warnings}")
        print(f"🔵 Suggestions: {suggestions}")
        print(f"📝 Total Issues: {len(self.issues)}")
        
        # Count by file type
        file_types = {}
        for issue in self.issues:
            ext = Path(issue.file_path).suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        print(f"\n📁 Issues by file type:")
        for file_type, count in file_types.items():
            print(f"   {file_type or 'no extension'}: {count} issues")
        
        # Show top issues
        print(f"\n🎯 Top Issues to Fix:")
        critical_issues = [i for i in self.issues if i.severity == 'critical'][:5]
        for i, issue in enumerate(critical_issues, 1):
            print(f"   {i}. {issue.file_path}:{issue.line_number} - {issue.description}")


def auto_debug_project(project_path: str = None) -> Dict[str, Any]:
    """Main function to automatically debug entire project"""
    if project_path is None:
        project_path = str(PROJECT_ROOT)
    
    print("🚀 AI-Powered Automatic Code Debugger")
    print("=" * 45)
    print(f"📁 Analyzing project: {project_path}")
    print("🤖 Using: Google Gemini 2.0 Flash AI")
    print()
    
    debugger = GeminiCodeDebugger(project_path)
    
    # Step 1: Analyze entire codebase
    issues = debugger.analyze_entire_codebase()
    debugger.show_analysis_summary()
    
    if not issues:
        return {"status": "success", "message": "No issues found in the project!"}
    
    # Step 2: Auto-fix all issues
    fix_results = debugger.auto_fix_all_issues()
    
    # Step 3: Verify fixes
    verification_results = debugger.verify_fixes()
    
    # Combine results
    final_results = {
        "analysis": {
            "total_issues_found": len(issues),
            "critical_issues": len([i for i in issues if i.severity == 'critical']),
            "warnings": len([i for i in issues if i.severity == 'warning']),
            "suggestions": len([i for i in issues if i.severity == 'suggestion'])
        },
        "fixes": fix_results,
        "verification": verification_results,
        "overall_status": verification_results["status"]
    }
    
    print(f"\n🎉 Auto-Debug Complete!")
    print(f"📊 Found: {len(issues)} issues")
    print(f"🔧 Fixed: {fix_results['fixes_applied']} issues")
    print(f"✅ Status: {verification_results['message']}")
    
    return final_results


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-debug project using Gemini AI')
    parser.add_argument('--project', '-p', type=str, help='Project path to debug')
    args = parser.parse_args()
    
    project_path = args.project or str(PROJECT_ROOT)
    results = auto_debug_project(project_path)
    
    print(f"\n📋 Final Results:")
    print(f"   Status: {results['overall_status']}")
    print(f"   Issues Found: {results['analysis']['total_issues_found']}")
    print(f"   Fixes Applied: {results['fixes']['fixes_applied']}")