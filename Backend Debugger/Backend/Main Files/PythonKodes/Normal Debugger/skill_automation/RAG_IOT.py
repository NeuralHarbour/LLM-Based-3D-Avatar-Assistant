import asyncio
from pathlib import Path
import os
import sys
import importlib.util
from dotenv import load_dotenv
from .tools import upsert_memories_from_log,add_automation
from langchain_core.prompts import ChatPromptTemplate
from .agent import HomeAgent,create_tool_node_with_fallback,handle_tool_error
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from .const import AGENT_SYSTEM_PROMPT 
import uuid
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from .graph import _summarize_and_trim,_validate_device_request,_should_continue,State

def print_message_content(event):
    """Helper function to print only the message content."""
    if isinstance(event, dict) and "messages" in event:
        messages = event["messages"]
        if isinstance(messages, list):
            for msg in messages:
                if isinstance(msg, (HumanMessage, AIMessage, ToolMessage)):
                    # For tool messages, include the name if available
                    if isinstance(msg, ToolMessage) and hasattr(msg, 'name'):
                        print(f"Tool {msg.name}: {msg.content}")
                    else:
                        # Skip empty messages
                        if msg.content:
                            print(f"{msg.__class__.__name__}: {msg.content}")

async def main():
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    env_path = project_root / "API_KEYS.env"
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found at {env_path}")
    
    load_dotenv(dotenv_path=str(env_path))
    wolfram_api_key = os.environ.get("WOLFRAM_ALPHA_API_KEY")
    
    if not wolfram_api_key:
        raise ValueError("WOLFRAM_ALPHA_API_KEY not found in environment variables")
    base_data_path = project_root / "BASE_DATA.py"
    if not base_data_path.exists():
        raise FileNotFoundError(f"BASE_DATA.py not found at {base_data_path}")
    
    sys.path.insert(0, str(project_root))
    
    try:
        spec = importlib.util.spec_from_file_location("BASE_DATA", base_data_path)
        base_data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(base_data)
    except Exception as e:
        raise ImportError(f"Failed to import BASE_DATA: {str(e)}")
    primary_assistant_prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        ("placeholder", "{messages}"),
    ])

    part_1_tools = [
        upsert_memories_from_log,add_automation
    ]
    part_1_assistant_runnable = primary_assistant_prompt | base_data.llm.bind_tools(part_1_tools)
    builder = StateGraph(State)
    
    builder.add_node("assistant", HomeAgent(part_1_assistant_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))
    builder.add_node("validate_device", _validate_device_request)
    
    # Add edges
    builder.add_edge(START, "assistant")
    
    # Add conditional edges from assistant
    builder.add_conditional_edges(
        "assistant",
        _should_continue,
        {
            "tools": "tools",
            "validate_device": "validate_device",
            "end": END
        }
    )
    
    # Add edges from other nodes back to assistant or to end
    builder.add_edge("tools", "assistant")
    builder.add_edge("validate_device", "assistant")


    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

    tutorial_questions = [
        'hey',
        'create an automation to check the camera every 30 min',
    ]

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    for question in tutorial_questions:
        print("\n--- New Question ---")
        events = graph.stream(
            {"messages": ("user", question)}, config, stream_mode="values"
        )
        for event in events:
            print_message_content(event)

if __name__ == "__main__":
    asyncio.run(main())