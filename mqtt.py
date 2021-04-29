import paho.mqtt.Client as mqtt
import ssl
import time
import sys
import json

class MQTTClient:
    def connect(self, user_name, password, clean_session, host, port):
        """ Setup and connect to MQTT broker (using TLS) with the provided parameters 
        :param user_name: For authentication with the broker
        :type user_name: String
        :param password: For authentication with the broker
        :type password: String
        :param clean_session: If the client should connection with a clean session or not
        :type clean_session: Boolean
        :param host: Address of host to connect to
        :type host: String
        :param port: Port of host to connect to
        :type host: Int
        """ 
        self.__client = mqtt.Client (client_id = "" , clean_session = clean_session)
        self.__client.username_pw_set (user_name, password)
        # configure TLS connection
        self.__client.tls_set (cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
        self.__client.tls_insecure_set (False)

        # call back methods
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.on_subscribe = self.__on_subscribe
        self.__client.on_unsubscribe = self.__on_unsubscribe

        # connect using keepalive to 60
        print("connecting")
        self.__client.connect(host, port, keepalive = 60)
        self.__client.loop_forever(retry_first_connection=False)
        self.__client.connected_flag = False
        while not self.__client.connected_flag:           #wait in loop
            print("not yet")
            time.sleep (1)

    def disconnect(self):
        """ Disconnected from the MQTT broker, if connected """
        if self.__client.connected_flag == True:
            self.__client.disconnect()
            self.__client.loop_stop()
        self.__stop_threads = True
        # self._f.close()
    
    def __on_connect(self, userdata, flags, rc):
        pass

    def __on_disconnect(self, userdata, rc):
        pass
    
    def __on_message(self, userdata, msg):
        pass

    def __on_publish(self, userdata, mid):
        pass

    def __on_subscribe(self, userdata, mid, granted_qos):
        pass
    
    def __on_unsubscribe(self, userdata, mid):
        pass

    def set_callbacks(self, callbacks):
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
        self.__client.on_connect = callback
    
    def set_on_disconnect(self, callback):
        self.__client.on_disconnect = callback

    def set_on_message(self, callback):
        self.__client.on_message = callback

    def set_on_publish(self, callback):
        self.__client.on_publish = callback
    
    def set_on_subscribe(self, callback):
        self.__client.on_subscribe = callback
    
    def set_on_unsubscribe(self, callback):
        self.__client.on_unsubscribe = callback
    


    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        if self._client.connected_flag:
            self.__client.publish(self, topic, payload, qos, retain, properties)
    
    def subscribe(self, topic, qos=0, options=None, properties=None):
        if self._client.connected_flag:
            self.__client.subscribe(self, topic, qos, options, properties)
