
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

class BarcodeScanner():

	def capture_image():
		# initialize the camera and grab a reference to the raw camera capture
		with PiCamera() as camera:
			# rawCapture = PiRGBArray(camera)
			# allow the camera to warmup
			time.sleep(0.1)
			# grab an image from the camera
			camera.capture('code.jpeg')
			# camera.capture('pics/'+i+'.jpeg')
			# image = rawCapture.array

	def get_barcode():
		path = "code.jpeg"
		# path = 'pics/'+i+'.jpeg'
		image = cv2.imread(path)
		barcodes = pyzbar.decode(image)
		if barcodes != None:
			for barcode in barcodes:
				decoded = barcode.data.decode()
				print(decoded)

	def delete_image():
		os.remove("code.jpeg")

	def main():
		image_in_memory = False
		try:
			while True:
				self.capture_image()
				image_in_memory = True
				self.get_barcode()
				self.delete_image()
				image_in_memory = False
				i-=-1
				time.sleep(0.5)
		except KeyboardInterrupt:
			if image_in_memory == True:
				self.delete_image()


if __name__ == '__main__':
	# barcode_image()
	# Scanner()
	bs = BarcodeScanner()
	bs.main()




























