
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import os
import time
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from RPLCD import CharLCD
from dbConn import MongoDB




class BarcodeScanner():
	def __init__(self):
		
		self.code = None
		self.start_time = time.time()
		self.send_to_db = False
		self.delete_wait_time = 5

		# for BCM Mode
		# lcd_rs = 25
		# lcd_en = 24
		# lcd_d4 = 23
		# lcd_d5 = 17
		# lcd_d6 = 18
		# lcd_d7 = 22
		# lcd_backlight = 4

		# for Board Mode
		lcd_rs = 22
		lcd_en = 18
		lcd_d4 = 16
		lcd_d5 = 11
		lcd_d6 = 12
		lcd_d7 = 15
		lcd_backlight = 4

		# Define LCD column and row size for 16x2 LCD.
		lcd_columns = 16
		lcd_rows = 2

		self.lcd = CharLCD(cols=lcd_columns, rows=lcd_rows, pin_rs=lcd_rs, pin_e=lcd_en, pins_data=[lcd_d4, lcd_d5, lcd_d6, lcd_d7], numbering_mode=GPIO.BOARD)
		self.lcd.clear()

		self.db = MongoDB()

		GPIO.setmode(GPIO.BOARD)
		self.red_light = 40
		self.green_light = 37
		self.buzzer = 38
		self.button_remove = 32

		GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button for delete
		GPIO.setup(self.green_light, GPIO.OUT) # Green Light
		GPIO.setup(self.red_light, GPIO.OUT) # Red Light
		GPIO.setup(self.buzzer, GPIO.OUT) # Buzzer
		GPIO.setup(self.button_remove, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button for remove

		GPIO.add_event_detect(10, GPIO.RISING, callback=self.button_callback)
		GPIO.add_event_detect(self.button_remove, GPIO.RISING, callback=self.remove_item)
		# lcd.write_string('Hello world!')
		# message = input("Press enter to quit\n\n")
		# lcd.clear()

	def remove_item():
		print("Enter Remove")
		self.lcd.clear()
		self.lcd.write_string('Scan the item')
		if self.code != None:
			self.send_to_mongo(override=True)
		scanned = False
		image_in_memory = False
		while scanned != True:
			self.capture_image()
			image_in_memory = True
			barcode = self.get_barcode()

			if barcode != None:
				self.code = barcode
				self.db.doneWithItem(self.code)
				self.lcd.clear()
				self.lcd.write_string('Item removed! Good Job!')
				self.code = None
				scanned = True

			self.delete_image()
			image_in_memory = False
			time.sleep(0.5)

	def capture_image(self):
		# initialize the camera and grab a reference to the raw camera capture
		with PiCamera() as camera:
			# rawCapture = PiRGBArray(camera)
			# allow the camera to warmup
			time.sleep(0.1)
			# grab an image from the camera
			camera.capture('code.jpeg')
			# camera.capture('pics/'+i+'.jpeg')
			# image = rawCapture.array

	def send_to_mongo(self, override):
		time_elapsed = time.time() - self.start_time
		if self.send_to_db == False and time_elapsed > self.delete_wait_time and self.code != None:
			print("Adding to MongoDB")
			self.db.insertItem(self.code)
			self.send_to_db = True
			self.code = None
		elif override == True:
			print("Adding to MongoDB")
			self.db.insertItem(self.code)
			self.send_to_db = True
			self.code = None


	def get_barcode(self):
		path = "code.jpeg"
		# path = 'pics/'+i+'.jpeg'
		image = cv2.imread(path)
		barcodes = pyzbar.decode(image)
		if barcodes != None:
			for barcode in barcodes:
				self.lcd.clear()
				if self.send_to_db == False and self.code != None:
					self.send_to_mongo(override = True)
				decoded = str(barcode.data.decode())
				self.start_time = time.time()
				self.send_to_db = False
				print(decoded)
				self.lcd.write_string('Item Added! :)')
				GPIO.output(self.green_light, GPIO.HIGH)
				GPIO.output(self.buzzer, GPIO.HIGH)
				time.sleep(0.5)
				GPIO.output(self.green_light, GPIO.LOW)
				GPIO.output(self.buzzer, GPIO.LOW)
				return decoded
		return None

	def delete_image(self):
		os.remove("code.jpeg")

	def button_callback(self, temp):
		print("Button was pressed!")
		time_elapsed = time.time() - self.start_time
		if time_elapsed < self.delete_wait_time:
			self.lcd.clear()
			self.lcd.write_string('Deleted! We got you!!')
			print("Made the item disappear. We challenge James Bond to find it.")
			self.code = None
			GPIO.output(self.green_light, GPIO.HIGH)
			GPIO.output(self.buzzer, GPIO.HIGH)
			time.sleep(0.3)
			GPIO.output(self.green_light, GPIO.LOW)
			GPIO.output(self.buzzer, GPIO.LOW)

			time.sleep(0.3)

			GPIO.output(self.green_light, GPIO.HIGH)
			GPIO.output(self.buzzer, GPIO.HIGH)
			time.sleep(0.3)
			GPIO.output(self.green_light, GPIO.LOW)
			GPIO.output(self.buzzer, GPIO.LOW)
		else:
			print("Try deleting using WebApp!")
			self.lcd.clear()
			self.lcd.write_string('Delete in App!')
			GPIO.output(self.red_light, GPIO.HIGH)
			GPIO.output(self.buzzer, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(self.red_light, GPIO.LOW)
			GPIO.output(self.buzzer, GPIO.LOW)

			time.sleep(1)

			GPIO.output(self.red_light, GPIO.HIGH)
			GPIO.output(self.buzzer, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(self.red_light, GPIO.LOW)
			GPIO.output(self.buzzer, GPIO.LOW)

	def button_test(self):
		try:
			GPIO.add_event_detect(10, GPIO.RISING, callback=self.button_callback) # Setup event on pin 10 rising edge
			message = input("Press enter to quit\n\n")
			GPIO.cleanup()
		except KeyboardInterrupt:
			GPIO.cleanup()


	def main(self):
		
		image_in_memory = False
		try:
			while True:
				self.capture_image()
				image_in_memory = True
				barcode = self.get_barcode()

				if barcode != None:
					self.code = barcode

				self.send_to_mongo(override=False)
				self.delete_image()
				image_in_memory = False
				time.sleep(0.5)
		except KeyboardInterrupt:
			self.lcd.clear()
			GPIO.cleanup()
			if image_in_memory == True:
				self.delete_image()




if __name__ == '__main__':
	# barcode_image()
	# Scanner()
	bs = BarcodeScanner()
	# bs.button_test()
	bs.main()




























