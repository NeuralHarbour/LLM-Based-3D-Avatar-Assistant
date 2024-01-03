# module_japanese.py
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------#
'''
     ██╗ █████╗ ██████╗  █████╗ ███╗   ██╗███████╗███████╗███████╗    ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
     ██║██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
     ██║███████║██████╔╝███████║██╔██╗ ██║█████╗  ███████╗█████╗      ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
██   ██║██╔══██║██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ╚════██║██╔══╝      ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚█████╔╝██║  ██║██║     ██║  ██║██║ ╚████║███████╗███████║███████╗    ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
 ╚════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
'''                                                                                                                 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import random
import yaml
from datetime import datetime
from janome.tokenizer import Tokenizer

#----------------重要なキーワード-------------------#
時間_キーワード = ['時間','時刻','何時']
スタンドアロン_グリート = ['こんにちは','やほー','よ']


#------------------------------------------------#

#--------------ここで関数を宣言します----------------#
async def load_messages():
    with open('./PresetResponses/jp.yaml', 'r',encoding='utf-8') as file:
        messages = yaml.safe_load(file)
    return messages

async def get_time_of_day():
    current_time = datetime.now().time()
    if datetime.strptime('21:00:00', '%H:%M:%S').time() <= current_time or current_time < datetime.strptime('01:00:00', '%H:%M:%S').time():
        return '夜'
    elif current_time < datetime.strptime('06:00:00', '%H:%M:%S').time():
        return '夜'  # In case you want to consider early morning hours as night as well
    elif current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
        return '朝'
    elif current_time < datetime.strptime('17:00:00', '%H:%M:%S').time():
        return '午後'
    else:
        return '夕方'


async def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date

#-------------------------------------------------#

#---------------日本語テキストの処理-----------------#
async def process_japanese_message(message, websocket):
    messages = await load_messages()
    tokenizer = Tokenizer()
    tokens = []
    jp_message_lower = ' '.join(message)
    jp_words = tokenizer.tokenize(jp_message_lower)
    for token in jp_words:
        tokens.append(token.surface)
    print(tokens)

    #*********** 独立した単語を処理する ***********#
    if len(tokens) == 1:
        print("Received Standalone")
        if any(言葉 in 時間_キーワード for 言葉 in tokens):
            resp = random.choice(messages['dynamic_responses']['時間_質問'])
            await websocket.send(resp)

        elif any(言葉 in スタンドアロン_グリート for 言葉 in tokens):
            for key, options in messages['jp_greetings'].items():
                if key in jp_message_lower:
                    response = random.choice(options)
                    await websocket.send(response)
        else:
            response = random.choice(messages['dynamic_responses']['デフォルト'])
            await websocket.send(response)
    #*******************************************#

    #************プリセットコマンド****************#
    for i in range(len(tokens) - 1):
        if (
            (tokens[i] == '何' and tokens[i+1] == '時') or 
            (tokens[i] == '時間') or 
            (tokens[i] == "時刻") or 
            (tokens[i] == "何時")
        ):  
         
            current_time = datetime.now().strftime("%I:%M %p")
            time_response = f"時刻は {current_time} です。"
            await websocket.send(time_response)
            continue
        else:
            response = random.choice(messages['dynamic_responses']['デフォルト'])
            await websocket.send(response)
    #********************************************#


#-------------------------------------------------#