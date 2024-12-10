from src.boredassistant import BoredAssistant
from src.config import SQLALCHEMY_DATABASE_URI
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bored = BoredAssistant()


@app.route("/suggest", methods=["GET"])
def suggest_activity():
    print("looking for something to do...")
    suggestion = bored.suggest_activity()
    bored.clear_preferences()
    return jsonify(suggestion)


@app.route("/preference", methods=["POST"])
def add_preference():
    print("Adding preference endpoint called")
    try:
        data = request.get_json()
        print(data)
        print(type(data))
        if not data:
            return jsonify({"status": "error", "message": "No Json data received"}), 400
        bored.add_preferences(data)
        return (
            jsonify({"status": "sucess", "preferences": json.dumps(bored.activities)}),
            200,
        )
    except Exception as e:
        print(e)
        return jsonify({"status": "error"}), 400


@app.route("/preference", methods=["DELETE"])
def clear_preferences():
    print("***" * 5, "Calling Clear Preferences")
    bored.clear_preferences()
    return jsonify({"success": "Deleted preference"}), 200


@app.route("/weather/<zip_code>", methods=["GET"])
def get_weather(zip_code):
    print("getting weather")
    response = bored.getWeather(zip_code)
    print("returning weather response: ", response)
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
    """
    from src.weatherservice import WeatherService

    w = WeatherService()
    try:
        zip_code = "92392"  # Example zip code (Beverly Hills)
        radius = 50  # Radius in kilometers
        country = "us"
        nearby_cities = w.get_surrounding_cities(zip_code, radius, country)

        print("Nearby Cities:")
        for city in nearby_cities:
            print(
                f"{city['city']} (Postal Code: {city['postal_code']}), Distance: {city['distance_km']:.2f} km"
            )
    except ValueError as e:
        print(e)

    """
