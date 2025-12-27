from dotenv import load_dotenv
from langchain_core.globals import set_verbose, set_debug
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
import re
from datetime import datetime
from langchain_openai import ChatOpenAI
from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files, list_file, set_project_folder

_ = load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGroq(model="openai/gpt-oss-120b")
llm = ChatOpenAI(model="gpt-4o")


def sanitize_folder_name(name: str) -> str:
    """Convert project name to a safe folder name."""
    # Remove special characters, replace spaces with underscores
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[-\s]+', '_', name)
    return name.strip('_')


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    
    # Create unique folder name for this project
    folder_name = sanitize_folder_name(resp.name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_folder = f"{folder_name}_{timestamp}"
    
    # Set the project folder for all tools
    set_project_folder(project_folder)
    
    print(f"\n{'='*60}")
    print(f"🚀 Creating project: {resp.name}")
    print(f"📁 Project folder: {project_folder}")
    print(f"{'='*60}\n")
    
    return {"plan": resp, "project_folder": project_folder}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan
    
    print(f"\n📋 Implementation Plan:")
    print(f"Total steps: {len(resp.implementation_steps)}")
    for i, step in enumerate(resp.implementation_steps, 1):
        print(f"  {i}. {step.filepath}")
    print()
    
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        project_folder = state.get("project_folder", "generated_project")
        print(f"\n{'='*60}")
        print(f"✅ Project completed successfully!")
        print(f"📁 Location: generated_projects/{project_folder}")
        print(f"{'='*60}\n")
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    print(f"\n⚙️  Step {coder_state.current_step_idx + 1}/{len(steps)}: {current_task.filepath}")

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, list_file, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)