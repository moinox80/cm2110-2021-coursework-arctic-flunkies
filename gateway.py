import mqtt
import Adafruit_IO as aio
import json
import threading
import time
from queue import Queue

class Gateway:
    def __init__(self):
        """self.__q = Queue()
        queue_thread = threading.Thread(
            target=self.run_queue,
            daemon=True
        ).start()"""

        self.__mqtt = mqtt.MQTTClient()
        self.__mqtt.set_callbacks({
            "on_connect": self.mqtt_on_connect,
            "on_disconnect": self.mqtt_on_disconnect,
            "on_message": self.mqtt_on_message,
            "on_publish": self.mqtt_on_publish,
            "on_subscribe": self.mqtt_on_subscribe,
            "on_unsubscribe": self.mqtt_on_unsubscribe
        })
        self.__mqtt.connect("sociot", "s7ci7tRGU", "soc-broker.rgu.ac.uk", 8883)

        self.__aio_client = aio.Client("arthur_s", "aio_aDxm81JJmPzBbK3PAcEN9bW2sRWC")

        self.__feeds = ("closing-temp", "curtain", "curtain-time", "window")
        self.__feed_watch = {}

        aio_thread = threading.Thread(
            target=self.monitor_feeds,
            daemon=True
        ).start()
    
    def send_to_feed(self, feed, data):
        try:
            self.__aio_client.create_data(feed, aio.Data(value=data))
        except aio.RequestError:
            print("Error while connecting to Adafruit")

    def data(self, feed):
        try:
            return self.__aio_client.data(feed)
        except aio.RequestError:
            print("Error while connecting to Adafruit")
    
    def mqtt_on_connect(self, client, userdata, flags, rc):
        print("Connected with rc code " + str(rc))
    
    def monitor_feeds(self):
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
                        self.__mqtt.publish("windows/0/" + value_name, self.__feed_watch[value_name])
            except IndexError:
                pass

    def mqtt_on_disconnect(self, client, userdata, rc):
        pass

    def mqtt_on_message(self, client, userdata, message):
        pass

    def mqtt_on_publish(self, client, userdata, mid):
        pass

    def mqtt_on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def mqtt_on_unsubscribe(self, client, userdata, mid):
        pass

    """def run_queue(self):
        while True:
            if not self.__q.empty():"""
