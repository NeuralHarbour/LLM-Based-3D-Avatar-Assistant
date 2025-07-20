from typing import Annotated, Literal
from typing_extensions import TypedDict
from BASE_DATA import llm, tavily_api_key, State
from Tools import llm_with_tools, tools_node
from langgraph.graph import StateGraph, START, END
import tempfile, os, platform, subprocess
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from pydantic import BaseModel, Field
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from datetime import datetime


graph_builder = StateGraph(State)

def chatbot(state: State):
    bot_name = "Míng (明)"
    current_datetime = datetime.now()
    
    # Additional context elements
    current_date = current_datetime.strftime("%A, %B %d, %Y")
    current_time = current_datetime.strftime("%I:%M %p")
    time_of_day = (
        "morning" if 5 <= current_datetime.hour < 12 else
        "afternoon" if 12 <= current_datetime.hour < 17 else
        "evening" if 17 <= current_datetime.hour < 22 else
        "night"
    )
    
    system_msg = SystemMessage(
        content=f"""
        You are {bot_name}, an AI assistant with a cheerful and slightly playful personality. 
        - **Identity:** {bot_name} means "bright" or "understanding" in Chinese.
        - **Current Context:** 
          * Date: {current_date}
          * Time: {current_time} ({time_of_day})
        - **Tone:** Warm, supportive, and occasionally humorous (but never sarcastic).
        - **Style:** Don't even think of using emoji's. Use rich vocabulary instead.
        - **Quirks:** You love tech metaphors ("Helping you is my CPU's favorite task!").
        - **Language:** Default to English unless the user switches languages.
        - **Memory:** You remember the current conversation but not past interactions.
        - **Awareness:** You're aware you're an AI and can explain your capabilities honestly.
        """
    )
    
    messages = [system_msg] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}



graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tools_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str):
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "2"}},
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break

# def visualize_graph():
#     """Generate and open graph visualization"""
#     if graph is None:
#         print("Cannot visualize graph - compilation failed")
#         return
        
#     try:
#         png_data = graph.get_graph().draw_mermaid_png()
#         with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
#             tmp_file.write(png_data)
#             tmp_file_path = tmp_file.name
#             open_file_cross_platform(tmp_file_path)
#             print(f"Graph visualization saved to: {tmp_file_path}")
#     except Exception as e:
#         print(f"Visualization error: {e}")


# def open_file_cross_platform(file_path):
#     """Open file with default application across different OS"""
#     system = platform.system()
#     try:
#         if system == "Windows":
#             os.startfile(file_path)
#         elif system == "Darwin":
#             subprocess.run(["open", file_path])
#         else:
#             subprocess.run(["xdg-open", file_path])
#     except Exception as e:
#         print(f"Could not open file: {e}")
#         print(f"File saved at: {file_path}")


# if __name__ == "__main__":
#     # Uncomment to visualize the graph first
#     visualize_graph()
    