# House Temperature Monitoring using AWS IoT and Raspberry
Developed smart home automation project with Node.js and Python, using AWS IoT, AWS Lambda, Amazon SNS and a Raspberry Pi 3. With an AWS IoT Button it is possible to send an alert to housemates and to receive your house's temperature on your smartphone.

If you want to read a detailed description or a step-by-step guide to replicate this project, I suggest you to check out the Hackster link written below.

# Useful Links
LinkedIn profile: https://www.linkedin.com/in/roberto-falconi  
GitHub repository: https://github.com/RobertoFalconi/HouseTemperatureMonitoring  
Hackster full description: https://www.hackster.io/Falkons/house-temperature-monitoring-using-aws-iot-and-raspberry-pi-3b6410  
SlideShare presentation: https://www.slideshare.net/RobertoFalconi4/house-temperature-monitoring-using-aws-iot-and-raspberry-pi  
YouTube video: https://youtu.be/gQxOSbcN79s   

# How to run House Temperature Monitoring using AWS IoT and Raspberry

NOTE: this is a brief guide to run the program. For full guide checkout the Hackster project page: https://www.hackster.io/Falkons/house-temperature-monitoring-using-aws-iot-and-raspberry-pi-3b6410

Open a terminal window wherever you want to, then:
`$ git clone https://github.com/RobertoFalconi/HouseTemperatureMonitoring.git`
`$ cd HouseTemperatureMonitoring`
`$ sudo raspi-config`

Enable I2C: "5 Interfacing Operations" -> "I2C" -> "Yes"

Configure your circuit to run TMP102 (Hackster link for full explaination) and check if it is working:

`$ sudo pigpiod`
`$ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         
$ i2cget -y 1 0x48 0 b
0x18`

If you get 48 in position 8x40 and 0x18 (which means 22 °C or something like that, it's working)

Link your AWS IoT Button to your AWS Account: 
Configure your Button: https://docs.aws.amazon.com/iot/latest/developerguide/iot-button-lambda.html
Configure your Raspberry Pi:

`$ python3 PervasiveSystems.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>`
