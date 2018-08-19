**ST0324 Internet of Things CA2 Step-by-step Tutorial**

##### SCHOOL OF DIGITAL MEDIA AND INFOCOMM TECHNOLOGY (DMIT)

# IOT CA2 SmartPark

# Step-by-step Tutorial

ST 0324 Internet of Things (IOT)


## Table of Contents


- Section 1 Overview of SmartPark
- Section 2 Hardware requirements
- Section 3 Hardware setup
- Section 4 Create a “Thing”
- Section 5 DynamoDB Setup
- Section 6 AWS EC2 Hosting of Web Application
- Section 7 Reading RFID/NFC tags setup
- Section 8 Program setup
- Section 9 Web interface setup
- Section 10 Expected outcome
- Section 11 References


## Section 1 Overview of SmartPark

### A. What is SmartPark about?

SmartPark is a showcase of what a Smart Carpark can look like. It has a few features such as
recommending an empty parking lot to a user that is the nearest to a lobby (for malls). It also has led
lights to indicate if the lot is taken or not, which allows users to see from afar if that section of the
carpark is taken so that he/she does not have to drive there and try to find the lots. Users can also
visit the web interface that is accessible by both computer or mobile to check which lot they park
their car in, in the event that they have forgotten. Apart from that, parking history can also be viewed
online to see which carpark did they access previously and details such as time and pricing will also
be there. Other features which normal carparks also have are free first 10 minutes parking, which
will be scaled down to 15 seconds for demonstration purposes.

### B. How the final RPI set-up looks like

```
Final Set-up
```

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image001.png "Optional title")

```
Overview of SmartPark internally
```

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image002.png "Optional title")


### C. How the web application looks like
![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image003.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image004.png "Optional title")

## Section 2 Hardware requirements

### A. Hardware checklist

As the application has multiple functions such as detecting light & motion, here are the hardware
needed and what they are used for. There will be a total of 3 parking lots and 2 gates (entry & exit).

##### 3 Light-Dependant Resistor (LDR)

a) Light-Dependant Resistor (LDR) are light sensitive resistors which
change resistance based on how much light they are exposed to. In
this case, the resistance is higher when it is dark. We will use this
hardware to tell whether or not a vehicle is parked. This will be
done by placing the resistor below the vehicle. Based on testing,
the raw values from the MCP3008 ADC will be >0.62 if an object is
above it.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image005.jpg "Optional title")

##### 3 Analog-to-Digital Converter

a) The Raspberry Pi has no built-in analogue inputs
which make it difficult to work with our Light-
Dependent Resistor. Hence, this converter will be
used to convert the analogue inputs to digital signals
for the RPi.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image006.jpg "Optional title")

##### 6 LED (3 Red, 3 Green)

a) To connect the LEDs, Ensure that the longer leg is connected to the
positive supply of the circuit (power) while the shorter one is to the
negative side of the circuit (ground). In this case, 2 of the LEDs will be
used for each parking lot to tell if the lot is occupied (1 Green LED, 1 Red
LED).

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image007.png "Optional title")

##### 2 LCD Screen

a) For this application, we will use the LCD Screen for both
the entry gate and exit gate to show information like
available lots, recommended parking lot & price of
parking.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image008.jpg "Optional title")

##### 3 Half-Size Breadboard

a) For this application, we will be using an
additional Breadboard which is half-size to
simulate a parking lot. Do note that this is
not necessary but it would be better as the
initial breadboard will not be too cluttered.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image009.jpg "Optional title")

##### 9 Resistors (6 x 330 Ω Resistors, 3 x 10K Ω Resistor)

a) Resistors help ensure that small current will flow and
the Raspberry Pi will not be damaged.
As this application requires 2 LEDs for each lot, we will
also use 2 resistors that are 330 Ohms each.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image010.png "Optional title")

b) As this application requires a Light Dependent
Resistor, we will use a 10K ohms Resistor to help
moderate the flow of current.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image011.jpg "Optional title")

##### 5 RFID / NFC MFRC522 Card Reader Module

a) We will use 5 RFID readers (2 for gates, 3 for lots).
This RFID will scan to check if the card is there. This
will be used to check if the car is there and for
payment. Any amount of RFID card can be used for
this application to work.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image012.jpg "Optional title")

## Section 3 Hardware setup

In this section, we will connect all the necessary components described in Section 2.

### Fritzing Diagram
![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image013.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image014.png "Optional title")

## Section 4 Create a “Thing”

#### Setting Up Your “Thing”

