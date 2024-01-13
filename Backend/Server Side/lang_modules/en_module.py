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
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

from langdetect import detect
import sys

#######################################################################


yes_no_question_words = ["do","will","would","could","have","did","should","has","Did","Do","Will","Would","Could","Have","Should","Has","have", "was", "were", "might", "must","shall","Are you","is it","can you"]
normal_question_words = ["what","who","where","when","why","how","Can you,","What","Who","Where","When","Why","How","Can you"]

API_KEY = open('PALM_api.txt', 'r').read()
llm = GooglePalm(google_api_key=API_KEY)
llm.temperature = 0.3

last_message = None
last_user_message = None
common_keywords = None
prompt_spam = None
last_three_user_message = None

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
long_no_message = False

#################################################

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful chatbot.Don't use AI as a prefix for messages"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ],
)
chat_history = ChatMessageHistory()
memory = ConversationBufferMemory(return_messages=True,chat_memory=chat_history)
llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,memory = memory)
loaded_model = joblib.load('intent.pkl')



########### DECLARE FUNCTIONS HERE ##############
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
    return messages

async def predict_emotion(word):
    # Suppress specific warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    try:
        # Load the saved model
        with open("emotion_classifier.pkl", "rb") as pipeline_file:
            saved_pipeline = joblib.load(pipeline_file)

        new_data = [word]
        # Make predictions using the loaded model
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

############################################


