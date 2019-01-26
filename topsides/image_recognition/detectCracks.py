import numpy as np
import cv2 as cv
import cmath
#from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)

while(1):
    # read the current video capture frame
    _, frame = cap.read()

    # blur for better edge finding
    blur = cv.GaussianBlur(frame,(5,5),0)
    # create threshold for edge finding
    ret, thresh = cv.threshold(blur, 127, 255, 0)
    # convert bgr colour to hsv for better colour detection
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    # create blue boundaries
    lower_blue = np.array([100,100,30])
    upper_blue = np.array([150,255,255])
    # create mask based on blue detection
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(frame, frame, mask= mask)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(mask, 4, 0.01, 10)
    if corners is not None:
        corners = np.int0(corners)
        cord = []
        for i in corners:
            x,y = i.ravel()
            cord.append([x, y])
            cv.circle(frame, (x, y), 3, 255, -1)

    print(cord)
    def sort(elem):
        return elem[1]
    cord.sort(key=sort)
    print('sort: ', cord)
    def swap(l, i, j):
        temp = l[i]
        l[i] = l[j]
        l[j] = temp
    if cord[0][0] > cord[1][0]:
        swap(cord, 0, 1)
    if cord[2][0] > cord[3][0]:
        swap(cord, 2, 3)
    print('swap: ', cord)
    len1 = cmath.sqrt(((cord[3][1] - cord[2][1])**2) + ((cord[3][0] - cord[2][0])**2))
    len2 = cmath.sqrt(((cord[1][1] - cord[0][1])**2) + ((cord[1][0] - cord[0][0])**2))
    length = (len1 + len2) / 2
    wid1 = cmath.sqrt(((cord[3][1] - cord[1][1])**2) + ((cord[3][0] - cord[1][0])**2))
    wid2 = cmath.sqrt(((cord[2][1] - cord[0][1])**2) + ((cord[2][0] - cord[0][0])**2))
    width = (wid1 + wid2) / 2
    if length > width:
        ratio = length/width
    else:
        ratio = width/length
    length = ratio * 1.9
    length = length / 0.1
    length = round(length)
    length = length * 0.1
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, str(length) + ' cm', (20, 400), font, 3, (255,255,255), 2, cv.LINE_AA)
    # find the contours in the blue
    """_, contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # draw the detected contours on top of the main frame
    for contour in contours:
        area = cv.contourArea(contour)
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        # if area > 4000:
            #cv.drawContours(frame, contour, -1, (0,255,0), 3)
            #cv.drawContours(frame,[box],0,(0,255,0),2)    
    
    # based on the measurements of the detected contours, find aspect ratio
    x,y,w,h = cv.boundingRect(mask)
    if h != 0 and w !=0:
        if w > h:
            aspect_ratio = float(w)/h
        else:
            aspect_ratio = float(h)/w
        # calculate longest length of blue tape, print on top of frame
        length = aspect_ratio * 2.0
        length = length / 0.1
        length = round(length)
        length = length * 0.1
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame, str(length) + ' cm', (20, 400), font, 3, (255,255,255), 2, cv.LINE_AA)
    """
    # show the final video output(s)
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    # exit when escape key is hit
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()