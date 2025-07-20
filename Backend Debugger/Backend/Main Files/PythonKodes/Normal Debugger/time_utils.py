import requests
import pytz
from datetime import datetime
import re
import nltk
from typing import Dict, Optional, List, Tuple
import unicodedata

# Download required NLTK data (only needs to run once)
try:
    nltk.download('words', quiet=True)
    from nltk.corpus import words
    english_words = set(words.words())
except:
    # Fallback if NLTK is not available
    english_words = set()

# GeoNames configuration
GEONAMES_USERNAME = "neuralharbourai"
GEONAMES_BASE_URL = "http://api.geonames.org"

# Supported languages with their ISO 639-1 codes
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean'
}

# Language-specific location patterns and keywords
LANGUAGE_PATTERNS = {
    'zh': {
        'time_keywords': ['时间', '几点', '现在', '当前时间', '什么时间', '时候'],
        'location_patterns': [
            r'在([^\s，。！？\d]{2,10})',  # 在北京, 在上海
            r'([^\s，。！？\d]{2,10})的时间',  # 北京的时间
            r'([^\s，。！？\d]{2,10})现在几点',  # 北京现在几点
        ]
    },
    'ja': {
        'time_keywords': ['時間', '今', '現在', '何時', 'いま', '時刻'],
        'location_patterns': [
            r'([^\s、。！？\d]{2,10})の時間',  # 東京の時間
            r'([^\s、。！？\d]{2,10})で何時',  # 東京で何時
            r'([^\s、。！？\d]{2,10})は今何時',  # 東京は今何時
        ]
    },
    'ko': {
        'time_keywords': ['시간', '몇시', '지금', '현재', '시각'],
        'location_patterns': [
            r'([^\s，。！？\d]{2,10})의?\s?시간',  # 서울의 시간, 서울 시간
            r'([^\s，。！？\d]{2,10})에서\s?몇시',  # 서울에서 몇시
            r'([^\s，。！？\d]{2,10})\s?지금\s?몇시',  # 서울 지금 몇시
        ]
    },
    'en': {
        'time_keywords': ['time', 'what time', 'current time', 'now', 'clock'],
        'location_patterns': [
            r'time\s+in\s+([A-Za-z\s]{2,30})',
            r'what\s+time\s+is\s+it\s+in\s+([A-Za-z\s]{2,30})',
            r'current\s+time\s+in\s+([A-Za-z\s]{2,30})',
        ]
    }
}

def detect_language(text: str) -> str:
    """
    Detect the primary language of the input text based on character patterns
    """
    # Count different character types
    char_counts = {
        'latin': 0,
        'cjk': 0,
        'korean': 0,
        'japanese_hiragana': 0,
        'japanese_katakana': 0
    }
    
    for char in text:
        if char.isalpha():
            if ord(char) < 128:  # ASCII
                char_counts['latin'] += 1
            elif '\u4e00' <= char <= '\u9fff':  # CJK ideographs
                char_counts['cjk'] += 1
            elif '\uac00' <= char <= '\ud7af':  # Korean Hangul
                char_counts['korean'] += 1
            elif '\u3040' <= char <= '\u309f':  # Hiragana
                char_counts['japanese_hiragana'] += 1
            elif '\u30a0' <= char <= '\u30ff':  # Katakana
                char_counts['japanese_katakana'] += 1
    
    total_chars = sum(char_counts.values())
    if total_chars == 0:
        return 'en'  # Default to English
    
    # Determine language based on character distribution
    if char_counts['korean'] / total_chars > 0.3:
        return 'ko'
    elif (char_counts['japanese_hiragana'] + char_counts['japanese_katakana']) / total_chars > 0.2:
        return 'ja'
    elif char_counts['cjk'] / total_chars > 0.5:
        return 'zh'
    else:
        return 'en'

def extract_location_multilingual(text: str, detected_lang: str = None) -> List[str]:
    """
    Extract location names from text in multiple languages
    """
    if not detected_lang:
        detected_lang = detect_language(text)
    
    locations = []
    
    # Use language-specific patterns
    if detected_lang in LANGUAGE_PATTERNS:
        patterns = LANGUAGE_PATTERNS[detected_lang]['location_patterns']
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            locations.extend([match.strip() for match in matches if match.strip()])
    
    # Fallback: extract potential location names using general patterns
    if not locations:
        # For CJK languages, look for sequences of 2-6 characters that could be place names
        if detected_lang in ['zh', 'ja', 'ko']:
            # Extract potential CJK location names
            cjk_pattern = r'[\u4e00-\u9fff\uac00-\ud7af\u3040-\u309f\u30a0-\u30ff]{2,6}'
            potential_locations = re.findall(cjk_pattern, text)
            locations.extend(potential_locations)
        else:
            # For Latin-based languages, use the original English extraction logic
            locations.extend(extract_location_from_text(text))
    
    return list(set(locations))  # Remove duplicates

