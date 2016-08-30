#By SOHAN VICHARE 
#import required libraries and dependencies
import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
import itertools as it
import sys
import operator
import time
import glob

#define main webcam detection method, runs in a while true loop, press escape key to break
def detect(fil):
	img = cv2.imread(fil)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	sensitivity = 0
	lower_color = np.array([5, 120, 150])
	upper_color = np.array([30, 255, 255])
	mask = cv2.inRange(hsv, lower_color, upper_color)
	image = img.copy()
	image = cv2.bitwise_and(image, image, mask=mask)
	gray = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT,2 , 100)
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		rng = 0
		for (x, y, r) in circles:
			cv2.circle(img, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

	cv2.imshow("circles", img)
	cv2.waitKey(0)


for (i,image_file) in enumerate(glob.iglob('Balls/*.png')):
		detect(image_file)

cv2.destroyAllWindows()
