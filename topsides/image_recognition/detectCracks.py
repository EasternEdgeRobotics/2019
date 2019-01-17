import numpy as np
import cv2 as cv
import cmath
#from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)

while(1):
    _, frame = cap.read()

    blur = cv.GaussianBlur(frame,(5,5),0)
    ret, thresh = cv.threshold(blur, 127, 255, 0)


    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #blue stuff
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    _, contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 5000:
            cv.drawContours(frame, contour, -1, (0,255,0), 3)

    x,y,w,h = cv.boundingRect(mask)
    if h != 0 and w !=0:
        if w > h:
            aspect_ratio = float(w)/h
        else:
            aspect_ratio = float(h)/w
        length = aspect_ratio * 1.9
        length = length / 0.1
        length = round(length)
        length = length * 0.1
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame, str(length), (20, 400), font, 3, (255,255,255), 2, cv.LINE_AA)

    res = cv.bitwise_and(frame, frame, mask= mask)
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
