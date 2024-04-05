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
from inspect import signature
from multiprocessing import process
import websockets
import random
import yaml
import requests
from datetime import datetime
import json
import joblib
import calendar

#------- LANGCHAIN IMPORTS ---------#
from langchain.embeddings.google_palm import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory
#-----------------------------------#

import warnings
import re
from weather import main_stuff
from spot import stream, pause_and_play, resume_play, stop
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
import spacy

nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
#######################################################################


yes_no_question_words = ["do","will","would","could","have","did","should","has","Did","Do","Will","Would","Could","Have","Should","Has","have", "was", "were", "might", "must","shall","Are you","is it","can you"]
normal_question_words = ["what","who","where","when","why","how","Can you,","What","Who","Where","When","Why","How","Can you"]

co = cohere.Client('jgVbzAZZjadMZW82BWMn50IiUfcDu3yivXlsHOLy')
API_KEY = open('PALM_api.txt', 'r').read()
llm = GooglePalm(google_api_key=API_KEY)
llm.temperature = 0.3

english_words = set(words.words())

with open('country_final.json', encoding='utf-8') as f:
    data = json.load(f)
    print("Loaded COUNTRY.JSON")

with open('./PresetResponses/en.yaml', 'r') as file:
    messages = yaml.safe_load(file)
    print("Loaded RESPONSES.JSON")

countries = {country['name'] for country in data}
cities = {city['name'] for country in data for state in country.get('states', []) for city in state.get('cities', [])}
states = {state['name'] for country in data for state in country.get('states', [])}

valid_cities = {city['name'].lower() for country in data for state in country.get('states', []) for city in state.get('cities', [])}

last_message = None
last_user_message = None
common_keywords = None
prompt_spam = None
last_three_user_message = None
conversation_state = None
x = None
previous_conversation_state = None
received_message = None

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

#################################################
current_time_prompt = datetime.now().strftime("%I:%M %p")
current_date_prompt = datetime.now().strftime("%Y-%m-%d")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"You are a helpful chatbot.Your name is Deborah assume you are virtual human assist the users needs.You are given the following data,The Time : {current_time_prompt},The Date:{current_date_prompt} answer the users question accordingly.If you dont know the answer to a question simply say you dont know"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ],
)
chat_history = ChatMessageHistory()
memory = ConversationBufferMemory(return_messages=True,chat_memory=chat_history)
llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,memory = memory)
loaded_model = joblib.load('intent.pkl')



########### DECLARE FUNCTIONS HERE ##############
async def get_intent(inputs, examples):
    response = co.classify(
      inputs=inputs,
      examples=examples,
    )
    predicted_intent = response[0].predictions if response else None
    return predicted_intent