a) First, navigate to IoT Core within the AWS website by clicking on services, then IoT Core.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image021.png "Optional title")

b) Under manage, select things and choose register a thing.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image022.png "Optional title")

c) Choose Create a single thing.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image023.png "Optional title")

d) Enter a name for your thing, for example, SmartPark. Leave the rest of the fields by their
default values. Click next.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image024.png "Optional title")

e) Click create certificate. After a few seconds, the following page will appear. Download all
four files. As for the root CA, download the VeriSign Class 3 Public Primary G5 root CA
certificate file.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image025.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image026.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image027.png "Optional title")

f) Once done, rename the four files accordingly.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image028.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image029.png "Optional title")

g) Move these four files into a directory in the raspberry pi.

h) Click activate.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image030.png "Optional title")

i) Click register thing. You will create a policy later.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image031.png "Optional title")

j) Navigate to policies under the secure section. Click create a policy.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image032.png "Optional title")

k) Enter a name for your policy, for example, SmartParkPolicy and enter the following under
Add statements

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image033.png "Optional title")

l) Navigate to certificates under secure section. Select the certificate you created previously,
and click attach policy. Attach the policy you created previously.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image034.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image035.png "Optional title")

m) Select the certificate you created previously again, and click attach thing. Attach the policy
you previously created. Attach the thing you created previously.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image036.png "Optional title")

#### Create AWS Role

a) Run the following command on your Raspberry Pi to install the AWS Command-line client on your Raspberry Pi

```
sudo pip install awscli --upgrade --user
```
b) Edit the .profile to include the path of the AWS client

```
sudo nano ~/.profile
```

c) Add in the following code after the last line and save the file

```
export PATH=~/.local/bin:$PATH
```

d) Type the following command at the command-line prompt to make the new settings take effect immediately

```
source ~/.profile
```
e) Create a file named iot-role-trust.json in the same folder as the four certifcate and key
files with the following contents:
```
{^
"Version":"2012- 10 - 17",
"Statement":[{
"Effect": "Allow",
"Principal": {
"Service": "iot.amazonaws.com"
},
"Action": "sts:AssumeRole"
}]
}
```
f) Create a file named iot-policy.json in the same folder as the four certifcate and key files
with the following contents:
```
{^
"Version": "2012- 10 - 17",
"Statement": [
{
"Effect": "Allow",
"NotAction": [
"iam:*",
"organizations:*"
],
"Resource": "*"
},
{
"Effect": "Allow",
"Action": [
"iam:CreateServiceLinkedRole",
"iam:DeleteServiceLinkedRole",
"iam:ListRoles",
"organizations:DescribeOrganization"
],
"Resource": "*"
}
]
}
```
g) Type the following command to install the AWS Command-Line Interface Client on your Raspberry Pi

```
sudo pip install awscli
```
h) Take note of your AWS educate’s Access Key ID and Secret Access Key ID.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image037.png "Optional title")

i) Type the following command in your Raspberry Pi terminal so that you can use the AWS CLI to configure your credentials file:
```
aws configure
```
j) Enter the Access Key ID and Secret Access Key id you obtained previously.
```
AWS Access key ID: <Enter Access Key>
AWS Secret Access Key: <Enter Secret Access Key>
Default Region name: us-west- 2
Default output format: <Default value>
```
k) Run this command while in the same folder as iot-role-trust.json file.
```
aws iam create-role --role-name my-iot-role --assume-role-
policy-document file://iot-role-trust.json
```

l) Run this command while in the same folder as iot-policy.json file.
```
aws iam put-role-policy --role-name my-iot-role --policy-
name iot-policy --policy-document file://iot-policy.json
```

## Section 5 DynamoDB Setup

#### DynamoDB

a) First, navigate to DynamoDB within the AWS website by clicking on services, then
DynamoDB. Click create table.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image038.png "Optional title")

b) Enter the table name “Carparks” and the primary key “Carpark_Name”, then click create.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image039.png "Optional title")

c) Click create table again, enter the table name “Parking” and the primary key “RFID” and
“Timestamp”, then click create.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image040.png "Optional title")

d) Click create table again, enter the table name “Parking_Lots” and the primary key “ID” and
“Carpark_Name”, then click create.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image041.png "Optional title")

e) Next, navigate back to IoT Core within the AWS website by clicking on services, then IoT
Core. Click Act, then create button at the top right corner.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image042.png "Optional title")

f) Create the first rule with the name “Carparks”. Under attribute, enter “*”, topic filter
enter “sensors/carparkdb”.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image043.png "Optional title")

