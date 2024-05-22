#--------------------------------------------------------------------------------------------------------#

'''

███████╗███╗   ██╗ ██████╗ ██╗     ██╗███████╗██╗  ██╗    ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝████╗  ██║██╔════╝ ██║     ██║██╔════╝██║  ██║    ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
█████╗  ██╔██╗ ██║██║  ███╗██║     ██║███████╗███████║    ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
██╔══╝  ██║╚██╗██║██║   ██║██║     ██║╚════██║██╔══██║    ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████╗██║ ╚████║╚██████╔╝███████╗██║███████║██║  ██║    ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

'''
                                                                                                           
#--------------------------------------------------------------------------------------------------------#



import asyncio
from xml.dom.minidom import Entity
import websockets
import random
import yaml
import requests
from datetime import datetime
import json
import joblib
import calendar
import geocoder

#------- LANGCHAIN IMPORTS ---------#
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder,PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory
from langchain.agents import AgentType, initialize_agent, load_tools


#-----------------------------------#

import warnings
import re
from spot import stream, pause_and_play, resume_play, stop,stream_album
from weather import get_user_city
from datetime import timedelta
import time
import nltk

from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

from langdetect import detect
import sys

import cohere
from cohere.responses.classify import Example

import pytz
import en_module_files.question_check as qn
import en_module_files.time as tm
import en_module_files.date as dt
import en_module_files.day as day
import global_files.global_contstants as gb
import global_files.music_identifier as mi
import global_files.ply_func as ply
import global_files.langchain_tools as l_t
import spacy
from ytmusicapi import YTMusic

import os


nlp = spacy.load("en_core_web_sm")
ytmusic = YTMusic()


#######################################################################


yes_no_question_words = ["do","will","would","could","have","did","should","has","Did","Do","Will","Would","Could","Have","Should","Has","have", "was", "were", "might", "must","shall","Are you","is it","can you"]
normal_question_words = ["what","who","where","when","why","how","Can you,","What","Who","Where","When","Why","How","Can you"]

co = cohere.Client('LgdR8YS9USe6BU9XEAOoj873Wo8iCdavKkplpFxg')
API_KEY = open('PALM_api.txt', 'r').read()
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=API_KEY, temperature=0.3)

english_words = set(words.words())

with open('country_final.json', encoding='utf-8') as f:
    data = json.load(f)
    print("Loaded COUNTRY.JSON")

with open('./PresetResponses/en.yaml', 'r') as file:
    messages = yaml.safe_load(file)
    print("Loaded RESPONSES.JSON")
    print("Loaded CONVERSATION.JSON")

countries = {country['name'] for country in data}
cities = {city['name'] for country in data for state in country.get('states', []) for city in state.get('cities', [])}
states = {state['name'] for country in data for state in country.get('states', [])}
valid_cities = {city['name'].lower() for country in data for state in country.get('states', []) for city in state.get('cities', [])}


playlist_extension = ".xtx"
playlist_path = r'D:/3DavatarAssistant/Backend/Server Side/Playlists/'

last_message = None
last_user_message = None
common_keywords = None
prompt_spam = None
last_three_user_message = None
conversation_state = None
x = None
previous_conversation_state = None
received_message = None
place_name = None
current_playlist = None
OBTAINED_LANG_TO = None
OBTAINED_LANG_FROM = None
message = None
############## GLOBAL BOOLEAN ###################

is_yes_no_question = False
is_normal_question = False
expected_yes_response = False
expected_response = False
time_flag = False
day_flag = False
date_flag = False
today_date_flag = False
tomorrow_date_flag = False
yesterday_date_flag = False
current_time_flag = False
no_flag = False
current_day_flag = False
tomorrow_day_flag = False
yesterday_day_flag = False
monthly_flag = False
thank_flag = False
weather_flag = False
is_spamming = False
long_message = False
state_changed = False
long_no_message = False
song_playing = False
expecting_song_name = False
is_paused = False
play_flag = False
play_album = False
song_enquiry = False
special_music_case1 = False
repeat_flag = False
silent_flag = False
expecting_playlist_name = False
just_created_playlist = False
REALTIME_TRANSLATION = False
#################################################
current_time_prompt = datetime.now().strftime("%I:%M %p")
current_date_prompt = datetime.now().strftime("%Y-%m-%d")

os.environ["OPENWEATHERMAP_API_KEY"] = "0045edc38259072fdc9fbfd7d6655d70"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"You are a helpful chatbot.Your name is Deborah assume you are virtual human assist the users needs.You are given the following data,The Time : {current_time_prompt},The Date:{current_date_prompt} answer the users question accordingly,You have the ability to do many things such as play music,create playlists etc.If you dont know the answer to a question simply say you dont know"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ],
)

intent_prompt_template = (
    "Classify the intent of what the user is referring to based on the message: '{message}'. "
    "You are given the following intents 'WEATHER','SONG','PLAYLIST','TRANSLATE','NEWS','QUESTION','TIME','DATE','SCHEDULE','SILENT','REPEAT','ALARM','TIMER','CHANGE LOOK','GREET'. "
    "Reply with one of these."
)

chat_history = ChatMessageHistory()
memory = ConversationBufferMemory(return_messages=True,chat_memory=chat_history,memory_key="chat_history")
llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,memory = memory)
loaded_model = joblib.load('intent.pkl')

tools = load_tools(["openweathermap-api"], llm)
weather_chain = initialize_agent(
    tools=tools, llm=llm, agent="conversational-react-description",memory = memory,verbose=True
)
QA_agent = initialize_agent(tools=l_t.tools, llm=llm, agent='conversational-react-description',memory = memory,verbose=True)

########### DECLARE FUNCTIONS HERE ##############
async def get_intent(inputs, examples):
    response = co.classify(
      inputs=inputs,
      examples=examples,
    )
    predicted_intent = response[0].predictions if response else None
    return predicted_intent

def classify_intent(message):
    # Format the prompt
    prompt = intent_prompt_template.format(message=message)
    
    # Generate the intent classification
    intent_result = llm.generate([prompt])
    
    # Extract the response
    intent_response = intent_result.generations[0][0].text.strip().lower()
    
    return intent_response

