#!/usr/bin/env python3
"""
Quick demonstration of the AI Auto-Debugger functionality
"""

import os
from dotenv import load_dotenv
from agent.auto_debugger import GeminiCodeDebugger

load_dotenv()

def demo_auto_debugger():
    """Demonstrate the auto-debugger on the existing generated_project."""
    
    print("🤖 AI Auto-Debugger Demonstration")
    print("=" * 50)
    
    # Use test_project for demonstration
    project_path = "test_project"
    
    # Check if we have a test project
    if not os.path.exists(project_path):
        print(f"❌ No {project_path} found. Please create test files first.")
        return
    
    print(f"📁 Found {project_path} folder")
    files = os.listdir(project_path)
    print(f"   Files: {', '.join(files)}")
    
    print("\n🔍 Initializing Gemini Code Debugger...")
    debugger = GeminiCodeDebugger(project_path)
    
    print("\n📊 Analyzing entire codebase...")
    analysis = debugger.analyze_entire_codebase()
    
    print(f"\n✅ Analysis Complete!")
    print(f"   Files analyzed: {len(analysis.get('files_analyzed', []))}")
    print(f"   Total issues found: {analysis.get('total_issues', 0)}")
    
    if analysis.get('total_issues', 0) > 0:
        print(f"\n⚠️  Issues breakdown:")
        for severity, count in analysis.get('issues_by_severity', {}).items():
            if count > 0:
                print(f"   {severity}: {count}")
        
        print(f"\n🛠️  Starting automatic fixes...")
        fix_results = debugger.auto_fix_all_issues()
        
        print(f"\n✅ Auto-fix Complete!")
        print(f"   Files fixed: {fix_results.get('files_fixed', 0)}")
        print(f"   Issues resolved: {fix_results.get('issues_resolved', 0)}")
        
        if fix_results.get('failed_fixes'):
            print(f"   Failed fixes: {len(fix_results['failed_fixes'])}")
            for fail in fix_results['failed_fixes']:
                print(f"     - {fail}")
                
        print(f"\n🔍 Verifying fixes...")
        verification = debugger.verify_fixes()
        print(f"   Verification result: {'✅ PASSED' if verification.get('all_fixed', False) else '⚠️  SOME ISSUES REMAIN'}")
        
    else:
        print("🎉 No issues found! Your code is clean.")
    
    return analysis

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        exit(1)
    
    demo_auto_debugger()