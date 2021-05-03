import window_mechanism as wm 
import TemperatureSensor as ts 
import curtain as c
import csv
import mqtt
import random
import time
import threading

class Window():
    WINDOW_MECHANISM = wm.WindowMechanism()
    TEMPERATURE_SENSOR = ts.TemperatureSensor()
    CURTAIN = c.Curtain()
    FIELD_NAMES = ["id","pref_temp","curtain_time"]

    def __init__(self, id=0, preferred_temperature=0, curtain_time="0700-1900"):
        self.id = id
        self.__preferred_temperature = preferred_temperature
        self.__curtain = self.CURTAIN
        self.__curtain.set_time_setting(curtain_time)

        self.__window_mechanism = self.WINDOW_MECHANISM
        self.__temp_sensor = self.TEMPERATURE_SENSOR

        self.__head = "Window #" + str(id) + "<< "
        
        #self.__field_names_csv = self.__to_csv_format(self.FIELD_NAMES)

        self.__mqtt = mqtt.MQTTClient()
        self.__mqtt.set_on_connect(self.__mqtt_on_connect)
        self.__mqtt.set_on_message(self.__mqtt_on_message)
        self.__mqtt.connect("sociot", "s7ci7tRGU", "soc-broker.rgu.ac.uk", 8883)

        self.run_window()
    
    def run_window(self):
        threading.Thread(
            target=window_work,
            daemon=True
        ).start()

    def window_work(self):
        room_temp = self.__temp_sensor.get_room_temperature()
        pref_temp = self.__preferred_temperature
        out_temp = self.__temp_sensor.get_outside_temperature()
        
        while True:
            #When room temperature is higher than the preferred temperature and room temperature is higher than outside
            if room_temp > pref_temp and room_temp > out_temp:
                self.__window_mechanism.open_window()

                while self.__temp_sensor.get_room_temperature() > pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp - 1)
                    print(self.__head + "Airing room: " + str(room_temp))
                    time.sleep(0.5)

                self.__window_mechanism.close_window()
                printself.__(head + "Temperature stabilized")
            #When room temperature is lower than preferred temperature and room temperature is lower than outside.
            elif room_temp < pref_temp and room_temp > out_temp:
                self.__window_mechanism.close_window()

                while self.__temp_sensor.get_room_temperature() < pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp + 1)
                    print(self.__head + "Heating room: " + str(room_temp))
                    time.sleep(0.5)
                    
                print(self.__head + "Temperature stabilized")
            #When room temperature is lower than preferred temperature and room temperature is lower than outside
            elif room_temp < pref_temp and room_temp < out_temp:
                self.__window_mechanism.open_window()

                while self.__temp_sensor.get_room_temperature() < pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp + 1)
                    print(self.__head + "Warming room: " + str(room_temp))
                    time.sleep(0.5)
                
                self.__window_mechanism.close_window()
                print(self.__head + "Temperature stabilized")
            #When room temperature is higher than preferred temperature and room temperature is lower than outside
            elif room_temp > pref_temp and room_temp < out_temp:
                print(self.__head + "Air Conditioner turned on")

                while self.__temp_sensor.get_room_temperature() > pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp - 1)
                    print(self.__head + "Cooling room: " + str(room_temp))
                    time.sleep(0.5)
                
                print(self.__head + "Temperature stabilized")
        
    def set_preferred_temperature(self, new_value):
        self.__preferred_temperature = new_value

    def get_preferred_temperature(self):
        return self.__preferred_temperature
    
    def get_mqtt_topic_header(self):
        return "windows/" + self.id + "/"
    
    def update_file_value(self, window_id, attribute, value):
        window_data = []

        with open('window_data.txt', mode='r') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.FIELD_NAMES)
            for row in reader:
                id_int = int(row["id"])

                if id_int == window_id:
                    row[attribute] = value
                
                window_data.append(row)

        with open('window_data.txt', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            writer.writeheader()
            writer.writerows(window_data)
    
    """def __to_csv_format(self, list_in):
        csv_string = ""
        list_length = len(list_in)
        for i in range(0, list_length):
            csv_string += elm
            if i == list_length - 1: break
            csv_string += ","
        return csv_string"""

    def __mqtt_on_connect(client, userdata, flags, rc):
        header = get_mqtt_topic_header()
        self.__mqtt.subscribe(header + "pref-temp")
        self.__mqtt.subscribe(header + "curtain")
        self.__mqtt.subscribe(header + "curtain-time")
        self.__mqtt.subscribe(header + "window")

    def __mqtt_on_disconnect(client, userdata, rc):
        pass

    def __mqtt_on_message(client, userdata, message):
        if message.topic == "window":
            if message.payload == "Open":
                self.__window_mechanism.open_window()
            elif message.payload == "Closed":
                self.__window_mechanism.close_window()
        elif message.topic == "pref-temp":
            self.set_preferred_temperature(int(message.payload))
        elif message.topic == "curtain":
            if message.payload == "Open":
                self.__curtain.open_curtain()
            elif message.payload == "Closed":
                self.__curtain.close_curtain()
        elif message.topic == "curtain-time":
            self.__curtain.set_time_setting(message.payload)

    def __mqtt_on_publish(client, userdata, mid):
        pass

    def __mqtt_on_subscribe(client, userdata, mid, granted_qos):
        pass

    def __mqtt_on_unsubscribe(client, userdata, mid):
        pass
