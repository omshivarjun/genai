#!/usr/bin/env python3
"""
Simple test to show the AI Auto-Debugger working
"""

from agent.tools import auto_debug_with_gemini

print("🚀 Testing AI Auto-Debugger Tool")
print("=" * 40)

try:
    result = auto_debug_with_gemini.invoke({})
    print("✅ Auto-debugger completed!")
    print(result)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()