g) Under Set one or more actions section, click add action, select “split message into multiple
columns of a database table”. Select configure action. Under table name, select the
“Carparks” table. Under IAM role name, select the role you created previously, “my-iot-
role”. Click add action, then create rule.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image044.png "Optional title")

h) Create the second rule with the name “Parking”. Under attribute, enter “*”, topic filter
enter “sensors/parkingdb”.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image045.png "Optional title")

i) Under Set one or more actions section, click add action, select “split message into multiple
columns of a database table”. Select configure action. Under table name, select the
“Parking” table. Under IAM role name, select the role you created previously, “my-iot-
role”. Click add action, then create rule.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image046.png "Optional title")

j) Create the second rule with the name “Parking_Lot”. Under attribute, enter “*”, topic
filter enter “sensors/parkinglotdb”.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image047.png "Optional title")

k) Under Set one or more actions section, click add action, select “split message into multiple
columns of a database table”. Select configure action. Under table name, select the
“Parking_Lots” table. Under IAM role name, select the role you created previously, “my-
iot-role”. Click add action, then create rule.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image048.png "Optional title")

l) Now that we had created the rules, we can add items to the carparks and parking_lots
table. Navigate to the test section of IoT Core in AWS.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image049.png "Optional title")

m) Scroll down to Publish. Enter the topic “sensors/carparkdb”. Enter the following in the text
field below:
```
{
“Carpark_Name”: “Bukit Batok Carpark”,
“Available_Lots”: “3”
}
```
n) The items are now in the Carparks table.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image050.png "Optional title")

o) Next, Enter the topic “sensors/parkinglotdb”. Enter the following in the text field below:
```
{
"ID": "A1",
"Carpark_Name": "Bukit Batok Carpark",
"Current_Holder": "None",
"Distance": "3"
}
```

Press publish, then update the text field and press publish again.
```
{
"ID": "B1",
"Carpark_Name": "Bukit Batok Carpark",
"Current_Holder": "None",
"Distance": "11"
}
```

Enter the last lot and press publish again.
```
{
"ID": "C1",
"Carpark_Name": "Bukit Batok Carpark",
"Current_Holder": "None",
"Distance": "16"
}
```

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image051.png "Optional title")

p) The “Parking” table will be updated when a car enters through the entry gate.

#### REST API endpoint of your “Thing”


a) Navigate to Things under Manage section in AWS IoT Core.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image051.png "Optional title")

b) Select the thing you created previously and go to the interact section.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image052.png "Optional title")

c) Take note of the string under HTTPS. You will need it later for some of the python codes.


## Section 6 AWS EC2 Hosting of Web Application

We used AWS EC2 to host our SmartPark web application. The following instructions demonstrate
how to create, connect to and host the web application on the EC2 instance.

#### Creation of EC2 Instance


a) First, navigate to EC2 within the AWS website by clicking on services, then EC2.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image021.png "Optional title")

b) Under the Create Instance section, click launch instance.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image054.png "Optional title")

c) Select Amazon Linux AMI

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image055.png "Optional title")

d) Click next with default values until step 6: configure security group. Click Add rule and
select the type ‘HTTP’ like so. This is so that port 80 is open for our web interface.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image056.png "Optional title")

e) Click review and launch, then click launch, choose create a new key pair and enter a key
pair name. Finally, click download key pair. This key pair is used so that we will be able to
SSH into the instance we created to host the web interface.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image057.png "Optional title")

f) After downloading, click launch instance, and the instance should take awhile to load up.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image058.png "Optional title")

g) Once the instance state and status checks are running and 2/2 checks respectively, you are
ready to connect to the EC2 instance that you’ve just created.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image059.png "Optional title")

#### Connecting to EC2 Instance

To connect to and move the web application files into our EC2 instance, two third-party programs
are required. Firstly, PuTTY so that we can SSH into the instance to perform commands such as
running the python files. Secondly, WinSCP to secure copy the required web application files into the
instance.

a) Head over to the following two websites to download and install WinSCP and PuTTY.

https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
https://winscp.net/eng/download.php

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image060.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image061.png "Optional title")

b) Once you have installed both softwares, open PuTTYgen.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image062.png "Optional title")

c) Choose RSA, click load and browse to the .pem file that you download previously (the key
pair). Click ok on the “successfully imported” dialog box.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image063.png "Optional title")

d) Choose save private key and click yes on the warning. A .ppk file is now saved. You are
now ready to SSH into the instance that you’ve created.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image064.png "Optional title")

