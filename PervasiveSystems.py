'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

'''
/*
 * Modifications copyright (C) 2018 Roberto Falconi
 * LinkedIn: https://www.linkedin.com/in/robertofalconi95/
 * GitHub: https://github.com/RobertoFalconi95/HouseTemperatureMonitoring
 * Full description: https://www.hackster.io/Falkons/house-temperature-monitoring-with-aws-and-raspberry-3b6410
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

# TO EMULATE AWS IoT Button FROM AWS Test:

'''
{
  "serialNumber": "G030PT023203RNXB",
  "batteryVoltage": "1697mV",
  "clickType": "SINGLE"
}
'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import argparse
import json
import os
import sys
import AWSIoTPythonSDK
sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import getopt
import datetime
import pigpio
import tmp_sensors
	
#i2c bus of the Raspberry Pi 3
i2c_bus = 1
#TMP 102 address on the i2c bus
addr = 0x48

dev_pi = pigpio.pi()
dev_tmp = dev_pi.i2c_open(i2c_bus, addr, 0)
#for TMP 102 read from register 0x0
register_n = 0

AllowedActions = ['both', 'publish', 'subscribe']

TriggerD = False

def tmp102_reading(byte0, word0):
    #calculation of the temperature based on
    #the first word and the first byte
    # !!! not tested for negative temperatures !!!!
    #last 4 bits of the word0
    l4b = (word0 & 0b1111000000000000)>>12
    temperature = ((byte0<<4) | l4b) * 0.0625
    return temperature

# Custom MQTT message callback
def customCallback(client, userdata, message):
    global TriggerD
    try: # Check if the message is from AWS IoT Button
        clickType = message.payload.split(",")[2].split(":")[1].strip("}").strip().strip('"')
        print("Click type: " + clickType)
        
        if (clickType == "SINGLE"):
            print("E-mail sent")
            
        if (clickType == "DOUBLE"):
            
            if TriggerD == False: 
                print("Switching on TMP102")
                TriggerD = True
                
            elif TriggerD == True: 
                print("Switching off TMP102")
                TriggerD = False
                
        if (clickType == "LONG"):
            print("Ciaoooooooooooooo")
            
    except IndexError:
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="iotbutton/+", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
command_str = ''
topic = "iotbutton/0"
delay_s = 5
sensor_sn = 'My Raspberry Pi 3'

try:
	while True:
		while TriggerD == True:
			loopCount += 1
			t_word = dev_pi.i2c_read_word_data(dev_tmp, register_n)
			t = tmp_sensors.tmp102_reading(t_word)
			timestamp = datetime.datetime.now()
			print(' Temperature: {} C   Loop # {:d}'.format(t,loopCount))
			print(' Time: {} \n'.format(timestamp))
			msg = '"Device": "{:s}", "Temperature": "{}", "Record number": "{}"'.format(sensor_sn, t,loopCount)
			msg = '{'+msg+'}'
			myAWSIoTMQTTClient.publish(topic, msg, 1)
			print('Sleeping...')
			time.sleep(delay_s)
except KeyboardInterrupt:
	pass
    
    
print('Exiting the loop');
r = dev_pi.i2c_close(dev_tmp)
myAWSIoTMQTTClient.disconnect()
print('Disconnected from AWS')
    
    
