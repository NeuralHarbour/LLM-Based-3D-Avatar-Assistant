import asyncio
import sys
sys.path.append('../en_module')
import en_module
import global_files.global_contstants as gb


async def handle_yes_response(words_in_last_message, message,websocket):
    if 'date' in words_in_last_message:
        en_module.date_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
            en_module.today_date_flag = True
        elif any(word in ['yesterday', 'yesterdays','last days'] for word in words_in_last_message):
            en_module.yesterday_date_flag = True
        elif any(word in ['tomorrow','tomorrows','next days'] for word in words_in_last_message):
            en_module.tomorrow_date_flag = True
        else:
            en_module.today_date_flag = True

    elif 'time' in words_in_last_message:
        en_module.time_flag = True
        if any(word in ['current','now'] for word in words_in_last_message):
            en_module.current_time_flag = True
        else:
            en_module.current_time_flag = True

    elif 'weather' in words_in_last_message:
        en_module.weather_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
            en_module.weather_flag = True
        else:
            en_module.weather_flag = False
    elif 'month' in words_in_last_message:
        if any(word in ['this', 'current'] for word in words_in_last_message):
            en_module.monthly_flag  = True
        else:
            en_module.monthly_flag = False
    else:
        en_module.expected_yes_response = False
                             
        prompt_with_yes = f"Ask me what i want to know ?"
        res_final = gb.send_response_with_LLM(message,prompt_with_yes)
        await websocket.send(res_final)

async def handle_expected_response(words_in_last_message, message,websocket):
    if 'day' in words_in_last_message:
        en_module.day_flag = True
        if any(word in ['today','current'] for word in words_in_last_message):
            en_module.current_day_flag = True
        elif any(word in ['yesterday','last day'] for word in words_in_last_message):
            en_module.yesterday_day_flag = True
        elif any(word in ['tomorrow','next days'] for word in words_in_last_message):
            en_module.tomorrow_day_flag = True
        else:
            '''
            stop_words = set(stopwords.words("english"))
            filtered_words = [word for word in words_in_last_message if word not in stop_words]

            # Part-of-speech tagging
            tagged_words = pos_tag(filtered_words)
            keywords = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]
            print("Keywords:", keywords)
            '''
            en_module.day_flag = False
    elif 'time' in words_in_last_message:
        en_module.time_flag = True
        if any(word in ['now','current'] for word in words_in_last_message):
            en_module.current_time_flag = True
        elif any(word in ['month', 'year', 'week'] for word in words_in_last_message):
            en_module.monthly_flag = True
        else:
            prompt_about_question = message
            res_final = gb.send_response_with_LLM(message,prompt_about_question)
            await websocket.send(res_final)

    elif 'date' in words_in_last_message:
        en_module.date_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
            en_module.today_date_flag = True
        elif any(word in ['yesterday', 'yesterdays','last days'] for word in words_in_last_message):
            en_module.yesterday_date_flag = True
        elif any(word in ['tomorrow','tomorrows','next days'] for word in words_in_last_message):
            en_module.tomorrow_date_flag = True
        else:
            en_module.today_date_flag = True

    elif 'weather' in words_in_last_message:
        en_module.weather_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in words_in_last_message):
            en_module.weather_flag = True
        else:
            en_module.weather_flag = False

    elif 'month' in words_in_last_message:
        en_module.monthly_flag = True
        if any(word in ['this', 'current'] for word in words_in_last_message):
            en_module.monthly_flag  = True
        else:
            en_module.monthly_flag = True

    else:
        response = message
        while response.endswith('?'):
            prompt_about_question = message
            res_final = gb.send_response_with_LLM(message,prompt_about_question)
            await websocket.send(res_final)
    expected_response = False

