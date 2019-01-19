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
    # Apply Canny edge detection algorithm to get a binary output of edges
    edges = cv2.Canny(mask, 75, 150)
    return edges, mask

def region_of_interest(image):
    line_image = np.zeros_like(image)
    height = image.shape[0]
    width = image.shape[1]
    
    # (x1,y1)(x2,y2)
    # tl_roi = np.array([(0,0),(width/3,height/3)])
    tm_roi = np.array([(width/3,(height/3)-100),(2*width/3,height/3)])
    # tr_roi = np.array([(2*width/3,0),(width,height/3)])
    ml_roi = np.array([((width/3)-100,height/3),(width/3,2*height/3)])
    # mm_roi = np.array([(width/3,height/3),(2*width/3,2*height/3)])
    mr_roi = np.array([(2*width/3,height/3),((2*width/3)+100,2*height/3)])
    # bl_roi = np.array([(0,2*height/3),(width/3,height)])
    bm_roi = np.array([(width/3,2*height/3),(2*width/3,(2*height/3)+100)])
    # br_roi = np.array([(2*width/3,2*height),(width,height)])

    roi_arr = [tm_roi, ml_roi, mr_roi, bm_roi]
    # print('roi_arr:', roi_arr[0])
    arr = [(roi_arr[i][0][0],roi_arr[i][1][0], roi_arr[i][0][1],roi_arr[i][1][1]) for i in range(0,len(roi_arr))]

    cv2.rectangle(line_image, (int(ml_roi[0][0]),int(ml_roi[0][1])), (int(ml_roi[1][0]),int(ml_roi[1][1])), (209,69,77.6), 2)
    cv2.rectangle(line_image, (int(mr_roi[0][0]),int(mr_roi[0][1])), (int(mr_roi[1][0]),int(mr_roi[1][1])), (209,69,77.6), 2)
    cv2.rectangle(line_image, (int(tm_roi[0][0]),int(tm_roi[0][1])), (int(tm_roi[1][0]),int(tm_roi[1][1])), (209,69,77.6), 2)
    cv2.rectangle(line_image, (int(bm_roi[0][0]),int(bm_roi[0][1])), (int(bm_roi[1][0]),int(bm_roi[1][1])), (209,69,77.6), 2)

    image = cv2.addWeighted(image, 0.8, line_image, 0.5, 1)

    # rectangle = np.array([(100,height), (540,height), (540,100), (100,100)])
    # mask = np.zeros_like(image)
    # cv2.fillPoly(mask, np.int32([rectangle]), 255)
    # masked_image = cv2.bitwise_and(image, mask)
    return roi_arr

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            if line is not None and len(line) is not 0:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 0), 3)
    return line_image

def region_calc():
    """Calculate regions that have hough lines in them. Return list of zeros and one"""

    return None

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
    # dir = up

    isStarted = None
    roi_status = region_calc()

    isDone = None

    start_control_logic()

    # while isDone is not True:
    #     roi_status = region_calc()
    #     main_control_logic(roi_status)

    
    print('Line Following Task Finished')
    return None

if __name__ == '__main__':
    # create video object that opens back camera for calls in opencv api
    video = cv2.VideoCapture(0)

    while True:
        # grabs, decodes, and returns the next video frame, returns false if no more frames in video
        ret, frame = video.read()

        roi = frame[200:250,0:640]

        roi_arr = region_of_interest(frame)

        # Restart loop is camera not found
        if not ret:
            video = cv2.VideoCapture(0)
            continue

        edges, mask = preprocess(frame)

        # apply probabilistic hough transform, takes random subset of points for optimization over regular hough transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, np.array([]), minLineLength = 0, maxLineGap=50)

        line_image = display_lines(frame, lines)

        weighted_image = cv2.addWeighted(frame, 0.8, line_image, 0.5, 1)

        # Displays the canny filtered image and original image overlayed with hough transform lines in seperate windows
        cv2.imshow("ROI Frame", roi_arr[1])    
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(25)
        if key == 27:
            break

        control()

    video.release()
    cv2.destroyAllWindows()