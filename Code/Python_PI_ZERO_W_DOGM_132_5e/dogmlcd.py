#!/usr/bin/env python

import spidev, atexit, time
import RPi.GPIO as GPIO

DOG_LCD_M081 = 1
DOG_LCD_M162 = 2
DOG_LCD_M163 = 3
DOG_LCD_M132 = 4

# DOG_LCD_COMMAND_CLEAR = 0x01
# DOG_LCD_COMMAND_HOME = 0x02

# DOG_LCD_CURSOR_ON  = 0x02
# DOG_LCD_CURSOR_OFF = 0x00

# DOG_LCD_DISPLAY_ON = 0x04
# DOG_LCD_DISPLAY_OFF = 0x00

# DOG_LCD_BLINK_OFF = 0x00
# DOG_LCD_BLINK_ON = 0x01

# DOG_LCD_SCROLL_LEFT = 0x18
# DOG_LCD_SCROLL_RIGHT = 0x1C

DOG_LCD_DISPLAY_ON = 0xAF
DOG_LCD_DISPLAY_OFF = 0xAE

DOG_LCD_START_LINE_SET_NULL = 0x40
DOG_LCD_SET_ADC_REVERSE = 0xA1 # nochmal checken
DOG_LCD_COMMON_OUTPUT_MODE_SELECT = 0xC0
DOG_LCD_SET_DISPLAY_NORMAL = 0xA6

enable_hw_spi = True
hw_spi_speed = 1000000