def extract_location_from_text(text: str) -> List[str]:
    """
    Extract potential location names from text by filtering out common English words
    and looking for capitalized phrases that could be place names.
    """
    words_list = re.findall(r'\b[A-Za-z]+\b', text)
    
    potential_locations = []
    for length in range(4, 0, -1):
        for i in range(len(words_list) - length + 1):
            phrase = ' '.join(words_list[i:i + length])

            phrase_words = phrase.lower().split()
            if all(word in english_words for word in phrase_words):
                continue

            if phrase[0].isupper() and len(phrase) > 2:
                potential_locations.append(phrase)

    for word in words_list:
        if (word[0].isupper() and 
            word.lower() not in english_words and 
            len(word) > 2 and 
            word not in potential_locations):
            potential_locations.append(word)
    
    return potential_locations

def search_location_multilingual(location_query: str, language: str = 'en') -> Optional[Dict]:
    """
    Search for location using GeoNames API with multilingual support
    """
    # Try multiple search strategies
    search_strategies = [
        {'q': location_query, 'lang': language},
        {'q': location_query, 'lang': 'en'},
        {'q': location_query},
    ]
    
    for params in search_strategies:
        try:
            url = f"{GEONAMES_BASE_URL}/searchJSON"
            params.update({
                'maxRows': 3,
                'username': GEONAMES_USERNAME,
                'style': 'FULL'
            })
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if 'geonames' in data and len(data['geonames']) > 0:
                location = data['geonames'][0]
                alternate_names = get_alternate_names(location.get('geonameId'), language)
                
                result = {
                    'name': location.get('name', ''),
                    'country': location.get('countryName', ''),
                    'admin1': location.get('adminName1', ''),
                    'latitude': location.get('lat'),
                    'longitude': location.get('lng'),
                    'timezone_id': location.get('timezone', {}).get('timeZoneId') if location.get('timezone') else None,
                    'population': location.get('population', 0),
                    'feature_class': location.get('fcl', ''),
                    'feature_code': location.get('fcode', ''),
                    'alternate_names': alternate_names,
                    'geonameId': location.get('geonameId')
                }
                
                return result
                
        except requests.RequestException as e:
            print(f"GeoNames API request failed for {params}: {e}")
            continue
        except Exception as e:
            print(f"Error processing GeoNames response for {params}: {e}")
            continue
    
    return None

