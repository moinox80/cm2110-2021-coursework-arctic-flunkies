import random
import Weather_api as wa
class TemperatureSensor:
    api = wa.weatherApi()
    MEASURED_ROOM_TEMP = random.uniform(15.0, 28.0)
    MEASURED_OUTSIDE_TEMP = api.get_current_temperature()

    def __init__(self):
        self.__room_temperature = self.MEASURED_ROOM_TEMP
        self.__outside_temperature = self.MEASURED_OUTSIDE_TEMP
        
    def get_room_temperature(self):
        return self.__room_temperature

    def get_outside_temperature(self):
        return self.__outside_temperature

    def set_room_temperature(self, new_value):
        self.__room_temperature = new_value
    
    

        