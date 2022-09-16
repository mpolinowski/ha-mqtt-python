import json, sys, time
import paho.mqtt.client as mqtt
import optparse
# Import MQTT Broker configuration from config.py
from config import *


def parse_options():
    # create OptionParser object
	parser = optparse.OptionParser()
	
	# add options
	parser.add_option('-f', type = 'string', dest = "filename",
					help = 'INFO :: Specify the configuration file location')
	
    # check if filepath is defined
	(options, args) = parser.parse_args()
	if (options.filename == None):
			print ('ERROR :: Use the flag -f to specify a configuration file location')
			exit(0)

	filepath = options.filename
			
	
	return filepath


def on_connect(client, userdata, flags, rc, properties=None):
    if rc==0:
        print("INFO :: Connected to MQTT Broker")
    else:
        print("ERROR :: Connection failed:", rc)


if __name__ == "__main__":
    # connect mqttv5 client
    client = mqtt.Client(client_id = mqtt_client_id, protocol = mqtt.MQTTv5, transport = mqtt_transport)
    client.username_pw_set(username = mqtt_username, password = mqtt_password)
    client.connect(host = mqtt_server_host, port = mqtt_server_port,
                    keepalive = mqtt_keepalive, bind_address = mqtt_bind_address, bind_port = mqtt_bind_port, properties = None)
    client.on_connect = on_connect

    # parse options to get filepath
    get_filepath = parse_options()

    # # load configuration file
    f = open(get_filepath)
    json_array = json.load(f)
    
    # publish configuration updates
    for entity in json_array['entities']:
        client.publish(entity['topic'],entity['payload'],retain=True)
        time.sleep(0.100)
    f.close()

    # disconnect
    client.loop_stop()
    client.disconnect()
    print("INFO :: Closed connection to broker")
    sys.exit()