# House Temperature Monitoring using AWS IoT and Raspberry
## Video and description
https://www.youtube.com/watch?v=gQxOSbcN79s  
Developed smart home automation project with Node.js and Python, using AWS IoT, AWS Lambda, Amazon SNS and a Raspberry Pi 3. With an AWS IoT Button it is possible to send an alert to housemates and to receive your house's temperature on your smartphone.

If you want to read a detailed description or a step-by-step guide to replicate this project, I suggest you to check out the Hackster link written below.

Project for Pervasive Systems course of MSc in Engineering in Computer Science at Sapienza, University of Rome.  

# Useful links
- Portfolio: https://robertodaguarcino.com  
- LinkedIn: https://www.linkedin.com/in/roberto-falconi  
- GitHub: https://github.com/RobertoFalconi  
- SlideShare: https://www.slideshare.net/RobertoFalconi4  
- Hackster: https://www.hackster.io/Falkons/house-temperature-monitoring-using-aws-iot-and-raspberry-pi-3b6410  
- YouTube: https://youtu.be/gQxOSbcN79s  
- Portfolio: http://www.robertodaguarcino.com  
- Examinator: http://ichatz.me/Site/PervasiveSystems2018  
 
# How to run House Temperature Monitoring using AWS IoT and Raspberry  

NOTE: this is a brief guide to run the program. For full guide checkout the Hackster project page:  
- https://www.hackster.io/Falkons/house-temperature-monitoring-using-aws-iot-and-raspberry-pi-3b6410  

For a good-looking presentation, checkout the slideshare presentation and the YouTube video:
- https://www.slideshare.net/RobertoFalconi4/house-temperature-monitoring-using-aws-iot-and-raspberry-pi  
- https://youtu.be/gQxOSbcN79s  

Open a terminal window wherever you want to, then:  
`$ git clone https://github.com/RobertoFalconi/HouseTemperatureMonitoring.git`  
`$ cd HouseTemperatureMonitoring`  
`$ sudo raspi-config`  

Enable I2C: "5 Interfacing Operations" -> "I2C" -> "Yes"  

Configure your circuit to run TMP102 (Hackster link for full explaination) and check if it is working:  

`$ sudo pigpiod`  
`$ sudo i2cdetect -y 1`  
`     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f`  
`00:          -- -- -- -- -- -- -- -- -- -- -- -- --`  
`10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --`  
`20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --`  
`30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --`  
`40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --`  
`50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --`  
`60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --`  
`70: -- -- -- -- -- -- -- --`  
`$ i2cget -y 1 0x48 0 b`  
`0x18`  

If you get 48 in position 8x40 and 0x18 (which means 22 °C or something like that, it's working).  

Link your AWS IoT Button to your AWS Account.  
Configure your Button with AWS Lambda and Amazon SNS.  
Configure your Raspberry Pi.  

Run the MQTT Client on your RPi:  
`$ python3 PervasiveSystems.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>`  

Double click your AWS IoT Button and checkout with a browser if TMP102 is gathering temperaturature information and if RPi is sending it to AWS Test console.

# Story
## Introduction
This project allows you to monitor your house’s temperature whenever you want to, with all your devices with a browser (i.e. your smartphone, your tablet or your computer).
To do this, it is necessary to link an AWS IoT Button, a Raspberry Pi 3 model B (I didn't tested it on other models, but I think it should works on older/newer models too) and a temperature sensor like TMP102 with Amazon Web Services, in particular I used AWS IoT, AWS Lambda and Amazon SNS; also requires Node.js and Python languages skill and a bit of MQTT protocol knowledge.
I decided to realize this project for the exam of Pervasive Systems, as a student of MSc in Engineering in Computer Science at Sapienza - University of Rome.
1. Configuring your AWS IoT Button
First of all, it’s needed to connect your AWS IoT Button to a Wi-Fi Network and to link it with your AWS Account. You can easily accomplish this goal with the AWS IoT Button Dev app for Android or iOS.
2. Creating a Lambda rule with AWS Lambda
Now, by going to AWS Lambda it's possible to create a new Lambda function. The developer guide provided by Amazon can be helpful. The procedure will generate a REST API point: remember to take note of it.
3. Creating an Amazon SNS Rule
Now, you just have to make a new Amazon SNS Rule via Amazon SNS dashboard (tutorial here), create a new topic and subscribe to it (insert here your e-mail and your REST API). After subscribing, a Topic ARN will be generated. Come back to AWS Lambda and in the Node.js code replace the fake Topic ARN with your real one.
4. Connecting Raspberry Pi 3 to AWS
In AWS IoT dashboard, in the manage menu, create a new thing, compile all the required fields and download all the four files (public key, private key,  certificate and certification authority).
5. Reading temperature and sending data to AWS
Now, I configured the circuit in this way:
I connected a T type breakout board to a breadboard with a GPIO connector for RPi 3. Then, I linked the breakout board with the TMP102 in this way:
IMG_3131 2.jpg
T type breakout board connected to a breadboard and to a TMP102 (bung used to avoid the use of a soldering) 
(Breakout board -> TMP102)
SDA1 -> SDA
SCL1 -> SCL
5VO -> VCC
GND -> ADD0
Finally, if you’re on Raspbian last version you can enable I2C by typing:
$ sudo raspi-config
And going to interfacing options. After that type:
$ sudo apt-get install -y python-smbus
$ sudo apt-get install -y i2c-tools
And check if TMP102 is reached by Raspberry Pi 3 with:
$ i2cdetect -y 1 
 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
And you can see if it works thanks to:
$ sudo pigpiod
$ i2cget -y 1 0x48 0 b
0x18
In my case, it returns 0x18 (which means 22 °C).
6. Run the program
Download the repository:
$ git clone https://github.com/RobertoFalconi95/HouseTemperatureMonitoring.git
And start the program.
$ sudo pigpiod
$ python3 PervasiveSystems.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>
Your Raspberry Pi 3 will start an MQTT client.
Single click your AWS IoT Button to send an alert or double click it to start recording temperature of your house via TMP102 and automatically sending it to AWS IoT.
Now, you can use your browser to read the temperature of your home wherever (and whenever) you want to. I hope I was as clear as possible, enjoy!
Thumbs up and share if you liked my work, comment for feedback or criticism, thank you!
