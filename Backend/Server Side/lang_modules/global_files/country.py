import json
import pytz
from datetime import datetime
import nltk
nltk.download('words')

from nltk.corpus import words

english_words = set(words.words())

with open('country_final.json', encoding='utf-8') as f:
    data = json.load(f)

countries = {country['name'] for country in data}
cities = {city['name'] for country in data for state in country.get('states', []) for city in state.get('cities', [])}
states = {state['name'] for country in data for state in country.get('states', [])}

valid_cities = {city['name'].lower() for country in data for state in country.get('states', []) for city in state.get('cities', [])}

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




def get_current_time_in_timezone(timezone):
    now = datetime.now(timezone)
    return now.strftime("%I:%M %p")

sentence = "what is the time in saudi arabia ?"
location = find_location(sentence)

if location:
    print("Location:", location)
    country_name = location.get('Country')
    state_name = location.get('State')
    city_name = location.get('City')

    current_time = get_current_time_in_timezone(location['Timezone'])

    if city_name:
        print(f"Current time in {city_name}, {country_name} is {current_time}")
    elif state_name:
        print(f"Current time in {state_name}, {country_name} is {current_time}")
    elif country_name:
        print(f"Current time in {country_name} is {current_time}")
else:
    print("No country, city, district, or state is mentioned in the sentence.")