async def log_conversation(message, response):
    global chat_history
    global memory
    global is_yes_no_question
    global is_normal_question
    global last_message
    global last_user_message
    global last_three_user_message
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
        conversation = {"messages":[]}
    conversation["messages"].append(new_human_message)
    conversation["messages"].append(new_ai_response)
    with open('conversation_log.json', 'w') as file:
        json.dump(conversation, file)

    messages = conversation["messages"]

    for m in messages:
        if m["sender"] == "human":
            chat_history.add_user_message(m["body"])
            last_user_message = m["body"]
        elif m["sender"] == "ai":
            chat_history.add_ai_message(m["body"])
            last_message = m["body"]

    question = last_message
    question = question.lower()
    question = word_tokenize(question)

    first_word = question[0] if question else None

    contains_yes_no = any(x in question for x in yes_no_question_words)
    contains_normal = any(word in question for word in normal_question_words)

    if last_message is None or any(word not in ["do","will","would","could","have","did","should","has","Did","Do","Will","Would","Could","Have","Should","Has","have", "was", "were", "might", "must","shall","Are you","is it","what","who","where","when","why","how","Can you","What","Who","Where","When","Why","How"] for word in last_message.split()):
        thank_flag = False
    else:
        thank_flag = True

    if first_word in yes_no_question_words and last_message.endswith('?'):
        is_yes_no_question = True
        is_normal_question = False

    elif first_word in normal_question_words or last_message.endswith('?'):
        is_normal_question = True
        is_yes_no_question = False
    else:
        is_yes_no_question = False
        is_normal_question = False
    return chat_history

async def load_messages():
    with open('./PresetResponses/en.yaml', 'r') as file:
        messages = yaml.safe_load(file)

        print("LOADED Responses.Json")
    return messages

async def predict_emotion(word):
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    try:
        with open("emotion_classifier.pkl", "rb") as pipeline_file:
            saved_pipeline = joblib.load(pipeline_file)

        new_data = [word]
        predictions = saved_pipeline.predict(new_data)
        return predictions

    except FileNotFoundError:
        print("Model file not found.")
        return None

async def get_time_of_day():
    current_time = datetime.now().time()
    if datetime.strptime('21:00:00', '%H:%M:%S').time() <= current_time or current_time < datetime.strptime('01:00:00', '%H:%M:%S').time():
        return 'night'
    elif current_time < datetime.strptime('06:00:00', '%H:%M:%S').time():
        return 'night'  # In case you want to consider early morning hours as night as well
    elif current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
        return 'morning'
    elif current_time < datetime.strptime('17:00:00', '%H:%M:%S').time():
        return 'afternoon'
    else:
        return 'evening'


async def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date

async def conversation_LLM(message, do):
    prompts = [do]
    llm_result = llm_chain({"question": prompts})  
    generated_response = llm_result['text']
    generated_response = generated_response.rstrip('.;')
    res = generated_response.split('.')
    results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    time_flag = False
    monthly_flag = False
    return res_final

async def get_conversation_state(state, message):
    global conversation_state
    if state == "time":
        print("Conversation state : ", state)

        conversation_state = state
        prompt = f"Continue the conversation based on {message}. The topic is about time. Speak as if you are chatting with a friend.Also Make use of {current_time_prompt} if needed"
        generated_response = await conversation_LLM(message, prompt)

        return generated_response 
        
    elif state == "start":
        print("Conversation state:", state)

        conversation_state = state
        prompt = f"The user just greeted you.The user says {last_message}. Start a conversation by asking like how are you. Dont greet again"
        generated_response = await conversation_LLM(message, prompt)

        return generated_response
        

    elif state == "seasonal":
        print("Conversation state:",state)
        pass

    elif state == "Thenks":
        pass

    elif state == "No":
        pass

    elif state == "current date":
        pass

    elif state == "yesterdays date":
        pass

    elif state == "tomorrows date":
        pass

    elif state == "question":
        pass

    elif state == "current day":
        pass

    elif state == "day tomorrow":
        pass

    elif state == "day yesterday":
        pass

    elif state == "detailed weather":
        pass

    elif state == "less-detailed weather":
        pass

    elif state == "salutation-correction":
        pass

    elif state == "salutation":
        pass

    elif state == "salutation-goodnight":
        pass

    elif state == "foreign_time":
        print("Conversation State:",state)
        conversation_state = state
        pass

    else:
        print("END")
        return None

def find_location(sentence):
    words = sentence.split()
    for length in range(len(words), 0, -1):
        for i in range(len(words) - length + 1):
            phrase = ' '.join(words[i:i + length])
            if phrase.lower() in english_words:
                continue
            
            for country in data:
                if phrase.lower() == country['name'].lower():
                    timezone_str = country['timezones'][0]['zoneName']
                    timezone = pytz.timezone(timezone_str)
                    return {'Country': country['name'], 'Timezone': timezone}
                
                for state in country.get('states', []):
                    if phrase.lower() == state['name'].lower():
                        timezone_str = country['timezones'][0]['zoneName']
                        timezone = pytz.timezone(timezone_str)
                        return {'State': state['name'], 'Country': country['name'], 'Timezone': timezone}
                    
                    for city in state.get('cities', []):
                        if phrase.lower() == city['name'].lower():
                            timezone_str = country['timezones'][0]['zoneName']
                            timezone = pytz.timezone(timezone_str)
                            return {'City': city['name'], 'Country': country['name'], 'Timezone': timezone}
    
    return None