async def handle_long_message(message,message_lower, websocket):
    if 'day' in message_lower:
        en_module.day_flag = True
        if any(word in ['today','current'] for word in message_lower):
            en_module.current_day_flag = True
        elif any(word in ['yesterday','last day'] for word in message_lower):
            en_module.yesterday_day_flag = True
        elif any(word in ['tomorrow','next days'] for word in message_lower):
            en_module.tomorrow_day_flag = True
        else:
            '''
            stop_words = set(stopwords.words("english"))
            filtered_words = [word for word in words_in_last_message if word not in stop_words]

            # Part-of-speech tagging
            tagged_words = pos_tag(filtered_words)
            keywords = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]
            print("Keywords:", keywords)
            '''
            en_module.day_flag = False

    elif 'date' in message_lower:
        en_module.date_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
            en_module.today_date_flag = True
        elif any(word in ['yesterday', 'yesterdays','last days'] for word in message_lower):
            en_module.yesterday_date_flag = True
        elif any(word in ['tomorrow','tomorrows','next days'] for word in message_lower):
            en_module.tomorrow_date_flag = True
        else:
            en_module.today_date_flag = False

    elif 'time' in message_lower:
        en_module.time_flag = True
        if any(word in ['current','now'] for word in message_lower):
            en_module.current_time_flag = True
        else:
            en_module.current_time_flag = True

    elif 'weather' in message_lower:
        en_module.weather_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
            en_module.weather_flag = True
        else:
            en_module.weather_flag = False

    elif 'month' in message_lower:
        if any(word in ['this', 'current'] for word in message_lower):
            en_module.monthly_flag  = True
        else:
            en_module.monthly_flag = False
    else:
        en_module.expected_yes_response = False
                             
        prompt_with_yes = f"Tell the user that you don't understand"
        res_final = gb.send_response_with_LLM(message,prompt_with_yes)
        await websocket.send(res_final)
    en_module.long_message = False

async def handle_no_long_message(message,message_lower, websocket):
    if 'day' in message_lower:
        en_module.day_flag = True
        if any(word in ['today','current'] for word in message_lower):
            en_module.current_day_flag = True
        elif any(word in ['yesterday','last day'] for word in message_lower):
            en_module.yesterday_day_flag = True
        elif any(word in ['tomorrow','next days'] for word in message_lower):
            en_module.tomorrow_day_flag = True
        else:
            '''
            stop_words = set(stopwords.words("english"))
            filtered_words = [word for word in words_in_last_message if word not in stop_words]

            # Part-of-speech tagging
            tagged_words = pos_tag(filtered_words)
            keywords = [word for word, tag in tagged_words if tag.startswith('NN') or tag.startswith('JJ')]
            print("Keywords:", keywords)
            '''
            en_module.day_flag = False

    elif 'date' in message_lower:
        en_module.date_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
            en_module.today_date_flag = True
        elif any(word in ['yesterday', 'yesterdays','last days'] for word in message_lower):
            en_module.yesterday_date_flag = True
        elif any(word in ['tomorrow','tomorrows','next days'] for word in message_lower):
            en_module.tomorrow_date_flag = True
        else:
            en_module.today_date_flag = False

    elif 'time' in message_lower:
        en_module.time_flag = True
        if any(word in ['current','now'] for word in message_lower):
            en_module.current_time_flag = True
        else:
            en_module.current_time_flag = True

    elif 'weather' in message_lower:
        en_module.weather_flag = True
        if any(word in ['today', 'todays', 'current', "today's"] for word in message_lower):
            en_module.weather_flag = True
        else:
            en_module.weather_flag = False

    elif 'month' in message_lower:
        if any(word in ['this', 'current'] for word in message_lower):
            en_module.monthly_flag  = True
        else:
            en_module.monthly_flag = False
    else:
        en_module.expected_yes_response = False
                             
        prompt_with_yes = f"Tell the user that you don't understand"
        res_final = gb.send_response_with_LLM(message,prompt_with_yes)
        await websocket.send(res_final)
    en_module.long_no_message = False