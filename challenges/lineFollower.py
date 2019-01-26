import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

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
    mask = cv2.erode(mask,kernel,iterations = 1)

    # Apply Canny edge detection algorithm to get a binary output of edges
    edges = cv2.Canny(mask, 75, 150)
    return edges, mask

def region_of_interest(image):
    line_image = np.zeros_like(image)
    height = image.shape[0]
    width = image.shape[1]
    m_h = height//2
    m_w = width//2

    # (x1,y1)(x2,y2)
    tm_roi = np.array([(m_w-80,   m_h-60),      (m_w+80,     m_h-180)])
    ml_roi = np.array([(m_w-240,  m_h-60),      (m_w-80,     m_h+60)])
    mr_roi = np.array([(m_w+80,   m_h-60),      (m_w+240,    m_h+60)])
    bm_roi = np.array([(m_w-80,   m_h+60),      (m_w+80,     m_h+180)])

    roi_arr = [tm_roi, ml_roi, mr_roi, bm_roi]

    # arr = [(range(int(roi_arr[i][0][0]),int(roi_arr[i][1][0])), range(int(roi_arr[i][0][1]),int(roi_arr[i][1][1]))) for i in range(0,len(roi_arr))]

    # Draw regions of interest: (x1,x2)(y1,y2)
    cv2.rectangle(line_image, (int(ml_roi[0][0]), int(ml_roi[0][1])), (int(ml_roi[1][0]), int(ml_roi[1][1])), (209,69,77.6), 2)
    cv2.rectangle(line_image, (int(mr_roi[0][0]), int(mr_roi[0][1])), (int(mr_roi[1][0]), int(mr_roi[1][1])), (209,69,77.6), 2)
    cv2.rectangle(line_image, (int(tm_roi[0][0]), int(tm_roi[0][1])), (int(tm_roi[1][0]), int(tm_roi[1][1])), (209,69,77.6), 2)
    cv2.rectangle(line_image, (int(bm_roi[0][0]), int(bm_roi[0][1])), (int(bm_roi[1][0]), int(bm_roi[1][1])), (209,69,77.6), 2)

    image = cv2.addWeighted(image, 0.8, line_image, 0.5, 1)
    # print('arr:', arr)
    return roi_arr, image

# Create geometric entities from thresholded image
def create_lines(image, mask):
    # apply probabilistic hough transform, takes 
    # random subset of points for optimization over regular hough transform
    lines = cv2.HoughLinesP(mask, 1, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap=10)

    line_image = np.zeros_like(image)
    if lines is not None:
        hor_line = False
        ver_line = False
        hor_x1, hor_y1, hor_x2, hor_y2 = np.empty([1,1]), np.empty([1,1]), np.empty([1,1]), np.empty([1,1])
        ver_x1, ver_y1, ver_x2, ver_y2 = np.empty([1,1]), np.empty([1,1]), np.empty([1,1]), np.empty([1,1])
        for line in lines:

            if line is not None and len(line) is not 0:
                x1, y1, x2, y2 = line[0]
                ang = math.degrees(math.atan((y2-y1)/(x2-x1)))
                if ang > 45 or ang < -45: # Vert Line
                    ver_line=True

                    ver_x1, ver_y1, ver_x2, ver_y2 = np.append(ver_x1, x1), np.append(ver_y1, y1), np.append(ver_x2, x2), np.append(ver_y2, y2)
                    x2, x1 = int((x1+x2)/2), int((x1+x2)/2)

                else:        # horizontal line
                    hor_line = True

                    hor_x1, hor_y1, hor_x2, hor_y2 = np.append(hor_x1, x1), np.append(hor_y1, y1), np.append(hor_x2, x2), np.append(hor_y2, y2)
                    y2, y1 = int((y1+y2)/2), int((y1+y2)/2)
        
        if hor_line is True:
            hor_x1 = int(np.amin(hor_x1, axis=0))
            hor_y1 = int(np.mean(hor_y1, axis=0))
            hor_x2 = int(np.amax(hor_x2, axis=0))
            hor_y2 = int(np.mean(hor_y2, axis=0))
            # if hor_y2 > 100000000:
            #     hor_y2 = 1000
            # if hor_x2 > 1000000:
            #     hor_x2 = 1000
            # print('hor_x1',hor_x1)
            # print('hor_x2', hor_x2)
            # print('hor_y1',hor_y1)
            # print('hor_y2', hor_y2)
            cv2.line(line_image, (hor_x1, hor_y1), (hor_x2, hor_y2), (255, 255, 0), 3)
        if ver_line is True:
            ver_x1 = int(np.mean(ver_x1, axis=0))
            ver_y1 = int(np.amin(ver_y1, axis=0))
            ver_x2 = int(np.mean(ver_x2, axis=0))
            ver_y2 = int(np.amax(ver_y2, axis=0))
            if ver_y2 > 640:
                ver_y2 = 640
            if ver_x2 > 640:
                ver_x2 = 640
            # print('ver_x1', ver_x1)
            # print('ver_x2', ver_x2)
            # print('ver_y1', ver_y1)
            # print('ver_y2', ver_y2)
            cv2.line(line_image, (ver_x1, ver_y1+50), (ver_x2, ver_y2+50), (255, 255, 0), 3)
    weighted_image = cv2.addWeighted(image, 0.8, line_image, 0.5, 1)
    return weighted_image, lines

