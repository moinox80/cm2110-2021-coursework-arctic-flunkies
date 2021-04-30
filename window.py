import window_mechanism as wm 
import TemperatureSensor as ts 
import csv
import mqtt
import random

class Window():
    WINDOW_MECHANISM = wm.WindowMechanism()
    TEMPERATURE_SENSOR = ts.TemperatureSensor()

    def __init__(self):
        self.id = random.randrange(0, 1000)
        self.__window_mechanism = self.WINDOW_MECHANISM
        self.__temp_sensor = self.TEMPERATURE_SENSOR
        self.__preferred_temperature = 0
        self.__mqtt = mqtt.MQTTClient()
        self.__mqtt.connect("sociot", "s7ci7tRGU", True, "soc-broker.rgu.ac.uk", 8883)
            
    
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
        
    def set_preferred_temperature(self, new_value):
        self.__preferred_temperature = new_value

    def get_preferred_temperature(self):
        return self.__preferred_temperature
    
    def get_mqtt_topic_header(self):
        return "windows/" + self.id + "/"
    

    def mqtt_on_connect(client, userdata, flags, rc):
        header = get_mqtt_topic_header()
        self.__mqtt.subscribe(header + "set_state")
        self.__mqtt.subscribe(header + "set_schedule")
        self.__mqtt.subscribe(header + "remove_schedule")
        self.__mqtt.subscribe(header + "set_condition")
        self.__mqtt.subscribe(header + "remove_condition")

    def mqtt_on_disconnect(client, userdata, rc):
        pass

    def mqtt_on_message(client, userdata, message):
        pass

    def mqtt_on_publish(client, userdata, mid):
        pass

    def mqtt_on_subscribe(client, userdata, mid, granted_qos):
        pass

    def mqtt_on_unsubscribe(client, userdata, mid):
        pass
