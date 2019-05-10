import numpy as np
import cv2 as cv
import cmath

def detectCracks(frame):
    # blur for better edge finding
    blur = cv.GaussianBlur(frame,(5,5),0)

    # create threshold for edge finding
    ret, thresh = cv.threshold(blur, 127, 255, 0)

    # convert bgr colour to hsv for better colour detection
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    # create blue boundaries
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # create mask based on blue detection
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(frame, frame, mask=mask)

    kernel = np.ones((3,3),np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(mask, 4, 0.01, 10)
    if corners is not None:
        corners = np.int0(corners)
        cord = []
        for i in corners:
            x,y = i.ravel()
            cord.append([x, y])
            cv.circle(frame, (x, y), 3, 255, -1)

    cord.sort(key=sort)

    if cord[0][0] > cord[1][0]:
        swap(cord, 0, 1)
    if cord[2][0] > cord[3][0]:
        swap(cord, 2, 3)
    print(cord)

    len1 = pythagC((cord[1][0]-cord[0][0]), (cord[1][1]-cord[0][1]))
    len2 = pythagC((cord[3][0]-cord[2][0]), (cord[3][1]-cord[2][1]))
    length = (len1 + len2) / 2
    length = length.real    # Return real part of length
    wid1 = pythagC((cord[3][1]-cord[1][1]),(cord[3][0]-cord[1][0]))
    wid2 = pythagC((cord[2][1]-cord[0][1]),(cord[2][0]-cord[0][0]))
    width = (wid1 + wid2) / 2
    width = width.real      # Return real part of width

    if length > width:
        ratio = length/width
    else:
        ratio = width/length

    length = ratio * 1.9
    length = length / 0.1
    length = round(length)
    length = length * 0.1

    frame_height = frame.shape[0] # 480
    frame_width = frame.shape[1]  # 640

    cv.putText(frame, str(length) + ' cm', (frame_width//4, frame_height//2), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv.LINE_AA)


    frame = cv.resize(frame, (frame_width//2,frame_height//2))
    cv.imshow('frame', frame)
    cv.moveWindow("Frame", 0, 0)

    return str(length)

def sort(elem):
    return elem[1]

def swap(l, i, j):
    temp = l[i]
    l[i] = l[j]
    l[j] = temp

def pythagC(a, b):
    c = cmath.sqrt(a * a + b * b)
    return c

if __name__ == '__main__':
    length = detectCracks()