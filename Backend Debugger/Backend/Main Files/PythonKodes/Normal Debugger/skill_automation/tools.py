from typing import Annotated, Any, Optional
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import InjectedStore
from langchain_core.tools import Tool, StructuredTool, InjectedToolArg
from langgraph.store.base import BaseStore
from ulid import ULID
import yaml  # Using built-in yaml module
import aiofiles
from collections.abc import Mapping
import json
from pydantic import BaseModel

class AddAutomationArgs(BaseModel):
    time_pattern: str
    message: str
    automation_yaml: Optional[str] = None

# Add automation function
def add_automation(
    time_pattern: str,
    message: str,
    automation_yaml: str | None = None,
    *,
    config: Annotated[RunnableConfig, InjectedToolArg]
) -> str:
    '''
    Tool to create and add automations
    '''
    try:
        config_dir = Path("config")
        config_dir.mkdir(parents=True, exist_ok=True)
        automation_path = config_dir / "automation.yaml"

        automation_data = {
            "id": str(ULID()),
            "alias": f"Camera Check {time_pattern}",
            "description": "Automated camera check",
            "trigger": {
                "platform": "time_pattern",
                "pattern": time_pattern,
            },
            "action": {
                "service": "camera.snapshot",
                "data": {"message": message},
            },
        }

        if automation_yaml:
            try:
                custom_config = yaml.safe_load(automation_yaml)
                automation_data.update(custom_config)
            except yaml.YAMLError as e:
                return f"Error parsing custom YAML: {str(e)}"

        existing_automations = []
        if automation_path.exists():
            try:
                with open(automation_path, 'r') as f:
                    content = f.read()
                    if content.strip():
                        existing_automations = yaml.safe_load(content) or []
                        if not isinstance(existing_automations, list):
                            existing_automations = [existing_automations]
            except yaml.YAMLError as e:
                return f"Error reading existing automations: {str(e)}"

        existing_automations.append(automation_data)

        with open(automation_path, 'w') as f:
            yaml.dump(existing_automations, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        return f"Successfully added camera check automation (ID: {automation_data['id']}) to run {time_pattern}"
    except Exception as e:
        return f"Error creating automation: {str(e)}"

# Structured tool for add_automation
add_automation_tool = StructuredTool.from_function(
    func=add_automation,
    name="add_automation",
    description="Add an automation to check cameras periodically",
    args_schema=AddAutomationArgs
)

# Upsert memories function
async def upsert_memories_from_log(
    *,
    config: Annotated[RunnableConfig, InjectedToolArg],
    store: Annotated[BaseStore, InjectedStore],
) -> str:
    '''
    Tool for memory upsertion
    '''
    try:
        with open('conversation_log.json', 'r') as file:
            conversation = json.load(file)

        messages = conversation.get("messages", [])
        upserted_count = 0

        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                human_message = messages[i]
                ai_message = messages[i + 1]

                if human_message["sender"] == "human" and ai_message["sender"] == "ai":
                    mem_id = ULID()
                    await store.aput(
                        namespace=(config["configurable"]["user_id"], "memories"),
                        key=str(mem_id),
                        value={
                            "content": human_message["body"],
                            "context": ai_message["body"],
                        },
                    )
                    upserted_count += 1

        return f"Successfully upserted {upserted_count} memories from conversation log"
    except FileNotFoundError:
        return "Conversation log file not found"
    except json.JSONDecodeError:
        return "Error reading conversation log file"

# Tool for upsert_memories_from_log
upsert_memories_tool = Tool.from_function(
    func=upsert_memories_from_log,
    name="upsert_memories_from_log",
    description="Read the conversation log JSON file and upsert all messages as memories"
)
