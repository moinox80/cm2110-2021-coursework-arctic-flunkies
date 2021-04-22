import random

class TemperatureSensor:

    MEASURED_ROOM_TEMP = random.uniform(15.0, 28.0)
    MEASURE_OUTSIDE_TEMP = random.uniform(5.0, 30.0)

    def __init__(self):
        self.__room_temperature = self.MEASURED_ROOM_TEMP
        self.__outside_temperature = self.MEASURE_OUTSIDE_TEMP
        
    def get_room_temperature(self):
        return self.__room_temperature

    def get_outside_temperature(self):
        return self.__outside_temperature

    def set_room_temperature(self, new_value):
        self.__room_temperature = new_value
    
    

        