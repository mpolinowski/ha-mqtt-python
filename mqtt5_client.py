import json
import paho.mqtt.client as mqtt
import sys
import time

from config import *

f = open('config_topics.json')

json_array = json.load(f)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc==0:
        print("INFO :: Connected to MQTT Broker")
    else:
        print("ERROR :: Connection failed:", rc)

if __name__ == "__main__":
    client = mqtt.Client(client_id = mqtt_client_id, protocol = mqtt.MQTTv5, transport = mqtt_transport)
    client.username_pw_set(username = mqtt_username, password = mqtt_password)
    client.connect(host = mqtt_server_host, port = mqtt_server_port,
                    keepalive = mqtt_keepalive, bind_address = mqtt_bind_address, bind_port = mqtt_bind_port, properties = None)
    client.on_connect = on_connect

    for entity in json_array['entities']:
        client.publish(entity['topic'],entity['payload'],retain=True)
        time.sleep(0.100)
    f.close()

    client.loop_stop()
    client.disconnect()
    print("INFO :: Closed connection to broker")
    sys.exit()