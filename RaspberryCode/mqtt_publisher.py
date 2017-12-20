# Created by Omer Shwartz (www.omershwartz.com)
#
# This script uses device credentials to publish events to the MQTT broker residing in Google Cloud.
# Using this code a device can 'talk' to the server.
#
# This file may contain portions of cloudiot_mqtt_example.py licensed to Google
# under the Apache License, Version 2.0. The original version can be found in
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
#
############################################################

import datetime
import time
import os, filecmp, md5

import jwt
import paho.mqtt.client as mqtt

from time import gmtime, strftime
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from threading import Thread
from time import sleep

project_id = 'universalclockandweather'  # Enter your project ID here
registry_id = 'raspberrym123'  # Enter your Registry ID here
device_id = 'rasp123'  # Enter your Device ID here
ca_certs = 'roots.pem'  # The location of the Google Internet Authority certificate, can be downloaded from https://pki.google.com/roots.pem
private_key_file = 'rsa_private.pem'  # The location of the private key associated to this device

# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
algorithm = 'RS256'
mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 443  # port 8883 is blocked in BGU network
mqtt_topic = '/devices/{}/{}'.format(device_id,
                                     'events')  # Published messages go to the 'events' topic that is bridged to pubsub by Google
###

tempToServer = 0
mesaggeFromServer = 0
sidePress = 0
hash1 = 0


def threaded_function():
    global tempToServer
    t = strftime("%H:%M", gmtime())
    message = 'Time:' + t

    sense.show_message(message, scroll_speed=(0.08), text_colour=[176, 224, 230], back_colour=[0, 0, 0])
    sense.clear()

    temp = sense.get_temperature()
    message = 'Temp: %.2f ' % (temp)
    tempToServer = '%.2f' % temp
    sense.show_message(message, scroll_speed=(0.08), text_colour=[200, 0, 200], back_colour=[0, 0, 0])
    sense.clear()


def showMessageFromServer(message):
    print("about to print:" + message)
    sense.show_message(message, scroll_speed=(0.08), text_colour=[200, 0, 200], back_colour=[0, 0, 0])
    print ("FINISH print server message on sensor")


def pushed_left(event):
    global sidePress
    if event.action != ACTION_RELEASED:
        sidePress = 'left'
        print('LEFT')
        # = sidePress, tempToServer
        # print(payload)


def pushed_right(event):
    global sidePress
    if event.action != ACTION_RELEASED:
        sidePress = 'right'
        print('RIGHT')


sense = SenseHat()

############ Joystick listner##########
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right


def create_jwt():
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.utcnow(),
        # The time the token expires.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


# Create our MQTT client. The client_id is a unique string that identifies
# this device. For Google Cloud IoT Core, it must be in the format below.
client = mqtt.Client(
    client_id=('projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id,
        cloud_region,
        registry_id,
        device_id)))

# With Google Cloud IoT Core, the username field is ignored, and the
# password field is used to transmit a JWT to authorize the device.
client.username_pw_set(
    username='unused',
    password=create_jwt())

# Enable SSL/TLS support.
client.tls_set(ca_certs=ca_certs)

# Register message callbacks. https://eclipse.org/paho/clients/python/docs/
# describes additional callbacks that Paho supports. In this example, the
# callbacks just print to standard out.
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Connect to the Google MQTT bridge.
client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

# set the join file path that both publisher and sub' will read/write to

_cached_stamp = 0
filename = 'serverFiles/serverUpdates.txt'
while True:
    stamp = os.stat(filename).st_mtime
    if stamp != _cached_stamp:
        _cached_stamp = stamp
        print ("There is an update in FILE")
        f = open("serverFiles/serverUpdates.txt", "r")
        sss = f.read()
        print ("the file is:" + sss)
        if len(sss) > 1:
            print ("Message gets from client, reading it")
            thread = Thread(target=showMessageFromServer(sss))
            thread.start()
            thread.join()
        else:
            print ("The Message is empty")
            thread = Thread(target=threaded_function)
            thread.start()
            thread.join()
    else:
        print ("No added nothing, starting new iteration")
        thread = Thread(target=threaded_function)
        thread.start()
        thread.join()

    client.loop_start()
    # Start the network loop.
    # Publish num_messages mesages to the MQTT bridge once per second.
    for i in range(1):
        temp = sense.get_temperature()
        tempToServer = '%.2f' % temp
        t = strftime("%H:%M", gmtime())
        if sidePress == 0:
            break;

        payload = sidePress + "," + tempToServer + "," +t

        print('Publishing Message {}'.format(i))
        print (payload)
        # Publish "payload" to the MQTT topic. qos=1 means at least once
        # delivery. Cloud IoT Core also supports qos=0 for at most once
        # delivery.
        client.publish(mqtt_topic, payload, qos=1)

        # Send events every second
        time.sleep(1)

    # End the network loop and finish.
    client.loop_stop()
    print('Finished sending message.')
