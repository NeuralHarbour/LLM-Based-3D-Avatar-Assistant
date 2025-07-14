from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from BASE_DATA import llm
from langgraph.graph.message import add_messages
import tempfile
import os
import subprocess
import platform

class State(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str

def classify_intent(state: State):
    """Enhanced intent classification for character assistant"""
    last_msg = state["messages"][-1]["content"].lower()
    
    # Audio/Music intents
    if any(phrase in last_msg for phrase in ["play music", "start music", "music on"]):
        intent = "play_music"
    elif any(phrase in last_msg for phrase in ["volume up", "louder", "increase volume"]):
        intent = "audio_volume_up"
    elif any(phrase in last_msg for phrase in ["volume down", "quieter", "decrease volume"]):
        intent = "audio_volume_down"
    elif any(phrase in last_msg for phrase in ["mute", "silence", "volume off"]):
        intent = "audio_volume_mute"
    elif any(phrase in last_msg for phrase in ["play audiobook", "start audiobook", "audiobook"]):
        intent = "play_audiobook"
    elif any(phrase in last_msg for phrase in ["play radio", "start radio", "radio on"]):
        intent = "play_radio"
    elif any(phrase in last_msg for phrase in ["play podcast", "start podcast", "podcast"]):
        intent = "play_podcasts"
    elif any(phrase in last_msg for phrase in ["music settings", "audio settings"]):
        intent = "music_settings"
    elif any(phrase in last_msg for phrase in ["like this song", "love this music"]):
        intent = "music_likeness"
    elif any(phrase in last_msg for phrase in ["dislike this song", "hate this music", "skip this"]):
        intent = "music_dislikeness"
    elif any(phrase in last_msg for phrase in ["what song", "music query", "what's playing"]):
        intent = "music_query"
    
    # IoT/Smart Home intents
    elif any(phrase in last_msg for phrase in ["turn on lights", "lights on", "hue on"]):
        intent = "iot_hue_lighton"
    elif any(phrase in last_msg for phrase in ["turn off lights", "lights off", "hue off"]):
        intent = "iot_hue_lightoff"
    elif any(phrase in last_msg for phrase in ["dim lights", "lights dim", "darker"]):
        intent = "iot_hue_lightdim"
    elif any(phrase in last_msg for phrase in ["brighten lights", "lights up", "brighter"]):
        intent = "iot_hue_lightup"
    elif any(phrase in last_msg for phrase in ["change light color", "light color"]):
        intent = "iot_hue_lightchange"
    elif any(phrase in last_msg for phrase in ["turn on wemo", "wemo on", "plug on"]):
        intent = "iot_wemo_on"
    elif any(phrase in last_msg for phrase in ["turn off wemo", "wemo off", "plug off"]):
        intent = "iot_wemo_off"
    elif any(phrase in last_msg for phrase in ["make coffee", "start coffee", "brew coffee"]):
        intent = "iot_coffee"
    elif any(phrase in last_msg for phrase in ["start cleaning", "vacuum", "clean house"]):
        intent = "iot_cleaning"
    
    # Calendar intents
    elif any(phrase in last_msg for phrase in ["set appointment", "schedule meeting", "add event"]):
        intent = "calendar_set"
    elif any(phrase in last_msg for phrase in ["check calendar", "what's scheduled", "my appointments"]):
        intent = "calendar_query"
    elif any(phrase in last_msg for phrase in ["cancel appointment", "remove event", "delete meeting"]):
        intent = "calendar_remove"
    
    # Alarm intents
    elif any(phrase in last_msg for phrase in ["set alarm", "wake me up", "alarm for"]):
        intent = "alarm_set"
    elif any(phrase in last_msg for phrase in ["check alarm", "what alarms", "alarm status"]):
        intent = "alarm_query"
    elif any(phrase in last_msg for phrase in ["remove alarm", "cancel alarm", "delete alarm"]):
        intent = "alarm_remove"
    
    # Social intents
    elif any(phrase in last_msg for phrase in ["check facebook", "social media", "what's happening"]):
        intent = "social_query"
    elif any(phrase in last_msg for phrase in ["post to facebook", "share on social", "post update"]):
        intent = "social_post"
    
    # Email intents
    elif any(phrase in last_msg for phrase in ["send email", "email to", "write email"]):
        intent = "email_sendemail"
    elif any(phrase in last_msg for phrase in ["check email", "any emails", "email inbox"]):
        intent = "email_query"
    elif any(phrase in last_msg for phrase in ["add contact", "new contact", "save contact"]):
        intent = "email_addcontact"
    elif any(phrase in last_msg for phrase in ["find contact", "contact info", "phone number"]):
        intent = "email_querycontact"
    
    # List management intents
    elif any(phrase in last_msg for phrase in ["add to list", "create list", "new list"]):
        intent = "lists_createoradd"
    elif any(phrase in last_msg for phrase in ["remove from list", "delete from list"]):
        intent = "lists_remove"
    elif any(phrase in last_msg for phrase in ["check list", "what's on list", "show list"]):
        intent = "lists_query"
    
    # Weather and news intents
    elif any(phrase in last_msg for phrase in ["weather", "forecast", "temperature"]):
        intent = "weather_query"
    elif any(phrase in last_msg for phrase in ["news", "headlines", "what's happening"]):
        intent = "news_query"
    
    # Transport intents
    elif any(phrase in last_msg for phrase in ["call taxi", "uber", "lyft", "ride"]):
        intent = "transport_taxi"
    elif any(phrase in last_msg for phrase in ["traffic", "road conditions", "commute"]):
        intent = "transport_traffic"
    elif any(phrase in last_msg for phrase in ["buy ticket", "book ticket", "travel ticket"]):
        intent = "transport_ticket"
    elif any(phrase in last_msg for phrase in ["transport info", "bus schedule", "train times"]):
        intent = "transport_query"
    
    # Food intents
    elif any(phrase in last_msg for phrase in ["order food", "takeaway", "delivery"]):
        intent = "takeaway_order"
    elif any(phrase in last_msg for phrase in ["restaurant", "where to eat", "food nearby"]):
        intent = "takeaway_query"
    elif any(phrase in last_msg for phrase in ["recipe", "how to cook", "cooking instructions"]):
        intent = "cooking_recipe"
    elif any(phrase in last_msg for phrase in ["cooking tips", "cooking help", "kitchen advice"]):
        intent = "cooking_query"
    
    # Q&A intents
    elif any(phrase in last_msg for phrase in ["what is", "define", "definition"]):
        intent = "qa_definition"
    elif any(phrase in last_msg for phrase in ["calculate", "math", "solve"]):
        intent = "qa_maths"
    elif any(phrase in last_msg for phrase in ["currency", "exchange rate", "convert money"]):
        intent = "qa_currency"
    elif any(phrase in last_msg for phrase in ["stock price", "shares", "market"]):
        intent = "qa_stock"
    elif re.search(r'\b(who|what|when|where|why|how)\b', last_msg):
        intent = "qa_factoid"
    
    # Entertainment intents
    elif any(phrase in last_msg for phrase in ["play game", "start game", "game"]):
        intent = "play_game"
    elif any(phrase in last_msg for phrase in ["movie recommendation", "what movie", "film suggestion"]):
        intent = "recommendation_movies"
    elif any(phrase in last_msg for phrase in ["event recommendation", "what to do", "activities"]):
        intent = "recommendation_events"
    elif any(phrase in last_msg for phrase in ["place recommendation", "where to go", "locations"]):
        intent = "recommendation_locations"
    
    # Time/Date intents
    elif any(phrase in last_msg for phrase in ["what time", "current time", "time now"]):
        intent = "datetime_query"
    elif any(phrase in last_msg for phrase in ["convert time", "timezone", "time conversion"]):
        intent = "datetime_convert"
    
    # General intents
    elif any(phrase in last_msg for phrase in ["hello", "hi", "hey", "good morning", "good evening"]):
        intent = "general_greet"
    elif any(phrase in last_msg for phrase in ["joke", "funny", "make me laugh"]):
        intent = "general_joke"
    elif any(phrase in last_msg for phrase in ["something weird", "be quirky", "random"]):
        intent = "general_quirky"
    
    # Default fallback
    else:
        intent = "unknown"
    
    return {"intent": intent}

def handle_audio_volume_up(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🔊 Volume increased! The sound is now louder."}]}

def handle_audio_volume_down(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🔉 Volume decreased! The sound is now quieter."}]}

def handle_audio_volume_mute(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🔇 Audio muted! Everything is now silent."}]}

def handle_play_music(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🎵 Playing your favorite music! Enjoy the tunes."}]}

def handle_play_audiobook(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "📚 Starting your audiobook! Get comfortable and enjoy the story."}]}

def handle_play_radio(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "📻 Radio is now playing! Tuned to your favorite station."}]}

def handle_play_podcasts(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🎙️ Starting your podcast! Time for some interesting conversations."}]}

def handle_iot_hue_lighton(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "💡 Lights are now on! The room is illuminated."}]}

