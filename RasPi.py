#By SOHAN VICHARE
#import required libraries and dependencies
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
from video import create_capture
from common import clock, draw_str
import itertools as it
import sys
import operator
import time
import socket
import math


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 54321
x = 1
s.bind((host, port))
print ('Listening')
s.listen(1)
conn, addr = s.accept()
print 'Connected by:', addr




#define main webcam detection method, runs in a while true loop, press escape key to break
def detect(image):
	imgLength = len(image)
	imgWidth = len(image[0])
	pointAr = [0,0,0]
	img = image
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	sensitivity = 0
	lower_color = np.array([5, 120, 150])
	upper_color = np.array([30, 255, 255])
	mask = cv2.inRange(hsv, lower_color, upper_color)
	image = img.copy()
	image = cv2.bitwise_and(image, image, mask=mask)
	gray = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,2 , 100)
	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		rng = 0
		for (x, y, r) in circles:
			cv2.circle(img, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                        print(r)
			pointAr = [x,y,r]
	return pointAr

def distance(radius):
	return 4/radius

def geometry(point):
	calVal = 25
	x = point[0]
	y = point[1]
	r = point[2]
	dInInches = distance(r)
	print dInInches
	'''width=900'''
	offCenter = x-900/2
	inchesOffCenter = calVal*dInInches*offCenter
	angle = math.asin(inchesOffCenter/dInInches)
	return dInInches, angle

camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1)

while (1):
        data = conn.recv(1024)
        print('Received: ', data.decode("utf-8"))
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imshow('rawCapture.array', image)
        dInInches, angle = geometry(detect(rawCapture.array))
        print("{distance: " + str(dInInches) + ", angle: " + str(angle) + "}")
	
