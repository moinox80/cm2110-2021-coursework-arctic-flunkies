import window_mechanism as wm 
import TemperatureSensor as ts 
import csv
import mqtt
import random
import time

class Window():
    WINDOW_MECHANISM = wm.WindowMechanism()
    TEMPERATURE_SENSOR = ts.TemperatureSensor()

    def __init__(self):
        self.id = 0
        #self.id = random.randrange(0, 1000)
        self.__window_mechanism = self.WINDOW_MECHANISM
        self.__temp_sensor = self.TEMPERATURE_SENSOR
        self.__preferred_temperature = 0

        self.__mqtt = mqtt.MQTTClient()
        self.__mqtt.set_on_connect(self.)
        self.__mqtt.connect("sociot", "s7ci7tRGU", "soc-broker.rgu.ac.uk", 8883)
            
    
    def window_work(self):
        room_temp = self.__temp_sensor.get_room_temperature()
        pref_temp = self.__preferred_temperature
        out_temp = self.__temp_sensor.get_outside_temperature()

        #When room temperature is higher than the preferred temperature and room temperature is higher than outside
        if room_temp > pref_temp and room_temp > out_temp:
            self.__window_mechanism.open_window()

            while self.__temp_sensor.get_room_temperature() > pref_temp:
                self.__temp_sensor.set_room_temperature(room_temp - 1)
                print("Airing room: " + str(room_temp))
                time.sleep(0.5)

            self.__window_mechanism.close_window()
            print("Temperature stabilized")
        #When room temperature is lower than preferred temperature and room temperature is lower than outside.
        elif room_temp < pref_temp and room_temp > out_temp:
            self.__window_mechanism.close_window()

            while self.__temp_sensor.get_room_temperature() < pref_temp:
                self.__temp_sensor.set_room_temperature(room_temp + 1)
                print("Heating room: " + str(room_temp))
                time.sleep(0.5)
                
            print("Temperature stabilized")
        #When room temperature is lower than preferred temperature and room temperature is lower than outside
        elif room_temp < pref_temp and room_temp < out_temp:
            self.__window_mechanism.open_window()

            while self.__temp_sensor.get_room_temperature() < pref_temp:
                self.__temp_sensor.set_room_temperature(room_temp + 1)
                print("Warming room: " + str(room_temp))
                time.sleep(0.5)
            
            self.__window_mechanism.close_window()
            print("Temperature stabilized")
        #When room temperature is higher than preferred temperature and room temperature is lower than outside
        elif room_temp > pref_temp and room_temp < out_temp:
            print("Air Conditioner turned on")

            while self.__temp_sensor.get_room_temperature() > pref_temp:
                self.__temp_sensor.set_room_temperature(room_temp - 1)
                print("Cooling room: " + str(room_temp))
                time.sleep(0.5)
            
            print("Temperature stabilized")
        
    def set_preferred_temperature(self, new_value):
        self.__preferred_temperature = new_value

    def get_preferred_temperature(self):
        return self.__preferred_temperature
    
    def get_mqtt_topic_header(self):
        return "windows/" + self.id + "/"
    

    def __mqtt_on_connect(client, userdata, flags, rc):
        header = get_mqtt_topic_header()
        self.__mqtt.subscribe(header + "closing-temp")
        self.__mqtt.subscribe(header + "curtain")
        self.__mqtt.subscribe(header + "curtain-time")
        self.__mqtt.subscribe(header + "window")

    def __mqtt_on_disconnect(client, userdata, rc):
        pass

    def __mqtt_on_message(client, userdata, message):
        if message.topic == "window":
            if message.payload == "Open":
                wm.open_window()
            elif message.payload == "Closed":
                wm.close_window()
        elif message.topic == "closing-temp":

        elif message.topic == "curtain":

        elif message.topic == "curtain-time":

    def __mqtt_on_publish(client, userdata, mid):
        pass

    def __mqtt_on_subscribe(client, userdata, mid, granted_qos):
        pass

    def __mqtt_on_unsubscribe(client, userdata, mid):
        pass
