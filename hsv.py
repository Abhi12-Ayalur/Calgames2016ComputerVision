#By SOHAN VICHARE 2015
#import required libraries and dependencies
import numpy as np
import cv2
from video import create_capture
from common import clock, draw_str
import itertools as it
import sys
import operator
import time
import imutils

#define main webcam detection method, runs in a while true loop, press escape key to break
def detect():
	while True:
		#read current frame from webcam capture
		ret, img = capture.read()
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		lower_color = np.array([200,0,0])
		upper_color = np.array([360,255,254])
		mask = cv2.inRange(hsv, lower_color, upper_color)
		image = img.copy()
		image = cv2.bitwise_and(image, image, mask=mask)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		(cnts, _) = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
		screenCnt = None
		contours = cnts
		for i in range (0, len(contours)):
			cnt = contours[i]
			M = cv2.moments(cnt)
			existMoments = float(M['m10'])
			if (existMoments != 0.0):
				x = int(M['m10']/M['m00'])
				y = int(M['m01']/M['m00'])
				area = cv2.contourArea(cnt)
				area = int(area)
				if (250<area<2000):
					screenCnt = cnt
					cv2.drawContours(image, [cnt], -1, (0, 255, 0), 3)

		cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
		cv2.imshow("lol take 2", image)
		if cv2.waitKey(20) == 27:
			break;

# initialize the camera and grab a reference to the raw camera capture
capture = cv2.VideoCapture(0)
# allow the camera to warmup
time.sleep(0.1)
#set the video source to the computers first option (usually a built in webcam)
video_src = 0
#begin capturing video using video.py to deal with dropped frames
cam = create_capture(video_src)

#run main detection method
detect()

cam.release()

cv2.destroyAllWindows()