e) In the EC2 management console, take note of the Public DNS value. In this case, it is ec2-
52 - 37 - 2 - 61.us-west-2.compute.amazonaws.com.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image065.png "Optional title")

f) The default user name of the instance we had created is ec2-user. Within PuTTY, enter the
host name, ec2-user@ec2- 52 - 37 - 2 - 61.us-west-2.compute.amazonaws.com.
(<user_name>@<public DNS>)

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image066.png "Optional title")

g) Next, navigate to connection, SSH then auth. Under private key file for authentication,
browse to the .ppk file you created previously.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image067.png "Optional title")

h) Click Open, then click yes on the PuTTY security alert. You should now be SSH in to the EC2
instance that you’ve created.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image068.png "Optional title")

i) Now open WinSCP. Enter the public DNS value under host name and ec2-user under host
name like so.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image069.png "Optional title")

j) Click advanced. navigate to authentication under SSH. Under private key file, browse to
the .ppk file that you created previously.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image070.png "Optional title")

k) Click OK, save as a site and login. Click YES when the warning dialog pops up. You are now
connected to the instance.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image071.png "Optional title")

l) Create a new directory in the instance, named SmartPark. Navigate into it and move the
necessary web application files (Refer to section 8 and the zip files for the code) and the
rootca.pem, public.pem.key, private.pem.key and certifcate.pem.crt downloaded
previously into it.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image072.png "Optional title")

#### Running the Web Application


a) Open the PuTTY connection that you established previously and install tmux. tmux allows
the web application to continue running even if the SSH connection to the instance is
closed.
```
sudo yum install tmux

```
Type ‘y’ when asked to.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image073.png "Optional title")

b) Install the required libraries for the python files.

```
sudo pip install gevent
sudo pip install flask
sudo pip install AWSIoTPythonSDK
sudo pip install boto3
```

c) Navigate to SmartPark folder and run tmux

```
cd SmartPark/
tmux
```

d) Run both server.py and getData.py within tmux then detach.

```
sudo python server.py &
sudo python getData.py &
tmux detach
```
![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image074.png "Optional title")

e) Close the PuTTY connection. Return to EC2 management console and take note of the IPV4
public IP address. Open that IP address in the browser.
The web application should be up and running.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image075.png "Optional title")

## Section 7 Reading RFID/NFC tags setup

#### Enable SPI and prepare the MFRC522 libraries

If your raspberry pi is not configured with the MFRC522 libraries, you can follow the following
instructions to set it up.

##### << Enable SPI via raspi-config >>


a) Run raspi-config, choose menu item “5 Interfacing Options” and enable SPI.

```
sudo rasp-config
```
![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image076.png "Optional title")

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image077.png "Optional title")

##### << Enable device tree in boot.txt>>

a) Modify the /boot/config.txt to enable SPI

```
sudo nano /boot/config.txt
```

b) Ensure these lines are included in config.txt

```
device_tree_param=spi=on
dtoverlay=spi-bcm2835
```

**<< Install Python-dev>>**
c) Install the Python development libraries

```
sudo apt-get install python-dev
```

**<< Install SPI-Py Library >>**

d) Set up the SPI Python libraries since the card reader uses the SPI interface
```
git clone https://github.com/lthiery/SPI-Py.git
cd /home/pi/SPI-Py
sudo python setup.py install
```

**<< Install RFID library >>**

e) Clone the MFRC522-python library and copy out the required files to your project directory
```
git clone https://github.com/rasplay/MFRC522-python.git
cd MFRC52 2 - python
sudo cp *.py ~/SmartPark
```
f) Edit the MFRC522.py file that you just cloned from GitHub.
```
sudo nano ~/SmartPark/MFRC522.py
```
g) Scroll down to the function “__init__” and make the following changes:

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image078.png "Optional title")

## Section 8 Program setup

The following codes are needed for the application to work. As there are 3 parking lots, all the
parking lot have the same python code except that the string is a little different as 2 lots cannot
have the same name. To ensure that the report does not go over 100 pages, we will only be
providing the python codes. The team has also made other codes like the javascript that is needed
for the website to run such as **‘lot_id.js’** and **‘parking_history.js’**. These files are provided in the ZIP
folder but not the tutorial.

### A. Installing Necessary Libraries

a) Install boto3 using the command below.

```
sudo pip install boto3
```

b) Install the rpi-lcd library using the commands below.

```
sudo pip install rpi-lcd
```
### B. entry.py

