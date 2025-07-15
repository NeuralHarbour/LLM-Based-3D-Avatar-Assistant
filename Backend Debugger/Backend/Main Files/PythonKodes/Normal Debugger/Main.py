from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from BASE_DATA import llm,tavily_api_key
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import tempfile, os, platform, subprocess
from langchain_tavily import TavilySearch
import json
from langchain_core.messages import ToolMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

class ToolNode:
    def __init__(self,tools:list) -> None:
        self.tools_by_name = {tool.name:tool for tool in tools}

    def __call__(self,inputs:dict):
        if messages := inputs.get("messages",[]):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs=[]

        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(ToolMessage(content=json.dumps(tool_result),name=tool_call["name"],tool_call_id=tool_call["id"],))
        return {"messages":outputs}

tool = TavilySearch(api_key=tavily_api_key,max_results=2)
tools = [tool]
tool_node = ToolNode(tools=[tool])
llm_with_tools = llm.bind_tools(tools)

def route_tools(state: State):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    messages = state.get("messages", [])
    if not messages:
        raise ValueError(f"No messages found in state: {state}")
    ai_message = messages[-1]
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}



graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END}
)
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile()



def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant : ", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break

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

# try:
#     png_data = graph.get_graph().draw_mermaid_png()
#     with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
#         tmp_file.write(png_data)
#         tmp_file_path = tmp_file.name
#         open_file_cross_platform(tmp_file_path)
# except Exception as e:
#     print(f"error : {e}")