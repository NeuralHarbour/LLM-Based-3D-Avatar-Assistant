import sys
sys.path.append('../en_module_files')
import en_module as en
import re
from global_contstants import send_response_with_LLM

async def music_identifier(message,last_message,websocket):
    random_request = [f"Is the following message asking to play a random song ? Reply with 'yes' or 'no' only.\n\nMessage: {message}"]
    song_name_result = en.llm._generate(random_request)
    song_name_check = song_name_result.generations[0][0].text.lower()

    if song_name_check == 'yes':
        random_request = [f"Recoomend a good song to listen to for the user.Only print the song name along with the artist"]
        random_name_result = en.llm._generate(random_request)
        random_name_check = random_name_result.generations[0][0].text.lower()
        song_name = random_name_check
        en.play_flag = True
        en.special_music_case1 = True
    else:

        check_music_name = [f"Does the message: {message} contain the name of the song or an album? Reply with 'yes' or 'no' only"]
        song_name_result = en.llm._generate(check_music_name)
        song_name_check = song_name_result.generations[0][0].text.lower()

        if song_name_check == 'yes':
            en.play_flag = True

        else:
            get_music_name_from_last_reply = [f"Does the last reply contain a song name ? Reply with a 'yes' or 'no' Last Reply: {last_message}"]
            name_last_reply = en.llm._generate(get_music_name_from_last_reply)
            name_check = name_last_reply.generations[0][0].text.lower()

            if name_check == 'yes':
                ask_yourself_check = [f"Does the last reply ask the user whether you should play it or not ? Reply with a 'yes' or 'no' Last Reply : {last_message}"]
                check_reply = en.llm._generate(ask_yourself_check)
                name_check = check_reply.generations[0][0].text.lower()

                if name_check == 'yes':
                    print("MUSIC QUESTION DETEKTED")
                else:
                    is_user_asking = [f"Is the user asking to play it ? Reply with a 'yes' or 'no' Message:{message}"]
                    name_last_reply = en.llm._generate(is_user_asking)
                    name_check = name_last_reply.generations[0][0].text.lower()
                    if name_check == 'yes':
                        music_name_from_last_reply = [f"Get the song name from last reply: {last_message}"]
                        name_last_reply = en.llm._generate(music_name_from_last_reply)
                        name_check = name_last_reply.generations[0][0].text.lower()
                        song_name = name_check
                        print("KUNTENTZ OF DA VERIYABLE SONG NEIM : ",song_name)
                        en.play_flag = True
                        en.song_enquiry = True
            else:
                is_user_asking_song = [f"is the user simply asking to play a song regardless of his/her favourite song ?.Reply with a 'yes' or 'no' message:{message}"]
                song_reply = en.llm._generate(is_user_asking_song)
                song_check = song_reply.generations[0][0].text.lower()
                if song_check == "yes": 
                    prompt_unknown = f"Get the song name from the user"
                    res_final = await send_response_with_LLM(message,prompt_unknown)
                    await websocket.send(res_final)
                    en.expecting_song_name = True
                    en.message = "None"
                else:
                    is_user_asking_favourite_song = [f"is the user is asking to play his/her favourite song. Reply with a 'yes' or 'no' message:{message}"]
                    name_last_reply = en.llm._generate(is_user_asking_favourite_song)
                    name_check = name_last_reply.generations[0][0].text.lower()
                    if name_check == 'yes':
                        find_song = f"Find the favourite song name from the previous messages based on the message reply with the song name.If no song name is found return 'None' message : {message}"
                        res_final = await en.conversation_LLM(message,find_song)
                        if 'None' not in res_final:
                            res_final_str = ''.join(res_final)
                            cleaned_string = re.sub(r'(\[.*?\]|AI:)', '', res_final_str)
                                
                            print(cleaned_string)

                            song_name = cleaned_string
                            en.play_flag = True
                            en.special_music_case1 = True
                        else:
                            print("YOU DON'T HAVE ANY FAVOURITES")
                    else:
                        check_music_name = f"Get the name of the song or album from the user.If the user requests a random song give a random song name of your choice"
                        res_final = await send_response_with_LLM(message,check_music_name)
                        await websocket.send(res_final)