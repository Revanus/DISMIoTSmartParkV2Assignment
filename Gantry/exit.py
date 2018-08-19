#  ================================================================
#  IOT Assignment 2 - Exit Gantry
#  Authors: Tang Wei Shawn, Sim Shi Jie Keith, Pang Yong Jie
#  ================================================================
#  Import necessary API/Modules/Libraries
#  ================================================================

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
from time import sleep
from dateutil.parser import parse
import RPi.GPIO as GPIO
from rpi_lcd import LCD
import MFRC522
import signal
import boto3
import json
import ast
import re
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

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


# To get the entrytime of the rfid(car)
def get_timestamp(uid, carparkname):
    table = dynamodb.Table('Parking')
    response = table.scan(
        FilterExpression=Attr('RFID').contains(uid) & Attr('CurrentStatus').contains('Active') & Attr('Carpark_Name').contains(carparkname)
    )
    item = response['Items']
    RFID, Timestamp, CurrentStatus, Carpark_Name = str(item).split(',', 3)
    ts, actual_timestamp = str(Timestamp).split(':', 1)
    actual_timestamp = re.sub("['u]", '', actual_timestamp)
    actual_timestamp = actual_timestamp.lstrip()

    return actual_timestamp


# To set the status of the row to be Inactive as car has exited
def set_status(uid, timestamp,pricepaid):
    table = dynamodb.Table('Parking')
    table.update_item(
        Key={
            'RFID': uid,
            'Timestamp': timestamp
        },
        UpdateExpression='SET CurrentStatus = :val, Price_Paid = :val2',
        ExpressionAttributeValues={
            ':val': "Inactive",
            ':val2': pricepaid
        }
    )
    return None


# To get the price that has to be paid
def get_price (timestampraw):
    timestamp = parse(timestampraw)
    delta = datetime.now() - timestamp
    secondsparked = int(delta.total_seconds())
    if secondsparked - 15 > 0:
        price = secondsparked * 0.001
        price = Decimal(price).quantize(Decimal("0.01"))
    else:
        price = "0.00"
    if float(price) > 0:
        display("Price of Parking", "$"+str(price))
    else:
        display("Entry is Free", "")

    return str(price)


#  ===================================================================
#  Variable Declarations
#  ===================================================================
carparkname = "Bukit Batok Carpark"
uid = None
prev_uid = None
continue_reading = True
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()
lcd = LCD()

dynamodb = boto3.resource('dynamodb', aws_access_key_id="XXXXXXXXXXXXXXXXXXXX",
                          aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                          region_name='us-west-2')



#  ===================================================================
#  Main
#  ===================================================================
if __name__ == "__main__":
    # Publish to the same topic in a loop forever
    print("Exit Gantry Scanning for Next Car")
    while continue_reading:
        display("   Smart Park   ", "Please Slow Down")
        # Scan for cards
        (status, TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

        # If a card is found, delete and dislay payment
        if status == mfrc522.MI_OK:
            # Get the UID of the card
            (status, uid) = mfrc522.MFRC522_Anticoll()
            print("Car detected! The UID is {}".format(uid))

            if check_if_exists(str(uid), carparkname) is True:

                # Data
                uid = str(uid)
                timestamp = get_timestamp(uid, carparkname)
                price = get_price(timestamp)
                set_status(uid, timestamp, price)
                print("Price was "+price)
                sleep(3)
                display("Have a Nice Day", "")
                sleep(2)
            else:
                print("Car Not Found in Car Park")
            print("Exit Gantry Scanning for Next Car")