def handle_iot_hue_lightoff(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🌙 Lights are now off! The room is dark and cozy."}]}

def handle_iot_hue_lightdim(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🔅 Lights dimmed! Perfect ambiance for relaxation."}]}

def handle_iot_hue_lightup(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🔆 Lights brightened! The room is now well-lit."}]}

def handle_iot_coffee(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "☕ Coffee maker started! Your fresh brew will be ready soon."}]}

def handle_calendar_set(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "📅 Event added to your calendar! I'll remind you when it's time."}]}

def handle_weather_query(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🌤️ Today looks partly cloudy with a high of 72°F. Perfect weather for outdoor activities!"}]}

def handle_general_greet(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "Hello there! 👋 I'm your friendly character assistant. How can I help you today?"}]}

def handle_general_joke(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "Why don't scientists trust atoms? Because they make up everything! 😄"}]}

def handle_qa_maths(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🧮 I'd love to help with your math problem! What calculation would you like me to solve?"}]}

def handle_play_game(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🎮 Game time! What would you like to play? I can suggest some fun options!"}]}

def handle_news_query(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "📰 Here are today's top headlines: Technology advances, weather updates, and local community news!"}]}

def handle_takeaway_order(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🍕 I can help you order food! What type of cuisine are you in the mood for?"}]}

def handle_recommendation_movies(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🎬 Based on your preferences, I recommend checking out some popular recent releases or classic favorites!"}]}

def handle_transport_taxi(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🚗 I can help you call a ride! Where would you like to go?"}]}

def handle_alarm_set(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "⏰ Alarm set! I'll make sure to wake you up at the right time."}]}

def handle_email_sendemail(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "📧 I can help you compose an email! Who would you like to send it to?"}]}

