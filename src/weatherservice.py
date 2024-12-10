import pgeocode
import os
import requests
import json
from geopy.distance import geodesic
import pandas as pd
import csv


class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = os.getenv("WEATHER_URL")
        self.weather_data = None
        self.city = None

    def getWeather(self, zip_code):
        nomi = pgeocode.Nominatim("us")
        location = nomi.query_postal_code(zip_code)
        self.city = location.place_name
        units = "imperial"
        param_url = f"lat={location.latitude}&lon={location.longitude}&appid={self.api_key}&units={units}"
        url = self.base_url + param_url
        # print("url: ", url)
        try:
            # Make the API request
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            weather_data = response.json()
            # print(json.dumps(weather_data, indent=2))
        except Exception as e:
            print(e)
        # Extract relevant data
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        rain_chance = weather_data.get("rain", {}).get(
            "1h", 0
        )  # Rain in the last 1 hour (default to 0)
        feelsLike = weather_data["main"]["feels_like"]
        icon_urls = []
        weather_description = []
        weather_main_description = []
        for weather in weather_data["weather"]:
            icon_code = weather["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_urls.append(icon_url)
            weather_description.append(weather["description"])
            weather_main_description.append(weather["main"])
        # Display the results
        # print(f"Temperature: {temperature}°F")
        # print(f"Humidity: {humidity}%")
        # print(f"Chance of Rain (last hour): {rain_chance} mm")

        response = {
            "weather_data": weather_data["main"],
            "wind": weather_data["wind"],
            "description": ",".join(weather_description),
            "description_main": ",".join(weather_main_description),
            "icon_links": icon_urls,
            "rain": weather_data["rain"] if "rain" in weather_data else None,
        }
        self.weather_data = response
        return response

    def getSurroundingCities(self, zip_code):
        # get cooridates of starting city
        nomi = pgeocode.Nominatim("us")
        location = nomi.query_postal_code(zip_code)
        latitude, longitude = location.latitude, location.longitude

        # geolocator = Nominatim(user_agent="my_geocoder")

        # Define a radius (in km) for surrounding cities
        radius = 50

        # Find nearby cities
        nearby_cities = []
        for zip_code in nomi.query_all():
            try:
                city_location = nomi.query_postal_code(zip_code)
                city_coords = (city_location.latitude, city_location.longitude)
                distance = geodesic((latitude, longitude), city_coords).km
                if 0 < distance <= radius:
                    nearby_cities.append(city_location.place_name)
            except Exception:
                pass

        print(nearby_cities)

    def get_surrounding_cities(self, zip_code, radius=50, country="us"):
        columns = [
            "country",
            "postal_code",
            "place_name",
            "state",
            "state_code",
            "county",
            "county_code",
            "community",
            "latitude",
            "longitude",
            "accuracy",
        ]
        # Initialize Nominatim for the specified country
        nomi = pgeocode.Nominatim(country)

        # Get coordinates of the starting postal code
        location = nomi.query_postal_code(zip_code)
        print("location: ", location)
        if location is None:
            print("Invalid postal code!")
            return []

        latitude, longitude = location.latitude, location.longitude

        # Get the path to the pgeocode data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_path = os.path.join(script_dir, "US.txt")

        # Load all postal codes for the country
        if not os.path.exists(dataset_path):
            raise ValueError(
                f"Dataset for country {country} not found at {dataset_path}"
            )
        all_locations = pd.read_csv(
            dataset_path,
            sep=r"\s+",
            header=None,
            names=columns,
            engine="python",
            quoting=csv.QUOTE_MINIMAL,
        )
        print(all_locations.head)

        # Filter and find nearby cities
        nearby_cities = []
        for _, city in all_locations.iterrows():
            # Skip rows with missing data
            if (
                pd.isnull(city["latitude"])
                or pd.isnull(city["longitude"])
                or pd.isnull(city["place_name"])
            ):
                continue

            # Get city coordinates
            city_coords = (city["latitude"], city["longitude"])
            print(city)

            # Calculate distance
            try:
                distance = geodesic((latitude, longitude), city_coords).km
                if 0 < distance <= radius:  # Exclude the starting city itself
                    nearby_cities.append(
                        {
                            "city": city["place_name"],
                            "postal_code": city["postal_code"],
                            "distance_km": distance,
                        }
                    )
            except Exception as e:
                pass  # Skip invalid entries
            input("enter to continue")

        return sorted(nearby_cities, key=lambda x: x["distance_km"])
