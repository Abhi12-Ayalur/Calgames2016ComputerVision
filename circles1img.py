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
import glob

#define main webcam detection method, runs in a while true loop, press escape key to break
def detect(fil):
	img = cv2.imread(fil)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	sensitivity = 0
	lower_color = np.array([5, 120, 150])
	upper_color = np.array([30, 255, 255])
	mask = cv2.inRange(hsv, lower_color, upper_color)
	cv2.imshow('mask', mask)
	image = img.copy()
	image = cv2.bitwise_and(image, image, mask=mask)
	cv2.imshow('final thresh', image)
	#cv2.waitKey(0)
	gray = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	#gray = cv2.equalizeHist(gray)
	#gray = auto_canny(gray, sigma=0.001)
	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT,2 , 100)
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		rng = 0
		for (x, y, r) in circles:
			cv2.circle(img, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			'''rng = r/2
			if (x<len(image)-rng and y<len(image[0])-rng):
				redSum = 0
				blueSum = 0
				greenSum = 0
				score = 0
				for xBound in range(x-rng-1, x+rng):
				    for yBound in range(y-rng-1, y+rng):
						redSum += image[xBound][yBound][2]
						if (image[xBound][yBound][2] <= 180 and image[xBound][yBound][2] >= 130 and image[xBound][yBound][1] <= 180 and image[xBound][yBound][1] >= 135 and image[xBound][yBound][0] <= 220 and image[xBound][yBound][0] >= 120):
							score = score + 1
						blueSum += image[xBound][yBound][0]
						greenSum += image[xBound][yBound][1]
				redSum = redSum / ((2*rng + 1) * (2*rng + 1))
				blueSum = blueSum / ((2*rng + 1) * (2*rng + 1))
				greenSum = greenSum / ((2*rng + 1) * (2*rng + 1))
				if (redSum <= 180 and redSum >= 130 and greenSum <= 180 and greenSum >= 135 and blueSum <= 220 and blueSum >= 120):
					print(str(redSum) + " " + str(greenSum) + " " + str(blueSum))
					print(str(x) + " " + str(y) + " " + str(r))
					cv2.circle(img, (x, y), r, (0, 255, 0), 4)
					cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
				if (score >= ((2*rng + 1) * (2*rng + 1) * 0.1)):
					cv2.circle(img, (x, y), r, (0, 255, 0), 4)
					cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)'''


		# show the output image
	cv2.imshow("circles", img)
	cv2.waitKey(0)

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged


for (i,image_file) in enumerate(glob.iglob('Balls/*.png')):
		detect(image_file)

cv2.destroyAllWindows()