async def log_conversation(message, response):
    global chat_history
    global is_yes_no_question
    global is_normal_question
    global last_message
    global last_user_message
    global last_three_user_message
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
    prompt = do
    prompts = [prompt]
    llm_result = llm_chain({"question": prompts})  
    generated_response = llm_result['text']
    generated_response = generated_response.rstrip('.;')
    res = generated_response.split('.')
    results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    time_flag = False
    monthly_flag = False
    print(res_final)
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
    is_paused = False

    ## GLOBAL VARIABLES ##

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

    #-------------------------------------------------------------------------------------------------------#
    ########################################## PRESET COMMANDS ##############################################
    if 'please say again' in message_lower or 'server is busy' in message_lower:
        please_say_again_counter += 1
        if please_say_again_counter > 2:
            error_response = "Sorry I am Busy"
            await websocket.send(error_response)
    else:
        please_say_again_counter = 0

    time_of_day = await get_time_of_day()
        
    if 'time' in words or time_flag:
        tokens = nltk.word_tokenize(message)
        tagged = nltk.pos_tag(tokens)
        time_index = [i for i, word in enumerate(tokens) if word.lower() == 'time']

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
                        res_final = await gb.send_response(message,resp)
                        await websocket.send(res_final)
                    else:

                        conversation_state = None

                        expected_yes_response = True
                        expected_response = True
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
                expected_yes_response = True
                expected_response = True
                res_final = await gb.send_response(message, resp)
                await websocket.send(res_final)
                time_flag = False

    elif 'date' in words or date_flag:
        tokens = nltk.word_tokenize(message)
        tagged = nltk.pos_tag(tokens)
        date_index = [i for i, word in enumerate(tokens) if word.lower() == 'date']

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

                        resp = "Did you mean what is today's date ?"
                        expected_yes_response = True
                        expected_response = True
                        res_final = await gb.send_response(message,response)
                        await websocket.send(res_final)
                    else:

                        conversation_state = None

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
        if len(words) == 1:
            prompt_single_question = f"Based on the message:{message} reply accordingly"
            res_final = await gb.send_response_with_LLM(message,prompt_single_question)
            await websocket.send(res_final)
        else:
            for entity_text, entity_type in entities:
                if entity_type == 'DATE':
                    print("Found Date Entity")
                    conversation_state = "question_date"
                    res_final = await gb.send_question_answer(message)
                    await websocket.send(res_final)
                elif entity_type == 'TIME':
                    print("Found Time entity")
                    conversation_state = "question_time"
                    res_final = await gb.send_question_answer(message)
                    await websocket.send(res_final)

            if not entities:

                conversation_state = "question"
                res_final = await gb.send_question_answer(message)
                await websocket.send(res_final)

    elif 'day' in words or day_flag:
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

    elif 'play' in words:
        conversation_state = None
        play_index = words.index('play')
        if play_index + 1 < len(words):
            song_name = ' '.join(words[play_index + 1:])
            stream(song_name)
            song_playing = True
            await log_conversation(message, "Sure")
            await websocket.send("Sure")
        else:
            prompt_music_question = f"Ask the user what you should play based on the message : {message}"
            res_final = await gb.send_response_with_LLM(message,prompt_music_question)
            await websocket.send(res_final)
            expecting_song_name = True

    elif expecting_song_name:
        song_name = message
        stream(song_name)
        song_playing = True
        expecting_song_name = False
        await log_conversation(message, "Sure")
        await websocket.send("Sure")

    elif song_playing:
        if 'pause' in words:
            pause_and_play()
            is_paused = True
            await log_conversation(message, "Sure")
            await websocket.send("Sure")

        elif'resume' in words and is_paused:
            resume_play()
            is_paused = False
            await log_conversation(message, "Sure")
            await websocket.send("Sure")

        elif 'stop' in words:
            stop()
            song_playing = False
            is_paused = False
            await log_conversation(message, "Done")
            await websocket.send("Done")

    elif 'change' in words:
        if 'look' in words:
            conversation_state = None
            await log_conversation(message, "Sure! How do you like my new look")
            await websocket.send("Sure! How do you like my new look")


    elif 'timer' in words:
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
        if 'set' in words:
            print("ALARM REQUEST")
            conversation_state = None
            await log_conversation(message, "Alarm Started")
            await websocket.send("Alarm Started")


    elif 'weather' in words or weather_flag:
        if len(words) > 1 or weather_flag:
            if 'today' or 'current' or 'todays' in words or weather_flag:
                weather_flag = False
                if 'detailed' in words:

                    conversation_state = "detailed weather"

                    x = main_stuff()
                    await log_conversation(message, x)
                    split_pattern = r'(?<!\d)\.(?!\d)'

                    res = re.split(split_pattern, x)
                    results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
                    res_final = '.'.join(results)
                    await websocket.send(res_final)
                else:

                    conversation_state = "less-detailed weather"

                    y = main_stuff()
                    index_description = y.find('The overall condition is described as')
                    if index_description != -1:
                        index_full_stop = y.find('.', index_description)
                        if index_full_stop != -1:
                            extracted_message = y[:index_full_stop + 1].strip()
                            await log_conversation(message, extracted_message)
                            split_pattern = r'(?<!\d)\.(?!\d)'

                            res = re.split(split_pattern, extracted_message)
                            results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
                            res_final = '.'.join(results)
                            await websocket.send(res_final)
                        else:
                            await log_conversation(message, y)
                            await websocket.send(y)
                    else:
                        await log_conversation(message, y)
                        await websocket.send(y)
            else:

                conversation_state = None

                response = "Sorry I am unable to get the weather forecast.I will be able to help you with today's weather"
                res_final = await gb.send_response(message,response)
                await websocket.send(res_final)
        else:
            if random.random() < 0.5:

                conversation_state = None

                resp = "Did you mean what is today's weather ?"
                expected_yes_response = True
                expected_respone = True
                res_final = await gb.send_response(message,response)
                await websocket.send(res_final)
            else:

                conversation_state = None

                expected_yes_response = True
                expected_respone = True
                prompt_about_date = "ask whether the user meant today's weather"
                res_final = await gb.send_response_with_LLM(message,prompt_about_date)
                await websocket.send(res_final)

    else:
        if any(greeting in message_lower for greeting in ['good morning', 'good afternoon', 'good evening', 'good night']) and intent_str == 'greet':
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

            conversation_state = 'salutation-goodnight'

            correction = random.choice(messages['corrections']).format(time_of_day=time_of_day, greeting=message_lower)
            res_final = await gb.send_response(message,correction)
            await websocket.send(res_final)


        elif len(words) == 1: 
            for key, options in messages['greetings'].items():
                if key in message_lower and intent_str=='greet':
                    conversation_state = "start"

                    response = random.choice(options)
                    res_final = await gb.send_response(message,response)
                    await websocket.send(res_final)

                    await asyncio.sleep(5)
                    x = await get_conversation_state(conversation_state,response)

                    print(conversation_state)
                    await websocket.send(str(x))
                    break
            else:
                response = random.choice(messages['dynamic_responses']['default'])
                await log_conversation(message, response)
                conversation_state = None
                expected_yes_response = True
                expected_response=True
                res = response.split('.')
                results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
                res_final = '.'.join(results)
                await websocket.send(res_final)

        elif len(words) > 1: 
            for key, options in messages['greetings'].items():
                if key in message_lower and intent_str=='greet':
                    conversation_state = "start"

                    prompt_about_day = f"The user just greeted and asked you something along with it.Based on the {message} answer accordingly"

                    res_final = await gb.send_response_with_LLM(message,prompt_about_day)
                    await websocket.send(res_final)

        elif intent_str == 'fallback':
            prompt_unknown = f"The user said something you dont understand. Based on the {message} answer accordingly"

            res_final = await gb.send_response_with_LLM(message,prompt_unknown)
            await websocket.send(res_final)

        elif conversation_state == None and (previous_conversation_state != conversation_state) and intent_str == 'fallback':
            conversation_state = None
            response = random.choice(messages['dynamic_responses']['default'])
            await log_conversation(message, response)
            expected_yes_response = True
            expected_response=True
            res = response.split('.')
            results = [f"{await predict_emotion(sentence)}{sentence}" for sentence in res]
            res_final = '.'.join(results)
            await websocket.send(res_final)

    print("CURRENT CONVERSATION STATE : ",conversation_state)
    print("Song Playing : ",song_playing)


    #------------------- TOPIC SELECTOR ----------------------#
    if conversation_state != None and intent_str != 'fallback':
        if previous_conversation_state == conversation_state:
            prmpt = f"Based on the user's query {message} and Based on your last reply : {last_message}.Continue Chatting with Your Friend"
            reply_state = await conversation_LLM(message,prmpt)
            await log_conversation(message,reply_state)
            await websocket.send(reply_state)
    #---------------------------------------------------------#