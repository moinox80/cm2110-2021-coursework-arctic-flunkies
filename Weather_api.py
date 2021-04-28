import requests
import json
url = "https://community-open-weather-map.p.rapidapi.com/find"

querystring = {"q":"london","cnt":"1","mode":"null","lon":"0","type":"link, accurate","lat":"0","units":"metric"}

headers = {
    'x-rapidapi-key': "1ee9e278d4msh3e637e58cb6150cp1c278fjsncb7f528a56f2",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

class weatherApi():
    CURRENT_TEMP = ""
    CURRENT_HUMIDITY = ""
    CURRENT_WEATHER = ""
    WEATHER_DESCRIPTION = ""
    x = response.json()
    if x["cod"] != "404":
        y = x["list"]
        z = y[0]["main"]

        CURRENT_TEMP = z["temp"]
        CURRENT_HUMIDITY = z["humidity"]
            
        q = y[0]["weather"]


        CURRENT_WEATHER = q["main"]
        WEATHER_DESCRIPTION = q["description"]

    def __init__(self): 
            self.__current_temperature = self.CURRENT_TEMP
            self.__current_humidity = self.CURRENT_HUMIDITY
            self.__current_weather = self.CURRENT_WEATHER
            self.__weather_description = self.WEATHER_DESCRIPTION
    
            
  
    def get_current_temperature(self):
        return self.__current_temperature

    def get_current_humidity(self):
        return self.__current_humidity

    def get_current_weather(self):
        return self.__current_weather

    def get_weather_description(self):
        return self.__weather_description
