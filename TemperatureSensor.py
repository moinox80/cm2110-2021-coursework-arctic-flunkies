import random
import Weather_api as wa
class TemperatureSensor:
    #Stating the temperatures from the api and a random float for the room temperature
    api = wa.WeatherApi()
    MEASURED_ROOM_TEMP = random.uniform(15.0, 28.0)
    MEASURED_OUTSIDE_TEMP = api.get_current_temperature()

    ##Initializing attributes
    def __init__(self):
        self.__room_temperature = self.MEASURED_ROOM_TEMP
        self.__outside_temperature = self.MEASURED_OUTSIDE_TEMP
    
    #Getter methods for the temperaure
    def get_room_temperature(self):
        return int(self.__room_temperature)

    def get_outside_temperature(self):
        return int(self.__outside_temperature)

    #Mehod to set the room temperature
    def set_room_temperature(self, new_value):
        self.__room_temperature = new_value
    
    

        