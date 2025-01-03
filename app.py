from src.boredassistant import BoredAssistant
from src.config import SQLALCHEMY_DATABASE_URI
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from src.models import db
from sqlalchemy.orm import Session

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bored = BoredAssistant()
db.init_app(app)
# add models after db is created
from src.models import User


with app.app_context():
    print("SQLALCHEMY_DATABASE_URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    db.create_all()
    print("****Database checked and initialized if necessary")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email", None)
    zipcode = data.get("zipcode", None)
    interests = data.get("interests", None)
    chat_history = data.get("chat_history", None)

    if not username:
        return (
            jsonify({"status": "error", "message": "Username is required to Login"}),
            400,
        )

    # Check if the user exists by username or email
    user = User.query_user(username)

    if user:
        # Update the login status
        if user.isLoggedIn:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "User is already logged in",
                        **user.to_json(),
                    }
                ),
                300,
            )
        user.isLoggedIn = True
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "User logged in successfully",
                    **user.to_json(),
                }
            ),
            200,
        )
    else:
        # Create a new user
        print("Creating new user")
        new_user = User(
            username=username,
            email=email,
            zipcode=zipcode,
            isLoggedIn=True,
            interests=interests,
            chat_history=chat_history,
        )
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "New user created and logged in successfully",
                    **new_user.to_json(),
                }
            ),
            201,
        )


@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email", None)

    if not username:
        return (
            jsonify({"status": "error", "message": "Username is required to logout"}),
            400,
        )

    # Find the user by username or email
    user = User.query_user(username)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    if not user.isLoggedIn:
        return (
            jsonify({"status": "success", "message": "User is already logged out"}),
            200,
        )

    # Update the user's logged-in status
    user.isLoggedIn = False

    return (
        jsonify(
            {
                "status": "success",
                "message": "User logged out successfully",
                "username": user.username,
                "email": user.email,
                "isLoggedIn": user.isLoggedIn,
            }
        ),
        200,
    )


@app.route("/user", methods=["GET"])
def get_user():
    username = request.args.get("username")
    user = User.query_user(username)
    if not username:
        return jsonify({"status": "error", "message": "Username is required"}), 400
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify(user.to_json()), 200


@app.route("/suggest", methods=["GET"])
def suggest_activity():
    print("looking for something to do...")
    username = request.args.get("username", None)
    suggestion = bored.suggest_activity(username)
    bored.clear_preferences(username)
    if suggestion["status"] == "error":
        return jsonify(suggestion)
    return jsonify(suggestion), 200


@app.route("/preference", methods=["POST"])
def add_preference():
    print("Adding preference endpoint called")
    try:
        username = request.args.get("username", None)
        data = request.get_json()
        print(data)
        print(type(data))
        if not data:
            return jsonify({"status": "error", "message": "No Json data received"}), 400
        preferences = bored.add_preferences(data, username)
        return (
            jsonify({"status": "sucess", "preferences": json.dumps(preferences)}),
            200,
        )
    except Exception as e:
        print(e)
        return jsonify({"status": "error"}), 400


@app.route("/preference", methods=["DELETE"])
def clear_preferences():
    print("***" * 5, "Calling Clear Preferences")
    username = request.args.get("username", None)
    bored.clear_preferences(username)
    return jsonify({"status": "success", "message": "Deleted preference"}), 200


@app.route("/weather/<zip_code>", methods=["GET"])
def get_weather(zip_code):
    print("getting weather")
    response = bored.getWeather(zip_code)
    print("returning weather response: ", response)
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
