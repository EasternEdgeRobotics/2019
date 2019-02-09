import cv2
import numpy as np
import math

# create video object that opens back camera for calls in opencv api

videoFeed = 1
video = cv2.VideoCapture(videoFeed)
# video = cv2.VideoCapture('udpsrc port=420 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

def preprocess(orig_frame):
    # Blurs image using a gaussian filter kernal, (n,m) are width and height, must be + and odd #'s, 0 is border type
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)

    # Converts from bgr colorspace to hsv colorspace
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define hsv bounds for red
    low_red1 = np.array([0,80,0])
    up_red1 = np.array([40,255,255])
    low_red2 = np.array([130,68,0])
    up_red2 = np.array([180,255,255])

    # Threshold the hsv image to get only red colors
    mask1 = cv2.inRange(hsv, low_red1, up_red1)
    mask2 = cv2.inRange(hsv, low_red2, up_red2)


    mask_ne = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((70,70),np.uint8)
    mask = cv2.erode(mask_ne,kernel,iterations = 1)

    # Apply Canny edge detection algorithm to get a binary output of edges
    edges = cv2.Canny(mask, 75, 150)
    return edges, mask, mask_ne

def findLines(mask, frame):
    lines = cv2.HoughLinesP(mask, 1, np.pi/180, 100, np.array([]), minLineLength = 100, maxLineGap=10)
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
    return line_image, ver, hor

def findLinesLSD(mask, frame):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lsd = cv2.createLineSegmentDetector(0)
    lines = lsd.detect(hsv)[0]
    ver = 0
    hor = 0
    line_image = np.zeros_like(frame)
    if lines is not None:
        for l in lines:
            if l is not None and len(l) is not 0:
                x0, y0, x1, y1 = l.flatten()
                cv2.line(line_image, (x0, y0), (x1, y1), (255, 255, 0), 3)
                ang = math.degrees(math.atan((y1-y0)/(x1-x0)))

                if abs(ang) > 45:
                    ver = ver + 1
                else:
                    hor = hor + 1

    print('hor:', hor,'vert:', ver)
    return line_image, ver, hor

def findMoments(frame, mask, mask_ne, ver, hor, main_dir, last_line):
    '''Function for finding moments of image mask'''
    height = frame.shape[0] # 480
    width = frame.shape[1]  # 640
    mid_height = height//2  # 240
    mid_width = width//2    # 320
    height_start = 60        # 60
    height_end = height - 60 # 420

    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX,cY), 6, (255,255,0), -1)
        cv2.line(frame, (cX, cY), (mid_width, mid_height), (255, 255, 0), 3)
        bounds = 40

        # Horizontal line
        if ver == 0:
            last_line = 'horizontal'
            error_dir = ''
            error = abs(cY - mid_height)
            if cY > mid_height + bounds:
                error_dir = 'Up'
            elif cY < mid_height - bounds:
                error_dir = 'Down'
            else:
                error_dir = 'None'
            print('Horizontal line','| Drive:', main_dir,'| Vertical error:', error,  '| Correct:', error_dir)

        # Vertical line
        elif hor == 0:
            last_line = 'vertical'
            error_dir = ''
            error = abs(cX - mid_width)
            if cX > mid_width + bounds:
                error_dir = 'Left'
            elif cX < mid_width - bounds:
                error_dir = 'Right'
            else:
                error_dir = 'None'
            print('Vertical Line','| Drive:', main_dir, '| Horizontal Error:', error, '| Correct:', error_dir)

        # Corner            
        elif hor > 10 and ver > 10:
            corner_dir = ''
            error = 0
            # Corner inlet: Horizontal, Determine corner outlet: Up or Down
            if last_line == 'horizontal':
                top_roi = mask_ne[79:80].any()
                bot_roi = mask_ne[419:420].any()
                print('top_roi',top_roi,'bot_roi',bot_roi)
                corner_dir = 'vertical'
                error = abs(cX - mid_width)
                if top_roi:
                    main_dir = 'up'
                if bot_roi:
                    main_dir = 'down'
                    print('maindir1',main_dir)
                print('maindir2',main_dir)
            # Corner inlet: Vertical, Determine corner outlet: Left or Right
            elif last_line == 'vertical':
                left_roi = mask_ne[0:height,0:1].any()
                right_roi = mask_ne[0:height,639:640].any()
                print('left_roi',left_roi,'right_roi',right_roi)
                corner_dir = 'horizontal'
                error = abs(cY - mid_height)
                if left_roi:
                    main_dir = 'left'
                if right_roi:
                    main_dir = 'right'
            elif last_line == 'corner':
                pass
            # print('Corner from',last_line,'to',corner_dir,'| Drive:', main_dir,'| Error:', error)
            print('Corner | Drive:', main_dir,'| Error:', error)
            last_line = 'corner'

        else:
            print('.')
    return last_line, main_dir



if __name__ == '__main__':
    print('Enter Initial Direction')
    dir = input()
    print('Initial direction chosen:', dir)

    direction =   { 'w':'up',
                    'a':'left',
                    's':'down',
                    'd':'right'}
    last_line = ''
    main_dir = direction[dir]

    while True: 
        # Read camera frames

        # e1 = cv2.getTickCount()
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(videoFeed)
            # video = cv2.VideoCapture('udpsrc port=420 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
            continue

        edges, mask, mask_ne = preprocess(frame)
        line_image, ver, hor = findLines(mask, frame)
        # line_image, ver, hor = findLinesLSD(mask, frame)
        last_line, main_dir = findMoments(frame, mask, mask_ne, ver, hor, main_dir, last_line)


        weighted_image = cv2.addWeighted(frame, 0.8, line_image, 0.5, 1)
        weighted_image
        cv2.imshow("Frame", mask_ne)
        cv2.imshow("Mask", weighted_image)

        # e2 = cv2.getTickCount()
        # t = (e2 - e1)/cv2.getTickFrequency()
        # print( t )
        key = cv2.waitKey(25)
        if key == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()