from email import message
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import sys
import os
import global_contstants as glb
import random
import re
from langchain_core.prompts import PromptTemplate
from langchain.chains import SequentialChain,LLMChain

sys.path.append('../')
import en_module as en


ddg_search = DuckDuckGoSearchRun()
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

#--------CUSTOM LANGCHAIN TOOLS--------#

class SilentHandlerTool(BaseTool):
    """Handle silent mode based on the user's message."""

    name = "silent_handler"
    description = "Handle silent mode based on the user's message"

    def _run(self, message: str) -> str:
        print(f"[DEBUG] SilentHandlerTool received message: {message}")
        repeat_command = [f"Check if the user is asking to be silent with some duration or not. Based on the message:\n\n{message}\n\nReply with 'yes' or 'no'"]
        repeat_result = en.llm._generate(repeat_command)
        repeat_response = repeat_result.generations[0][0].text.lower()
        print(f"[DEBUG] LLM response for silent mode check: {repeat_response}")

        if "yes" in repeat_response:
            en.silent_flag = True
            print("[DEBUG] Silent mode enabled")
            return "SILENT MODE ENABLED"
        else:
            en.silent_flag = False
            print("[DEBUG] Silent mode not requested")
            return "Silent mode not requested."

    async def _arun(self, message: str) -> str:
        raise NotImplementedError("This tool does not support async")

class RepeatHandlerTool(BaseTool):
    name = "repeat_handler"
    description = "Handle repeat mode based on the user's message"

    def _run(self, message: str) -> str:
        print(f"[DEBUG] RepeatHandlerTool received message: {message}")
        repeat_command = [f"Check if the user is asking to repeat based on the message:\n\n{message}\n\nReply with 'yes' or 'no'"]
        repeat_result = en.llm._generate(repeat_command)
        repeat_response = repeat_result.generations[0][0].text.lower()
        print(f"[DEBUG] LLM response for repeat mode check: {repeat_response}")

        if "yes" in repeat_response:
            en.repeat_flag = True
            print("[DEBUG] Repeat mode enabled")
            return "REPEAT MODE ENABLED"
        else:
            en.repeat_flag = False
            print("[DEBUG] Repeat mode not requested")
            return "Repeat mode not requested."

    async def _arun(self, message: str) -> str:
        raise NotImplementedError("This tool does not support async")

'''
Almost plays any music by surfing on the internet to get the details

1.Implemented direct play 
2.Implemented direct random song play
3.Implemented song enquiry
4.Implemented favourite song player
5.Implemented playing songs from a given movie
6.Implemented random song player based on the entities such as date,artist,language etc
7.Now if the user asks to play it after enquiry it will play it
8.Now plays a whole album
9.Recommends song based on the mood

'''
#*********MUSIC FUNCTIONS*************#
class MusicTool(BaseTool):
    name = "music_tool"
    description = "Handle all music-related requests, including playing songs, recommending random songs, and identifying song names."

    def _run(self, message: str) -> str:
        """
        Use the LLM to identify and handle the user's request related to music.
        Args:
            message (str): The user's current message.
        Returns:
            str: A response indicating the action taken or a message to the user.
        """

        print(f"/n[DEBUG] MusicTool received message: {message}")
        if has_song_last_reply(en.last_message):
            song_name_last = extract_song_name_from_message(en.last_message)
            if song_name_last != "none":
                print(f"[DEBUG] Playing specific song from last message : {song_name_last}")
                if is_asking_playing(en.message):
                    en.play_flag = True
                    en.message = song_name_last
                    return f"Playing {song_name_last}"
                else:
                    en.play_flag = False
            else:
                en.play_flag = False
                en.expecting_song_name = True
                return "What song should i play ? "
                
            


        if is_asking_playing(en.message):
            en.play_flag = True
            if check_song_name_in_message(message):
                song_name = extract_song_name_from_message(message)
                if song_name != "none":
                    print(f"[DEBUG] Playing specific song: {song_name}")
                    en.message = song_name
                    return f"Playing {song_name}"

            elif is_asking_favourite_song(message):
                x = check_favourite_song(message)
                if x != "None":
                    print(f"[DEBUG] Playing users favourite song : {x}")
                    en.message = x
                    return f"Playing {x}"
                else:
                    return "You don't have any favourite songs"


            else:
                movie_series_name = extract_movie_series_names(message)
                if movie_series_name != 'None':
                    en.message = movie_series_name
                    return f"Playing {movie_series_name}"
                else:
                    en.play_flag = False
                    en.expecting_song_name = True
                    return "What song should i play ? "

        else:
            en.play_flag = False

    async def _arun(self, message: str) -> str:
        raise NotImplementedError("This tool does not support async")

