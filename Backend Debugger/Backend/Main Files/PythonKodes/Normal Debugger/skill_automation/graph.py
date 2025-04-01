"""Langgraph graphs for Home Generative Agent."""
from __future__ import annotations  # noqa: I001

import copy
import json
import logging
from typing import Literal

from langchain_core.messages import (
    AnyMessage,
    BaseMessage,
    HumanMessage,
    RemoveMessage,
    SystemMessage,
    ToolMessage,
    trim_messages,
)
from langchain_core.runnables import RunnableConfig  # noqa: TCH002
from langgraph.store.base import BaseStore  # noqa: TCH002
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import ValidationError

from .const import (
    CONF_SUMMARIZATION_MODEL_TEMPERATURE,
    CONF_SUMMARIZATION_MODEL_TOP_P,
    CONF_VLM,
    CONTEXT_MAX_MESSAGES,
    CONTEXT_SUMMARIZE_THRESHOLD,
    EMBEDDING_MODEL_PROMPT_TEMPLATE,
    RECOMMENDED_SUMMARIZATION_MODEL_TEMPERATURE,
    RECOMMENDED_SUMMARIZATION_MODEL_TOP_P,
    RECOMMENDED_VLM,
    SUMMARY_INITIAL_PROMPT,
    SUMMARY_PROMPT_TEMPLATE,
    SUMMARY_SYSTEM_PROMPT,
    TOOL_CALL_ERROR_TEMPLATE,
    VLM_NUM_PREDICT,
)
import asyncio
from pathlib import Path
import os
import sys
import importlib.util
from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

LOGGER = logging.getLogger(__name__)

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

class State(MessagesState):
    """Extend the MessagesState to include a summary key."""

    summary: str
    devices: dict 

def _summarize_and_trim(
        state: State, config: RunnableConfig, *, store: BaseStore
    ) -> dict[str, list[AnyMessage]]:
    """Coroutine to summarize and trim message history."""
    summary = state.get("summary", "")

    if summary:
        summary_message = SUMMARY_PROMPT_TEMPLATE.format(summary=summary)
    else:
        summary_message = SUMMARY_INITIAL_PROMPT

    messages = (
        [SystemMessage(content=SUMMARY_SYSTEM_PROMPT)] +
        state["messages"] +
        [HumanMessage(content=summary_message)]
    )

    model = base_data.llm

    LOGGER.debug("Summary messages: %s", messages)
    response = model.invoke(messages)
    trimmed_messages = trim_messages(
        messages=state["messages"],
        token_counter=len,
        max_tokens=CONTEXT_MAX_MESSAGES,
        strategy="last",
        start_on="human",
        include_system=True,
    )
    messages_to_remove = [m for m in state["messages"] if m not in trimmed_messages]
    LOGGER.debug("Messages to remove: %s", messages_to_remove)
    remove_messages = [RemoveMessage(id=m.id) for m in messages_to_remove]

    return {"summary": response.content, "messages": remove_messages}


def get_dummy_devices():
    """Return a dictionary of dummy devices with their details."""
    return {
        "front door camera": {"id": "cam001", "type": "camera", "location": "front"},
        "backyard camera": {"id": "cam002", "type": "camera", "location": "backyard"},
        "garage camera": {"id": "cam003", "type": "camera", "location": "garage"},
        # Add more devices as needed
    }

def _should_continue(state: State) -> Literal["tools", "validate_device", "end"]:
    """
    Determine the next step in the conversation flow.
    """
    last_message = state["messages"][-1]
    
    # Check for tool calls first
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    # Check for device-related keywords
    message_content = last_message.content.lower()
    if "camera" in message_content:
        return "validate_device"
        
    return "end"

def _validate_device_request(state: State) -> dict:
    """
    Validate device mentions and return appropriate response state.
    """
    last_message = state["messages"][-1]
    message_content = last_message.content.lower()
    devices = get_dummy_devices()
    
    # Check for specific device mentions
    mentioned_devices = [
        (name, details) for name, details in devices.items() 
        if name.lower() in message_content
    ]
    
    if not mentioned_devices and "camera" in message_content:
        # Only "camera" was mentioned, list available devices
        available_devices = list(devices.keys())
        response = (
            f"I see you mentioned a camera. Here are the available cameras:\n"
            f"{', '.join(available_devices)}.\n"
            f"Please specify which camera you'd like to use."
        )
        return {"messages": [AIMessage(content=response)]}
    
    elif mentioned_devices:
        # Specific device found, store it and continue to automation
        device_name, device_details = mentioned_devices[0]
        state["current_device"] = device_details
        return {"messages": state["messages"]}
    
    # No device-related content, continue normal flow
    return {"messages": state["messages"]}