async def play_song(message, websocket):
    conversation_state = None
    artist_name = None
    max_view_count = 0
    max_view_video_id = None
    max_view_track = None
    videoid = None
    global play_album

    prompt_song_name = [f"Extract the song name from the following message: '{message}'. If an artist name is present in the message, extract it as well, separated by a comma. If no artist name is present, return 'none' as the artist name. Don't identify the artist name based on the song name on your own even if you know it'"]
    llm_result = llm._generate(prompt_song_name)
    song_name = llm_result.generations[0][0].text.strip()
    data = song_name.split(',')

    print(f"\033[33mSong Name - {data[0]}\033[0m")
    if len(data) > 1 and data[1].strip():
        artist_name = data[1].strip()
        print(f"\033[33mArtist Name - {artist_name}\033[0m")
    else:
        print(f"\033[33mArtist Name - nothing\033[0m")

    if data[0]:
        search_query = f"{data[0]} {artist_name}" if artist_name else data[0]
        search_results = ytmusic.search(search_query)

        for result in search_results:
            if result.get('resultType') == 'song':
                videoid = result.get('videoId')
                song_name = re.sub(r'[^\w\s]', '', result.get('title'))
                artists = [artist.get('name') for artist in result.get('artists', [])]
                album_name = result.get('album', {}).get('name')
                thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')

                video_details = ytmusic.get_song(videoid)
                view_count_str = video_details.get('microformat').get('microformatDataRenderer').get('viewCount')
                view_count = int(view_count_str.replace(',', ''))

                search_words = data[0].lower().split()
                song_words = song_name.lower().split()

                if artist_name and artist_name.lower() not in ['none', 'nothing']:
                    if any(word in song_words for word in search_words) and any(artist_name.lower() in artist.lower() for artist in artists):
                        if view_count > max_view_count:
                            max_view_count = view_count
                            max_view_video_id = videoid


                else:
                    if view_count > max_view_count:
                        max_view_count = view_count
                        max_view_video_id = videoid

            elif result.get('resultType') == 'album':
                album_name = result.get('title')
                album_artists = [artist.get('name') for artist in result.get('artists', []) if artist.get('name') != 'Album']
                album_thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')
                album_browse_id = result.get('browseId')
                album_id = ytmusic.get_album(album_browse_id)
                album_playlist_id = album_id.get('audioPlaylistId')
                play_album = True


        if max_view_video_id:
            max_view_track = None
            for result in search_results:
                if result.get('resultType') == 'song' and result.get('videoId') == max_view_video_id:
                    videoid = result.get('videoId')
                    song_name = re.sub(r'[^\w\s]', '', result.get('title'))
                    artists = [artist.get('name') for artist in result.get('artists', [])]
                    album_name = result.get('album', {}).get('name')
                    thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')

                    max_view_track = {
                        'videoId': videoid,
                        'Song Name': song_name,
                        'Artist(s)': ', '.join(artists),
                        'Views': max_view_count,
                        'Album': album_name,
                        'Thumbnail URL': thumbnail_url
                    }
                    break

            if max_view_track:
                print('Track with the most views:')
                for key, value in max_view_track.items():
                    print(f'{key}: {value}')
                print()

                stream(max_view_video_id)
                artist_names = max_view_track['Artist(s)']
                song_name = max_view_track['Song Name']
                song_playing = True
        elif play_album:
            print('Album Name:', album_name)
            print('Album Artist(s):', ', '.join(album_artists))
            print('Album Thumbnail URL:', album_thumbnail_url)
            print('Album Playlist ID:', album_playlist_id)
            print()
            song_playing = True
            stream_album(album_playlist_id)
        else:
            stream(videoid)
            print('Video ID : ',videoid)
            print('Song Name : ',song_name)
            print('Artist : ',artists)
            print('Album Name : ',album_name)
            print('Thumbnail URL : ',thumbnail_url)
            song_playing = True

    else:
        prompt_music_question = f"based on your message: '{message}' give an answer"
        res_final = await gb.send_response_with_LLM(message, prompt_music_question)
        await websocket.send(res_final)
        expecting_song_name = True


def is_song_name(message):
    pattern = r'^[\w\s]+$'
    return bool(re.match(pattern, message))


def get_current_time_in_timezone(timezone):
    now = datetime.now(timezone)
    return now.strftime("%I:%M %p")

    
############################################


