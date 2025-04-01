import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import importlib.util
from langchain.agents import Tool,initialize_agent,AgentType,create_react_agent,AgentExecutor
import datetime
from langchain.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
import yaml
from ulid import ULID
import re

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

class ReminderAgent:
    def __init__(self,llm):
        self.llm = llm

        self.tools = [
            Tool(name="Set_Reminder",func=self.Set_Reminder,description="Used for setting reminder"),
            Tool(name="Cancel_Reminder",func=self.Cancel_Reminder,description="Used for cancelling reminder"),
        ]

        template = '''Answer the following questions as best you can. You have access to the following tools:
        {tools}
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Remember: NEVER include both an Action and a Final Answer in the same response. Either use an Action to gather information, or provide a Final Answer, but not both.

        Begin!
        Question: {input}
        history: {chat_history}
        Thought:{agent_scratchpad}'''

        prompt = PromptTemplate.from_template(template)

        agent = create_react_agent(base_data.llm, self.tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
        )

        self.agent_with_message_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: base_data.history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def Set_Reminder(self, query):
        now = datetime.datetime.now()

        recurring_pattern = r"every\s+(\d+)\s+(minute|hour|day)s?"
        match = re.search(recurring_pattern, query, re.IGNORECASE)
        if match:
            interval_value = int(match.group(1))
            interval_unit = match.group(2).lower()
            recurring_info = {
                "interval_value": interval_value,
                "interval_unit": interval_unit
            }
        else:
            recurring_info = {
                "interval_value": None,
                "interval_unit": "once"
            }

        prompt = PromptTemplate(
            input_variables=["question"],
            template=f"""Given a user query for a reminder, extract:
            1. The date and time to set the reminder for
            2. The time when to trigger the reminder
            Today's date and time are {now}.
            Format outputs as:
            Date: DD/MM/YYYY
            Time: HH:MM
            Trigger: HH:MM (time when reminder should trigger)
            User query: \"{query}\"""")
        
        chain = prompt | base_data.llm
        Base_message_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: base_data.history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )
        response = Base_message_history.invoke(
            {"input": query}, 
            {"configurable": {"session_id": "unused"}}
        )
   
        content = response.content if hasattr(response, 'content') else response
        data = {}
        for line in content.split('\n'):
            if ':' in line:
                key, value = line.split(': ')
                data[key.strip()] = value.strip()

        def convert_to_24_hour(time_str):
            try:
                time_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
                return time_obj.strftime("%H:%M")  # Convert back to 24-hour format
            except ValueError:
                try:
                    # If already in 24-hour format
                    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                    return time_obj.strftime("%H:%M")
                except ValueError:
                    return time_str
    
        nested_data = {
            "id": str(ULID()),
            "alias": query,
            "description": "Set Reminder",
            "date": {
                "time": convert_to_24_hour(data.get('Time', '')),
                "_date": data.get('Date', ''),
                "trigger_time": convert_to_24_hour(data.get('Trigger', ''))
            },
            "recurring": recurring_info
        }
    
        if os.path.exists('reminders.yaml'):
            with open('reminders.yaml', 'r') as file:
                existing_data = yaml.safe_load(file) or []
            existing_data.append(nested_data)
            with open('reminders.yaml', 'w') as file:
                yaml.dump(existing_data, file)
        else:
            with open('reminders.yaml', 'w') as file:
                yaml.dump([nested_data], file)
    
        return nested_data

    def Cancel_Reminder(self,query):
        pass

    def run(self, query):
        return self.agent_with_message_history.invoke(
            {"input": query},
            {"configurable": {"session_id": "unused"}},
        )



