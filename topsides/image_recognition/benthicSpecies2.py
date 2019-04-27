import numpy as np
import cv2 as cv
import cmath

cap = cv.VideoCapture(0)

while(1):
    # read the video capture frame
    _, frame = cap.read()
    # blur for better edge finding
    blur = cv.GaussianBlur(frame,(5,5),0)
    # create threshold for edge finding
    ret, thresh = cv.threshold(blur, 127, 255, 0)
    # convert bgr colour to hsv for better colour detection
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    # create blue boundaries
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,65])
    # create mask based on blue detection
    mask = cv.inRange(hsv, lower_black, upper_black)
    res = cv.bitwise_and(frame, frame, mask= mask)

    frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    count = 0
    tri = 0
    sqr = 0
    rect = 0 
    circ = 0
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 100:
            cv.drawContours(frame, contour, -1, (0,255,0), 3)
            count += 1
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.04 * peri, True)
            if len(approx) == 3:
                tri += 1
            elif len(approx) == 4:
                (x, y, w, h) = cv.boundingRect(approx)
                ratio = w / float(h)
                if ratio >= 0.9 and ratio <= 1.1:
                    sqr += 1
                else:
                    rect += 1
            else:
                circ += 1
    count -= 2
    rect -= 2
    print(count)
    print(tri)
    print(sqr)
    print(rect)
    print(circ)

    cv.circle(frame, (70, 300), 20, (0,0,255), -1)
    pts = np.array([[70, 330], [50, 360], [90, 360]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv.fillPoly(frame, [pts], (0, 0, 255))
    cv.rectangle(frame, (50, 381), (90, 389), (0,0,255), -1)
    cv.rectangle(frame, (50, 410), (90, 450), (0,0,255), -1)
    font = cv.FONT_HERSHEY_COMPLEX_SMALL
    cv.putText(frame, str(circ), (10, 310), font, 2, (0, 0, 255), 2, cv.LINE_AA)
    cv.putText(frame, str(tri), (10, 355), font, 2, (0, 0, 255), 2, cv.LINE_AA)
    cv.putText(frame, str(rect), (10, 400), font, 2, (0, 0, 255), 2, cv.LINE_AA)
    cv.putText(frame, str(sqr), (10, 445), font, 2, (0, 0, 255), 2, cv.LINE_AA)


    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
cap.release()