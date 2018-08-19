#  ================================================================
#  IOT Assignment 2 - Get Data
#  Authors: Pang Yong Jie, Sim Shi Jie Keith, Tang Wei Shawn
#  ================================================================
#  Import necessary API/Modules/Libraries
#  ================================================================
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import ast
from boto3.dynamodb.conditions import Key, Attr
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import re

#  ===============================================================
#  Functions
#  ===============================================================
# Custom MQTT message callback
def customCallback(client, userdata, message):
    global currentHolder
    print("Received a new message: ")
    print(message.payload)
    currentHolder = message.payload
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    

# Helper class to convert a DynamoDB item to JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
    
# Getting the lot ID based on the current holder retrieved    
def get_lotid(currentHolder):

    table = dynamodb.Table('Parking_Lots')
    
    # Retrieving the values from the DynamoDB table based on the current holder
    response = table.scan(
        FilterExpression= Attr('Current_Holder').contains(currentHolder)
    )
    
    items = response['Items']
    
    # Retrieving the lot id and carpark and set it as the mqtt message if there are values found
    if items:
        Distance, current_Holder, current_Holder2, current_Holder3, current_Holder4, currentHolder_5, Carpark_Name, ID=str(items).split(',', 7)
        lot, lot_id= str(ID).split(':', 1)
        lot_id = re.sub("['u }\] ]", '', lot_id)
        park, car_park = str(Carpark_Name).split(':', 1)
        car_park = re.sub("^\su'", '', car_park)
        car_park = re.sub("'$", '', car_park)
        mqtt_message =  "Your lot ID is "+lot_id+ " at "+ car_park
    
    #Set the mqtt message as No lot ID found if no values are found
    else:
        mqtt_message = "No lot ID found"
    
    # Publish the mqtt message to topic sensors/lotid
    my_rpi.publish("sensors/lotid", mqtt_message, 1)
    print("Lot ID sent")
    print("Awaiting for request")

    return None

#  ===================================================================
#  Variable Declarations
#  ===================================================================
currentHolder = ""
host = "xxxxxxxxxxxxxx.iot.us-west-2.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

#  ===================================================================
#  Main
#  ===================================================================
if __name__ == "__main__":
    
    my_rpi = AWSIoTMQTTClient("basic2PubSub")
    my_rpi.configureEndpoint(host, 8883)
    my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
    my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
    my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    my_rpi.connect()
    
    # Subscribing to topic sensors/currenHolder to retrieve the current holder
    my_rpi.subscribe("sensors/currentHolder", 1, customCallback)

    dynamodb = boto3.resource('dynamodb', aws_access_key_id="XXXXXXXXXXXXXXXXXXXX",
                              aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                              region_name='us-west-2')
    print("Awaiting for request")
    
    while True:
        global currentHolder
        if currentHolder is not "":
            # Calling get_lotid function with currentHolder passed in as the parameter
            get_lotid(currentHolder)
            # Set the currentHolder to an empty string so that the loop will continue after get_lotid function is complete
            currentHolder = ""




