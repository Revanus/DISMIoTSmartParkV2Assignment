#  ================================================================
#  IOT Assignment 2 - Server.py
#  Authors: Pang Yong Jie, Sim Shi Jie Keith, Tang Wei Shawn
#  ================================================================
#  Import necessary API/Modules/Libraries
#  ================================================================
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from flask import Flask, request, Response, render_template, Markup
from multiprocessing import Process, Value
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import boto3
import re
from boto3.dynamodb.conditions import Key, Attr

#  ===============================================================
#  Functions
#  ===============================================================
# Custom MQTT message callback
def customCallback(client, userdata, message):
    global lotid
    print("Received a new message: ")
    print(message.payload)
    lotid=message.payload
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Get the parking history based on the current holder and carpark name retrieved
def get_history(uid, carparkname):
    
    z=""
    
    table = dynamodb.Table('Parking')
    
    # Retrieving the values from the DynamoDB table based on the current holder and carpark name
    response = table.scan(
        FilterExpression=Attr('RFID').contains(uid) & Attr('Carpark_Name').contains(carparkname)
    )
    
    item = response['Items']
    
    y = list()
    
    # Retrieving the current status, timestamp, carpark name and price paid and store it in list y if there are values found
    if item:
        for i in item:
            x, cs, Current_Status, ts, Timestamp, r, RFID, cpn, Carpark_Name, pp, PricePaid = str(i).split("u'")  
            actual_current_status = re.sub("',\s$", '', Current_Status)
            y.append(actual_current_status)
            actual_timestamp = re.sub("',\s$", '', Timestamp)
            y.append(actual_timestamp)
            actual_rfid = re.sub("',\s$", '', RFID)
            y.append(actual_rfid)
            actual_carpark_name = re.sub("',\s$", '', Carpark_Name)
            y.append(actual_carpark_name)
            actual_pricepaid = re.sub("'}$", '', PricePaid)
            y.append(actual_pricepaid)
        
        # z contains data with the rows and html formatting 
        # y contain the list with the appropriate values 
        # b is the row count
        z = "<table><tr><th>Current Status</th><th>Timestamp</th><th>RFID</th><th>Carpark Name</th><th>Price Paid</th></tr>"
        for b in range(len(y)/5):
            z = z+"<tr>"
            for c in range(5):
                z = z+"<td>" + y[c+(5*b)] + "</td>"
            z = z+"</tr>"
        z = z+"</table>"
        
    # Set z as No history found with html formatting if there are no values found
    else:
        z = "<strong>No history found.</strong>"
    
    # Return z
    return z


# Set the mqtt message with the current holder retrieved and publish the mqtt message to topic sensors/currentHolder
def subgetLot(currentHolder):
    global lotid
    mqtt_message = currentHolder
    my_rpi.publish("sensors/currentHolder", mqtt_message, 1)
    print("Request sent")
    
    while lotid is "":
        sleep(1)
        print("Waiting for messages to come in");
        
    retrieved = lotid
    
    # Set the lotid to an empty string so that the loop will execute again if the function is called again
    lotid = ""
    
    # Return the lot id received
    return retrieved

    
app = Flask(__name__)

# Creation of the homepage in flask server
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/lotid", methods=['GET','POST'])
def formLot():
    if request.method == 'POST':
        # Retrieving the current holder from the web interface
        currentHolder = request.form['currentholder']
        # Calling subgetLot function with currentHolder passed in as the parameter and retrieve the lot id
        response = subgetLot(currentHolder)  
        # Send back the lot id to the web interface and display it
        templateData = {
            'response' : response
        }
        
    return render_template('pin.html', **templateData)

@app.route("/parkinghistory", methods=['GET','POST'])
def formHistory():
    if request.method == 'POST':
        # Retrieving the current holder from the web interface
        currentHolderH = request.form['currentholderH']
        # Retrieving the carpark from the web interface
        carparkH = request.form['carpark']
        # Calling get_History function with currentHolderH and carparkH passed in as the parameter and retrieve variable z
        response = get_history(currentHolderH, carparkH)
        # Declaring the response as HTML safe 
        response = Markup(response)
        # Send back the response to the web interface and display it
        templateData = {
            'response' : response
        }
        
    return render_template('pin.html', **templateData)

#  ===================================================================
#  Variable Declarations
#  ===================================================================
lotid = ""
host = "XXXXXXXXXXXXXX.iot.us-west-2.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"
access_key = "AKIAXXXXXXXXXXXXXXXX"
secret_access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

dynamodb = boto3.resource('dynamodb', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key,
                              region_name='us-west-2')


#  ===================================================================
#  Main
#  ===================================================================
if __name__ == '__main__':

    my_rpi = AWSIoTMQTTClient("basicPubSub")
    my_rpi.configureEndpoint(host, 8883)
    my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
    my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
    my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
    
    # Connect and subscribe to AWS IoT
    my_rpi.connect()
    
    # Subscribing to topic sensors/lotid to retrieve the lot id
    my_rpi.subscribe("sensors/lotid", 1, customCallback)
    
    try:
        http_server = WSGIServer(('0.0.0.0', 80), app)
        app.debug = True
        http_server.serve_forever()
        
    except:
        print("Exception")
