from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
import json
from pathlib import Path
from dotenv import load_dotenv
import os

history = ChatMessageHistory()
memory = ConversationBufferMemory(return_messages=True, chat_memory=history, memory_key="chat_history")

load_dotenv(dotenv_path="./API_KEYS.env")
google_api_key = os.environ.get("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in the .env file. Please ensure it's set.")


llm = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    google_api_key=google_api_key,
    temperature=0.3,
    max_retries=2,
    max_output_tokens=2048,  # Limit output size
    # Add request timeout
    request_timeout=30.0
)

def log_conversation(message, response):
    global history
    global memory
    memory.clear()

    new_human_message = {
        "sender": "human",
        "body": message
    }
    new_ai_response = {
        "sender": "ai",
        "body": response
    }

    conversation = {
        "messages": []
    }

    try:
        with open('conversation_log.json', 'r') as file:
            conversation = json.load(file)
    except FileNotFoundError:
        conversation = {"messages": []}

    conversation["messages"].append(new_human_message)
    conversation["messages"].append(new_ai_response)

    with open('conversation_log.json', 'w') as file:
        json.dump(conversation, file)

    messages = conversation["messages"]

    for m in messages:
        if m["sender"] == "human":
            history.add_user_message(m["body"])
        elif m["sender"] == "ai" and m["body"]:
            history.add_ai_message(m["body"])

    return history


def load_memory_from_json(file_path):
    global history
    history = ChatMessageHistory()

    try:
        with open(file_path, 'r') as file:
            conversation = json.load(file)

        for message in conversation.get("messages", []):
            if message["sender"] == "human":
                history.add_user_message(message["body"])
            elif message["sender"] == "ai":
                history.add_ai_message(message["body"])

    except FileNotFoundError:
        print(f"No previous conversation found at {file_path}. Starting fresh.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file at {file_path}. Starting fresh.")

    return history
