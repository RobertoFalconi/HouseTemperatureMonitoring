#!bin/python3
#reading TMP 102 and TMP 106 sensors

def tmp102_reading(word):
	#calculation of the temperature based on 
	#the first word read out of register 0x0 of TMP102
	#sensor reading are the first 12 bits
	
	# !!! not tested for negative temperatures !!!!
	
	#byte with inedx 0 (first 8 bit):
	byte0 = (word & 0b0000000011111111)
	#last 4 bits of the word0
	l4b = (word & 0b1111000000000000)>>12
	temperature = ((byte0<<4) | l4b) * 0.0625
	return temperature
	
def tmp006_reading(word):
	#calculation of the temperature based on 
	#the first word (16 bits) from the TMP006 regster 0x1
	#we need to extract first 14 bits
	
	#byte with inedx 0 (first 8 bit):
	byte0 = (word & 0b0000000011111111)
	#last 6 bits of the word0
	l6b = (word & 0b1111110000000000)>>10
	#putting it together into 14-bit reading 
	data = (byte0<<6) | l6b
	#obtain the most significant bit: 1 if negative T
	msb = data >> 13
	if (msb == 0):
		#temperature is positive
		data = data
	else:
		#temperature is negative
		#invert the reading and add one
		data = (data ^ 0xFFFF) + 1
		#select 14 bit
		data = data & 0b0011111111111111
		data = -data
	  
	#conversion into degC -> divide by 32
	temperature = data / 32
	return temperature
''' end '''