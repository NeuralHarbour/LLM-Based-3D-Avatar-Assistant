from datetime import datetime,timedelta
import sys
sys.path.append('../en_module')
import en_module as en
import calendar

async def handle_current_day(message,websocket,callback):
    en.conversation_state = "current day"
    day = datetime.today()
    check = calendar.day_name[day.weekday()]
    date_response = f"Today is {check}"
    await en.log_conversation(message, date_response)
    res = date_response.split('.')
    results = [f"{await en.predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    en.day_flag = False
    en.current_day_flag = False
    await websocket.send(res_final)

async def handle_tomorrow_day(message,websocket,callback):
    en.conversation_state = "day tomorrow"
    tomorrow = datetime.today() + timedelta(days=1)
    day_of_week = calendar.day_name[tomorrow.weekday()]
    date_response = f"Tomorrow is {day_of_week}"
    await en.log_conversation(message, date_response)
    res = date_response.split('.')
    results = [f"{await en.predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    en.day_flag=False
    en.tomorrow_day_flag = False
    await websocket.send(res_final)

async def handle_yesterday_day(message,websocket,callback):
    en.conversation_state = "day yesterday"
    tomorrow = datetime.today() - timedelta(days=1)
    day_of_week = calendar.day_name[tomorrow.weekday()]
    date_response = f"Yesterday was {day_of_week}"
    await en.log_conversation(message, date_response)
    res = date_response.split('.')
    results = [f"{await en.predict_emotion(sentence)}{sentence}" for sentence in res]
    res_final = '.'.join(results)
    en.day_flag=False
    en.yesterday_day_flag = False
    await websocket.send(res_final)