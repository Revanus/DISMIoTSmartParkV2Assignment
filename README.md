# DISMIoTSmartParkV2Assignment

What is SmartPark about?
__________________________
SmartPark is a showcase of what a Smart Carpark can look like. It has a few features such as recommending an empty parking lot to a user that is the nearest to a lobby (for malls). It also has LED lights to indicate if the lot is taken or not, which allows users to see from afar if that section of the carpark is taken so that he/she does not have to drive there and try to find the lots. Users can also visit the web interface that is accessible by both computer or mobile to check which lot they park their car in, in the event that they have forgotten. Apart from that, parking history can also be viewed online to see which carpark did they access previously and details such as time and pricing will also be there. Other features which normal carparks also have are free first 10 minutes parking, which will be scaled down to 15 seconds for demonstration purposes.

How the final set-up looks like
![alt text](/README images/image1.png)
__________________________
How the web application looks like
__________________________
__________________________
__________________________

Hardware Checklist
__________________________

LDR
Light-Dependant Resistor (LDR) are light sensitive resistors which change resistance based on how much light they are exposed to. In this case, the resistance is higher when it is dark. We will use this hardware to tell whether or not a vehicle is parked. This will be done by placing the resistor below the vehicle. Based on testing, the raw values from the MCP3008 ADC will be >0.62 if an object is above it.

3 Analog-to-Digital Converter
The Raspberry Pi has no built-in analogue inputs which make it difficult to work with our Light-Dependent Resistor. Hence, this converter will be used to convert the analogue inputs to digital signals for the RPi.

6 LED (3 Red, 3 Green)
To connect the LEDs, Ensure that the longer leg is connected to the positive supply of the circuit (power) while the shorter one is to the negative side of the circuit (ground). In this case, 2 of the LEDs will be used for each parking lot to tell if the lot is occupied (1 Green LED, 1 Red LED).

2 LCD Screen
For this application, we will use the LCD Screen for both the entry gate and exit gate to show information like available lots, recommended parking lot & price of parking.

3 Half-Size Breadboard
For this application, we will be using an additional Breadboard which is half-size to simulate a parking lot. Do note that this is not necessary but it would be better as the initial breadboard will not be too cluttered. 

9 Resistors (6 x 330 Ω Resistors, 3 x 10K Ω Resistor)
Resistors help ensure that small current will flow and the Raspberry Pi will not be damaged.
As this application requires 2 LEDs for each lot, we will also use 2 resistors that are 330 Ohms each.

5 RFID / NFC MFRC522 Card Reader Module
We will use 5 RFID readers (2 for gates, 3 for lots). This RFID will scan to check if the card is there. This will be used to check if the car is there and for payment. Any amount of RFID card can be used for this application to work.

Hardware setup

_______________

Create a “Thing”
First, navigate to IoT Core within the AWS website by clicking on services, then IoT Core.

Under manage, select things and choose register a thing.



















