#  ================================================================
#  IOT Assignment 2 - Entry Gantry
#  Authors: Tang Wei Shawn, Sim Shi Jie Keith, Pang Yong Jie
#  ================================================================
#  Import necessary API/Modules/Libraries
#  ================================================================
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO
from rpi_lcd import LCD
import MFRC522
import signal
import boto3
import re
import json
import ast
from boto3.dynamodb.conditions import Key, Attr


#  ===============================================================
#  Functions
#  ===============================================================

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


# To get recommended_lot that is nearest to the lobby based on the distance from lobby
def recommended_lot():
    table = dynamodb.Table('Parking_Lots')
    response = table.scan(
        FilterExpression=Attr('Carpark_Name').contains(carparkname) & Attr('Current_Holder').contains('None')
    )

    items = response['Items']
    list_of_distances = {}
    for i in items:
        Distance, current_holder, Carpark_Name, ID = str(i).split(',', 3)
        d, actual_distance = str(Distance).split(':', 1)
        lot, actual_lot = str(ID).split(':', 1)
        actual_distance = re.sub("['u ]", '', actual_distance)
        actual_lot = re.sub("['u} ]", '', actual_lot)
        list_of_distances[actual_lot] = actual_distance

    try:
        display1 = "Recommended Lot is:"
        display2 = "{}".format(min(list_of_distances))

    except:
        display1 = "Entry Granted"
        display2 = "But No Lots"

    return display1, display2


# To display strings on the LCD
def display(string1, string2):
    # LCD Display
    lcd.text(string1, 1)
    lcd.text(string2, 2)


# To check if the rfid(car) already exists or not in the Parking table
def check_if_exists(uid, carparkname):
    table = dynamodb.Table('Parking')
    response = table.scan(
        FilterExpression=Attr('RFID').contains(uid) & Attr('CurrentStatus').contains('Active') & Attr('Carpark_Name').contains(carparkname)
    )
    item = response['Items']
    if item:
        return True
    else:
        return False


# To get the number of available lots
def available_lots(carparkname):
    table = dynamodb.Table('Carparks')
    response = table.query(
        KeyConditionExpression=Key('Carpark_Name').eq(carparkname),
    )

    for i in response[u'Items']:
        json.dumps(i, cls=DecimalEncoder)

    availablelotsjson = (ast.literal_eval(json.dumps(i)))
    number = availablelotsjson['Available_Lots']
    if int(number) > 0:
        display1 = "Available lots:"
        display2 = number
    else:
        display1 = "   CARPARK IS   "
        display2 = "      FULL      "
    return display1, display2


#  ===================================================================
#  Variable Declarations
#  ===================================================================
carparkname = "Bukit Batok Carpark"
uid = None
prev_uid = None
continue_reading = True
host = "XXXXXXXXXXXXXXXXXX.us-west-2.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()
lcd = LCD()


my_rpi = AWSIoTMQTTClient("basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("sensors/parkingdb", 1, customCallback)

dynamodb = boto3.resource('dynamodb', aws_access_key_id="XXXXXXXXXXXXXXXXXXXX",
                          aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                          region_name='us-west-2')


#  ===================================================================
#  Main
#  ===================================================================
if __name__ == "__main__":
    print("Entry Gantry Scanning for Next Car")

    # Publish to the same topic in a loop forever
    while continue_reading:
        # Scan for cards
        # Constantly Display Available lots
        display1, display2 = available_lots(carparkname)
        display(display1, display2)
        (status, TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

        # If a card is found
        if status == mfrc522.MI_OK:

            # Get the UID of the card
            (status, uid) = mfrc522.MFRC522_Anticoll()

            print("Car detected! The UID is {}".format(uid))

            if check_if_exists(str(uid), carparkname) is False:

                # Display recommended lot
                display1, display2 = recommended_lot()
                display(display1, display2)

                # Data
                timestamp = datetime.now()
                currentstatus = "Active"
                pricepaid = "0.00"
                mqtt_message = "{\"RFID\":\"" + str(uid) + "\",\"Timestamp\":\"" + str(timestamp) + "\",\"CurrentStatus\":\"" + currentstatus + "\",\"Carpark_Name\":\"" + carparkname + "\",\"Price_Paid\":\"" + pricepaid + "\" }"
                my_rpi.publish("sensors/parkingdb", mqtt_message, 1)
                sleep(2)
            else:
                print("Car is already in "+carparkname)
            print("Entry Gantry Scanning for Next Car")