class Music_random_tool(BaseTool):
    name = "random_music_tool"
    description = "Handles all random music queries"

    def _run(self,message:str) -> str:
        if check_random_song_request(message):
            song_name = recommend_random_song(message)
            print(f"[DEBUG] Random song recommended: {song_name}")
            if is_asking_playing:
                en.play_flag = True
                en.message = song_name
                return f"Playing {song_name}"
            else:
                en.play_flag = False

    async def _arun(self, message: str) -> str:
        raise NotImplementedError("This tool does not support async")

class Music_enquiry_tool(BaseTool):
    name = "music_enquiry_tool"
    description = "Handles all music enquiries"

    def _run(self,message:str) -> str:
        if is_enquiring_song(message):
            search_results = ddg_search.run(message)
            print(f"[DEBUG] searching in duck duck go")

            if search_results:
                return f"{search_results}"
                en.play_flag = False
            else:
                return "No valid music request found."

        print("[DEBUG] No valid music request found")

        return "No valid music request found."

    async def _arun(self, message: str) -> str:
        raise NotImplementedError("This tool does not support async")

def check_random_song_request(message: str) -> bool:
    print(f"[DEBUG] Checking if message requests a random song: {message}")
    prompt = [f"Does the following message imply a request for a random song, even if the word 'random' is not explicitly stated? Reply with 'yes' or 'no' only.\n\nMessage: {message}"]
    result = en.llm._generate(prompt)
    response = result.generations[0][0].text.lower()
    print(f"[DEBUG] LLM response for random song check: {response}")
    return response == 'yes'

def random_song_checks(message: str):

    genre_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message contain a genre ? If so reply with the Genre else None: {input_text}"
    )
    year_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message contain a year or decade such as 80s,90s,2010 like that? If so reply with the year else None: {input_text}"
    )
    season_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message specify a season such as 'christmas','summer' like that ? If so reply with the season else None: {input_text}"
    )
    show_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message specify a tvshow,movie,series,drama,video game or anything like that ? If so reply with the appropriate tag else None: {input_text}"    
    )
    artist_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message specify an artist name ? If so reply with the artist name else None: {input_text}"
    )
    language_prompt = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message specify a language ? If so reply with the name of the language else None: {input_text}"
    )

    keyword_tag = PromptTemplate(
        input_variables=["input_text"],
        template="Does the message specify any keywords like 'hits','popular' etc ? If so reply with the keyword else None: {input_text}"
    )

    genre_chain = LLMChain(prompt=genre_prompt, llm=en.llm, output_key="genre_text")
    year_chain = LLMChain(prompt=year_prompt, llm=en.llm, output_key="year_text")
    season_chain = LLMChain(prompt=season_prompt,llm = en.llm, output_key="season_text")
    show_chain = LLMChain(prompt=show_prompt,llm = en.llm, output_key="show_text")
    artist_chain = LLMChain(prompt=artist_prompt,llm = en.llm, output_key="artist_text")
    language_chain = LLMChain(prompt=language_prompt,llm = en.llm,output_key="language_text")
    keyword_chain = LLMChain(prompt=keyword_tag,llm = en.llm, output_key="keyword_text")

    sequential_chain = SequentialChain(
        chains=[genre_chain, year_chain,season_chain,show_chain,artist_chain,keyword_chain],
        input_variables=["input_text"],
        output_variables=["genre_text", "year_text","season_text","show_text","artist_text","keyword_text","language_text"]
    )

    input_data = {'input_text': message}
    result = sequential_chain.apply([input_data])[0]

    song_info = {
        "song_genre": result.get("genre_text", "None"),
        "song_year": result.get("year_text", "None"),
        "song_season":result.get("season_text","None"),
        "song_show":result.get("show_text","None"),
        "song_artist":result.get("artist_text","None"),
        "song_keyword":result.get("keyword_text","None"),
        "song_language":result.get("language_text","None")
    }

    print("SONG INFO : ",song_info)

    return song_info

