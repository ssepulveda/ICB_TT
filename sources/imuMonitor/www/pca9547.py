import smbus

bus=smbus.SMBus(1)

## Class to manage the I2C Multiplexor PCA9547
#
#
class PCA9547:
	## Addres of the multiplexor
	address=None
	
	## Consructor
	#	
	# Defines the address for the multiplexor
	# @param self The objetc pointer
	# @param address Address to be used
	def __init__(self,address=0x70):
		self.address=address

	## Sets the current enabled channel
	#	
	# @param self The objetc pointer
	# @param channel the channel to enable
	def setChannel(self,channel=0):
		channel+=8
		bus.write_byte(self.address,channel)

	## Gets the current enabled channel
	#	
	# @param self The objetc pointer
	# @return the enabled channel number
	def getChannel(self):
		return bus.read_byte(self.address)

	## Resets the multiplexor
	#	
	# When reseted, the PCA9547 restore to the default channel, 0.
	# @param self The objetc pointer
	def resetChannel(self):
		bus.write_byte(self.address,0x08)