def region_calc(image, mask, roi_arr):
    """Calculate regions that have hough lines in them. Return list of zeros and one"""
    line_image = np.zeros_like(image)
    # print('roi_arr:', roi_arr)
    for region in roi_arr:
        # print('regionx:', range(region[0][0],region[1][0]))
        # print('regiony:', range(region[0][1],region[1][1]))
        lines = cv2.HoughLinesP(    mask[region[0][0]:region[1][0], 
                                         region[0][1]:region[1][1]], 
                                    1, np.pi/180, 50, np.array([]), minLineLength = 0, maxLineGap=50)

        if lines is not None:
            for line in lines:
                if line is not None and len(line) is not 0:
                    y1, x1, y2, x2 = line[0]
                    print('x1, y1, x2, y2:',x1, y1, x2, y2)
                    cv2.line(line_image,    (x1+region[0][0], y1+region[0][1]), 
                                            (x2+region[0][0], y2+region[0][1]), 
                                            (255, 255, 0), 3)

    weighted_image = cv2.addWeighted(image, 0.8, line_image, 0.5, 1)
    return weighted_image, line_image

def start_control_logic():
    """Control loop for starting line follower"""
    return None

def main_control_logic(roi_status):
    """Completes logic loop of which direction to send robot in"""

    # if up and down are True, and left and right are False -> keep going in current direction

    # elif left and right are True, and up and down are False -> keep going in current direction

    # elif left and up are True
    # elif up and right are True
    # elif right and down are True
    # elif down and left are True

    return None

def control():
    dir = {
        'up': 0,
        'down': 0,
        'left': 0,
        'right': 0    
    }

    isStarted = None


    roi_status = region_calc()


    start_control_logic()

    # while isDone is not True:
    #     roi_status = region_calc()
    #     main_control_logic(roi_status)

    
    print('Line Following Task Finished')
    return None

if __name__ == '__main__':

    # create video object that opens back camera for calls in opencv api
    videoFeed = 1
    video = cv2.VideoCapture(videoFeed)

    isDone = False

    while isDone is not True: 
        # Read camera frames
        ret, frame = video.read()
        if not ret:
            video = cv2.VideoCapture(videoFeed)
            continue

        # roi_arr, roi_image = region_of_interest(frame)

        edges, mask = preprocess(frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        lsd = cv2.createLineSegmentDetector(0)
        lines = lsd.detect(hsv)[0]
        for l in lines:
            x0, y0, x1, y1 = l.flatten()
            # //do whatever and plot using:
            cv2.line(frame, (x0, y0), (x1,y1), 255, 1, cv2.LINE_AA)

        # weighted_image, lines = create_lines(frame, mask)

        # region_weights, line_image = region_calc(frame, mask, roi_arr)    

        cv2.imshow("weighted image", frame)
        cv2.imshow("Frame", hsv)

        key = cv2.waitKey(25)
        if key == 27:
            break

        # control()

    video.release()
    cv2.destroyAllWindows()