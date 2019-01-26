import cv2
import numpy as np
import math
import sys
sys.path.append("../raspi/")
import fControl

# create video object that opens back camera for calls in opencv api
videoFeed = 1
video = cv2.VideoCapture('udpsrc port=420 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

isDone = False

# orb = cv2.ORB_create()
# test = cv2.imread("star.jpg", cv2.COLOR_BGR2GRAY)

# kp2, des2 = orb.detectAndCompute(test, None)

def preprocess(orig_frame):
    # Blurs image using a gaussian filter kernal, (n,m) are width and height, must be + and odd #'s, 0 is border type
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)

    # Converts from bgr colorspace to hsv colorspace
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define hsv bounds for red
    low_red = np.array([0,100,75])
    up_red = np.array([180,255,255])

    # Threshold the hsv image to get only red colors
    mask = cv2.inRange(hsv, low_red, up_red)

    kernel = np.ones((50,50),np.uint8)
    kernel2 = np.ones((5,5),np.uint8)
    # mask = cv2.erode(mask,kernel,iterations = 1)

    # Apply Canny edge detection algorithm to get a binary output of edges
    edges = cv2.Canny(mask, 75, 150)
    return edges, mask

while isDone is not True: 
    # Read camera frames
    ret, frame = video.read()
    if not ret:
        video = cv2.VideoCapture(videoFeed)
        continue

    edges, mask = preprocess(frame)

    height = frame.shape[0] # 480
    width = frame.shape[1]  # 640
    mid_height = height//2  # 240
    mid_width = width//2    # 320

    lines = cv2.HoughLinesP(mask, 1, np.pi/180, 100, np.array([]), minLineLength = 10, maxLineGap=10)


    ver = 0
    hor = 0
    line_image = np.zeros_like(frame)
    if lines is not None:
        for l in lines:
            if l is not None and len(l) is not 0:
                x0, y0, x1, y1 = l[0]
                cv2.line(line_image, (x0, y0), (x1, y1), (255, 255, 0), 3)
                ang = math.degrees(math.atan((y1-y0)/(x1-x0)))

                if abs(ang) > 45:
                    ver = ver + 1
                else:
                    hor = hor + 1
    # print('hor:', hor,'vert:', ver)


    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX,cY), 8, (255,255,0), -1)
        cv2.line(frame, (cX, cY), (mid_width, mid_height), (255, 255, 0), 3)

        dir = 'left'

        # horizontal line
        if ver == 0:
            error = abs(cY - mid_height)
            if cY > mid_height + 20:
                print('Horizontal line Move Down, error is:',error)
            elif cY < mid_height - 20:
                print('Horizontal line Move Up, error is:',error)
            else:
                print('Horizontal line')

        # vertical line
        elif hor == 0:
            error = abs(cX - mid_width)
            if cX > mid_height + 20:
                print('Vertical line Move Left, error is:', error)
            elif cX < mid_height - 20:
                print('Vertical line Move Right, error is:', error)
            else:
                print('Vertical line')

        # Corner            
        elif hor > 10 and ver > 10:

            if dir == 'left':
                error = abs(cX - mid_width)
                
                print('corner point, go down, horizontal error is:', error)
                

            elif dir == 'up':
                error = abs(cY - mid_height)

                print('corner point, go left, vertical error is:', error)
        else:
            print(' ')


    weighted_image = cv2.addWeighted(frame, 0.8, line_image, 0.5, 1)

    cv2.imshow("Frame", mask)
    cv2.imshow("Mask", weighted_image)

    key = cv2.waitKey(25)
    if key == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()