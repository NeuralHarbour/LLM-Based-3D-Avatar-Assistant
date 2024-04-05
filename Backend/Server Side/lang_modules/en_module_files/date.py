import sys
sys.path.append('../en_module')
import en_module as en
from datetime import timedelta,datetime
import global_files.global_contstants as gb

async def handle_current_date(message,websocket,callback):
    en.conversation_state = "current date"
    current_date = await en.get_current_date()
    prompt_with_date = f"Tell the current date {current_date}"
    res_final = gb.send_response_with_LLM(message,prompt_with_date)
    await websocket.send(res_final)
    en.today_date_flag = False
    en.date_flag = False

async def handle_current_yesterday(message,websocket,callback):
    en.conversation_state = "yesterdays date"
    yesterday_date = datetime.now().date() - timedelta(days=1)
    response = f"tell yesterday's date {yesterday_date.strftime('%Y-%m-%d')}"
    res_final = gb.send_response_with_LLM(message,response)
    yesterday_date_flag = False
    en.date_flag = False
    await websocket.send(res_final)

async def handle_tomorrow_date(message,websocket,callback):
    en.conversation_state = "tomorrows date"

    tomorrow_date = datetime.now().date() + timedelta(days=1)
    response = f"tell tomorrows date  {tomorrow_date.strftime('%Y-%m-%d')}"
    res_final = gb.send_response_with_LLM(message,response)
    en.date_flag = False
    en.tomorrow_date_flag = False
    await websocket.send(res_final)

async def unexpected_use_case(message,websocket,callback):
    en.conversation_state = None
    prompt_with_time = f"Based on the message:{message} give an answer"
    res_final = await gb.send_response_with_LLM(message,prompt_with_time)
    en.time_flag = False
    await websocket.send(res_final)