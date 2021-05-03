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
        """Sets up virtual sensors and actuators as well as MQTT client"""
        self.id = id
        self.__preferred_temperature = preferred_temperature
        self.__curtain = self.CURTAIN
        self.__curtain.set_time_setting(curtain_time)

        self.__window_mechanism = self.WINDOW_MECHANISM
        self.__temp_sensor = self.TEMPERATURE_SENSOR

        self.__head = "Window #" + str(id) + " << "

        self.__mqtt = mqtt.MQTTClient()
        self.__mqtt.set_on_connect(self.__mqtt_on_connect)
        self.__mqtt.set_on_message(self.__mqtt_on_message)
        self.__mqtt.connect("sociot", "s7ci7tRGU", "soc-broker.rgu.ac.uk", 8883)

        self.run_window()
    
    def run_window(self):
        """Runs main loop on seperate thread"""
        threading.Thread(
            target=self.window_work,
            daemon=True
        ).start()

    def window_work(self):
        """Main loop, which monitors indoor and outside temperature and adjusts room temperature accordingly"""
        while True:
            room_temp = self.__temp_sensor.get_room_temperature()
            pref_temp = float(self.__preferred_temperature)
            out_temp = self.__temp_sensor.get_outside_temperature()

            #When room temperature is higher than the preferred temperature and room temperature is higher than outside
            if room_temp > pref_temp and room_temp > out_temp:
                self.__window_mechanism.open_window()

                while room_temp > pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp - 1)
                    print(self.__head + "Airing room: " + str(room_temp))
                    time.sleep(0.5)
                    room_temp = self.__temp_sensor.get_room_temperature()

                self.__window_mechanism.close_window()
                print(self.__head + "Temperature stabilized")
            #When room temperature is lower than preferred temperature and room temperature is lower than outside.
            elif room_temp < pref_temp and room_temp > out_temp:
                self.__window_mechanism.close_window()

                while room_temp < pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp + 1)
                    print(self.__head + "Heating room: " + str(room_temp))
                    time.sleep(0.5)
                    room_temp = self.__temp_sensor.get_room_temperature()
                    
                print(self.__head + "Temperature stabilized")
            #When room temperature is lower than preferred temperature and room temperature is lower than outside
            elif room_temp < pref_temp and room_temp < out_temp:
                self.__window_mechanism.open_window()

                while room_temp < pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp + 1)
                    print(self.__head + "Warming room: " + str(room_temp))
                    time.sleep(0.5)
                    room_temp = self.__temp_sensor.get_room_temperature()
                
                self.__window_mechanism.close_window()
                print(self.__head + "Temperature stabilized")
            #When room temperature is higher than preferred temperature and room temperature is lower than outside
            elif room_temp > pref_temp and room_temp < out_temp:
                print(self.__head + "Air Conditioner turned on")

                while room_temp > pref_temp:
                    self.__temp_sensor.set_room_temperature(room_temp - 1)
                    print(self.__head + "Cooling room: " + str(room_temp))
                    time.sleep(0.5)
                    room_temp = self.__temp_sensor.get_room_temperature()
                
                print(self.__head + "Temperature stabilized")
        
    def set_preferred_temperature(self, new_value):
        """Sets preferred temperature"""
        self.__preferred_temperature = new_value

    def get_preferred_temperature(self):
        """Gets preferred temperature"""
        return self.__preferred_temperature
    
    def get_mqtt_topic_header(self):
        """Gets the start of the MQTT topic, which includes the window id"""
        return "smart-windows/" + self.id + "/"
    
    def update_file_value(self, attribute, value):
        """Updates the specified value in the window_data.txt file"""
        window_data = []

        with open('window_data.txt', mode='r') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.FIELD_NAMES)

            for row in reader:
                try:
                    id_int = int(row["id"])
                    new_row = row.copy()

                    if str(id_int) == str(self.id):
                        new_row[attribute] = value

                    window_data.append(new_row)
                except ValueError:
                    pass

        with open('window_data.txt', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            writer.writeheader()
            writer.writerows(window_data)
    
    def __mqtt_on_connect(self, client, userdata, flags, rc):
        """On connection, subscribes to various topics on the MQTT broker"""
        print(self.__head + "Connected to MQTT broker with RC: " + str(rc))
        if rc == 0:
            header = self.get_mqtt_topic_header()
            self.__mqtt.subscribe(header + "pref-temp")
            self.__mqtt.subscribe(header + "curtain")
            self.__mqtt.subscribe(header + "curtain-time")
            self.__mqtt.subscribe(header + "window")
    
    def __mqtt_on_message(self, client, userdata, message):
        """When a message is received, run the code associated with the topic"""
        header = self.get_mqtt_topic_header()
        payload = message.payload.decode("utf-8")

        if message.topic == header + "window":
            if payload == "Open":
                self.__window_mechanism.open_window()
                print(self.__head + "WINDOW OPENED")
            elif payload == "Closed":
                self.__window_mechanism.close_window()
                print(self.__head + "WINDOW CLOSED")

        elif message.topic == header + "pref-temp":
            self.set_preferred_temperature(int(payload))
            self.update_file_value("pref_temp", payload)
            print(self.__head + "PREFERRED TEMPERATURE SET TO " + payload)

        elif message.topic == header + "curtain":
            if payload == "Open":
                self.__curtain.open_curtain()
                print(self.__head + "CURTAINS OPENED")
            elif payload == "Closed":
                self.__curtain.close_curtain()
                print(self.__head + "CURTAINS CLOSED")

        elif message.topic == header + "curtain-time":
            set_time_success = self.__curtain.set_time_setting(payload)
            if set_time_success:
                self.update_file_value("curtain_time", payload)
                print(self.__head + "SET CURTAINS OPEN TIME TO " + payload)
            else:
                print(self.__head + "ERROR: INVALID TIME RANGE FORMAT")