class DogLCD():
	def __init__(self, lcdSI, lcdCLK, lcdRS, lcdCSB, pin_reset, pin_backlight):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		if enable_hw_spi:
			self.spi = spidev.SpiDev()
			self.spi.open(0, 0)
			self.spi.max_speed_hz = hw_spi_speed

		self.lcdSI = lcdSI
		self.lcdCLK = lcdCLK
		self.lcdRS = lcdRS
		self.lcdCSB = lcdCSB
		self.lcdReset = pin_reset
		self.lcdBacklight = pin_backlight

		self.animations = [[],[],[],[],[],[],[],[]]

	def begin(self, model, contrast):

		self.model = model
		self.startAddress = [-1,-1,-1]

		# if (model==DOG_LCD_M081):
			# self.rows = 1
			# self.cols = 8
			# self.memSize = 80
			# self.startAddress[0] = 0
			# self.startAddress[1] = -1
			# self.startAddress[2] = -1
		# elif (model==DOG_LCD_M162):
			# self.rows = 2
			# self.cols = 16
			# self.memSize = 40
			# self.startAddress[0] = 0
			# self.startAddress[1] = 0x40
			# self.startAddress[2] = -1
		# elif (model==DOG_LCD_M163):
			# self.rows = 3
			# self.cols = 16
			# self.memSize = 16
			# self.startAddress[0] = 0
			# self.startAddress[1] = 0x10
			# self.startAddress[2] = 0x20
		if (model==DOG_LCD_M132):
			self.rows = 3
			self.cols = 16
			self.memSize = 16
			self.startAddress[0] = 0
			self.startAddress[1] = 0x10
			self.startAddress[2] = 0x20
		else:
			# Unknown or unsupported model
			return False

		if(self.lcdReset != -1):
			GPIO.setup(self.lcdReset, GPIO.OUT)
			GPIO.output(self.lcdReset, GPIO.HIGH)

		if(self.lcdBacklight != -1):
			GPIO.setup(self.lcdBacklight, GPIO.OUT)
			GPIO.output(self.lcdBacklight, GPIO.LOW)

		if(contrast < 0 or contrast > 0x3F):
			# Contrast falls outside valid range
			return False

		self.contrast = contrast
		
		if not enable_hw_spi:
			GPIO.setup(self.lcdCSB,GPIO.OUT);
			GPIO.output(self.lcdCSB,GPIO.HIGH);
			GPIO.setup(self.lcdSI,GPIO.OUT);
			GPIO.output(self.lcdSI,GPIO.HIGH);
			GPIO.setup(self.lcdCLK,GPIO.OUT);
			GPIO.output(self.lcdCLK,GPIO.HIGH);
		GPIO.setup(self.lcdRS,GPIO.OUT);
		GPIO.output(self.lcdRS,GPIO.HIGH);

	
		self.reset()
		return True

	def reset(self):
		if( self.lcdReset != -1):
			GPIO.output(self.lcdReset,GPIO.LOW)
			self.delay(40)
			GPIO.output(self.lcdReset,GPIO.HIGH)
			self.delay(40)
		else:
			self.delay(50)

		# if(self.model==DOG_LCD_M081):
			# self.instructionSetTemplate=0x30
		# elif(self.model==DOG_LCD_M162):
			# self.instructionSetTemplate=0x38
		# elif(self.model==DOG_LCD_M163):
			# self.instructionSetTemplate=0x38

		# self.setInstructionSet(1)

		# self.writeCommand(0x1D,30)

		# self.setContrast(self.contrast)

		# self.displayMode 	= DOG_LCD_DISPLAY_ON
		# self.cursorMode 		= DOG_LCD_CURSOR_ON
		# self.blinkMode 		= DOG_LCD_BLINK_OFF
		# self.writeDisplayMode()
		# self.entryMode 		= 0x04
	# #	self.clear()
		# self.leftToRight()

	def setContrast(self, contrast):
		if(contrast<0 or contrast>0x3F):
			return False

		# For 3.3v operation the booster must be on, which is
		# on the same command as the (2-bit) high-nibble of contrast
		self.writeCommand( (0x54 | ((self.contrast >> 4) & 0x03)), 30 )

		self.writeCommand( 0x6B, 30 )
		# Set low-nibble of the contrast
		self.writeCommand( (0x70 | (contrast & 0x0F) ), 30 )

	

	

	

	def createChar(self, char_pos, char_map):
		if(char_pos<0 or char_pos>7):
			return False

		baseAddress = char_pos*8
		self.setInstructionSet(0)
		for i in range(0,8):
			self.writeCommand((0x40|(baseAddress+i)),30)
			self.writeChar(char_map[i])
		self.setInstructionSet(0)
		self.writeDisplayMode()

	# def writeDisplayMode(self):
		# self.writeCommand((0x08 | self.displayMode | self.cursorMode | self.blinkMode), 30)



	def writeChar(self, value):
		# Switch to data mode
		GPIO.output( self.lcdRS, GPIO.HIGH )
		self.spiTransfer(value,30)
		return True
		
	def writeData(self, value):
		# Switch to data mode
		GPIO.output( self.lcdRS, GPIO.HIGH )
		self.spiTransfer(value,30)
		return True
		
	def writeDot(self, page, column_low, column_high, data_value, delay):
		# Switch to data mode
		self.writeCommand(0xB0 | page, delay)
		self.writeCommand(0x10 | column_high, delay)
		self.writeCommand(column_low, delay)
		self.spiTransfer(data_value,30)
		return True
		
	def writeCommand(self, value, delay):
		# Switch to command-mode
		GPIO.output( self.lcdRS, GPIO.LOW )
		self.spiTransfer(value,delay)

	def spiTransfer(self, value, delay):
		if enable_hw_spi:
			#value = self.ReverseBits( value )
			self.spi.xfer( [ value ] )
			self.delayMicroseconds( delay )
			return True

		# Ensure Clock starts high
		GPIO.output(self.lcdCLK,GPIO.HIGH)

		GPIO.output(self.lcdCSB,GPIO.LOW)

		for i in reversed(range(0,8)):
			GPIO.output( self.lcdSI, value & (1 << i) )
			GPIO.output( self.lcdCLK, GPIO.LOW )
			GPIO.output( self.lcdCLK, GPIO.HIGH )

		GPIO.output(self.lcdCSB,GPIO.HIGH)

		# Wait for command to complete
		self.delayMicroseconds( delay )
		
	def init(self, delay):
		self.writeCommand(DOG_LCD_START_LINE_SET_NULL, delay)
		self.writeCommand(DOG_LCD_SET_ADC_REVERSE, delay)
		self.writeCommand(DOG_LCD_COMMON_OUTPUT_MODE_SELECT, delay)
		self.writeCommand(DOG_LCD_SET_DISPLAY_NORMAL, delay)
		self.writeCommand(0xA2, delay)
		self.writeCommand(0x2F, delay)
		self.writeCommand(0xF8, delay)
		self.writeCommand(0x00, delay)
		self.writeCommand(0x23, delay)
		self.writeCommand(0x81, delay)
		self.writeCommand(0x1F, delay)
		self.writeCommand(0xAC, delay)
		self.writeCommand(0x00, delay)
		self.writeCommand(0xAF, delay)
		

	
	def write(self, string):
		string = str( string )
		for char in string:
			self.writeChar(ord(char))

	def delayMicroseconds(self, delay):
		time.sleep(delay/1000000)

	def delay(self, delay):
		time.sleep(delay/1000)
	# def clear(self):
		# self.writeCommand(DOG_LCD_COMMAND_CLEAR,1080)

	# def home(self):
		# self.writeCommand(DOG_LCD_COMMAND_HOME,1080)

	# def setCursor(self, col, row):
		# if( col > self.memSize or row >= self.rows ):
			# # Cursor outside of valid range
			# return False
		# address = (self.startAddress[row]+col) & 0x7F
		# self.writeCommand(0x80|address,30)

	# def noDisplay(self):
		# self.displayMode=DOG_LCD_DISPLAY_OFF #0x00
		# self.writeDisplayMode()

	# def display(self):
		# self.displayMode=DOG_LCD_DISPLAY_ON #0x04
		# self.writeDisplayMode()

	# def noCursor(self):
		# self.cursorMode=DOG_LCD_CURSOR_OFF #0x00
		# self.writeDisplayMode()

	# def cursor(self):
		# self.cursorMode=DOG_LCD_CURSOR_ON #0x02
		# self.writeDisplayMode()

	# def noBlink(self):
		# self.blinkMode=DOG_LCD_BLINK_OFF
		# self.writeDisplayMode()

	# def blink(self):
		# self.blinkMode=DOG_LCD_BLINK_ON
		# self.writeDisplayMode()

	# def scrollDisplayLeft(self):
		# self.setInstructionSet(0)
		# self.writeCommand(DOG_LCD_SCROLL_LEFT,30) # 0x18

	# def scrollDisplayRight(self):
		# self.setInstructionSet(0)
		# self.writeCommand(DOG_LCD_SCROLL_RIGHT,30) # 0x1C
		
	# def setBacklight(self, value, usePWM):
		# if(self.lcdBacklight!=-1 and value>=0):
			# if(value == LOW):
				# GPIO.output(self.lcdBacklight,GPIO.LOW)
			# else:
				# GPIO.output(self.lcdBacklight,GPIO.HIGH)

	# def setInstructionSet(self, instruction_set):
		# if( instruction_set < 0 or instruction_set > 3 ):
			# return False
		# self.writeCommand( self.instructionSetTemplate | instruction_set, 30 )
	def doubleHeight(self):
		self.writeCommand(0b00100110,30)

	def noDoubleHeight(self):
		self.writeCommand(0b00100001,30)

	def doubleHeightTop(self):
		self.writeCommand(0b00011000,30)

	def doubleHeightBottom(self):
		self.writeCommand(0b00010000,30)

	def createAnimation(self, anim_pos, anim_map, frame_rate):
		self.createChar(anim_pos, anim_map[0])
		self.animations[anim_pos] = [anim_map,frame_rate]
		self.setCursor(0,1)
	
	def updateAnimations(self):
		for i,animation in enumerate(self.animations):
			if len(animation) == 2:
				anim = animation[0]
				fps = animation[1]
				frame = anim[ int(round(time.time()*fps) % len(anim)) ]
				self.createChar(i,frame)
		self.setCursor(0,1)
	def leftToRight(self):
		self.entryMode|=0x02
		self.writeCommand(self.entryMode,30)

	def rightToLeft(self):
		self.entryMode&=~0x02
		self.writeCommand(self.entryMode,30)

	def autoScroll(self):
		self.entryMode|=0x01
		self.writeCommand(self.entryMode,30)

	def noAutoscroll(self):
		self.entryMode&=~0x01
		self.writeCommand(self.entryMode,30)
#atexit.register(lambda: GPIO.cleanup())
