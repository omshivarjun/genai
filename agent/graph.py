from dotenv import load_dotenv
from langchain.globals import set_verbose, set_debug
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files, detect_project_errors, start_interactive_editor, validate_file

_ = load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    max_retries=3
)


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    resp.plan = plan
    print(resp.model_dump_json())
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


def error_detector_agent(state: dict) -> dict:
    """Detects errors in the generated project."""
    print("🔍 Checking for errors in generated project...")
    
    # Use the detect_project_errors tool
    error_report = detect_project_errors.invoke({})
    
    has_errors = "error(s)" in error_report.lower()
    
    print(error_report)
    
    return {
        "error_report": error_report,
        "has_errors": has_errors,
        "status": "ERRORS_FOUND" if has_errors else "NO_ERRORS"
    }


def interactive_editor_agent(state: dict) -> dict:
    """Interactive editor for fixing errors."""
    error_report = state.get("error_report", "")
    
    print("\n🎯 Starting Interactive Editor Session")
    print("=" * 50)
    print("Errors detected in your project. You can now edit the code interactively.")
    print("The editor will help you fix syntax errors, missing tags, and other issues.")
    print("=" * 50)
    
    # Start the interactive editor
    try:
        result = start_interactive_editor.invoke({"file_path": ""})
        print(result)
        
        # After editing, check for errors again
        print("\n🔍 Re-checking for errors after editing...")
        new_error_report = detect_project_errors.invoke({})
        has_remaining_errors = "error(s)" in new_error_report.lower()
        
        return {
            "error_report": new_error_report,
            "has_errors": has_remaining_errors,
            "status": "EDITING_COMPLETE",
            "interactive_editing_done": True
        }
        
    except Exception as e:
        print(f"❌ Error in interactive editor: {e}")
        return {
            "status": "EDITOR_ERROR",
            "error_message": str(e),
            "has_errors": True
        }


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("error_detector", error_detector_agent)
graph.add_node("interactive_editor", interactive_editor_agent)

# Initial flow
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

# After coding, check for errors
graph.add_conditional_edges(
    "coder",
    lambda s: "error_detector" if s.get("status") == "DONE" else "coder",
    {"error_detector": "error_detector", "coder": "coder"}
)

# If errors found, go to interactive editor, otherwise end
graph.add_conditional_edges(
    "error_detector",
    lambda s: "interactive_editor" if s.get("has_errors") else "END",
    {"interactive_editor": "interactive_editor", "END": END}
)

# After interactive editing, check for errors again or end
graph.add_conditional_edges(
    "interactive_editor",
    lambda s: "error_detector" if s.get("has_errors") else "END",
    {"error_detector": "error_detector", "END": END}
)

graph.set_entry_point("planner")
agent = graph.compile()
if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)
