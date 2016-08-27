#By SOHAN VICHARE and ABHINAV AYALUR 2016
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

#define main webcam detection method, runs in a while true loop, press escape key to break
def detect():
	while True:
		ret, image = capture.read()
		output = image.copy()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		#gray = cv2.equalizeHist(gray)
		#auto = auto_canny(gray, sigma=0.001)
		circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.85, 100)
		if circles is not None:
			circles = np.round(circles[0, :]).astype("int")
			for (x, y, r) in circles:
				cv2.circle(gray, (x, y), r, (0, 255, 0), 4)
				cv2.rectangle(gray, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
				#print(image[x][y])
			# show the output image
		cv2.imshow("circles", gray)

		if cv2.waitKey(20) == 27:
			break;

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

# initialize the camera and grab a reference to the raw camera capture
capture = cv2.VideoCapture(0)

# allow the camera to warmup
time.sleep(0.1)

#begin capturing video using video.py to deal with dropped frames
cam = create_capture(0)

#run main detection method
detect()

cam.release()

cv2.destroyAllWindows()
