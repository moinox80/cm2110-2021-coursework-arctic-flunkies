import requests
import json
import csv

class WeatherApi:
    #Stating weather attributes
    CURRENT_TEMP = ""
    CURRENT_HUMIDITY = ""
    CURRENT_WEATHER = ""
    WEATHER_DESCRIPTION = ""
    CITY=""
    #Getting the city from the user or the file
    with open('user_data.txt', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
        
        if line_count < 1:
            CITY = input('Please input the city you live in: ')
        else:
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
            CITY = row["city"]
    
        line_count += 1
    
    #OpenWeatherMap api settings
    url = "https://community-open-weather-map.p.rapidapi.com/find"

    querystring = {"q": str(CITY),"cnt":"1","mode":"null","lon":"0","type":"link, accurate","lat":"0","units":"metric"}

    headers = {
        'x-rapidapi-key': "1ee9e278d4msh3e637e58cb6150cp1c278fjsncb7f528a56f2",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    x = response.json()
    if x["cod"] != "404":
        y = x["list"]
        z = y[0]["main"]

        CURRENT_TEMP = z["temp"]
        CURRENT_HUMIDITY = z["humidity"]
            
        q = y[0]["weather"]


        CURRENT_WEATHER = q[0]["main"]
        WEATHER_DESCRIPTION = q[0]["description"]
        
    #Initializing attributes
    def __init__(self): 
            self.__current_temperature = self.CURRENT_TEMP
            self.__current_humidity = self.CURRENT_HUMIDITY
            self.__current_weather = self.CURRENT_WEATHER
            self.__weather_description = self.WEATHER_DESCRIPTION
            self.__city = self.CITY
    
            
    #Getter methods from the api
    def get_current_temperature(self):
        return self.__current_temperature

    def get_current_humidity(self):
        return self.__current_humidity

    def get_current_weather(self):
        return self.__current_weather

    def get_weather_description(self):
        return self.__weather_description

    def get_weather_data(self):
        return "Temperature in " + str(self.__city) + " is " + str(self.__current_temperature) + "C\nThere is currently " + str(self.__weather_description) + "\nHumidity is " + str(self.__current_humidity)

    def get_city(self):
        return self.__city

    #Setter method for the city
    def set_city(self, new_value):
        self.__city = new_value

    