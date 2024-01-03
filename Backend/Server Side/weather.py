import geocoder
import requests
import yaml
import random
from io import StringIO

API_KEY = open("weather_api_key.txt", "r").read()
degree_symbol = "\u00b0"


def get_user_city():
    try:
        location = geocoder.ip("me")
        if location.city:
            return location.city
        else:
            return "City not found"

    except Exception as e:
        print("Error occurred:", e)
        return None


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


def load_responses():
    with open("responses.yaml", "r") as file:
        return yaml.safe_load(file)

def get_intro_phrases(responses):
    return responses["Intros"]["weather_intro"]

def recommend_activity(temp_celsius, humidity, wind_speed, description, responses):
    recommendations = []

    if temp_celsius > 32:
        recommendations.extend(responses["temperature_responses"]["hot"])

    if temp_celsius < 10:
        recommendations.extend(responses["temperature_responses"]["cold"])

    if "rain" in description.lower():
        if "light" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["light_rain"]
            )

        elif "moderate" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["moderate_rain"]
            )

        elif "very heavy" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["heavy_rain"]
            )

        elif "heavy intensity" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["heavy_intensity_rain"]
            )

        elif "extreme" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["extreme_rain"]
            )

        elif "freezing" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["freezing_rain"]
            )

        elif "light intensity shower" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"][
                    "light_intensity_shower_rain"
                ]
            )

        elif "shower rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["shower_rain"]
            )

        elif "heavy intensity shower" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"][
                    "heavy_intensity_shower_rain"
                ]
            )

        elif "ragged shower" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["ragged_shower_rain"]
            )

        else:
            recommendations.extend(
                responses["weather_condition_responses"]["rain"]["default"]
            )

    if "thunderstorm" in description.lower():
        if "light rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "thunderstorm_with_light_rain"
                ]
            )

        elif "heavy rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "thunderstorm_with_heavy_rain"
                ]
            )

        elif "rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "thunderstorm_rain"
                ]
            )

        elif "light" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "light_thunderstorm"
                ]
            )

        elif "heavy" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "heavy_thunderstorm"
                ]
            )

        elif "ragged" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "ragged_thunderstorm"
                ]
            )

        elif "light drizzle" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "thunderstorm_light_drizzle"
                ]
            )

        elif "drizzle" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "thunderstorm_drizzle"
                ]
            )

        elif "heavy drizzle" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"][
                    "thunderstorm_heavy_drizzle"
                ]
            )

        else:
            recommendations.extend(
                responses["weather_condition_responses"]["thunderstorm"]["default"]
            )

    if "drizzle" in description.lower():
        if "light intensity" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"][
                    "drizzle_light_intensity"
                ]
            )

        elif "heavy intensity" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"][
                    "drizzle_heavy_intensity"
                ]
            )

        elif "light intensity rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"][
                    "drizzle_light_intensity_rain"
                ]
            )

        elif "rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"]["drizzle_rain"]
            )

        elif "heavy intensity rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"][
                    "drizzle_heavy_intensity_rain"
                ]
            )

        elif "shower rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"][
                    "drizzle_shower_rain"
                ]
            )

        elif "heavy shower rain" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"][
                    "drizzle_heavy_shower_rain"
                ]
            )

        elif "shower" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"]["drizzle_shower"]
            )

        else:
            recommendations.extend(
                responses["weather_condition_responses"]["drizzle"]["default"]
            )

    if "snow" in description.lower():
        recommendations.extend(responses["weather_condition_responses"]["snow"])

    if "haze" in description.lower():
        recommendations.extend(responses["weather_condition_responses"]["haze"])

    if wind_speed > 10:
        recommendations.extend(
            responses["weather_condition_responses"]["wind_responses"]["high_wind"]
        )

    if "clear" in description.lower():
        recommendations.extend(responses["sky_condition_responses"]["clear_sky"])

    if "clouds" in description.lower():
        if "few" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["clouds"]["few"]
            )

        elif "scattered" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["clouds"]["scattered"]
            )

        elif "broken" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["clouds"]["broken"]
            )

        elif "overcast" in description.lower():
            recommendations.extend(
                responses["weather_condition_responses"]["clouds"]["overcast"]
            )

        else:
            recommendations.extend(
                responses["weather_condition_responses"]["clouds"]["default"]
            )

    recommendations.extend(responses["general_recommendations"])

    return recommendations


def main_stuff():
    # text to return to the human
    weather_text = StringIO()
    # lambda function to write to end of stringio (easier to replace all print functions with this)
    add_line_to_text = lambda string: weather_text.write(string + "\n")
    
    temperature_category = None
    wind_category = None

    user_city = get_user_city()
    if user_city:
        CITY = user_city

        weather_url = (
            f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
        )

        response = requests.get(weather_url)

        if response.status_code == 200:
            weather_data = response.json()
            temp_kelvin = weather_data["main"]["temp"]
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            feels_like_kelvin = weather_data["main"]["feels_like"]
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(
                feels_like_kelvin
            )
            wind_speed = weather_data["wind"]["speed"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]

            responses = load_responses()
            intro_phrases = get_intro_phrases(responses)
            intro = random.choice(intro_phrases)

            if temp_celsius < 25:
                temperature_category = "cold"
            elif 25 <= temp_celsius <= 32:
                temperature_category = "comfortable"
            elif 32 < temp_celsius <= 40:
                temperature_category = "hot"
            else:
                temperature_category = "scorching"


            if wind_speed < 2:
                wind_category = "calm"
            elif 2 <= wind_speed <= 4:
                wind_category = "gentle"
            elif 4 < wind_speed <= 6:
                wind_category = "moderate"
            else:
                wind_category = "strong"


            if humidity < 30:
                humidity_category = "low"
            elif 30 <= humidity <= 60:
                humidity_category = "moderate"
            else:
                humidity_category = "high"

            base_text = f"The Temperature stands at {temperature_category} {temp_celsius:.2f}{degree_symbol}C with a {humidity_category} humidity level of {humidity}% and a {wind_category} breeze blowing at {wind_speed}m/s. The overall condition is described as {description}."

            if temperature_category in ["cold", "hot"]:
                base_text = base_text.replace("stands at", "is")

            add_line_to_text(intro)
            add_line_to_text(base_text)

            responses = load_responses()
            recommendations = recommend_activity(
                temp_celsius, humidity, wind_speed, description, responses
            )

            if recommendations:
                # Splitting general recommendations from weather-based recommendations
                general_rec = [
                    rec
                    for rec in recommendations
                    if rec in responses["general_recommendations"]
                ]
                weather_rec = [
                    rec
                    for rec in recommendations
                    if rec not in responses["general_recommendations"]
                ]

                # Collecting weather-based recommendations
                if weather_rec:
                    num_weather_recommendations = min(
                        random.randint(2, 4), len(weather_rec)
                    )
                    selected_weather_recommendations = random.sample(
                        weather_rec, num_weather_recommendations
                    )
                    weather_recommendations_paragraph = "\n".join(
                        selected_weather_recommendations
                    )

                # Add_Line_To_Texting all recommendations together
                if weather_rec and general_rec:
                    add_line_to_text(
                        f"{weather_recommendations_paragraph}\n{random.choice(general_rec)}"
                    )
                elif weather_rec:
                    add_line_to_text(f"{weather_recommendations_paragraph}")

        else:
            add_line_to_text(
                f"Failed to fetch weather data. Status code: {response.status_code}"
            )
    return weather_text.getvalue()
