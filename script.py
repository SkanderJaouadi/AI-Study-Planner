import os
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

# Pretty UI Imports
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.status import Status

console = Console()

# --- CONFIGURATION ---
GEMMA_KEY = "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"
LLAMA_KEY = "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"

def create_agent_model(model_name: str, api_key: str):
    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        default_headers={"HTTP-Referer": "http://localhost:3000", "X-Title": "Pretty Planner"}
    )

gemma_3 = create_agent_model("google/gemma-3-27b-it:free", GEMMA_KEY)
llama_3 = create_agent_model("meta-llama/llama-3.3-70b-instruct:free", LLAMA_KEY)

class PlanState(TypedDict):
    goal: str
    roadmap: str
    schedule: str
    feedback: str
    is_valid: bool
    attempts: int

# --- AGENT NODES ---
def designer_node(state: PlanState):
    console.print(Panel("[bold cyan]Gemma 3[/bold cyan] is designing the curriculum...", border_style="cyan"))
    feedback_text = f"\nCRITIC FEEDBACK: {state.get('feedback', '')}" if state.get('feedback') else ""
    
    prompt = f"""Goal: {state['goal']}
    {feedback_text}
    Create a detailed study roadmap and a daily schedule in Markdown format."""
    
    res = gemma_3.invoke([HumanMessage(content=prompt)])
    return {"schedule": res.content, "attempts": state.get("attempts", 0) + 1}

def critic_node(state: PlanState):
    console.print(Panel("[bold magenta]Llama 3.3[/bold magenta] is auditing the plan...", border_style="magenta"))
    prompt = f"Critique this plan: {state['schedule']}\nIf perfect, say 'PASSED'. Else, give specific fixes."
    
    res = llama_3.invoke([HumanMessage(content=prompt)])
    is_valid = "PASSED" in res.content.upper()
    return {"feedback": res.content, "is_valid": is_valid}

# --- GRAPH ASSEMBLY ---
workflow = StateGraph(PlanState)
workflow.add_node("designer", designer_node)
workflow.add_node("critic", critic_node)
workflow.set_entry_point("designer")
workflow.add_edge("designer", "critic")

def route_after_critic(state):
    if state["is_valid"] or state["attempts"] >= 3: return "end"
    return "revise"

workflow.add_conditional_edges("critic", route_after_critic, {"revise": "designer", "end": END})
app = workflow.compile()

# --- RUN ---
if __name__ == "__main__":
    console.print(Panel.fit("[bold yellow]🚀 AI MULTI-AGENT STUDY PLANNER[/bold yellow]", border_style="yellow"))
    
    inputs = {"goal": "Master Advanced SQL in 7 days", "attempts": 0}
    
    # Show a spinner while the agents are talking to each other
    with console.status("[bold green]Agents collaborating... please wait...", spinner="dots"):
        final_state = app.invoke(inputs)
    
    # FINAL BEAUTIFUL OUTPUT
    console.print("\n")
    console.print(Panel(
        Markdown(final_state["schedule"]), 
        title="[bold green] FINAL VALIDATED STUDY PLAN[/bold green]", 
        border_style="green",
        padding=(1, 2)
    ))