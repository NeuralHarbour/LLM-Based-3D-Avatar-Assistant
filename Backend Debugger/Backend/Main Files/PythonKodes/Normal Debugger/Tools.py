from BASE_DATA import tavily_api_key, llm, State
from langchain_tavily import TavilySearch
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from typing import Optional, List
import requests
from datetime import datetime
import json
import random
from time_utils import find_location
import pytz
from tzlocal import get_localzone
import ntplib
from weather_utils import get_weather


# Web Search Tool
try:
    tavily_tool = TavilySearch(
        api_key=tavily_api_key, 
        max_results=3,
        search_depth="advanced" if tavily_api_key else "basic",
        include_answer=True,
        include_raw_content=False
    )
except Exception as e:
    print(f"Warning: Tavily search tool initialization failed: {e}")
    # Create a dummy tool if Tavily fails
    @tool
    def tavily_tool(query: str) -> str:
        """Fallback search tool when Tavily is not available"""
        return f"Search functionality temporarily unavailable for query: {query}"

@tool
def get_current_local_time() -> str:
    """Get precise current time for user's local location"""
    try:
        local_tz = get_localzone()
        current_time = datetime.now(local_tz)
        time_str = current_time.strftime('%I:%M %p').lstrip('0')
        return f"It's currently {time_str} here."
    except Exception as e:
        print(f"Local time lookup error: {e}")
        return "I couldn't determine the local time."

@tool
def get_time_for_location(user_input: str) -> str:
    """Get precise current time for specified places/countries"""
    try:
        location = find_location(user_input)
        if not location:
            raise ValueError("No location found")
            
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        ntp_time = datetime.fromtimestamp(response.tx_time)

        tz = pytz.timezone(location['Timezone'])
        localized_time = ntp_time.astimezone(tz)

        location_parts = []
        if 'City' in location:
            location_parts.append(location['City'])
        if 'State' in location:
            location_parts.append(location['State'])
        if 'Country' in location:
            location_parts.append(location['Country'])
        
        location_str = ", ".join(location_parts)
        time_str = localized_time.strftime('%I:%M %p').lstrip('0')
        
        return f"It's currently {time_str} in {location_str}."
    
    except Exception as e:
        print(f"Location time lookup error: {e}")
        return "I couldn't find the time for that location."

@tool
def get_current_local_date() -> str:
    """Get current date for user's local location"""
    try:
        local_tz = get_localzone()
        current_time = datetime.now(local_tz)
        date_str = current_time.strftime('%A, %B %d, %Y')
        return f"Today is {date_str} here."
    except Exception as e:
        print(f"Local date lookup error: {e}")
        return "I couldn't determine today's date."

@tool
def get_date_for_location(user_input: str) -> str:
    """Get current date for specified places/countries"""
    try:
        location = find_location(user_input)
        if not location:
            raise ValueError("No location found")
            
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        ntp_time = datetime.fromtimestamp(response.tx_time)

        tz = pytz.timezone(location['Timezone'])
        localized_time = ntp_time.astimezone(tz)
        
        location_parts = []
        if 'City' in location:
            location_parts.append(location['City'])
        if 'State' in location:
            location_parts.append(location['State'])
        if 'Country' in location:
            location_parts.append(location['Country'])
        
        location_str = ", ".join(location_parts)
        date_str = localized_time.strftime('%A, %B %d, %Y')
        return f"In {location_str}, today is {date_str}."
    except Exception as e:
        print(f"Location date lookup error: {e}")
        return "I couldn't find the date for that location."

@tool
def get_current_date() -> str:
    """Get current date (general purpose, uses local time)"""
    try:
        local_tz = get_localzone()
        current_time = datetime.now(local_tz)
        date_str = current_time.strftime('%A, %B %d, %Y')
        return f"Today is {date_str}."
    except Exception as e:
        print(f"Date lookup error: {e}")
        return "I couldn't determine today's date."

@tool
def get_weather_info(city_name: Optional[str] = None, language: str = "en") -> str:
    """
    Get current weather information for a city or user's current location.
    
    Args:
        city_name: Name of the city to get weather for. If None, uses user's current location.
        language: Language code for weather descriptions (en, fr, es, de, ja, etc.)
    
    Returns:
        Weather report string with temperature, humidity, wind speed, and conditions
    """
    try:
        weather_result = get_weather(city_name, language)
        return weather_result
    except Exception as e:
        return f"Error getting weather information: {str(e)}"


tools_list = [
    tavily_tool,               # Web search tool
    
    # Time-related tools
    get_current_local_time,    # Gets local time only
    get_time_for_location,     # Gets time for specified locations
    
    # Date-related tools
    get_current_local_date,    # Gets local date only
    get_date_for_location,    # Gets date for specified locations
    get_current_date,         # General date tool (local time as fallback)

    #Weather tools
    get_weather_info
    
    # Add other tools here as needed
]

tools_node = ToolNode(tools=tools_list)
llm_with_tools = llm.bind_tools(tools_list)


__all__ = [
    'tools_node', 
    'llm_with_tools', 
    'tools_list',
    'should_use_tools',
    'tavily_tool',
    'get_current_time',
    'get_weather_info', 
    'create_reminder',
    'search_music',
    'get_contact_info',
    'calculate_math',
    'get_app_info',

]