def recommend_random_song(message: str) -> str:
    import random
    
    print("[DEBUG] Recommending a random song")
    
    song_info = random_song_checks(message)
    genre = song_info.get("song_genre", None)
    year = song_info.get("song_year", None)
    season = song_info.get("song_season",None)
    show = song_info.get("song_show",None)
    artist = song_info.get("song_artist",None)
    keyword = song_info.get("keyword_text",None)
    language = song_info.get("language_text",None)
    
    song_year = '' if year == 'None' else year
    song_genre = '' if genre == 'None' else genre
    song_season = '' if season == 'None' else season
    song_show = '' if show == 'None' else show
    song_artist = '' if artist == 'None' else artist
    song_keyword = '' if keyword == 'None' else keyword
    song_language = '' if keyword == 'None' else language

    
    search_query = f"random {song_keyword} {song_year} {song_genre} {song_season} {song_show} {song_artist} {song_language} songs list"
    print("SEARCH_QUERY : ", search_query)
    search_results = ddg_search.run(search_query)
    
    song_names_result = LLMChain(
        llm=en.llm,
        prompt=PromptTemplate(
            input_variables=["message", "search_results"],
            template="From the search results, extract the song names and return them separated by newlines:\n\n{search_results}\n\nSong Names:",
        )
    )({"message": search_query, "search_results": search_results})
    
    print(f"[DEBUG] song_names_result: {song_names_result}")
    song_names = song_names_result["text"].split('\n')
    song_names = [song.strip() for song in song_names if song.strip()]
    
    if song_names:
        selected_song = random.choice(song_names)
        print("SELECTED SONG: ", selected_song)
        with_artist_song = extract_song_name_from_message(selected_song)
        return with_artist_song
    else:
        return "None"

def check_favourite_song(message:str) -> bool:
    print("f[DEBUG] Checking for favourite song")
    prompt = [f"Does the previous messages contain the name of the user's favourite song ? Reply with 'yes' or 'no' only message: {message}"]
    result = en.llm._generate(prompt)
    response = result.generations[0][0].text.lower()
    if response == 'yes':
        find_song = f"Extract the favourite song name from the previous messages based on the message reply with the song name.If no song name is found return 'None' message : {message}"
        result = en.llm._generate(prompt)
        response = result.generations[0][0].text.lower()
        if 'None' not in response:
            res_final_str = ''.join(response)
            cleaned_string = re.sub(r'(\[.*?\]|AI:)', '', res_final_str)
                                
            print(cleaned_string)

            song_name = cleaned_string
            return song_name
        else:
            print("YOU DON'T HAVE ANY FAVOURITES")
            return "None"

def check_song_name_in_message(message: str) -> bool:
    print(f"[DEBUG] Checking if message contains a song name: {message}")
    prompt = [f"Does the message contain the name of the song or an album? Reply with 'yes' or 'no' only message: {message}"]
    result = en.llm._generate(prompt)
    response = result.generations[0][0].text.lower()
    print(f"[DEBUG] LLM response for song name check: {response}")
    return response == 'yes'

def extract_song_name_from_message(message: str) -> str:
    print(f"[DEBUG] Extracting song name from message: {message}")

    # Search DuckDuckGo for the song name and artist name
    search_query = f"song name from the message '{message}'"
    search_results = ddg_search.run(search_query)

    if search_results:
        song_info = search_results.strip()
        print(f"[DEBUG] Song information from DuckDuckGo: {song_info}")
        parts = song_info.split('-', 1)
        if len(parts) == 2:
            artist_name, song_name = parts[0].strip(), parts[1].strip()
            return f"{artist_name} - {song_name}"
        else:
            return song_info.strip()
    else:
        return 'None'

