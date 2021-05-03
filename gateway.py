import mqtt
import Adafruit_IO as aio
import json
import threading
import time

class Gateway:
    def __init__(self):
        """Sets up MQTT and Adafruit connection clients"""
        self.__mqtt = mqtt.MQTTClient()
        self.__mqtt.set_on_connect(self.__mqtt_on_connect)
        self.__mqtt.connect("sociot", "s7ci7tRGU", "soc-broker.rgu.ac.uk", 8883)
        
        #self.__aio_client = aio.Client()
        self.__aio_client = aio.Client("arthur_s", "aio_aDxm81JJmPzBbK3PAcEN9bW2sRWC")

        self.__feeds = ("pref-temp", "curtain", "curtain-time", "window")
        self.__feed_watch = {}

        aio_thread = threading.Thread(
            target=self.__monitor_feeds,
            daemon=True
        ).start()
    
    def send_to_feed(self, feed, data):
        """Sends data to specified Adafruit feed"""
        try:
            self.__aio_client.create_data(feed, aio.Data(value=data))
        except aio.RequestError:
            print("Error while connecting to Adafruit")

    def data(self, feed):
        """Returns data from specified Adafruit feed"""
        try:
            return self.__aio_client.data(feed)
        except aio.RequestError:
            print("Error while connecting to Adafruit")
    
    def __mqtt_on_connect(self, client, userdata, flags, rc):
        """Prints out a string containing RC on connection"""
        print("Connected to MQTT broker with RC: " + str(rc))
    
    def __monitor_feeds(self):
        """Looks for changes in Adafruit feeds and publishes new data to MQTT broker"""
        while True:
            differences = []
            for feed in self.__feeds:
                try:
                    feed_data = self.__aio_client.data(feed)
                    new_value = feed_data[0].value

                    try:
                        if self.__feed_watch[feed] == new_value:
                            differences.append(False)
                        else:
                            differences.append(True)
                    except KeyError:
                        pass

                    self.__feed_watch[feed] = new_value
                except aio.RequestError:
                    pass
                
            try:
                for i in range(0, len(self.__feed_watch)):
                    if differences[i]:
                        value_name = self.__feeds[i]
                        self.__mqtt.publish("smart-windows/0/" + value_name, self.__feed_watch[value_name])
            except IndexError:
                pass
