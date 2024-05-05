#################################################################################################################################################################
'''
 /$$   /$$                                        /$$       /$$   /$$                     /$$                                  /$$$$$$  /$$$$$$
| $$$ | $$                                       | $$      | $$  | $$                    | $$                                 /$$__  $$|_  $$_/
| $$$$| $$  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$ | $$      | $$  | $$  /$$$$$$   /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$       | $$  \ $$  | $$  
| $$ $$ $$ /$$__  $$| $$  | $$ /$$__  $$|____  $$| $$      | $$$$$$$$ |____  $$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$      | $$$$$$$$  | $$  
| $$  $$$$| $$$$$$$$| $$  | $$| $$  \__/ /$$$$$$$| $$      | $$__  $$  /$$$$$$$| $$  \__/| $$  \ $$| $$  \ $$| $$  \__/      | $$__  $$  | $$  
| $$\  $$$| $$_____/| $$  | $$| $$      /$$__  $$| $$      | $$  | $$ /$$__  $$| $$      | $$  | $$| $$  | $$| $$            | $$  | $$  | $$  
| $$ \  $$|  $$$$$$$|  $$$$$$/| $$     |  $$$$$$$| $$      | $$  | $$|  $$$$$$$| $$      | $$$$$$$/|  $$$$$$/| $$            | $$  | $$ /$$$$$$
|__/  \__/ \_______/ \______/ |__/      \_______/|__/      |__/  |__/ \_______/|__/      |_______/  \______/ |__/            |__/  |__/|______/

©2024 NEURAL HARBOUR AI
'''

#################################################################################################################################################################

'''
 __                              __      _                  ___      _       _   
/ _\ ___ _ ____   _____ _ __    /__\ __ | |_ _ __ _   _    / _ \___ (_)_ __ | |_ 
\ \ / _ \ '__\ \ / / _ \ '__|  /_\| '_ \| __| '__| | | |  / /_)/ _ \| | '_ \| __|
_\ \  __/ |   \ V /  __/ |    //__| | | | |_| |  | |_| | / ___/ (_) | | | | | |_ 
\__/\___|_|    \_/ \___|_|    \__/|_| |_|\__|_|   \__, | \/    \___/|_|_| |_|\__|
                                                  |___/                          
'''

################## PACKAGE IMPORTS #######################
import asyncio
import websockets
import json

import re
import sys

sys.path.append('lang_modules')

#------------LANGUAGE MODULES---------#
import jp_module
import en_module
#-------------------------------------#

already_initialized = False
initial_message = "None"
initial_response = "None"
############### MAIN #######################
async def on_message(websocket):
    async for message in websocket:
        print(f"Data received: {message}")
        
        start = message.rfind('[')
        end = message.rfind(']')

        language = None
        if start != -1 and end != -1 and start < end:
            language = message[start:end + 1]
            message = message[:start] + message[end + 1:]  # Remove language tag from message
            print(f"Detected language: {language}")
        else:
            print("Language tag not found or invalid format")

        words  = message.split()
        if language == '[en]' or language == '[te]':
            if len(words) >=15:
                await websocket.send("I can't process this message")
            else:
                await en_module.process_en_message(message, websocket,callback = handle_received_message)
                continue

        elif language == '[ja]':
            print("Switching To Japanese Server")
            jp_message_lower = message.lower()
            jp_words = jp_message_lower.split()
            await jp_module.process_japanese_message(jp_words, websocket)
            continue

        elif language == '[zh]':
            print("Switching to Chinese Server")
            break

        elif language == '[ru]':
            print("Switching to Russian Server")
            break

        elif language == '[es]':
            print("Switching to Spanish Server")
            break

        else:
            print("Unsupported language")

async def handle_received_message(websocket, received_message):
    print("RECIEVED A KOLLBAK")
    message = received_message
    print(f"Data received: {message}")
        
    start = message.rfind('[')
    end = message.rfind(']')

    language = None
    if start != -1 and end != -1 and start < end:
        language = message[start:end + 1]
        message = message[:start] + message[end + 1:]  # Remove language tag from message
        print(f"Detected language: {language}")
    else:
        print("Language tag not found or invalid format")

    words  = message.split()
    if language == '[en]' or language == '[te]':
        if len(words) >=7:
            await websocket.send("I can't process this message")
        else:
            await en_module.process_en_message(message, websocket,callback = None)

    elif language == '[jp]':
        print("Switching To Japanese Server")
        jp_message_lower = message.lower()
        jp_words = jp_message_lower.split()
        await jp_module.process_japanese_message(jp_words, websocket)

    elif language == '[zh]':
        print("Switching to Chinese Server")

    elif language == '[ru]':
        print("Switching to Russian Server")

    elif language == '[es]':
        print("Switching to Spanish Server")

    else:
        print("Unsupported language")
    message = None
    print("MESSAGE SET AS NONE")

async def main():
    global already_initialized
    server = await websockets.serve(lambda ws, path: on_message(ws), "localhost", 8080)
    print('Server started')
    print('Listening on 8080')
    if not already_initialized:
        already_initialized = True
        await en_module.log_conversation(initial_message, initial_response)
    else:
        print("Conversation log already initialized.")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())



