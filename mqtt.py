import paho.mqtt.client as mqtt
import ssl
import time
import sys
import json
import threading

class MQTTClient:
    def __init__(self, client_id="", clean_session=True):
        """Initialises the Paho MQTT client and six of the callback methods"""
        self.__client = mqtt.Client (client_id=client_id, clean_session=clean_session)

        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.on_subscribe = self.__on_subscribe
        self.__client.on_unsubscribe = self.__on_unsubscribe

    def connect(self, username, password, host, port):
        """Starts a new thread for running the connection code"""
        threading.Thread(
            target=self.__connect_thread,
            args=(username, password, host, port),
            daemon=True
        ).start()

    def __connect_thread(self, username, password, host, port):
        """Establishes a secure connection to an MQTT broker"""
        self.__client.username_pw_set(username, password)

        self.__client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
        self.__client.tls_insecure_set (False)

        self.__stop_threads = False

        self.__client.connect(host, port, keepalive = 60)
        self.__client.loop_forever(retry_first_connection=False)
        self.__client.connected_flag = False
        while not self.__client.connected_flag:
            time.sleep(1)

    def disconnect(self):
        """Disconnects from the MQTT broker"""
        if self.__client.connected_flag == True:
            self.__client.disconnect()
            self.__client.loop_stop()
        self.__stop_threads = True
    
    def __on_connect(self, client, userdata, flags, rc):
        """On connection, set the connected flag to True and run the specified callback"""
        if rc == 0:
            self.__client.connected_flag = True
        else:
            self.__client.connected_flag = False

        try:
            self.__on_connect_method(client, userdata, flags, rc)
        except AttributeError:
            pass

    def __on_disconnect(self, client, userdata, rc):
        """On disconnection, set the connected flag to False and run the specified callback"""
        self.__client.connected_flag = False
        try:
            self.__on_disconnect_method(client, userdata, rc)
        except AttributeError:
            pass
    
    def __on_message(self, client, userdata, msg):
        """Run the specified callback on message receive"""
        try:
            self.__on_message_method(client, userdata, msg)
        except AttributeError:
            pass

    def __on_publish(self, client, userdata, mid):
        """Run the specified callback on publish"""
        try:
            self.__on_publish_method(client, userdata, mid)
        except AttributeError:
            pass

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        """Run the specified callback on subscribe"""
        try:
            self.__on_subscribe_method(client, userdata, mid, granted_qos)
        except AttributeError:
            pass
    
    def __on_unsubscribe(self, client, userdata, mid):
        """Run the specified callback on unsubscribe"""
        try:
            self.__on_unsubscribe_method(client, userdata, mid)
        except AttributeError:
            pass

    def set_callbacks(self, callbacks):
        """Allows for setting multiple callbacks via a dictionary"""
        if "on_connect" in callbacks:
            self.set_on_connect(callbacks["on_connect"])
        if "on_disconnect" in callbacks:
            self.set_on_disconnect(callbacks["on_disconnect"])
        if "on_message" in callbacks:
            self.set_on_message(callbacks["on_message"])
        if "on_publish" in callbacks:
            self.set_on_publish(callbacks["on_publish"])
        if "on_subscribe" in callbacks:
            self.set_on_subscribe(callbacks["on_subscribe"])
        if "on_unsubscribe" in callbacks:
            self.set_on_unsubscribe(callbacks["on_unsubscribe"])
    
    def set_on_connect(self, callback):
        """Sets on_connect callback"""
        self.__on_connect_method = callback
    
    def set_on_disconnect(self, callback):
        """Sets on_disconnect callback"""
        self.__on_disconnect_method = callback

    def set_on_message(self, callback):
        """Sets on_message callback"""
        self.__on_message_method = callback

    def set_on_publish(self, callback):
        """Sets on_publish callback"""
        self.__on_publish_method = callback
    
    def set_on_subscribe(self, callback):
        """Sets on_subscribe callback"""
        self.__on_subscribe_method = callback
    
    def set_on_unsubscribe(self, callback):
        """Sets on_unsubscribe callback"""
        self.__on_unsubscribe_method = callback

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        """Allows for easy publishing of a topic"""
        if self.__client.connected_flag:
            print("Publishing " + str(payload) + " to topic " + topic)
            self.__client.publish(topic, payload, qos, retain, properties)
        else:
            print("Connected flag is " + self.__client.connected_flag)
    
    def subscribe(self, topic, qos=0, options=None, properties=None):
        """Allows for easy subscribing to a topic"""
        if self.__client.connected_flag:
            print("Subscribing to topic " + topic)
            self.__client.subscribe(topic, qos, options, properties)
