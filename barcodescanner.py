
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

class BarcodeScanner():
	def __init__(self):
		GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
		GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # button for delete
		GPIO.setup(16, GPIO.OUT) # Green Light
		GPIO.setup(18, GPIO.OUT) # Buzzer

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

	def get_barcode(self):
		path = "code.jpeg"
		# path = 'pics/'+i+'.jpeg'
		image = cv2.imread(path)
		barcodes = pyzbar.decode(image)
		if barcodes != None:
			for barcode in barcodes:
				decoded = barcode.data.decode()
				print(decoded)
				GPIO.output(16, GPIO.HIGH)
				GPIO.output(18, GPIO.HIGH)
				time.sleep(0.5)
				GPIO.output(16, GPIO.LOW)
				GPIO.output(18, GPIO.LOW)

	def delete_image(self):
		os.remove("code.jpeg")

	def button_callback(self, temp):
		print("Button was pressed!")
		# GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
				self.get_barcode()
				self.delete_image()
				image_in_memory = False
				time.sleep(0.5)
		except KeyboardInterrupt:
			if image_in_memory == True:
				self.delete_image()




if __name__ == '__main__':
	# barcode_image()
	# Scanner()
	bs = BarcodeScanner()
	# bs.button_test()
	bs.main()




























