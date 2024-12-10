import openai
import os
import json
import copy
from .weatherservice import WeatherService
from .promptmanager import PromptManager


class BoredAssistant:
    def __init__(self):
        self._default_activities = {
            "indoor": [],
            "outdoor": [],
            "indoor and outdoor": [],
            "social": [],
            "zipCode": None,
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

    def add_preferences(self, preference: dict):
        print("adding preferences: ", preference)
        category = preference.get("category")
        self.selected_category = category
        items = preference.get("items")
        zipCode = preference.get("zipCode", None)
        self.activities["zipCode"] = zipCode
        print("adding preferences, for category: ", category)

        if category in self.activities:
            for item in items:
                if item not in self.activities[category]:
                    self.activities[category].append(item)
        else:
            print(
                f"Invalid category: {category}. Please choose from 'indoor', 'outdoor', or 'social'."
            )

    def clear_preferences(self):
        print("Clearing Preferences...")
        self.activities = copy.deepcopy(self._default_activities)

    def suggest_activity(self):
        if self.selected_category not in self.activities:
            return {
                "error": "Invalid category. Choose 'indoor', 'outdoor', or 'social'."
            }
        prompt = self.prompt_manager.add_prompt(self.selected_category, self.activities)
        print(f"Activites: {self.activities}")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.01,
                messages=self.prompt_manager.chat_history,
            )
            raw_suggestion = response.choices[0].message.to_dict()
            self.prompt_manager.add_response(raw_suggestion)
            # raw_suggestion = raw_suggestion.to_dict()
            self.prompt_manager.printChatHistory()
        except Exception as e:
            return f"Error getting suggestion: {e}"
        try:
            suggestion = json.loads(raw_suggestion["content"])
            print(type(suggestion))
            print("final response: ", suggestion)
            return suggestion
        except Exception as e:
            return f"Error translating suggestion to dict: {e}"

    def show_preferences(self):
        for category, items in self.activities.items():
            print(
                f"{category.capitalize()} activities: {', '.join(items) or 'No activities yet'}"
            )

    def getWeather(self, zip_code):
        return self.weather_service.getWeather(zip_code)
