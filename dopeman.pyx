#By SOHAN VICHARE
#import required libraries and dependencies
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from collections import deque
import cv2
from video import create_capture
from common import clock, draw_str
import itertools as it

import sys
import operator
import time
import socket
import math
from json import JSONEncoder, JSONDecoder

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 54321
x = 1
s.bind((host, port))
print ('Listening')
s.listen(1)
conn, addr = s.accept()
print 'Connected by:', addr
st = ""

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)
time.sleep(0.1)
pts = deque(maxlen=242)
def dummy():
		print('dummy is working')
		ds = JSONEncoder().encode({
				"dollop":"dalai llama"
		})
		conn.send(ds)
#define main webcam detection method, runs in a while true loop, press escape key to break
def detect():
	while True:
		start_time = time.time()
		camera.capture(rawCapture, format="bgr")
		frame = rawCapture.array #Image Resizing and Color Thresholding
		
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		lower_color = np.array([0, 130, 140])
		upper_color = np.array([30, 255, 255])
		mask = cv2.inRange(hsv, lower_color, upper_color)
		#mask = cv2.dilate(mask, None, iterations=2)
		'''cv2.imshow("mask frame", mask) #Show the masked frame'''
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		if len(cnts) > 0: #Checks for contours and circle
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			if radius > 10 and radius < 300:
				'''cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)'''
				pts.appendleft(center)
				InchesFinal, Angle = geometry([x,y,radius])
				ds = JSONEncoder().encode({
				"dInInches": InchesFinal,
				"Angle": Angle
				})
				conn.send(ds)
				print(time.time() - start_time)
		'''for i in xrange(1, len(pts)):
			if pts[i - 1] is None or pts[i] is None:
				continue
			thickness = int(np.sqrt(242 / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)'''
		'''cv2.imshow("Frame", frame) #Shows the final image with radius and circle'''	
		rawCapture.truncate(0)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
                
def auto_canny(image, sigma=0.33): #Uses algorithm to scan for circles
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	return edged

def distance(radius):
	return 2000/radius

def geometry(point): #Precalibrated value lets us find distance and angleS
		returnval = [0]
		if point[2] != 0:
				calVal = (1.875)/1000
				x = point[0]
				y = point[1]
				r = point[2]
	
				dInInches = distance(r)
				offCenter = x-120
				inchesOffCenter = calVal*dInInches*offCenter
				angle = math.asin(inchesOffCenter/dInInches)
				angle = angle*180/math.pi
				returnval = [dInInches, angle]
		return returnval

#print(detect())

'''a																																																																															aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa																																																								`
while (1) :
        st = conn.recv(1024)
        returned = JSONDecoder().decode(st)
        returned = returned['run']
        eval(returned)
        time.sleep(1)'''

while (1) :
		st = conn.recv(1024)
		returned = JSONDecoder().decode(st)
		returned = returned['run']
		eval(returned)
		time.sleep(1)
