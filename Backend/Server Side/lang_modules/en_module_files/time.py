import random
import asyncio
from datetime import datetime
import sys
sys.path.append('../en_module')
import en_module as en
import time
import global_files.global_contstants as gb

async def handle_current_time_request(message, websocket, callback):
    start_time = time.time()
    en.conversation_state = "time"

    current_time = datetime.now().strftime("%I:%M %p")
    time_response = f"The time is {current_time}."
    x = await gb.send_response(message,time_response)
    await websocket.send(x)

    try:
        received_message = await asyncio.wait_for(websocket.recv(), timeout=5)
        print("Received message within 5 seconds:", received_message)
        if callback:
            await callback(websocket, received_message)
    except asyncio.TimeoutError:
        start_time = time.time()
        print("No message received within 5 seconds")
        x = await en.get_conversation_state(en.conversation_state, time_response)
        await websocket.send(str(x))
        print(en.conversation_state)
    en.time_flag = False
    en.current_time_flag = False

async def handle_time_of_day(message,websocket,callback):
    en.conversation_state = "time of the day"

    current_time = datetime.now().strftime("%I:%M %p")
    prompt_with_time = f"Based on the message:{message} tell the time of day with {current_time} whether it is afternoon,morning like that"
    res_final = await gb.send_response_with_LLM(message,prompt_with_time)
    en.time_flag = False

    await websocket.send(res_final)

async def unexpected_use_case(message,websocket,callback):
    en.conversation_state = None
    prompt_with_time = f"Based on the message:{message} give an answer"
    res_final = await gb.send_response_with_LLM(message,prompt_with_time)
    en.time_flag = False
    await websocket.send(res_final)

async def handle_time_duration_request(message, websocket, callback):
    words = message.lower().split()
    duration_words = ['hours', 'minutes', 'seconds']
    duration_unit = [word for word in words if word in duration_words]

    if duration_unit:
        duration_unit = duration_unit[0]
        response = f"Based on the message '{message}', give an answer"
        res_final = await gb.send_response_with_LLM(message,response)
        await websocket.send(res_final)
    else:
        response = "I'm sorry, I couldn't understand the time duration you're asking about. Could you rephrase your request?"
        await websocket.send(response)