############### MAIN #######################
async def process_en_message(msg,websocket):
    messages = await load_messages()
    please_say_again_counter = 0
    song_playing = False
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
    

    message = ''.join(msg)
    message_lower = message.lower()
    words = message_lower.split()

    intent = loaded_model.predict([message])[0]
    confidence_scores = loaded_model.predict_proba([message])[0]

    print(f"Predicted Intent: {intent} - Confidence: {max(confidence_scores):.4f}")

    print(f"Data received: {message}")

    if is_yes_no_question:
        expected_response = False
        print("GOT A YES OR NO QUESTION")
        if expected_yes_response:
            words_in_last_message = word_tokenize(last_message.lower())
            if 'yes' in message_lower and len(words) == 1:
                print("LATEST MESSAGE : ",last_message)
                if 'date' in words_in_last_message:
                    date_flag = True
                    if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
                        today_date_flag = True
                    elif any(word in ['yesterday', 'yesterdays','last days'] for word in words_in_last_message):
                        yesterday_date_flag = True
                    elif any(word in ['tomorrow','tomorrows','next days'] for word in words_in_last_message):
                        tomorrow_date_flag = True
                    else:
                        today_date_flag = True

                elif 'time' in words_in_last_message:
                    time_flag = True
                    if any(word in ['current','now'] for word in words_in_last_message):
                        current_time_flag = True
                    else:
                        current_time_flag = True

                elif 'weather' in words_in_last_message:
                    weather_flag = True
                    if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
                        weather_flag = True
                    else:
                        weather_flag = False
                elif 'month' in words_in_last_message:
                    if any(word in ['this', 'current'] for word in words_in_last_message):
                        monthly_flag  = True
                    else:
                        monthly_flag = False
                else:
                    expected_yes_response = False
                             
                    prompt_with_yes = f"Ask me what i want to know ?"
                    prompts = [prompt_with_yes]
                    llm_result = llm_chain({"question": prompts})  
                    generated_response = llm_result['text']
                    generated_response = generated_response.rstrip('.;')
                    await log_conversation(message, generated_response)
                    res = generated_response.split('.')[0].strip()
                    result = await predict_emotion(res)
                    generated_response += f" {result}"
                    expected_yes_response = True
                    print(generated_response)
                    await websocket.send(generated_response)
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
            if 'day' in words_in_last_message:
                day_flag = True
                if any(word in ['today','current'] for word in words_in_last_message):
                    current_day_flag = True
                elif any(word in ['yesterday','last day'] for word in words_in_last_message):
                    yesterday_day_flag = True
                elif any(word in ['tomorrow','next days'] for word in words_in_last_message):
                    tomorrow_day_flag = True
                else:
                    '''
                    stop_words = set(stopwords.words("english"))
                    filtered_words = [word for word in words_in_last_message if word not in stop_words]

                    # Part-of-speech tagging
                    tagged_words = pos_tag(filtered_words)
                    keywords = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]
                    print("Keywords:", keywords)
                    '''
                    day_flag = False
            elif 'time' in words_in_last_message:
                time_flag = True
                if any(word in ['now','current'] for word in words_in_last_message):
                    current_time_flag = True
                elif any(word in ['month', 'year', 'week'] for word in words_in_last_message):
                    monthly_flag = True
                else:
                    prompt_about_question = message
                    llm_result = llm_chain({"question": prompt_about_question})
                    question_response = llm_result['text']
                    await log_conversation(message, question_response)
                    res = question_response.split('.')[0].strip()
                    result = await predict_emotion(res)
                    print(result)
                    day_question_response += f" {result}"
                    await websocket.send(question_response)

            elif 'date' in words_in_last_message:
                date_flag = True
                if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
                    today_date_flag = True
                elif any(word in ['yesterday', 'yesterdays','last days'] for word in words_in_last_message):
                    yesterday_date_flag = True
                elif any(word in ['tomorrow','tomorrows','next days'] for word in words_in_last_message):
                    tomorrow_date_flag = True
                else:
                    today_date_flag = True

            elif 'weather' in words_in_last_message:
                weather_flag = True
                if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
                    weather_flag = True
                else:
                    weather_flag = False

            elif 'month' in words_in_last_message:
                monthly_flag = True
                if any(word in ['this', 'current'] for word in words_in_last_message):
                    monthly_flag  = True
                else:
                    monthly_flag = True

            else:
                response = message
                while response.endswith('?'):
                    prompt_about_question = message
                    llm_result = llm_chain({"question": prompt_about_question})
                    question_response = llm_result['text']
                    await log_conversation(message, response)
                    res = response.split('.')[0].strip()
                    result = await predict_emotion(res)
                    print(result)
                    day_question_response += f" {result}"
                    await websocket.send(question_response)
            expected_response = False
        else:
            pass

    else:
        print("NOT A QUESTION")


    if long_message:
        if 'day' in message_lower:
            day_flag = True
            if any(word in ['today','current'] for word in message_lower):
                current_day_flag = True
            elif any(word in ['yesterday','last day'] for word in message_lower):
                yesterday_day_flag = True
            elif any(word in ['tomorrow','next days'] for word in message_lower):
                tomorrow_day_flag = True
            else:
                '''
                stop_words = set(stopwords.words("english"))
                filtered_words = [word for word in words_in_last_message if word not in stop_words]

                # Part-of-speech tagging
                tagged_words = pos_tag(filtered_words)
                keywords = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]
                print("Keywords:", keywords)
                '''
                day_flag = False

        elif 'date' in message_lower:
            date_flag = True
            if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
                today_date_flag = True
            elif any(word in ['yesterday', 'yesterdays','last days'] for word in message_lower):
                yesterday_date_flag = True
            elif any(word in ['tomorrow','tomorrows','next days'] for word in message_lower):
                tomorrow_date_flag = True
            else:
                today_date_flag = False

        elif 'time' in message_lower:
            time_flag = True
            if any(word in ['current','now'] for word in message_lower):
                current_time_flag = True
            else:
                current_time_flag = True

        elif 'weather' in message_lower:
            weather_flag = True
            if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
                weather_flag = True
            else:
                weather_flag = False

        elif 'month' in message_lower:
            if any(word in ['this', 'current'] for word in message_lower):
                monthly_flag  = True
            else:
                monthly_flag = False
        else:
            expected_yes_response = False
                             
            prompt_with_yes = f"Tell the user that you don't understand"
            prompts = [prompt_with_yes]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            expected_yes_response = True
            print(generated_response)
            await websocket.send(generated_response)
        long_message = False

    if long_no_message:
        if 'day' in message_lower:
            day_flag = True
            if any(word in ['today','current'] for word in message_lower):
                current_day_flag = True
            elif any(word in ['yesterday','last day'] for word in message_lower):
                yesterday_day_flag = True
            elif any(word in ['tomorrow','next days'] for word in message_lower):
                tomorrow_day_flag = True
            else:
                '''
                stop_words = set(stopwords.words("english"))
                filtered_words = [word for word in words_in_last_message if word not in stop_words]

                # Part-of-speech tagging
                tagged_words = pos_tag(filtered_words)
                keywords = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]
                print("Keywords:", keywords)
                '''
                day_flag = False

        elif 'date' in message_lower:
            date_flag = True
            if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
                today_date_flag = True
            elif any(word in ['yesterday', 'yesterdays','last days'] for word in message_lower):
                yesterday_date_flag = True
            elif any(word in ['tomorrow','tomorrows','next days'] for word in message_lower):
                tomorrow_date_flag = True
            else:
                today_date_flag = False

        elif 'time' in message_lower:
            time_flag = True
            if any(word in ['current','now'] for word in message_lower):
                current_time_flag = True
            else:
                current_time_flag = True

        elif 'weather' in message_lower:
            weather_flag = True
            if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
                weather_flag = True
            else:
                weather_flag = False

        elif 'month' in message_lower:
            if any(word in ['this', 'current'] for word in message_lower):
                monthly_flag  = True
            else:
                monthly_flag = False
        else:
            expected_yes_response = False
                             
            prompt_with_yes = f"Tell the user that you don't understand"
            prompts = [prompt_with_yes]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            expected_yes_response = True
            print(generated_response)
            await websocket.send(generated_response)
        long_no_message = False

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
        if len(words) > 1 and any(word in ['now', 'current'] for word in words) or time_flag:
            current_time = datetime.now().strftime("%I:%M %p")
            time_response = f"The time is {current_time}."
            await log_conversation(message, time_response)
            res = time_response.split('.')[0]
            result = await predict_emotion(res)
            print(result)
            time_response += f" {result}"
            await websocket.send(time_response)
            time_flag = False
            current_time_flag = False

        elif len(words) > 1 and any(word in ['month', 'year', 'week'] for word in words)or time_flag:
            prompt_with_time = message
            prompts = [prompt_with_time]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            time_flag = False
            monthly_flag = False
            print(generated_response)
            await websocket.send(generated_response)

        elif len(words) > 1 and 'day' in words or time_flag:
            current_time = datetime.now().strftime("%I:%M %p")
            prompt_with_time = f"Based on the message:{message} tell the time of day with {current_time} whether it is afternoon,morning like that"
            prompts = [prompt_with_time]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            time_flag = False
            print(generated_response)
            await websocket.send(generated_response)

        elif len(words) > 1 and not any(word in ['what','now','current','month','year','week'] for word in words) or time_flag:
            prompt_with_time = f"Based on the message:{message} give an answer"
            prompts = [prompt_with_time]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            time_flag = False
            print(generated_response)
            await websocket.send(generated_response)

        else:
            resp = random.choice(messages['dynamic_responses']['time_questions'])
            expected_yes_response = True
            expected_response = True
            await log_conversation(message, resp)
            res = resp.split('.')[0]
            result = await predict_emotion(res)
            print(result)
            resp += f" {result}"
            await websocket.send(resp)
        time_flag = False

    elif 'month' in words or monthly_flag:
        if 'current' in words or monthly_flag:
            monthly_flag = False
            current_date_obj = datetime.now()
            current_month = current_date_obj.strftime("%B")  # %B gives the full month name
            print(current_month)
            await websocket.send(current_month)
        else:
            prompt_with_time = f"Ask if the user meant the current month"
            prompts = [prompt_with_time]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            time_flag = False
            expected_yes_response = True
            expected_response = True
            print(generated_response)
            await websocket.send(generated_response)

    elif intent == 'Thank':
        if thank_flag:
            prompt_with_no = message
            prompts = [prompt_with_no]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            expected_yes_response = True
            print(generated_response)
            await websocket.send(generated_response)
            thank_flag = False
        else:
            prompt_with_no = f"Ask the user why are you saying thank you when you didnt do any help"
            prompts = [prompt_with_no]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            expected_yes_response = True
            expected_response = True
            print(generated_response)
            await websocket.send(generated_response)

    elif 'no' in words and len(words) == 1:
        if no_flag:
            no_flag = False
            prompt_with_yes = f"Ask me what i want to know ?"
            prompts = [prompt_with_yes]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            expected_yes_response = True
            print(generated_response)
            await websocket.send(generated_response)
        else:
            prompt_with_no = f"I said 'no' without a reason, it's not related to any question.Tell me that i don't understand ask me is there anything specific."
            prompts = [prompt_with_no]
            llm_result = llm_chain({"question": prompts})  
            generated_response = llm_result['text']
            generated_response = generated_response.rstrip('.;')
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            result = await predict_emotion(res)
            generated_response += f" {result}"
            expected_yes_response = True
            print(generated_response)
            await websocket.send(generated_response)


    elif 'date' in words or date_flag:
        if len(words) > 1 or date_flag:
            if any(word in ['today', 'todays','current'] for word in words) or today_date_flag:
                current_date = await get_current_date()
                prompt_with_date = f"Tell the current date {current_date}"
                prompts = [prompt_with_date]
                llm_result = llm_chain({"question": prompts})  
                generated_response = llm_result['text']
                generated_response = generated_response.rstrip('.;')
                await log_conversation(message, generated_response)
                res = generated_response.split('.')[0].strip()
                result = await predict_emotion(res)
                generated_response += f" {result}"
                print(generated_response)
                await websocket.send(generated_response)
                today_date_flag = False
                date_flag = False

            elif any(word in ['yesterday', 'yesterdays'] for word in words) or yesterday_date_flag:
                yesterday_date = datetime.now().date() - timedelta(days=1)
                response = f"tell yesterday's date {yesterday_date.strftime('%Y-%m-%d')}"
                prompts = [response]
                llm_result = llm_chain({"question": prompts})
                generated_response = llm_result['text']
                await log_conversation(message, generated_response)
                res = generated_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                generated_response += f" {result}"
                yesterday_date_flag = False
                date_flag = False
                await websocket.send(generated_response)

            elif any(word in ['tomorrow', 'tomorrows'] for word in words)or tomorrow_date_flag:
                tomorrow_date = datetime.now().date() + timedelta(days=1)
                response = f"tell tomorrows date  {tomorrow_date.strftime('%Y-%m-%d')}"
                prompts = [response]
                llm_result = llm_chain({"question": prompts})
                generated_response = llm_result['text']
                await log_conversation(message, generated_response)
                res = generated_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                date_flag = False
                tomorrow_date_flag = False
                generated_response += f" {result}"
                    
                date_flag = False
                await websocket.send(generated_response)

            else:
                response = f"tell the user that you don't understand"
                prompts=[response]
                llm_result = llm_chain({"question":prompts})
                generated_response = llm_result['text']
                await log_conversation(message, generated_response)
                res = generated_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                generated_response += f" {result}"
                await websocket.send(generated_response)
        else:
            if random.random() < 0.5:
                resp = "Did you mean what is today's date ?"
                expected_yes_response = True
                expected_response = True
                await log_conversation(message, resp)
                res = resp.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                resp += f" {result}"
                await websocket.send(resp)
            else:
                prompt_about_date = "ask the user whether the user meant today's date or something else"
                expected_yes_response = True
                expected_response = True
                llm_result = llm_chain({"question": prompt_about_date})
                generated_response = llm_result['text']
                await log_conversation(message, generated_response)
                res = generated_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                generated_response += f" {result}"
                await websocket.send(generated_response)


    elif intent == 'question' and all(word not in words for word in ['time', 'date','weather','play','pause','resume','yes','sure','certainly','no','ok']):
        if len(words) == 1:
            single_word_response = "It seems you asked a single-word question. Please provide more context for a meaningful response."
            await log_conversation(message, single_word_response)
            res = single_word_response.split('.')[0].strip()
            result = await predict_emotion(res)
            print(result)
            single_word_response += f" {result}"
            await websocket.send(single_word_response)

        else:
            prompts = [message]
            llm_result = llm_chain({"question": message})
            generated_response = llm_result['text']
            qns = word_tokenize(generated_response)
            await log_conversation(message, generated_response)
            res = generated_response.split('.')[0].strip()
            expected_response = True
            expected_yes_response = True
            result = await predict_emotion(res)
            print(result)
            generated_response += f" {result}"
            if '?' in generated_response:
                print("QUESTION FOUND")
            await websocket.send(generated_response)

    elif 'day' in words or day_flag:
        if len(words) > 1 or day_flag:
            if 'today' in words or day_flag:
                day = datetime.today()
                check = calendar.day_name[day.weekday()]
                date_response = f"Today is {check}"
                await log_conversation(message, date_response)
                res = date_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                date_response += f" {result}"
                day_flag = False
                current_day_flag = False
                await websocket.send(date_response)

            elif 'tomorrow' in words or day_flag:
                tomorrow = datetime.today() + timedelta(days=1)
                day_of_week = calendar.day_name[tomorrow.weekday()]
                date_response = f"Tomorrow is {day_of_week}"
                await log_conversation(message, date_response)
                res = date_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                date_response += f" {result}"
                day_flag=False
                tomorrow_day_flag = False
                await websocket.send(date_response)

            elif 'yesterday' in words or day_flag:
                tomorrow = datetime.today() - timedelta(days=1)
                day_of_week = calendar.day_name[tomorrow.weekday()]
                date_response = f"Yesterday was {day_of_week}"
                await log_conversation(message, date_response)
                res = date_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                date_response += f" {result}"
                day_flag=False
                yesterday_day_flag = False
                await websocket.send(date_response)

        else:
            prompt_about_day = f"You don't understand what the user meant Ask what the user wants to know about the day."
            llm_result = llm_chain({"question": prompt_about_day})
            day_question_response = llm_result['text']
            expected_yes_response = True
            expected_response = True
            await log_conversation(message, day_question_response)
            res = day_question_response.split('.')[0].strip()
            result = await predict_emotion(res)
            print(result)
            day_question_response += f" {result}"
            await websocket.send(day_question_response)

    elif 'play' in words:
        play_index = words.index('play')
        if play_index + 1 < len(words):
            song_name = ' '.join(words[play_index + 1:])
            stream(song_name)
            song_playing = True
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

    elif 'weather' in words and intent == 'question' or weather_flag:
        if len(words) > 1 or weather_flag:
            if 'today' or 'current' or 'todays' in words or weather_flag:
                weather_flag = False
                if 'detailed' in words:
                    x = main_stuff()
                    res = x.split('.')[0]
                    result = await predict_emotion(res)
                    print(result)
                    x += f" {result}"
                    await log_conversation(message, x)
                    await websocket.send(x)
                else:
                    y = main_stuff()
                    index_description = y.find('The overall condition is described as')
                    if index_description != -1:
                        index_full_stop = y.find('.', index_description)
                        if index_full_stop != -1:
                            extracted_message = y[:index_full_stop + 1].strip()
                            res = extracted_message.split('.')[0]
                            result = await predict_emotion(res)
                            print(result)
                            extracted_message += f" {result}"
                            await log_conversation(message, extracted_message)
                            await websocket.send(extracted_message)
                        else:
                            await log_conversation(message, y)
                            await websocket.send(y)
                    else:
                        await log_conversation(message, y)
                        await websocket.send(y)
            else:
                response = "Sorry I am unable to get the weather forecast.I will be able to help you with today's weather"
                res = response.split('.')[0]
                result = await predict_emotion(res)
                print(result)
                response += f" {result}"
                await log_conversation(message, response)
                await websocket.send(response)
        else:
            if random.random() < 0.5:
                resp = "Did you mean what is today's weather ?"
                expected_yes_response = True
                expected_respone = True
                await log_conversation(message, resp)
                res = resp.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                resp += f" {result}"
                await websocket.send(resp)
            else:
                prompt_about_date = "ask whether the user meant today's weather"
                expected_yes_response = True
                expected_respone = True
                llm_result = llm_chain({"question": prompt_about_date})
                generated_response = llm_result['text']
                await log_conversation(message, generated_response)
                res = generated_response.split('.')[0].strip()
                result = await predict_emotion(res)
                print(result)
                generated_response += f" {result}"
                await websocket.send(generated_response)

    else:
        if any(greeting in message_lower for greeting in ['good morning', 'good afternoon', 'good evening', 'good night']) and intent == 'greet':
            if 'good ' + time_of_day not in message_lower:
                correction = random.choice(messages['corrections']).format(time_of_day=time_of_day, greeting=message_lower)
                await log_conversation(message, correction)
                res = correction.split('.')[0]
                result = await predict_emotion(correction)
                print(result)
                correction += f" {result}"
                await websocket.send(correction)

            if random.random() < 0.5:
                response = random.choice(messages['salutations'][f'good_{time_of_day}'])
                res = response.split('.')[0]
                result = await predict_emotion(response)
                response += f" {result}"
                print(result)
            else:
                prompts = [message]
                llm_result = llm_chain({"question": message})
                response = llm_result['text']
                res = response.split('.')[0].strip()
                result = await predict_emotion(response)
                print(result)
                response += f" {result}"
            await log_conversation(message, response)
            await websocket.send(response)

        elif 'good night' in message_lower and time_of_day not in ['night', 'evening']:
            correction = random.choice(messages['corrections']).format(time_of_day=time_of_day, greeting=message_lower)
            await log_conversation(message, correction)
            res = correction.split('.')[0]
            result = await predict_emotion(res)
            print(result)
            correction += f" {result}"
            await websocket.send(correction)


        elif len(words) == 1:
            for key, options in messages['greetings'].items():
                if key in message_lower:
                    response = random.choice(options)
                    res = response.split('.')[0]
                    result = await predict_emotion(res)
                    print(result)
                    response += f" {result}"
                    break
            else:
                response = random.choice(messages['dynamic_responses']['default'])
                expected_yes_response = True
                expected_response=True
                res = response.split('.')[0]
                result = await predict_emotion(res)
                print(result)
        else:
            response = random.choice(messages['dynamic_responses']['default'])
            expected_yes_response = True
            expected_response=True
            res = re.split('[.,]', response)[0]
            result = await predict_emotion(res)
            print(result)
            response += f" {result}"
        await log_conversation(message, response)
        await websocket.send(response)
        