def get_alternate_names(geoname_id: int, language: str = 'en') -> Dict[str, str]:
    """
    Get alternate names for a location in different languages
    """
    try:
        url = f"{GEONAMES_BASE_URL}/getJSON"
        params = {
            'geonameId': geoname_id,
            'username': GEONAMES_USERNAME,
            'style': 'FULL'
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        alternate_names = {}
        
        if 'alternateNames' in data:
            for alt_name in data['alternateNames']:
                lang = alt_name.get('lang', '')
                name = alt_name.get('name', '')
                
                if lang in SUPPORTED_LANGUAGES and name:
                    alternate_names[lang] = name
        
        return alternate_names
        
    except Exception as e:
        print(f"Error getting alternate names: {e}")
        return {}

def search_location_geonames(location_query: str) -> Optional[Dict]:
    """
    Enhanced search for location using GeoNames API with multilingual support
    """
    detected_lang = detect_language(location_query)
    return search_location_multilingual(location_query, detected_lang)

def get_timezone_info(lat: float, lng: float) -> Optional[str]:
    """
    Get timezone information for given coordinates using GeoNames timezone API
    """
    try:
        url = f"{GEONAMES_BASE_URL}/timezoneJSON"
        params = {
            'lat': lat,
            'lng': lng,
            'username': GEONAMES_USERNAME
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        return data.get('timezoneId')
    
    except Exception as e:
        print(f"Error getting timezone info: {e}")
        return None

def find_location(sentence: str) -> Optional[Dict]:
    """
    Find location information from a sentence using multilingual GeoNames API
    """
    detected_lang = detect_language(sentence)
    potential_locations = extract_location_multilingual(sentence, detected_lang)
    
    if not potential_locations:
        return None

    for location_query in potential_locations:
        location_data = search_location_multilingual(location_query, detected_lang)
        
        if location_data and location_data.get('name'):
            if not location_data.get('timezone_id') and location_data.get('latitude') and location_data.get('longitude'):
                timezone_id = get_timezone_info(
                    float(location_data['latitude']), 
                    float(location_data['longitude'])
                )
                location_data['timezone_id'] = timezone_id

            result = {
                'City': location_data['name'],
                'Country': location_data['country'],
                'Timezone': location_data.get('timezone_id', 'UTC'),
                'detected_language': detected_lang
            }

            alternate_names = location_data.get('alternate_names', {})
            if alternate_names:
                result['alternate_names'] = alternate_names
                if detected_lang in alternate_names:
                    result['local_name'] = alternate_names[detected_lang]
            if location_data.get('admin1'):
                result['State'] = location_data['admin1']
            
            # Add additional metadata
            result['coordinates'] = {
                'latitude': location_data.get('latitude'),
                'longitude': location_data.get('longitude')
            }
            result['population'] = location_data.get('population', 0)
            
            return result
    
    return None

def get_current_time_in_timezone(timezone_str: str) -> str:
    """
    Get current time in the specified timezone
    """
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
        return now.strftime("%I:%M %p").lstrip('0')
    except Exception as e:
        print(f"Error getting time for timezone {timezone_str}: {e}")
        utc_now = datetime.now(pytz.UTC)
        return utc_now.strftime("%I:%M %p").lstrip('0')

def get_location_time_info(sentence: str) -> Optional[Dict]:
    """
    Get comprehensive time information for a location mentioned in the sentence
    """
    location = find_location(sentence)
    
    if not location:
        return None
    
    timezone_str = location.get('Timezone', 'UTC')
    detected_lang = location.get('detected_language', 'en')
    
    try:
        tz = pytz.timezone(timezone_str)
        current_time = datetime.now(tz)
        
        result = {
            'location': location,
            'current_time': current_time.strftime("%I:%M %p").lstrip('0'),
            'current_date': current_time.strftime("%A, %B %d, %Y"),
            'timezone': timezone_str,
            'utc_offset': current_time.strftime("%z"),
            'detected_language': detected_lang,
            'formatted_response': format_multilingual_time_response(location, current_time, detected_lang)
        }
        
        return result
    
    except Exception as e:
        print(f"Error getting time info: {e}")
        return None

def format_multilingual_time_response(location: Dict, current_time: datetime, language: str = 'en') -> str:
    """
    Format a natural language response for time information in multiple languages
    """
    location_parts = []
    
    city_name = location.get('local_name', location.get('City', ''))
    if city_name:
        location_parts.append(city_name)
        
    if location.get('State'):
        location_parts.append(location['State'])
    if location.get('Country'):
        location_parts.append(location['Country'])
    
    location_str = ", ".join(location_parts)
    time_str = current_time.strftime('%I:%M %p').lstrip('0')
    date_str = current_time.strftime('%A, %B %d, %Y')
    
    if language == 'zh':
        return f"{location_str}现在是{time_str}。今天是{date_str}。"
    elif language == 'ja':
        return f"{location_str}の現在時刻は{time_str}です。今日は{date_str}です。"
    elif language == 'ko':
        return f"{location_str}의 현재 시간은 {time_str}입니다. 오늘은 {date_str}입니다."
    else:
        return f"It's currently {time_str} in {location_str}. Today is {date_str}."

# Test function (for debugging)
def test_multilingual_location_search():
    """Test the multilingual location search functionality"""
    test_queries = [
        "what time is it in Paris?",           # English
        "北京现在几点？",                        # Chinese
        "東京の時間は何時ですか？",                # Japanese  
        "서울 지금 몇시예요?",                    # Korean
        "current time in New York",           # English
        "上海的时间",                           # Chinese
        "ロンドン時間",                         # Japanese
        "부산 시간"                            # Korean
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        detected_lang = detect_language(query)
        print(f"Detected language: {detected_lang} ({SUPPORTED_LANGUAGES.get(detected_lang, 'Unknown')})")
        
        result = get_location_time_info(query)
        if result:
            print(f"Response: {result['formatted_response']}")
            if result['location'].get('alternate_names'):
                print(f"Alternate names: {result['location']['alternate_names']}")
        else:
            print("No location found")

# Export the main functions
__all__ = [
    "find_location", 
    "get_current_time_in_timezone", 
    "get_location_time_info",
    "format_multilingual_time_response",
    "search_location_geonames",
    "detect_language",
    "extract_location_multilingual",
    "search_location_multilingual",
    "SUPPORTED_LANGUAGES"
]

