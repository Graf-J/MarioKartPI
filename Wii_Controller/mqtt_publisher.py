from paho.mqtt import client as mqtt_client
import json

class Publisher:
    
    def __init__(self, broker_address, broker_port, topic, client_id):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.topic = topic
        self.client_id = client_id
        
        self.connect()
        
    
    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print "Connected to MQTT Broker!"
            else:
                print "Failed to connect"

        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker_address, self.broker_port)
        
    
    def start(self):
        self.client.loop_start()
        
    
    def publish(self, values):
        json_string = json.dumps(values)
        result = self.client.publish(self.topic, json_string)
        
        status = result[0]
        if status == 0:
            print "-> " + self.topic + " -> " + json_string
        else:
            print "Failed to send message to topic"
        
        
    
