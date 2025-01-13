import openai
import os
import json
import copy
from .weatherservice import WeatherService
from .promptmanager import PromptManager
import ast
from src.models import User
from src.models import db


class BoredAssistant:
    def __init__(self):
        self._default_activities = {
            "indoor": [],
            "outdoor": [],
            "indoor and outdoor": [],
            "social": [],
            # "zipCode": None,
            # "energyLevel": None,
        }
        self.selected_category = None
        self.activities = copy.deepcopy(self._default_activities)
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = openai.Client(api_key=self.api_key)
        self.weather_service = WeatherService()
        self.prompt_manager = PromptManager()

    def add_preferences(self, preference: dict, username):
        print("adding preferences: ", preference)
        category = preference.get("category")
        energyLevel = preference.get("energyLevel")
        items = preference.get("items")
        zipCode = preference.get("zipCode", None)

        if not username:
            self.selected_category = category
            self.activities["zipCode"] = zipCode
            self.activities["energyLevel"] = energyLevel
            if category in self.activities:
                for item in items:
                    if item not in self.activities[category]:
                        self.activities[category].append(item)
            return self.activities

        else:
            # update user object in db
            user = User.update_preferences(
                username, category, items, energyLevel, zipCode
            )
            if user:
                return user.interests

            else:
                print(
                    f"Invalid category: {category}. Please choose from 'indoor', 'outdoor', or 'social'."
                )
                return None

    def clear_preferences(self, username):
        print("Clearing Preferences...")
        self.activities = copy.deepcopy(self._default_activities)
        if username:
            User.clear_preferences(username)

    def suggest_activity(self, username):
        if self.selected_category not in self.activities:
            return {
                "status": "error",
                "message": "Invalid category. Choose 'indoor', 'outdoor', or 'social'.",
            }
        if not username:
            activities = self.activities
        else:
            user = User.query_user(username)
            if user:
                activities = user.interests
        prompt = self.prompt_manager.add_prompt(self.selected_category, activities)
        print(f"Activites: {activities}")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.01,
                messages=self.prompt_manager.chat_history,
            )
            raw_suggestion = response.choices[0].message.to_dict()
        except Exception as e:
            return {"status": "error", "message": f"Error getting suggestion: {e}"}
        try:
            parsed_suggestion = self.parse_to_dict(raw_suggestion["content"])
            if "content" in parsed_suggestion and isinstance(
                parsed_suggestion["content"], str
            ):
                try:
                    parsed_suggestion["content"] = json.loads(
                        parsed_suggestion["content"]
                    )
                except json.JSONDecodeError:
                    pass
            self.prompt_manager.add_response(parsed_suggestion)
            parsed_suggestion["status"] = "success"
            return parsed_suggestion
        except Exception as e:
            print("Error translating suggestion to dict: ", e)
            print("raw suggestion: ", raw_suggestion)
            print("type(suggestion): ", type(parsed_suggestion))
            print("parsed_suggestion: ", parsed_suggestion)
            self.prompt_manager.printChatHistory()
            return {
                "status": "error",
                "message": f"Error translating suggestion to dict: {e}",
            }

    def parse_suggestion(self, parsed_suggestion, max_depth, current_depth=0):
        # Check if recursion depth exceeds the max_depth
        if current_depth >= max_depth:
            return parsed_suggestion

        # If the suggestion is a string, try to parse it
        if isinstance(parsed_suggestion, str):
            try:
                parsed_suggestion = json.loads(parsed_suggestion)
            except json.JSONDecodeError:
                # If parsing fails, return the string as-is
                return parsed_suggestion

        # If the parsed suggestion is still a string, attempt parsing again recursively
        if isinstance(parsed_suggestion, str):
            return self.parse_suggestion(
                parsed_suggestion, max_depth, current_depth + 1
            )

        # If the parsed suggestion is a dictionary, return it
        return parsed_suggestion

    def show_preferences(self):
        for category, items in self.activities.items():
            print(
                f"{category.capitalize()} activities: {', '.join(items) or 'No activities yet'}"
            )

    def getWeather(self, zip_code):
        return self.weather_service.getWeather(zip_code)

    def parse_to_dict(self, data_str):
        try:
            # First, attempt to parse directly as a JSON string
            return json.loads(data_str)
        except json.JSONDecodeError:
            try:
                # Second, attempt to parse using ast.literal_eval for Python-style dicts
                return ast.literal_eval(data_str)
            except (ValueError, SyntaxError):
                # Last, replace single quotes with double quotes and try JSON parsing
                try:
                    normalized_str = data_str.replace("'", '"')
                    return json.loads(normalized_str)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse string as dict: {e}")
