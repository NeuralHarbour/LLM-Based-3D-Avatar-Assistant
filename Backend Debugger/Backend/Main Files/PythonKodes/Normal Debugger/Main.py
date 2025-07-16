from typing import Annotated,Literal
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from BASE_DATA import llm,tavily_api_key
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import tempfile, os, platform, subprocess
from langchain_tavily import TavilySearch
import json
import requests
from langchain_core.messages import ToolMessage
from pydantic import BaseModel,Field

class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical", "requests"] = Field(
        ...,
        description="Classify the message type to route to appropriate agent."
    )


class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None
    search_results: list | None
    context: dict | None


def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message as:
            - 'emotional': Emotional support, therapy, feelings, personal problems
            - 'logical': Facts, analysis, explanations, current events, recent information, real-time data that may need web search
            - 'requests': HTTP requests, API calls, web scraping, data fetching from specific URLs
            
            Consider: Does this involve making HTTP requests or API calls? → requests
            Is this about feelings/emotions? → emotional
            Otherwise (including questions that might need web search) → logical
            """
        },
        {"role": "user", "content": last_message.content}
    ])
    return {"message_type": result.message_type}


def router(state: State):
    message_type = state.get("message_type", "logical")
    if message_type == "emotional":
        return {"next": "therapist"}
    elif message_type == "requests":
        return {"next": "requests"}
    return {"next": "logical"}


def therapist_agent(state: State):
    last_message = state["messages"][-1]

    messages = [
        {"role": "system",
         "content": """You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
         },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


def needs_web_search(query: str) -> bool:
    """Determine if a query needs web search based on keywords and context"""
    web_search_indicators = [
        "current", "recent", "latest", "today", "news", "update", "what's happening",
        "stock price", "weather", "breaking", "2024", "2025", "now", "this year",
        "recent developments", "latest news", "current events", "real-time",
        "live", "trending", "status", "current state"
    ]
    
    query_lower = query.lower()
    return any(indicator in query_lower for indicator in web_search_indicators)


def logical_agent(state: State):
    last_message = state["messages"][-1]
    
    # Check if web search is needed
    if needs_web_search(last_message.content):
        return {"next": "logical_web_search"}
    else:
        # Regular logical processing without web search
        messages = [
            {"role": "system",
             "content": """You are a purely logical assistant. Focus only on facts and information.
                Provide clear, concise answers based on logic and evidence.
                Do not address emotions or provide emotional support.
                Be direct and straightforward in your responses."""
             },
            {
                "role": "user",
                "content": last_message.content
            }
        ]
        reply = llm.invoke(messages)
        return {"messages": [{"role": "assistant", "content": reply.content}]}


def logical_web_search(state: State):
    last_message = state["messages"][-1]
    
    # Perform web search
    tavily_search = TavilySearch(api_key=tavily_api_key)
    
    search_query_prompt = f"""
    Extract the main search query from this user message: "{last_message.content}"
    Return only the search query, nothing else.
    """
    
    query_result = llm.invoke([{"role": "user", "content": search_query_prompt}])
    search_query = query_result.content.strip()
    
    try:
        search_results = tavily_search.invoke(search_query)
        formatted_results = []
        for result in search_results[:5]:
            formatted_results.append({
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "url": result.get("url", "")
            })
        
        search_context = "\n".join([
            f"Title: {r['title']}\nContent: {r['content']}\nURL: {r['url']}\n---"
            for r in formatted_results
        ])
        
        messages = [
            {"role": "system",
             "content": f"""You are a logical assistant with access to current information through web search.
             Use the following search results to provide factual, logical answers.
             Be direct and straightforward. Cite your sources when possible.
             
             Search Results:
             {search_context}
             """
             },
            {"role": "user", "content": last_message.content}
        ]
        
        reply = llm.invoke(messages)
        
        return {
            "messages": [{"role": "assistant", "content": reply.content}],
            "search_results": formatted_results
        }
        
    except Exception as e:
        # Fall back to regular logical processing if search fails
        messages = [
            {"role": "system",
             "content": f"""You are a logical assistant. The web search failed with error: {str(e)}
             Provide the best answer you can based on your knowledge, but mention that you couldn't access current information.
             Focus only on facts and information. Be direct and straightforward."""
             },
            {"role": "user", "content": last_message.content}
        ]
        reply = llm.invoke(messages)
        return {"messages": [{"role": "assistant", "content": reply.content}]}