def handle_lists_createoradd(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "📝 List updated! I've added that item to your list."}]}

def handle_cooking_recipe(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "👨‍🍳 I'd love to help you cook! What dish would you like to prepare?"}]}

def handle_datetime_query(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🕐 The current time is 2:30 PM on a lovely Monday afternoon!"}]}

def handle_music_settings(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🎵 Music settings adjusted! Your audio preferences have been updated."}]}

def handle_general_quirky(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🤪 Did you know that honey never spoils? Archaeologists have found edible honey in ancient Egyptian tombs! How's that for quirky?"}]}

def fallback(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "🤔 I'm not quite sure what you'd like me to do. Could you try rephrasing that? I'm here to help!"}]}


graph_builder = StateGraph(State)
graph_builder.add_node("classify_intent", classify_intent)

intent_handlers = {
    "audio_volume_up": handle_audio_volume_up,
    "audio_volume_down": handle_audio_volume_down,
    "audio_volume_mute": handle_audio_volume_mute,
    "play_music": handle_play_music,
    "play_audiobook": handle_play_audiobook,
    "play_radio": handle_play_radio,
    "play_podcasts": handle_play_podcasts,
    "iot_hue_lighton": handle_iot_hue_lighton,
    "iot_hue_lightoff": handle_iot_hue_lightoff,
    "iot_hue_lightdim": handle_iot_hue_lightdim,
    "iot_hue_lightup": handle_iot_hue_lightup,
    "iot_coffee": handle_iot_coffee,
    "calendar_set": handle_calendar_set,
    "weather_query": handle_weather_query,
    "general_greet": handle_general_greet,
    "general_joke": handle_general_joke,
    "qa_maths": handle_qa_maths,
    "play_game": handle_play_game,
    "news_query": handle_news_query,
    "takeaway_order": handle_takeaway_order,
    "recommendation_movies": handle_recommendation_movies,
    "transport_taxi": handle_transport_taxi,
    "alarm_set": handle_alarm_set,
    "email_sendemail": handle_email_sendemail,
    "lists_createoradd": handle_lists_createoradd,
    "cooking_recipe": handle_cooking_recipe,
    "datetime_query": handle_datetime_query,
    "music_settings": handle_music_settings,
    "general_quirky": handle_general_quirky,
    "unknown": fallback
}

for intent_name, handler_func in intent_handlers.items():
    graph_builder.add_node(intent_name, handler_func)

graph_builder.add_conditional_edges(
    "classify_intent",
    lambda state: state["intent"],
    {intent_name: intent_name for intent_name in intent_handlers}
)


graph_builder.add_edge(START, "classify_intent")

for intent_name in intent_handlers.keys():
    graph_builder.add_edge(intent_name, END)

graph = graph_builder.compile()


# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
#         for value in event.values():
#             print("Assistant : ", value["messages"][-1].content)
# 
# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break
#         stream_graph_updates(user_input)
#     except:
#         user_input = "What do you know about LangGraph?"
#         print("User: " + user_input)
#         stream_graph_updates(user_input)
#         break

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
except:
    pass