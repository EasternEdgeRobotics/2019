import cv2
import numpy as np
import math

def preprocess(orig_frame):
    # Blurs image using a gaussian filter kernal, (n,m) are width and height, must be + and odd #'s, 0 is border type
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)

    # Converts from bgr colorspace to hsv colorspace
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define hsv bounds for red
    low_red1    = np.array([0,80,0])
    up_red1     = np.array([40,255,255])
    low_red2    = np.array([130,80,0])
    up_red2     = np.array([180,255,255])

    # Define hsv bounds for blue
    low_blue    = np.array([110,50,50])
    up_blue     = np.array([130,255,255])

    # Threshold the hsv image to get only red colors
    mask_red_low = cv2.inRange(hsv, low_red1, up_red1)
    mask_red_high = cv2.inRange(hsv, low_red2, up_red2)

    # Threshold the hsv image to get only blue colors
    mask_blue = cv2.inRange(hsv, low_blue, up_blue)

    mask_red_ne = cv2.bitwise_or(mask_red_low, mask_red_high)

    # kernel = np.ones((10,10),np.uint8)
    kernel = np.ones((70,70),np.uint8)
    mask = cv2.erode(mask_red_ne,kernel,iterations = 1)

    kernel_blue = np.ones((10,10),np.uint8)

    mask_blue = cv2.erode(mask_blue,kernel_blue,iterations = 1)

    # Apply Canny edge detection algorithm to get a binary output of edges
    edges = cv2.Canny(mask, 75, 150)
    return edges, mask, mask_red_ne, mask_blue

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

def findLinesLSD(frame):
    
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # Define hsv bounds for red
    # low_red1    = np.array([0,80,0])
    # up_red1     = np.array([40,255,255])
    # low_red2    = np.array([130,80,0])
    # up_red2     = np.array([180,255,255])

    # mask1 = cv2.inRange(hsv, low_red1, up_red1)
    # mask2 = cv2.inRange(hsv, low_red2, up_red2)
    # mask_ne = cv2.bitwise_or(mask1, mask2)
    # kernel = np.ones((10,10),np.uint8)
    # mask = cv2.erode(mask_ne,kernel,iterations = 1)

    # grey = cv2.bitwise_and(hsv, mask)

    lsd = cv2.createLineSegmentDetector(0)
    lines = lsd.detect(grey)[0]
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

    # print('hor:', hor,'vert:', ver)
    return line_image, ver, hor

def findMoments(frame, mask, mask_ne, ver, hor, main_dir, last_line, mask_blue):
    '''Function for finding moments of image mask'''
    height = frame.shape[0] # 480
    width = frame.shape[1]  # 640
    mid_height = height//2  # 240
    mid_width = width//2    # 320
    height_start = 0        # 60
    height_end = height # 420

    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX,cY), 6, (255,255,0), -1)
        cv2.line(frame, (cX, cY), (mid_width, mid_height), (255, 255, 0), 3)
        bounds = 40

        size_l_bound = 60
        size_h_bound = 120

        # Horizontal line
        if ver == 0:
            last_line = 'horizontal'
            error_dir = ''
            size_error = ''
            error = abs(cY - mid_height)

            # Line size conditionals
            line_size = np.count_nonzero(mask_ne[0:height,0:1])
            if line_size < size_l_bound:
                size_error = 'In'
            elif line_size > size_h_bound:
                size_error = 'Out'
            else:
                error_dir = 'None'

            # Left/Right error conditionals
            if cY > mid_height + bounds:
                error_dir = 'Up'
            elif cY < mid_height - bounds:
                error_dir = 'Down'
            else:
                error_dir = 'None'

            print('Horizontal line','| Drive:', main_dir,'| Vertical error:', error, '| Correct:', error_dir, '| Line size:', line_size, '| Correct:', size_error)
        # Vertical line
        elif hor == 0:
            last_line = 'vertical'
            error_dir = ''
            size_error = ''
            error = abs(cX - mid_width)
           
            # Line size conditionals
            line_size = np.count_nonzero(mask_ne[79:80])
            if line_size < size_l_bound:
                size_error = 'In'
            elif line_size > size_h_bound:
                size_error = 'Out'
            else:
                error_dir = 'None'

            # Left/Right error conditionals
            if cX > mid_width + bounds:
                error_dir = 'Left'
            elif cX < mid_width - bounds:
                error_dir = 'Right'
            else:
                error_dir = 'None'

            print('Vertical Line','| Drive:', main_dir, '| Horizontal Error:', error, '| Correct:', error_dir, '| Line size:', line_size, '| Correct:', size_error)
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

        # BLue line detection
        left_roi_blue = mask_blue[0:height,0:1].any()
        right_roi_blue = mask_blue[0:height,width-1:width].any()
        top_roi_blue = mask_blue[0:1,0:width].any()
        bot_roi_blue = mask_blue[height-1:height,0:width].any()
        blue_pixels = np.count_nonzero(mask_blue[180:320,100:540])  
        if left_roi_blue != True and right_roi_blue != True and top_roi_blue != True and bot_roi_blue != True and blue_pixels > 1000:
            print('Blue boi')

    return last_line, main_dir

def drawMap(frame):
    width = frame.shape[1]
    x2_map = width -1
    x1_map = width - 60
    y1_map = 0
    y2_map = 60
    xrange = [1,2,3,4]
    yrange = [1,2,3]

    for i in yrange:
        for j in xrange:
            cv2.rectangle(frame,(x1_map,y1_map),(x2_map,y2_map),(0,0,0),1)
            x1_map = x1_map - 60
            x2_map = x2_map - 60
        x2_map = width -1
        x1_map = width - 60
        y1_map = y1_map + 60
        y2_map = y2_map + 60
        text = 'Current Square'
        cv2.putText(frame, text, (width - 340, 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 0), 2)
    

    return frame

def runLineFollower():
   '''Add function run code'''

if __name__ == '__main__':
    # create video object that opens back camera for calls in opencv api
    videoFeed = 'lineVideo.mov'
    video = cv2.VideoCapture(videoFeed)
    # video = cv2.VideoCapture('udpsrc port=420 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

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
        # e1 = cv2.getTickCount()
        # Read camera frames
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(videoFeed)
            # video = cv2.VideoCapture('udpsrc port=420 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
            continue

        edges, mask, mask_ne, mask_blue = preprocess(frame)
        line_image, ver, hor = findLines(mask, frame)
        # line_image, ver, hor = findLinesLSD(frame)

        frame = drawMap(frame)

        last_line, main_dir = findMoments(frame, mask, mask_ne, ver, hor, main_dir, last_line, mask_blue)

        weighted_image = cv2.addWeighted(frame, 0.8, line_image, 0.5, 1)
        # cv2.imshow("Frame", mask_ne)
        cv2.imshow("Frame", weighted_image)

        # e2 = cv2.getTickCount()
        # print((e2 - e1)/cv2.getTickFrequency())

        key = cv2.waitKey(25)
        if key == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()