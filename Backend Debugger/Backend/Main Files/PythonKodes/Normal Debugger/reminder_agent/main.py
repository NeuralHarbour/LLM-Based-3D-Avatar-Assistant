
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import importlib.util
from langchain.agents import Tool,initialize_agent,AgentType,create_react_agent,AgentExecutor
import datetime
from langchain.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate



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
    def Set_Reminder(self,query):
        now = datetime.datetime.now()
        prompt = PromptTemplate.from_template(
              template = f"""
              Question: {query}
              Given a user, extract the time from the question.
              The current time is {now}.
              Format the time as HH:MM. 
              """
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"Given a query, extract the time from the query. The current time is {now}.",
                ),
                ("human", f"{query}"),
            ]
        )

        chain = prompt | base_data.llm
        response = chain.invoke({"input":query})
        print(response)
        return response

    def Cancel_Reminder(self,query):
        pass

    def run(self, query):
        return self.agent_with_message_history.invoke(
            {"input": query},
            {"configurable": {"session_id": "unused"}},
        )

research_agent = ReminderAgent(base_data.llm)
result = research_agent.run("I need to go to Morden Underground Station next Friday at 3 pm.")
print(result)

