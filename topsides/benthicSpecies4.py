import numpy as np
import cv2 as cv
import cmath

#cap = cv.VideoCapture(0)
cap = cv.VideoCapture('udpsrc port=5004 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv.CAP_GSTREAMER)
        

PI = 3.14159

while(1):
    # read the video capture frame
    _, frame = cap.read()
    #cv.imshow('frame',frame)
    #break
    # blur for better edge finding
    blur = cv.GaussianBlur(frame,(5,5),0)
    frameGray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # create threshold for edge finding
    ret, thresh = cv.threshold(frameGray, 120, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    count = 0
    tri = 0
    sqr = 0
    rect = 0 
    circ = 0
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 350 and area < 15000:
            M = cv.moments(contour)
            cX = int(M["m10"]/M["m00"])
            cY = int(M["m01"]/M["m00"])
            if(frame[cY,cX][0] < 50 and frame[cY,cX][1] < 50 and frame[cY,cX][2] < 50):
                cv.circle(frame, (cX,cY), 7, (255,255,0), -1)
                cv.drawContours(frame, contour, -1, (0,255,0), 3)
                count += 1
                ((x,y), (w,h), rot) = cv.minAreaRect(contour)
                if(float(w) > 0.0 and float(h) > 0.0):
                    ratio = w / float(h)
                    if ratio <= 0.4  or ratio >= 2.8:
                        #is rect
                        rect += 1
                    else:
                        peri = cv.arcLength(contour, True)
                        approx = cv.approxPolyDP(contour, 0.04 * peri, True)
                        if len(approx) == 3:
                            #is triangle
                            tri += 1
                        else:
                            (x,y), (MA, ma), angle = cv.fitEllipse(contour)
                            areaEllipse = PI/4 * MA * ma
                            if(abs(areaEllipse - area) < 100):
                                #is circle
                                circ += 1
                            else:
                                #is square
                                sqr += 1

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
    cv.imshow('thresh', thresh)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
cap.release()