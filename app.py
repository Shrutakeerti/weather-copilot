from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

API_KEY = "f55561b2a685e4a4575fb00d723b053c"  # Replace with your OpenWeatherMap API key


def extract_city_name(user_input):
    """Extract city name from user input."""
    match = re.search(r"temperature of ([\w\s]+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def handle_weather_query(user_input):
    """Handle weather queries."""
    city = extract_city_name(user_input)
    if city:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url).json()

            if response.get("cod") == 200:
                weather_desc = response["weather"][0]["description"]
                temperature = response["main"]["temp"]
                return f"The current weather in {city} is {weather_desc} with a temperature of {temperature}°C."
            else:
                return f"Sorry, I couldn't find weather information for {city}. Please check the city name."
        except Exception as e:
            return f"An error occurred while fetching the weather: {str(e)}"
    else:
        return "I couldn't understand the city name in your query. Please specify it clearly."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")
    if "temperature" in user_message.lower():
        reply = handle_weather_query(user_message)
    else:
        reply = f"You asked: {user_message}. How else can I assist you?"
    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=True)