def extract_movie_series_names(message: str) -> str:
    movie_prompt_template = PromptTemplate(
        input_variables=["message"],
        template="Does the message contain a movie/series/TV show? Reply with a 'yes' or 'no':\n\n{message}",
    )

    movie_name_prompt_template = PromptTemplate(
        input_variables=["message"],
        template="Extract the name of the movie/series/TV show from the message. If no name is present, return 'None'. Reply with the name or 'None' only.\n\n{message}",
    )

    song_names_prompt_template = PromptTemplate(
        input_variables=["message", "search_results"],
        template="Extract the name of the songs from the following search results along with the artist in this format 'artist name - song name'. Reply in this format and if nothing is present return 'None'.\n\nSearch Query: {message}\n\nSearch Results: {search_results}",
    )
    movie_chain = LLMChain(llm=en.llm, prompt=movie_prompt_template, output_key="movie_check")
    movie_name_chain = LLMChain(llm=en.llm, prompt=movie_name_prompt_template, output_key="movie_name")
    song_names_chain = LLMChain(llm=en.llm, prompt=song_names_prompt_template, output_key="song_names")

    overall_chain = SequentialChain(
        chains=[movie_chain, movie_name_chain],
        input_variables=["message"],
        output_variables=["movie_check", "movie_name"],
        verbose=True,
    )

    initial_result = overall_chain({"message": message})
    movie_name = initial_result["movie_name"]

    if movie_name != "None":
        search_query = f"{movie_name} movie soundtrack list"
        search_results = ddg_search(search_query)
        song_names_result = song_names_chain({"message": search_query, "search_results": search_results})
        song_names = song_names_result["song_names"].split('\n')
        song_names = [song for song in song_names if song.strip()]

        if song_names:
            selected_song = random.choice(song_names)
            print("SELECTED SONG : ",selected_song)
            return selected_song
        else:
            return "None"
    else:
        return "None"
    


def is_asking_playing(message: str) -> bool:
    prompt = [f"Is the user asking to play a song ? Reply with a 'yes' or 'no' :\n\n{message}"]
    result = en.llm._generate(prompt)
    response = result.generations[0][0].text.lower()
    print(f"[DEBUG] Is the user asking to play it: {response}")
    return response == 'yes'

def is_enquiring_song(message: str) -> bool:
    prompt = [f"Is the user enquiring about a song,album or artist ? Reply with a 'yes' or 'no' :\n\n{message}"]
    result = en.llm._generate(prompt)
    response = result.generations[0][0].text.lower()
    print(f"[DEBUG] Is the user enquiring it: {response}")
    return response == 'yes'

def has_song_last_reply(last_message: str) -> bool:
    if not last_message:
        print("[DEBUG] Last message is empty or None, assuming no song name")
        return "None"

    print(f"[DEBUG] Checking if last message contains a song name: {last_message}")
    prompt = [f"Does the last reply contain a song name ? Reply with a 'yes' or 'no' last reply:{last_message}"]
    result = en.llm._generate(prompt)
    song_response = result.generations[0][0].text.lower()

    return song_response == 'yes'

def is_asking_favourite_song(message:str) -> bool:
    prompt = [f"Is the user asking to play their favourite song ? Reply with a 'yes' or 'no' :\n\n{message}"]
    result = en.llm._generate(prompt)
    response = result.generations[0][0].text.lower()
    print(f"[DEBUG] Is the user enquiring it: {response}")
    return response == 'yes'

#*************************************#

'''
To translate text based on the users needs


'''


#________TRANSLATOR FUNCTIONS_________#

class translator(BaseTool):
    name = "translator"
    description = "Handle all translation related queries"

    def _run(self, message: str) -> str:
        """
        Use the LLM to identify and handle the user's request related to translation.
        Args:
            message (str): The user's current message.
        Returns:
            str: A response indicating the action taken or a message to the user.
        """

        is_translator_request = translator_check(message)
        if is_translator_request == 'yes':
            return "I am now acting as a translator."
        else:
            return "Please provide the text you want me to translate."



    async def _arun(self, message: str) -> str:
        raise NotImplementedError("This tool does not support async")



def translator_check(message: str) -> bool:
    translator_check_template = PromptTemplate(
        input_variables=["message"],
        template="Is the message asking to be a 'translator' ? Reply with 'yes' or 'no' :\n\n{message}"
    )

    translator_check_chain = LLMChain(llm=en.llm, prompt=translator_check_template, output_key="TRANSLATE_CHECK")

    overall_chain = SequentialChain(
        chains=[translator_check_chain],
        input_variables=["message"],
        output_variables=["TRANSLATE_CHECK"],
        verbose=True,
    )

    initial_result = overall_chain({"message": message})
    translate_check_result = initial_result["TRANSLATE_CHECK"].lower()
    print("[DEBUG] Result of translation check:", translate_check_result)

    return translate_check_result

