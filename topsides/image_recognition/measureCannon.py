import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

while(1):
    # read the video capture frame
    _, frame = cap.read()
    # blur for better edge finding
    blur = cv.GaussianBlur(frame,(5,5),0)
    frameGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)