This python file uses both the LCD and RFID Sensors to act as an entry gate. It will scan for an rfid
card and will insert a database entry to the dyanmodb table **only when the car is not active in the
carpark**. If the car is not active, it will insert an entry and the status of the car would be ‘active’ as it
is in the carpark. It will also retrieve the recommended lot that is determined based on the distance
the lot is from the lobby **only if the lot is empty**.

Do note that the Carpark name should be changed based on your database. This can be changed by
modifying the string **‘carparkname’**.


### C. CARPARKNAME_Lot_LOTNUMBER.py

Parking lot should be able to detect if the car is there if the RFID card is detected and the light level
is low. Once this occurs, the light should turn red and the Parking lot table will have a current
holder (value of UID), the available lots for the carpark should also decrease. Once the car leaves,
the reverse will happen where the available lots will go back up and the parking lot will appear as
None after the 20 seconds timeout.

Do note that the Carpark name should be changed based on your database. This can be changed by
modifying the string **‘Carpark’**. As parking lots cannot have the same name, we would have to
change it. This can be changed by modifying the string **‘Lot_Scanner’**. For this example, we showed
the example of **Bukit Batok Carpark** with **Lot A1**. Hence the naming convention will be
**BB_Lot_A1.py**

### D. exit.py

This python file uses both the LCD and RFID Sensors to act as an exit gate. It will scan for an rfid
card and determine the price. When a card is detected, It will display the price and change the
database entry of the car’s status to be inactive. The price that the user paid will also be inserted
into the entry so that the user can see his/her parking history. In normal carparks the first 10
minutes has a free entry but for demonstration purpose we made it 15 seconds.

Do note that the Carpark name should be changed based on your database. This can be changed by
modifying the string **‘carparkname’**.

### E. getData.py

This python file will get and send the lot ID to the web interface based on current holder ID
received. The program will subscribe to topic sensors/currentHolder and wait for incoming current
holder ID. Once it receives a current holder ID from topic sensors/currentHolder, it will access the
DynamoDB table called Parking_Lots and retrieve the lot ID based the current holder ID received.
Afterwards, it will publish to the topic sensors/lotid to be received by server.py.


### F. server.py

This python file will host the web interface via flask program. The web interface can retrieve the lot
ID based on the current holder ID sent and retrieve the parking history based on the current holder
ID and the carpark name sent. For the lot ID, the program will publish to topic
sensors/currentHolder based on the current holder ID sent from the web interface. The program
will at the same time subscribe to sensors/lotid and wait for incoming lot ID. Once it receives the lot
ID, it will be displayed in the web interface. For parking history, it will access the DynamoDB table
called Parking and retrieve all the current status, timestamp, carpark name and price paid based on
the current holder ID and the carpark sent from the web interface. These retrieved data will be
displayed in the web interface in table format.


## Section 9 Web interface setup

The following files are required for the web interface to work.

![Alt text](https://github.com/Revanus/DISMIoTSmartParkV2Assignment/blob/master/README%20images/image079.png "Optional title")

Due to how many files there are and how long it will be, it will not be written in this tutorial but
they are located in the ZIP folder provided.

## Section 10 Expected outcome

To test if the program works, run all the python files. server.py and getData.py will be run on the
AWS EC2 side. The following is the link to the video demonstration of what the application should
look like. https://www.youtube.com/watch?v=UOrKWCmZnu8

**Entry Gates** should be able to populate the database entry, retrieve available lots value, and show
recommended lots. It should only populate the table or show the lot if the car is not in the carpark.

**Parking Lots** should be able to detect if the car is there if the RFID card is detected and the light
level is low. Once this occurs, the light should turn red and the Parking lot table will have a current
holder (value of UID), the available lots for the carpark should also decrease. Once the car leaves,
the reverse will happen where the available lots will go back up and the parking lot will appear as
None after the 20 seconds timeout.

**Exit Gates** should change the database entry’s status of the car from active to inactive. It should
also be able to display the price and allow free entry if the car is not in the carpark for long. This
price will then be inserted into the database entry.

**The Website** should be able to be accessed from any device and allow users to retrieve their
current lot id and view their parking history by inputting in the value of the rfid card (value of uid).


## Section 11 References

Freepik Company S.L., 2018. Garage - Free transport icons. [Online]
Available at: https://www.flaticon.com/free-icon/garage_1022832
[Accessed 15 August 2018].

Start Bootstrap, 2018. Freelancer - One Page Theme - Start Bootstrap. [Online]
Available at: https://startbootstrap.com/template-overviews/freelancer/
[Accessed 15 August 2018].

```
-- End of CA2 Step-by-step tutorial --
```