#_____________________________________#

#-------------------------------------#

tools = [
    Tool(
        name="DuckDuckGo Search",
        func=ddg_search.run,
        description="Useful to get info from the internet. Use by default."
    ),
    Tool(
        name="Wikipedia Search",
        func=wiki.run,
        description="Useful when users request biographies or historical moments."
    ),
    Tool(
        name="silent_handler",
        func=SilentHandlerTool(),
        description="Handle silent mode based on the user's message",
    ),
    Tool(
        name="repeat_handler",
        func=RepeatHandlerTool(),
        description="Handle repeat mode based on the user's message",
    ),
    Tool(
        name="music_tool",
        func=MusicTool(),
        description="Handle all music-related requests, including playing songs, recommending random songs, and identifying song names.",
    ),
    Tool(
        name = "random_music_tool",
        func = Music_random_tool(),
        description = "Handles all random music queries",
    ),
    Tool(
        name = "music_enquiry_tool",
        func = Music_enquiry_tool(),
        description = "Handles all music enquiries"   
    ),
    Tool(
        name = "translator",
        func = translator(),
        description = "Handle all translation related queries"
    ),
]

# Uncomment to initialize and run the agent
# QA_agent = initialize_agent(tools=tools, llm=en.llm, agent='zero-shot-react-description', verbose=True)
# QA_agent.run("Can you stay silent for 1 minute")


'''
PROMPT_LIVE_TRANSLATE = [f"Is the user asking you to be a translator to translate between languages ? Reply with 'yes' or 'no' based on the message: {message}"]
            RESPONSE_GENERATE = llm._generate(PROMPT_LIVE_TRANSLATE)
            RESPONSE = RESPONSE_GENERATE.generations[0][0].text.lower()

            if RESPONSE == 'yes':
                prompt_lang_check = [f"Does the message contain the from and to languages ? Reply with a 'yes' or 'no' message:{message}"]
                lang_check_generate = llm._generate(prompt_lang_check)
                lang_check_response = lang_check_generate.generations[0][0].text.lower()

                if lang_check_response == 'yes':
                    REALTIME_TRANSLATION = True
                    prompt_translate_extract_to_lang = [f"extract the name of the language to be translated to from the message:{message}"]
                    RESPONSE_GENERATE = llm._generate(prompt_translate_extract_to_lang)
                    RESPONSE = RESPONSE_GENERATE.generations[0][0].text.lower()

                    prompt_translate_extract_from_lang = [f"extract the name of the language to be translated from. From the message:{message}"]
                    RESPONSE_GENERATE_ORIGINAL = llm._generate(prompt_translate_extract_from_lang)
                    RESPONSE_ORIGINAL = RESPONSE_GENERATE_ORIGINAL.generations[0][0].text.lower()

                    print("ORIGINAL LANGUAGE : ",RESPONSE_ORIGINAL)
                    print("TRANSLATION LANGUAGE : ",RESPONSE)

                    OBTAINED_LANG_TO = RESPONSE
                    OBTAINED_LANG_FROM = RESPONSE_ORIGINAL

                    prompt_reply = f"Tell the user that you will help with that in {OBTAINED_LANG_TO} language"
                    res_final = await gb.send_response_with_LLM(message, prompt_reply)
                    await websocket.send(res_final)

                else:
                    TRANSLATE_UNEXPECTED_CASE = f"The user asked something about translation based on the message reply accordingly message:{message}"
                    res_final = await gb.send_response_with_LLM(message, TRANSLATE_UNEXPECTED_CASE)
                    await websocket.send(res_final)

            else:
                TRANSLATE_NOLANG_CASE = [f"Find which one is missing from the message that is the original language or the language to translate to.Reply with 'original','tolang','both' message:{message}"]
                RESPONSE_GENERATE = llm._generate(TRANSLATE_NOLANG_CASE)
                RESPONSE = RESPONSE_GENERATE.generations[0][0].text.lower()
                print(RESPONSE)
'''