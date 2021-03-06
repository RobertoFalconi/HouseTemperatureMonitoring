# House Temperature Monitoring using AWS IoT and Raspberry
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