############### MAIN #######################
async def process_en_message(msg,websocket,callback= None):
    please_say_again_counter = 0
    song_name = None
    ## GLOBAL VARIABLES ##

    global message
    global is_spamming
    global is_yes_no_question
    global is_normal_question
    global common_keywords
    global prompt_spam
    global last_message
    global last_user_message
    global time_flag
    global day_flag
    global date_flag
    global today_date_flag
    global yesterday_date_flag
    global tomorrow_date_flag
    global no_flag
    global current_time_flag
    global current_day_flag
    global tomorrow_day_flag
    global yesterday_date_flag
    global monthly_flag
    global thank_flag
    global weather_flag
    global play_flag
    global long_message
    global long_no_message
    global last_three_messages
    global expected_yes_response
    global expected_response
    global conversation_state
    global x
    global received_message
    global song_playing
    global expecting_song_name
    global is_paused
    global song_enquiry
    global special_music_case1
    global place_name
    global repeat_flag
    global silent_flag
    global playlist_extension
    global playlist_path
    global expecting_playlist_name
    global REALTIME_TRANSLATION
    global OBTAINED_LANG_TO
    global OBTAINED_LANG_FROM

    #######################

    examples = [
        Example("Who is Elon Musk", "question"),
        Example("Who is Ed Sheeran","question"),
        Example("What is Machine Learning", "question"),
        Example("How is this correct", "question"),
        Example("is this hot or cold","question"),
        Example("is it today","question"),
        Example("is it cold ","question"),
        Example("isnt it ","question"),
        Example("Do you think you are good enough","question"),
        Example("whats the wind speed","question"),
        Example("Tell me Todays weather", "query"),
        Example("Current Date", "query"),
        Example("fruit", "fallback"),
        Example("shoe", "fallback"),
        Example("sample tech","fallback"),
        Example("I want to exchange my item for another color", "fallback"),
        Example("I ordered something and it wasn't what I expected. Can I return it?", "fallback"),
        Example("whats your return policy?", "question"),
        Example("Good morning", "greet"),
        Example("Set an alarm", "query"),
        Example("time of the year", "query"),
        Example("tell me about yourself", "query"),
        Example("is my package delayed ?", "question"),
        Example("Hello!", "greet"),
        Example("Hi there!", "greet"),
        Example("Thanks for your help!", "thank"),
        Example("Thank you!", "thank"),
        Example("play","query"),
        Example("play my playlist","query"),
        Example("nevermind dont create it","query"),
        Example("Can you play some music","question"),
        Example("play party rock anthem","query"),
        Example("play cruel angels thesis","query"),
        Example("can you play an instrument","question"),
        Example("can you play football","question"),
        Example("can you put a random song","question"),
        Example("stop","query"),
        Example("can you repeat along with me","question")
    ]

    message = ''.join(msg)
    message_lower = message.lower()
    words = message_lower.split()

    inputs = [message_lower]
    intent = await get_intent(inputs, examples)
    doc = nlp(message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    if entities:
        print("Recognized entities:")
        for entity_text, entity_type in entities:
            print(f"{entity_text} ({entity_type})")
    else:
        print("No entities found.")

    intent_str = str(intent).strip("[]'")
    print(f"Predicted Intent: {intent_str}")

    print(f"Data received: {message}")
    location = find_location(message)
    previous_conversation_state = conversation_state
    print("LAST CONVERSATION STATE : ", previous_conversation_state)

    if is_yes_no_question:
        expected_response = False
        print("GOT A YES OR NO QUESTION")
        if expected_yes_response:
            words_in_last_message = word_tokenize(last_message.lower())
            if 'yes' in message_lower and len(words) == 1:
                await qn.handle_yes_response(words_in_last_message, message, websocket)
            elif 'yes' in message_lower and len(words) > 1:
                long_message = True
            elif 'no' in message_lower and len(words) == 1:
                no_flag = True
            elif 'no' in message_lower and len(words) > 1:
                long_no_message = True
            else:
                expected_yes_response = False
        else:
            print("Recieved Something else")

    elif is_normal_question:
        expected_yes_response = False
        print("GOT A NORMAL QUESTION")
        words_in_last_message = word_tokenize(last_message.lower())
        print(words_in_last_message)
        print("LATEST MESSAGE : ",last_message)
        if expected_response:
            await qn.handle_expected_response(words_in_last_message, message, websocket)
        else:
            pass

    else:
        print("NOT A QUESTION")
    if long_message:
        await qn.handle_long_message(message,message_lower, websocket)

    if long_no_message:
        await qn.handle_no_long_message(message,message_lower, websocket)

    if REALTIME_TRANSLATION:
        TRANSLATE_STOP_COMMAND = [f"Is the user asking to stop the translation in english ? Reply with a 'yes' or 'no' message:{message}"]
        command_result = llm._generate(TRANSLATE_STOP_COMMAND)
        check_response = command_result.generations[0][0].text.lower()

        if check_response == 'yes':
            REALTIME_TRANSLATION = False
            TRANSLATE_TASK = f"The user has asked to stop translating.Reply back based on the message:{message}"
            res_final = await gb.send_response_with_LLM(message,TRANSLATE_TASK)
            await websocket.send(res_final)
        else:
            IDENTIFY_MESSAGE_LANGUAGE = [f"Identify the language of the message.Reply with the name of the language message:{message}"]
            LANG_IDENTIFY_GENERATE = llm._generate(IDENTIFY_MESSAGE_LANGUAGE)
            check_response = LANG_IDENTIFY_GENERATE.generations[0][0].text.lower()

            if check_response == OBTAINED_LANG_TO:
                TRANSLATE_TASK = f"Your task is to perform translation.Translate from {OBTAINED_LANG_TO} to {OBTAINED_LANG_FROM} based on the message:{message}"
                res_final = await gb.send_response_with_LLM(message,TRANSLATE_TASK)
                await websocket.send(res_final)
            else:
                TRANSLATE_TASK = f"Your task is to perform translation.Translate from {OBTAINED_LANG_FROM} to {OBTAINED_LANG_TO} based on the message:{message}"
                res_final = await gb.send_response_with_LLM(message,TRANSLATE_TASK)
                await websocket.send(res_final)

    if expecting_song_name:
        check_song = [f"Identify if the message is a song name or not ? Reply with a 'yes' if it's a song name else 'no' message:{message}"]
        check_result = llm._generate(check_song)
        check_response = check_result.generations[0][0].text.lower()
        if check_response == 'yes':
            print("YES !!!!!!!!")
            play_flag = True
        else:
            print("NOOOOO !!!!")
            expecting_song_name = False

    if expecting_playlist_name:
        PROMPT_RANDOM_NAME = [f"Is the user asking to name the playlist with some random name ? Reply with a 'yes' or 'no' message:{message}"]
        check_result = llm._generate(PROMPT_RANDOM_NAME)
        check_response = check_result.generations[0][0].text.lower()

        if check_response == 'yes':
            PROMPT_SUGGEST_RANDOM = [f"Suggest a random name for the playlist.Reply with the playlist name only"]
            check_result = llm._generate(PROMPT_SUGGEST_RANDOM)
            check_response_ply = check_result.generations[0][0].text.lower()

            playlist_name = check_response_ply
            ply.create_ply(playlist_name,playlist_extension,playlist_path)

            prompt_SUCCESS = f"Tell the user that I have created a playlist named {playlist_name}"
            res_final = await gb.send_response_with_LLM(message,prompt_SUCCESS)
            await websocket.send(res_final)
        else:
            PROMPT_CANCEL = [f"Is the user cancelling the playlist operation ? Reply with a 'yes' or 'no' message:{message}"]
            check_result = llm._generate(PROMPT_CANCEL)
            check_response = check_result.generations[0][0].text.lower()
            if check_response == 'yes':
                prompt_KANCEL = f"The user does not want the playlist to be created reply accordingly based on the message : {message}"
                res_final = await gb.send_response_with_LLM(message,prompt_KANCEL)
                await websocket.send(res_final)
            else:
                PROMPT_QUERY_CHECK = [f"Does the meesage contain the playlist name ? Reply with a 'yes' or 'no' message : {message}"]
                check_result = llm._generate(PROMPT_QUERY_CHECK)
                check_response = check_result.generations[0][0].text.lower()
                if check_response == 'yes':

                    extract_playlist_name = [f"Extract the name of the playlist to be created from the message.Reply with the Playlist name, message:{message}"]
                    extract_playlist_name_generate = llm._generate(extract_playlist_name)
                    extract_playlist_name_result = extract_playlist_name_generate.generations[0][0].text.lower()
                    print("PLAYLIST NAME : ",extract_playlist_name_result)
                    playlist_name = extract_playlist_name_result
                    ply.create_ply(playlist_name,playlist_extension,playlist_path)

                    prompt_SUCCESS = f"Tell the user that I have created a playlist named {playlist_name}"
                    res_final = await gb.send_response_with_LLM(message,prompt_SUCCESS)
                    await websocket.send(res_final)

                else:
                    print("EXITING THE PLAYLIST CREATOR !!!")
                    expecting_playlist_name = False

    #-------------------------------------------------------------------------------------------------------#
    ########################################## PRESET COMMANDS ##############################################

    time_of_day = await get_time_of_day()
   
    intent_response = classify_intent(message)
    print("LLM_INTENT : ",intent_response)

    if not repeat_flag and not expecting_playlist_name:
        expecting_playlist_name = False
        if intent_response == 'translate':      
            QA_ANSWER = QA_agent.run(f"{message}")
            await log_conversation(message,QA_ANSWER)
            await websocket.send(QA_ANSWER)
        elif intent_response == 'weather':
            GET_CITY_NAME = [f"Find the name of the city from the message : {message}.If there is no City return 'None'"]
            RESPONSE_NAME = llm._generate(GET_CITY_NAME)
            RESPONSE = RESPONSE_NAME.generations[0][0].text.lower()

            city_name = RESPONSE
            location = geocoder.ip("me")

            if city_name == 'None':
                WEATHER_RESULT = weather_chain.run(f"{message}")
            else:
                WEATHER_RESULT = weather_chain.run(f"{message} + {location}")

            await log_conversation(message, WEATHER_RESULT)
            res = WEATHER_RESULT.split('.')
            results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
            res_final = '.'.join(results)
            await websocket.send(res_final)
        else:

            if not REALTIME_TRANSLATION:

                if 'time' in words or time_flag:
                    tokens = nltk.word_tokenize(message)
                    tagged = nltk.pos_tag(tokens)
                    time_index = [i for i, word in enumerate(tokens) if word.lower() == 'time']
                    play_flag = False
                    expecting_song_name = False
                    if time_index:
                        time_pos_tag = tagged[time_index[0]][1]
                        if time_pos_tag.startswith('NN'):
                            if len(words) > 1 and any(word in ['now', 'current', 'present', 'today'] for word in words) or time_flag:
                                await tm.handle_current_time_request(message, websocket, callback)

                            elif len(words) > 1 and any(word in ['hours', 'minutes', 'seconds'] for word in words):
                                if any(word in ['current', 'now'] for word in words):
                                    res_final = await tm.handle_current_time_duration_request(message, websocket, callback)
                                else:
                                    await tm.handle_time_duration_request(message, websocket, callback)

                            elif len(words) == 1:
                                if random.random() < 0.5:

                                    conversation_state = None

                                    resp = "Did you mean what the time is ?"
                                    expected_yes_response = True
                                    expected_response = True
                                    expecting_song_name = False
                                    res_final = await gb.send_response(message,resp)
                                    await websocket.send(res_final)
                                else:

                                    conversation_state = None

                                    expected_yes_response = True
                                    expected_response = True
                                    expecting_song_name = False
                                    prompt_about_date = f"ask the user whether I meant the time or something else based on the message:{message}"
                                    res_final = await gb.send_response_with_LLM(message,prompt_about_date)
                                    await websocket.send(res_final)

                            else:
                                await tm.unexpected_use_case(message, websocket, callback)

                        elif time_pos_tag.startswith('JJ'):
                            await tm.unexpected_use_case(message, websocket, callback)

                        elif len(words) > 1 and location:
                            country_name = location.get('Country')
                            state_name = location.get('State')
                            city_name = location.get('City')

                            current_time = get_current_time_in_timezone(location['Timezone'])

                            if city_name:
                                await websocket.send(f"Current time in {city_name}, {country_name} is {current_time}")
                            elif state_name:
                                await websocket.send(f"Current time in {state_name}, {country_name} is {current_time}")
                            elif country_name:
                                await websocket.send(f"Current time in {country_name} is {current_time}")

                        else:
                            conversation_state = None
                            resp = random.choice(messages['dynamic_responses']['time_questions'])
                            expecting_song_name = False
                            expected_yes_response = True
                            expected_response = True
                            res_final = await gb.send_response(message, resp)
                            await websocket.send(res_final)
                            time_flag = False

                elif 'date' in words or date_flag:
                    expecting_song_name = False
                    tokens = nltk.word_tokenize(message)
                    tagged = nltk.pos_tag(tokens)
                    date_index = [i for i, word in enumerate(tokens) if word.lower() == 'date']
                    play_flag = False
                    if date_index:
                        date_pos_tag = tagged[date_index[0]][1]
                        if date_pos_tag.startswith('NN'):
                            if len(words) > 1 and any(word in ['today', 'current', 'present'] for word in words) or today_date_flag:
                                await dt.handle_current_date(message, websocket, callback)

                            elif len(words) > 1 and any(word in ['yesterday', 'yesterdays'] for word in words) or yesterday_date_flag:
                                await dt.handle_yesterday_date(message, websocket, callback)

                            elif len(words) > 1 and any(word in ['tomorrow', 'tomorrows'] for word in words) or tomorrow_date_flag:
                                await dt.handle_tomorrow_date(message, websocket, callback)

                            elif len(words) == 1:
                                if random.random() < 0.5:

                                    conversation_state = None
                                    expecting_song_name = False
                                    resp = "Did you mean what is today's date ?"
                                    expected_yes_response = True
                                    expected_response = True
                                    res_final = await gb.send_response(message,response)
                                    await websocket.send(res_final)
                                else:

                                    conversation_state = None
                                    expecting_song_name = False
                                    expected_yes_response = True
                                    expected_response = True
                                    prompt_about_date = "ask the user whether the user meant today's date or something else"
                                    res_final = await gb.send_response_with_LLM(message,prompt_about_date)
                                    await websocket.send(res_final)

                            else:
                                await dt.unexpected_use_case(message, websocket, callback)

                        elif date_pos_tag.startswith('JJ'):
                            await dt.unexpected_use_case(message, websocket, callback)


                elif intent_str == 'question' and not expecting_song_name:
                    play_flag = False
                    if len(words) == 1:
                        prompt_single_question = f"Based on the message:{message} reply accordingly"
                        res_final = await gb.send_response_with_LLM(message, prompt_single_question)
                        await websocket.send(res_final)
                    else:
                        for entity_text, entity_type in entities:
                            if entity_type == 'DATE':
                                print("Found Date Entity")
                                conversation_state = "question_date"
                                QA_ANSWER = QA_agent.run(f"{message}")
                                await log_conversation(message,QA_ANSWER)
                                await websocket.send(QA_ANSWER)
                            elif entity_type == 'TIME':
                                print("Found Time entity")
                                conversation_state = "question_time"
                                QA_ANSWER = QA_agent.run(f"{message}")
                                await log_conversation(message,QA_ANSWER)
                                await websocket.send(QA_ANSWER)
                            else:
                                expecting_song_name = False
                                play_flag = False
                                QA_ANSWER = QA_agent.run(f"{message}")
                                await log_conversation(message,QA_ANSWER)
                                await websocket.send(QA_ANSWER)


                        if not entities:
                            if song_playing:
                                if 'pause' in words:
                                    if not is_paused:
                                        pause_and_play()
                                        is_paused = True
                                        play_flag = False
                                        await log_conversation(message, "Sure")
                                        await websocket.send("Sure")
                                    else:
                                        play_flag = False
                                        await log_conversation(message, "Song is already paused")
                                        await websocket.send("Song is already paused")

                                elif 'resume' in words:
                                    if is_paused:
                                        resume_play()
                                        is_paused = False
                                        play_flag = False
                                        await log_conversation(message, "Sure")
                                        await websocket.send("Sure")
                                    else:
                                        play_flag = False
                                        await log_conversation(message, "Song is already playing")
                                        await websocket.send("Song is already playing")

                                elif 'stop' in words:
                                    stop()
                                    is_paused = False
                                    play_flag = False
                                    await log_conversation(message, "Done")
                                    await websocket.send("Done")
                                    song_playing = False

                                else:
                                    QA_ANSWER = QA_agent.run(f"{message}")
                                    await log_conversation(message,QA_ANSWER)
                                    await websocket.send(QA_ANSWER)
                                    conversation_state = None

                            else:
                                QA_ANSWER = QA_agent.run(f"{message}")
                                await log_conversation(message,QA_ANSWER)
                                await websocket.send(QA_ANSWER)
                                conversation_state = None

                elif 'day' in words or day_flag:
                    play_flag = False
                    if len(words) > 1 or day_flag:
                        if 'today' in words or day_flag:

                            day.handle_current_day(message,websocket,callback)

                        elif 'tomorrow' in words or day_flag:

                            day.handle_tomorrow_day(message,websocket,callback)

                        elif 'yesterday' in words or day_flag:

                            day.handle_yesterday_day(message,websocket,callback)

                    else:
                        prompt_about_day = f"You don't understand what the user meant Ask what the user wants to know about the day."

                        conversation_state = None

                        expected_yes_response = True
                        expected_response = True
                        res_final = await gb.send_response_with_LLM(message,prompt_about_day)
                        await websocket.send(res_final)

                elif 'change' in words:
                    play_flag = False
                    if 'look' in words:
                        conversation_state = None
                        await log_conversation(message, "Sure! How do you like my new look")
                        await websocket.send("Sure! How do you like my new look")


                elif 'timer' in words:
                    play_flag = False
                    if 'set' in words:
                        print("TIMER REQUEST")
                        conversation_state = None
                        await log_conversation(message, "Timer Started")
                        await websocket.send("Timer Started")
                    elif 'pause' in words:
                        conversation_state = None
                        await log_conversation(message, "Timer Paused")
                        await websocket.send("Timer Paused")
                    elif 'stop' in words:
                        conversation_state = None
                        await log_conversation(message, "Timer Stopped")
                        await websocket.send("Timer Stopped")

                elif 'alarm' in words:
                    play_flag = False
                    if 'set' in words:
                        print("ALARM REQUEST")
                        conversation_state = None
                        await log_conversation(message, "Alarm Started")
                        await websocket.send("Alarm Started")

                else:
                    if any(greeting in message_lower for greeting in ['good morning', 'good afternoon', 'good evening', 'good night']) and intent_str == 'greet':
                        play_flag = False
                        if 'good ' + time_of_day not in message_lower:

                            conversation_state = 'salutation-correction'

                            correction = random.choice(messages['corrections']).format(time_of_day=time_of_day, greeting=message_lower)
                            res_final = await gb.send_response(message,correction)
                            await websocket.send(res_final)

                        if random.random() < 0.5:

                            conversation_state = 'salutation'

                            response = random.choice(messages['salutations'][f'good_{time_of_day}'])
                            res_final = await gb.send_response(message,response)
                            await websocket.send(res_final)
                        else:

                            conversation_state = 'salutation'

                            prompt_greet = message
                            res_final = await gb.send_response(message,res_final)
                            await websocket.send(res_final)

                    elif 'good night' in message_lower and time_of_day not in ['night', 'evening']:
                        play_flag = False
                        expecting_song_name = False
                        conversation_state = 'salutation-goodnight'

                        correction = random.choice(messages['corrections']).format(time_of_day=time_of_day, greeting=message_lower)
                        res_final = await gb.send_response(message,correction)
                        await websocket.send(res_final)


                    elif len(words) == 1 and not any(word in ['pause', 'stop', 'resume','play'] for word in words):
                        play_flag = False
                        for key, options in messages['greetings'].items():
                            if key in message_lower and intent_str=='greet':
                                conversation_state = "start"
                                expecting_song_name = False
                                response = random.choice(options)
                                res_final = await gb.send_response(message,response)
                                await websocket.send(res_final)

                                try:
                                    received_message = await asyncio.wait_for(websocket.recv(), timeout=5)
                                    print("Received message within 5 seconds:", received_message)
                                    if callback:
                                        await callback(websocket, received_message)
                                except asyncio.TimeoutError:
                                    start_time = time.time()
                                    print("No message received within 5 seconds")
                                    x = await get_conversation_state(conversation_state, res_final)
                                    message = ""
                                    await log_conversation(message,x)
                                    await websocket.send(str(x))
                                    print(conversation_state)
                                break

                        else:
                            response = random.choice(messages['dynamic_responses']['default'])
                            await log_conversation(message, response)
                            conversation_state = None
                            expected_yes_response = True
                            expecting_song_name = False
                            play_flag = False
                            expected_response=True
                            res = response.split('.')
                            results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
                            res_final = '.'.join(results)
                            await websocket.send(res_final)

                    elif len(words) > 1: 
                        for key, options in messages['greetings'].items():
                            if key in message_lower and intent_str=='greet':
                                expecting_song_name = False
                                conversation_state = "start"

                                prompt_about_day = f"The user just greeted and asked you something along with it.Based on the {message} answer accordingly"

                                res_final = await gb.send_response_with_LLM(message,prompt_about_day)
                                await websocket.send(res_final)

                    elif conversation_state == None and (previous_conversation_state != conversation_state) and intent_str == 'fallback':
                        conversation_state = None
                        expecting_song_name = False
                        response = random.choice(messages['dynamic_responses']['default'])
                        await log_conversation(message, response)
                        expected_yes_response = True
                        expected_response=True
                        res = response.split('.')
                        results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
                        res_final = '.'.join(results)
                        await websocket.send(res_final)

                    prompt_music_check = [f"Is the following message asking to play music or asking for suggestion? Reply with 'music' or 'suggestion' only .\n\nMessage: {message}"]
                    llm_result = llm._generate(prompt_music_check)
                    if 'music' in llm_result.generations[0][0].text:
                        if len(words) > 1:
                            prompt_music_check = [f"Is the following message asking to play music? Reply with 'yes' or 'no' only.\n\nMessage: {message}"]
                            music_check_result = llm._generate(prompt_music_check)
                            music_check_response = music_check_result.generations[0][0].text.lower()

                            if 'yes' in music_check_response:
                                await mi.music_identifier(message,last_message,websocket)
                            else:
                                if not expecting_song_name:
                                    play_flag = False
                                    expecting_song_name = False
                                    prompt_unknown = f"The user said something you dont understand. Based on the {message} answer accordingly"
                                    res_final = await gb.send_response_with_LLM(message,prompt_unknown)
                                    await websocket.send(res_final)
        
                    else:
                        if song_playing:
                            if 'pause' in words:
                                expecting_song_name = False
                                if not is_paused:
                                    pause_and_play()
                                    is_paused = True
                                    play_flag = False
                                    await log_conversation(message, "Sure")
                                    await websocket.send("Sure")
                                else:
                                    play_flag = False
                                    await log_conversation(message, "Song is already paused")
                                    await websocket.send("Song is already paused")

                            elif 'resume' in words:
                                expecting_song_name = False
                                if is_paused:
                                    resume_play()
                                    is_paused = False
                                    play_flag = False
                                    await log_conversation(message, "Sure")
                                    await websocket.send("Sure")
                                else:
                                    play_flag = False
                                    await log_conversation(message, "Song is already playing")
                                    await websocket.send("Song is already playing")

                            elif 'stop' in words:
                                expecting_song_name = False
                                stop()
                                is_paused = False
                                play_flag = False
                                await log_conversation(message, "Done")
                                await websocket.send("Done")
                                song_playing = False
                            else:
                                repeat_command = [f"check if the user is asking to repeat along with the user based on the message .Reply with a 'yes' or 'no' message:{message}"]
                                repeat_result = llm._generate(repeat_command)
                                check_response = repeat_result.generations[0][0].text.lower()

                                if check_response == "yes":
                                    print("REPEAT MODE")
                                    prompt_repeat = f"Tell the user that you will repeat after the user"
                                    res_final = await gb.send_response_with_LLM(message,prompt_repeat)
                                    await websocket.send(res_final)
                                    repeat_flag = True
                                else:
                                    silent_command = [f"check if the user is asking to be silent based on the message. Reply with a 'yes' or 'no' message:{message}"]
                                    silent_result = llm._generate(silent_command)
                                    check_response = silent_result.generations[0][0].text.lower()
                                    if check_response == "yes":
                                        print("SILENT MODE")
                                        prompt_silent = f"Tell the user that you will be silent"
                                        res_final = await gb.send_response_with_LLM(message,prompt_silent)
                                        await websocket.send(res_final)
                                        silent_flag = True
                                    else:
                                        expecting_song_name = False
                                        play_flag = False
                                        prompt_unknown = f"The user said something you dont understand. Based on the {message} answer accordingly"
                                        res_final = await gb.send_response_with_LLM(message,prompt_unknown)
                                        await websocket.send(res_final)
                        else:
                            repeat_command = [f"check if the user is asking to repeat along with the user based on the message .Reply with a 'yes' or 'no' message:{message}"]
                            repeat_result = llm._generate(repeat_command)
                            check_response = repeat_result.generations[0][0].text.lower()

                            if check_response == "yes":
                                print("REPEAT MODE")
                                prompt_repeat = f"Tell the user that you will repeat after the user"
                                res_final = await gb.send_response_with_LLM(message,prompt_repeat)
                                await websocket.send(res_final)
                                repeat_flag = True
                            else:
                                silent_command = [f"check if the user is asking to be silent based on the message. Reply with a 'yes' or 'no' message:{message}"]
                                silent_result = llm._generate(silent_command)
                                check_response = silent_result.generations[0][0].text.lower()
                                if check_response == "yes":
                                    print("SILENT MODE")
                                    prompt_silent = f"Tell the user that you will be silent"
                                    res_final = await gb.send_response_with_LLM(message,prompt_silent)
                                    await websocket.send(res_final)
                                    silent_flag = True
                                else:
                                    playlist_enquiry = [f"check if the message is a playlist related enquiry ? Reply with a 'yes' or 'no' message:{message}"]
                                    playlist_result = llm._generate(playlist_enquiry)
                                    playlist_response = playlist_result.generations[0][0].text.lower()

                                    if playlist_response == "yes":
                                        playlist_intent = [f"Identify the intention of what the user wants to do with the playist.Reply with 'play_playlist','add_song','create_playlist','del_playlist','del_song','pause_playlist','repeat_playlist'.Anyting other than this comes under 'enquiry_playlist' based on the message:{message}"]
                                        playlist_intent_result = llm._generate(playlist_intent)
                                        playlist_response = playlist_intent_result.generations[0][0].text.lower()

                                        print("PLAYLIST INTENT : ",playlist_response)

                                        if playlist_response == 'create_playlist':
                                            name_contain_ply =[f"Does the message contain a name for the playlist to be created  Reply with a 'yes' or 'no' message:{message}"]
                                            name_contain_ply_check = llm._generate(name_contain_ply)
                                            name_contain_result = name_contain_ply_check.generations[0][0].text.lower()

                                            if name_contain_result == 'yes':
                                                extract_playlist_name_from_last_reply = [f"Does the last reply contain a name for the playlist ? Reply with a 'yes' or 'no' last message:{last_message}"]
                                                extract_playlist_name_generate = llm._generate(extract_playlist_name_from_last_reply)
                                                extract_playlist_name_result = extract_playlist_name_generate.generations[0][0].text.lower()

                                                if extract_playlist_name_result == 'yes':
                                                    USER_CONFIRM = [f"Is the user Insisting to create a playlist with the name from the previous message ? Reply with 'yes' or 'no' message:{message}"]
                                                    USER_CONFIRM_GENERATE = llm._generate(USER_CONFIRM)
                                                    USER_CONFIRM_GENERATE_RESULT = USER_CONFIRM_GENERATE.generations[0][0].text.lower()

                                                    if USER_CONFIRM_GENERATE_RESULT == 'yes':
                                                        extract_playlist_name_from_last_reply = [f"Extract the name of the playlist to be created from the last message.Reply with the Playlist name last message : {last_message}"]
                                                        extract_playlist_name_generate = llm._generate(extract_playlist_name_from_last_reply)
                                                        extract_playlist_name_result = extract_playlist_name_generate.generations[0][0].text.lower()

                                                        previous_playlist_name = extract_playlist_name_result
                                                        ply.create_ply(previous_playlist_name,playlist_extension,playlist_path)

                                                        PROMPT_SUCCESS = f"Tell the user that you have created a playlist named {previous_playlist_name}"
                                                        res_final = await gb.send_response_with_LLM(message,PROMPT_SUCCESS)
                                                        await websocket.send(res_final)
                                                else:
                                                    extract_playlist_name = [f"Extract the name of the playlist to be created from the message.Reply with the Playlist name, message:{message}"]
                                                    extract_playlist_name_generate = llm._generate(extract_playlist_name)
                                                    extract_playlist_name_result = extract_playlist_name_generate.generations[0][0].text.lower()
                                                    print("PLAYLIST NAME : ",extract_playlist_name_result)

                                                    playlist_name = extract_playlist_name_result
                                                    ply.create_ply(playlist_name,playlist_extension,playlist_path)

                                                    PROMPT_SUCCESS = f"Tell the user that you have created a playlist named {playlist_name}"
                                                    res_final = await gb.send_response_with_LLM(message,PROMPT_SUCCESS)
                                                    await websocket.send(res_final)
                                            else:
                                                expecting_playlist_name = True
                                                PROMPT_GET_USER_NAME = f"Ask the user for the name to be given for the playlist"
                                                res_final = await gb.send_response_with_LLM(message, PROMPT_GET_USER_NAME)
                                                await websocket.send(res_final)


                                        elif playlist_response == 'del_playlist':
                                            name_contain_ply =[f"Does the message contain a name for the playlist to be deleted ? Reply with a 'yes' or 'no' message:{message}"]
                                            name_contain_ply_check = llm._generate(name_contain_ply)
                                            name_contain_result = name_contain_ply_check.generations[0][0].text.lower()

                                            if name_contain_result == 'yes':
                                                extract_playlist_name = [f"Extract the name of the playlist to be deleted from the message.Reply with the Playlist name, message:{message}"]
                                                extract_playlist_name_generate = llm._generate(extract_playlist_name)
                                                extract_playlist_name_result = extract_playlist_name_generate.generations[0][0].text.lower()
                                                print("PLAYLIST NAME : ",extract_playlist_name_result)

                                                playlist_name = extract_playlist_name_result
                                        
                                                filepath = os.path.join(playlist_path, playlist_name + playlist_extension)
                                                if os.path.exists(filepath):
                                                    ply.del_ply(playlist_path,playlist_name,playlist_extension)

                                                    PROMPT_SUCCESS = f"Tell the user that you have deleted the playlist"
                                                    res_final = await gb.send_response_with_LLM(message,PROMPT_SUCCESS)
                                                    await websocket.send(res_final)
                                                else:
                                                    print("FILE DOES NOT EXIST")
                                                    PROMPT_GET_FILE_STATUS = f"The file does not exist.Tell the user that the file does not exist it might have been deleted"
                                                    res_final = await gb.send_response_with_LLM(message, PROMPT_GET_USER_NAME)
                                                    await websocket.send(res_final)

                                        elif playlist_response == 'enquiry_playlist':
                                            prompt_unknown = f"The user asked something about the playlist. Based on the {message} answer accordingly"
                                            res_final = await gb.send_response_with_LLM(message,prompt_unknown)
                                            await websocket.send(res_final)

                                        else:
                                            pass

                            
                                    else:
                                        expecting_song_name = False
                                        play_flag = False
                                        prompt_unknown = f"The user said something you dont understand. Based on the {message} answer accordingly"
                                        res_final = await gb.send_response_with_LLM(message,prompt_unknown)
                                        await websocket.send(res_final)


                #------------------- TOPIC SELECTOR ----------------------#
                if conversation_state != None and intent_str != 'fallback':
                    if previous_conversation_state == conversation_state:
                        prmpt = f"Based on the user's query {message} and Based on your last reply : {last_message}.Continue Chatting with Your Friend"
                        reply_state = await conversation_LLM(message,prmpt)
                        message = ""
                        await log_conversation(message,reply_state)
                        await websocket.send(reply_state)
                #---------------------------------------------------------#
    
                if play_flag:
                    song_playing = True
                    if song_enquiry:
                        await play_song(song_name,websocket)
                    elif special_music_case1:
                        await play_song(song_name,websocket)
                    else:
                        await play_song(message,websocket)

                if silent_flag:
                    for entity_text, entity_type in entities:
                        if entity_type == "TIME":
                            print("TIME TO BE SILENT : ",entity_text)
                            try:
                                # Use regular expressions to extract the value and unit
                                pattern = r"(\d+)\s*(\w+)"
                                match = re.match(pattern, entity_text)

                                if match:
                                    value = int(match.group(1))
                                    unit = match.group(2).lower()

                                    # Calculate the countdown time in seconds
                                    if unit.startswith("minute"):
                                        countdown_seconds = value * 60
                                    elif unit.startswith("hour"):
                                        countdown_seconds = value * 3600
                                    else:
                                        print(f"Unknown time unit: {unit}")
                                        continue

                                    # Start the countdown
                                    while countdown_seconds > 0:

                                        try:
                                            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                                            print("MESSAGE RECIEVED DURING SILENCE")
                                            if message:
                                                check_silence_stop = [f"check if the user is asking to stop the silent based on the message. Reply with a 'yes' or 'no' message:{message}"]
                                                silent_result = llm._generate(check_silence_stop)
                                                check_response = silent_result.generations[0][0].text.lower()
                                                print(check_response)
                                                if check_response == 'yes':
                                                    prompt_silence_stop = f"Tell the user that the silence has stopped. Based on the {message} answer accordingly"
                                                    res_final = await gb.send_response_with_LLM(message,prompt_unknown)
                                                    await websocket.send(res_final)
                                                    silent_flag = False
                                                    break
                                                else:
                                                    await websocket.send("SHHH...")
                                        except asyncio.TimeoutError:
                                            remaining_time = timedelta(seconds=countdown_seconds)
                                            print(f"Time remaining: {remaining_time}", end='\r')

                                        # Decrement the countdown time
                                        countdown_seconds -= 1

                                    print("Countdown finished!")
                                else:
                                    print("Invalid time format.")

                            except ValueError:
                                print("Invalid time format.")
                        else:
                            print("TIME TO BE SILENT : ",None)

                    #prompt_music_question = f"Based on the message:{message} get the name of the song.If its a random request give a song"
                    #res_final = await gb.send_response_with_LLM(message, prompt_music_question)
                    #search_results = ytmusic.search(res_final)
                    #is_paused = False
                    #for result in search_results:
                    #    if result.get('resultType') == 'song':
                    #        videoid = result.get('videoId')
                    #        song_name = result.get('title')
                    #        artists = [artist.get('name') for artist in result.get('artists', []) if artist.get('name') != 'Song']
                    #        album_name = result.get('album', {}).get('name')
                    #        thumbnail_url = result.get('thumbnails', [{}])[0].get('url', 'No thumbnail available')
                    #        print('Song Name:', song_name)
                    #        print('Artist(s):', ', '.join(artists))
                    #        print('Album:', album_name)
                    #        print('Thumbnail URL:', thumbnail_url)
                    #        print()
                    #        break
                    #stream(videoid)
                    #await log_conversation(message, f"Sure ... Playing {artists} - {song_name}")
                    #await websocket.send(f"Sure ... Playing {''.join(artists)} - {song_name}")
                    #song_playing = True

                print("CURRENT CONVERSATION STATE : ",conversation_state)
                print("PLAYLIST FLAG STATUS : ",expecting_playlist_name)
                print("CURRENT SONG : ",song_name)
                print("Song Playing : ",song_playing)
                print("Current Playlist : ",current_playlist)

            else:
                print("REALTIME TRANSLATOR ENABLED")
    else:
        if not expecting_playlist_name:
            repeat_command = [f"check if the user is asking to stop repeating based on the message .Reply with a 'yes' or 'no' message:{message}"]
            repeat_result = llm._generate(repeat_command)
            check_response = repeat_result.generations[0][0].text.lower()
            if check_response == "yes":
                prompt_repeat = f"Tell the user that you have stopped repeating after the user"
                res_final = await gb.send_response_with_LLM(message,prompt_repeat)
                await websocket.send(res_final)
                repeat_flag = False
            else:
                await websocket.send(message)
