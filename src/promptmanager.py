import json

from .weatherservice import WeatherService


class PromptManager:
    def __init__(self):
        self.chat_history = []
        self.initialize_system_prompt()
        self.weatherService = WeatherService()

    def initialize_system_prompt(self):
        system_content = {
            "role": "system",
            "content": """
                        You are a friendly, funny and witty assistant that is a GenZ person.
                        Your a master of the GenZ culture and slag and use words like (skibbidy, rizz, phantom tax, alpha, sigma, cap,no cap, slay,sus,drip,bro...etc) often. 
                        You help kids find something to do when they are bored and make them laugh at your suggestions.
                        Your responses (both remarks and suggestions) should be in the tone and jargen of a Gen-Z person. 
                        The format of the response should be in json like this {"remark":<your remarks>, "suggestions":[<yourListofSuggestions>]} and should be compatible with a python dict. the strings and keys in the json response should be in double quotes.
                        """,
        }
        self.chat_history.append(system_content)

    def add_prompt(self, category, activities):
        weather_data = None
        print("adding prompt....")
        # print("activities in prompt: ", activities)
        if "zipCode" in activities and activities["zipCode"]:
            weather_data = self.weatherService.getWeather(activities["zipCode"])
            print("city: ", self.weatherService.city)
        if not activities[category] or len(activities[category]) == 0:
            prompt = (
                f"Suggest some {category} activities in Gen Z slag "
                f"The funnier and more Gen Z slag that is used the better!"
            )
        else:
            prompt = (
                f"Suggest some {category} activities in Gen Z slag "
                f"based on this list of preferences: {', '.join(activities[category])}."
                f"And related things.The funnier and more Gen Z slag that is used the better!"
            )
        if category == "outdoor" and weather_data:
            prompt += f"""
            Include activities appropriate for weather, which is {weather_data["description"]}
            with a temperature of: {weather_data["weather_data"]["temp"]} F, wind speed: {weather_data["wind"]["speed"]} mph."""
        if "energyLevel" in activities and activities["energyLevel"]:
            prompt += f"Activities should be suitable for an energy level of {activities['energyLevel']}. where the energy level scale is from 1 to 10. 1 being lowest energy 10 being the heightest. 11 is rediculous amounts of energy. If energy level is a 1 or 11 make a funny Gen-z comment about their energy level."
        print(f"\nprompt: {prompt}\n")
        self.chat_history.append({"role": "user", "content": prompt})
        return prompt

    def add_response(self, response: dict):
        self.chat_history.append(
            {"role": "assistant", "content": json.dumps(response["content"])}
        )

    def printChatHistory(self):
        print("*" * 20)
        print("Printing Chat History")
        print("*" * 20)
        print("\n")
        for item in self.chat_history:
            print("role:", item["role"])
            if item["role"] == "assistant":
                try:
                    parsed = json.loads(item["content"])
                    if isinstance(parsed, str):
                        parsed = json.loads(parsed)
                    print("assisant content: ", json.dumps(parsed, indent=4))
                except json.JSONDecodeError as e:
                    print("Failed to parse JSON: ", e)
                    print(item["content"])
            else:
                print("content:", item["content"])
            print("\n")
        print("Done printing chat history")