def requests_agent(state: State):
    last_message = state["messages"][-1]
    
    # Check if web search is needed for the request
    if needs_web_search(last_message.content):
        return {"next": "requests_web_search"}
    else:
        # Regular request processing without web search
        analysis_prompt = f"""
        Analyze this user message and determine what action they want: "{last_message.content}"
        
        Common action types:
        - Music: play song, play playlist, stop music, next track, etc.
        - Alarms/Reminders: set alarm, set reminder, schedule task, etc.
        - Communication: call someone, send message, send email, etc.
        - Apps/System: open app, close app, system settings, etc.
        - Calendar: schedule meeting, create event, check calendar, etc.
        
        Extract:
        1. Action type
        2. Specific details (song name, time, contact, etc.)
        3. Any constraints or preferences
        """
        
        analysis_result = llm.invoke([{"role": "user", "content": analysis_prompt}])
        
        messages = [
            {"role": "system",
             "content": f"""You are a helpful assistant that handles action requests.
             You can help with:
             - Music requests (play songs, playlists, control playback)
             - Alarms and reminders (set alarms, schedule reminders)
             - Communication (make calls, send messages)
             - App and system controls
             - Calendar and scheduling
             
             Analysis of their request:
             {analysis_result.content}
             
             Since you can't actually perform these actions, acknowledge the request,
             explain what you would do, and ask for any additional details needed.
             Be helpful and specific about how you would handle their request.
             """
             },
            {"role": "user", "content": last_message.content}
        ]
        
        reply = llm.invoke(messages)
        return {"messages": [{"role": "assistant", "content": reply.content}]}


