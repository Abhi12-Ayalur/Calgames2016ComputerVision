#By SOHAN VICHARE 2015
#Person Detection code can detect people and faces, and can return a guess for the amount of people in a surveyed area given that the camera stays relatively stationary.

#import required libraries and dependencies
import numpy as np
import cv2
from video import create_capture
from common import clock, draw_str
import itertools as it
import sys
import operator
import time

#define main webcam detection method, runs in a while true loop, press escape key to break
def detect():
    while True:

        #read current frame from webcam capture
        ret, img = capture.read();


        #perform face detection using specified HAAR cascade
        recognized = cascade.detectMultiScale(img)

        #draw a rectangle around the faces detected
        for (x, y, w, h) in recognized:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #show the frame, with rectangles drawn over
        cv2.imshow('Person and Face Recognition + Counting', img)

        #listen for escape key to close window
        if cv2.waitKey(20) == 27:
            break


# initialize the camera and grab a reference to the raw camera capture
capture = cv2.VideoCapture(0)

#set the path to a defualt face HAAR cascade
cascade_fn="Assets/classifier.xml"
cascade = cv2.CascadeClassifier(cascade_fn)

# allow the camera to warmup
time.sleep(0.1)

#set the video source to the computers first option (usually a built in webcam)
video_src = 0

#begin capturing video using video.py to deal with dropped frames
cam = create_capture(video_src)

#set the path to an alternative face HAAR cascade for testing purposes
cascPathFace = 'Assets/classifier.xml'
cascade = cv2.CascadeClassifier(cascPathFace)

#run main detection method
detect()

cam.release()

cv2.destroyAllWindows()
