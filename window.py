import window_mechanism as wm 
import TemperatureSensor as ts 
import csv
class window():

    def __init__(self):
        self.__window_mechanism = wm.window_mechanism()
        self.__temp_sensor = ts.TemperatureSensor()
        self.__preferred_temperature = 0
            
    
    def window_work(self):
        #When  room temperature is higher than the preferred temperature and room temperature is lower than outside
        if (self.__temp_sensor.get_room_temperature() > self.__preferred_temperature) and (self.__temp_sensor.get_room_temperature() > self.__temp_sensor.get_outside_temperature()):
            self.__window_mechanism.open_window()
            while True:
                if self.__temp_sensor.get_room_temperature() > self.__preferred_temperature:
                    print("loop 1")
                    self.__temp_sensor.set_room_temperature(self.__temp_sensor.get_room_temperature() - 1)
                    print(self.__temp_sensor.get_room_temperature())
                else:
                    self.__window_mechanism.close_window()
                    print("Temperature stabilized")
                    break
        #When room temperature is lower than preferred temperature and room temperature is higher than outside.
        elif self.__temp_sensor.get_room_temperature() < self.__preferred_temperature and self.__temp_sensor.get_room_temperature() > self.__temp_sensor.get_outside_temperature():
              self.__window_mechanism.close_window()
              while True:
                if self.__temp_sensor.get_room_temperature() < self.__preferred_temperature:
                    print("loop 2")
                    self.__temp_sensor.set_room_temperature(self.__temp_sensor.get_room_temperature() + 1)
                    print("Heating room: " + str(self.__temp_sensor.get_room_temperature()))
                else:
                    print("Temperature stabilized")
                    break
        #When room temperature is lower than preferred temperature and room temperature is lower than outside
        elif self.__temp_sensor.get_room_temperature() < self.__preferred_temperature and self.__temp_sensor.get_room_temperature() < self.__temp_sensor.get_outside_temperature():
              self.__window_mechanism.open_window()
              while True:
                if self.__temp_sensor.get_room_temperature() < self.__preferred_temperature:
                    print("loop 3")
                    self.__temp_sensor.set_room_temperature(self.__temp_sensor.get_room_temperature() + 1)
                else:
                    self.__window_mechanism.close_window()
                    print("Temperature stabilized")
                    break
        #When room temperature is higher than preferred temperature and room temperature is lower than outside
        elif self.__temp_sensor.get_room_temperature() > self.__preferred_temperature and self.__temp_sensor.get_room_temperature() < self.__temp_sensor.get_outside_temperature():
            print("Air Conditioner turned on")
            while True:
                if self.__temp_sensor.get_room_temperature() > self.__preferred_temperature:
                    print("loop 4")
                    self.__temp_sensor.set_room_temperature(self.__temp_sensor.get_room_temperature() + 1)
                else:
                    print("Temperature stabilized")
                    break
        
    def setPreferredTemperature(self, new_value):
        self.__preferred_temperature = new_value