def requests_web_search(state: State):
    last_message = state["messages"][-1]
    
    # Perform web search for request-related information
    tavily_search = TavilySearch(api_key=tavily_api_key)
    
    search_query_prompt = f"""
    Extract the main search query from this user request: "{last_message.content}"
    Focus on finding current information that would help fulfill their request.
    Return only the search query, nothing else.
    """
    
    query_result = llm.invoke([{"role": "user", "content": search_query_prompt}])
    search_query = query_result.content.strip()
    
    try:
        search_results = tavily_search.invoke(search_query)
        formatted_results = []
        for result in search_results[:5]:
            formatted_results.append({
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "url": result.get("url", "")
            })
        
        search_context = "\n".join([
            f"Title: {r['title']}\nContent: {r['content']}\nURL: {r['url']}\n---"
            for r in formatted_results
        ])
        
        # Analyze the request with search context
        analysis_prompt = f"""
        Analyze this user message and determine what action they want: "{last_message.content}"
        
        Use the following search results to provide current information:
        {search_context}
        
        Common action types:
        - Music: play song, play playlist, stop music, next track, etc.
        - Alarms/Reminders: set alarm, set reminder, schedule task, etc.
        - Communication: call someone, send message, send email, etc.
        - Apps/System: open app, close app, system settings, etc.
        - Calendar: schedule meeting, create event, check calendar, etc.
        
        Extract:
        1. Action type
        2. Specific details (song name, time, contact, etc.)
        3. Any constraints or preferences
        4. Current information that's relevant
        """
        
        analysis_result = llm.invoke([{"role": "user", "content": analysis_prompt}])
        
        messages = [
            {"role": "system",
             "content": f"""You are a helpful assistant that handles action requests with access to current information.
             You can help with:
             - Music requests (play songs, playlists, control playback)
             - Alarms and reminders (set alarms, schedule reminders)
             - Communication (make calls, send messages)
             - App and system controls
             - Calendar and scheduling
             
             Current information from web search:
             {search_context}
             
             Analysis of their request:
             {analysis_result.content}
             
             Since you can't actually perform these actions, acknowledge the request,
             explain what you would do, include relevant current information,
             and ask for any additional details needed.
             Be helpful and specific about how you would handle their request.
             """
             },
            {"role": "user", "content": last_message.content}
        ]
        
        reply = llm.invoke(messages)
        
        return {
            "messages": [{"role": "assistant", "content": reply.content}],
            "search_results": formatted_results
        }
        
    except Exception as e:
        # Fall back to regular request processing if search fails
        analysis_prompt = f"""
        Analyze this user message and determine what action they want: "{last_message.content}"
        
        Common action types:
        - Music: play song, play playlist, stop music, next track, etc.
        - Alarms/Reminders: set alarm, set reminder, schedule task, etc.
        - Communication: call someone, send message, send email, etc.
        - Apps/System: open app, close app, system settings, etc.
        - Calendar: schedule meeting, create event, check calendar, etc.
        
        Extract:
        1. Action type
        2. Specific details (song name, time, contact, etc.)
        3. Any constraints or preferences
        """
        
        analysis_result = llm.invoke([{"role": "user", "content": analysis_prompt}])
        
        messages = [
            {"role": "system",
             "content": f"""You are a helpful assistant that handles action requests.
             The web search failed with error: {str(e)}
             
             You can help with:
             - Music requests (play songs, playlists, control playback)
             - Alarms and reminders (set alarms, schedule reminders)
             - Communication (make calls, send messages)
             - App and system controls
             - Calendar and scheduling
             
             Analysis of their request:
             {analysis_result.content}
             
             Since you can't actually perform these actions, acknowledge the request,
             explain what you would do, and ask for any additional details needed.
             Be helpful and specific about how you would handle their request.
             """
             },
            {"role": "user", "content": last_message.content}
        ]
        
        reply = llm.invoke(messages)
        return {"messages": [{"role": "assistant", "content": reply.content}]}


graph_builder = StateGraph(State)

graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)
graph_builder.add_node("logical_web_search", logical_web_search)
graph_builder.add_node("requests", requests_agent)
graph_builder.add_node("requests_web_search", requests_web_search)

graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")

graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {
        "therapist": "therapist",
        "logical": "logical", 
        "requests": "requests"
    }
)

graph_builder.add_conditional_edges(
    "logical",
    lambda state: state.get("next", "end"),
    {
        "logical_web_search": "logical_web_search",
        "end": END
    }
)

graph_builder.add_conditional_edges(
    "requests",
    lambda state: state.get("next", "end"),
    {
        "requests_web_search": "requests_web_search",
        "end": END
    }
)

graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical_web_search", END)
graph_builder.add_edge("requests_web_search", END)

graph = graph_builder.compile()


# def run_chatbot():
#     state = {"messages": [], "message_type": None}

#     while True:
#         user_input = input("Message: ")
#         if user_input == "exit":
#             print("Bye")
#             break

#         state["messages"] = state.get("messages", []) + [
#             {"role": "user", "content": user_input}
#         ]

#         state = graph.invoke(state)

#         if state.get("messages") and len(state["messages"]) > 0:
#             last_message = state["messages"][-1]
#             print(f"Assistant: {last_message.content}")


# if __name__ == "__main__":
#     run_chatbot()

def open_file_cross_platform(file_path):
    """Open file with default application across different OS"""
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":
            subprocess.run(["open", file_path])
        else:
            subprocess.run(["xdg-open", file_path])
    except Exception as e:
        print(f"Could not open file: {e}")
        print(f"File saved at: {file_path}")

try:
    png_data = graph.get_graph().draw_mermaid_png()
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_file.write(png_data)
        tmp_file_path = tmp_file.name
        open_file_cross_platform(tmp_file_path)
except Exception as e:
    print(f"error : {e}")