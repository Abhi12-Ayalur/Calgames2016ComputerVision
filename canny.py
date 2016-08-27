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
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blurred = gray

		#wide = cv2.Canny(blurred, 10, 200)
		#tight = cv2.Canny(blurred, 225, 250)
		auto = auto_canny(blurred, sigma=0.03)

		# show the images
		cv2.imshow("edge", auto)

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
