import cv2
import numpy as np

def black_line_detection(hsv, location, foundOnce, direction):
    # Threshold the hsv image for black
    low_black    = np.array([45,0,0])
    up_black     = np.array([45,255,50])
    mask_black = cv2.inRange(hsv, low_black, up_black)

    black_pixels_up     = np.count_nonzero(mask_black[(frame.shape[0]//2)-50:(frame.shape[0]//2)-40, 0:frame.shape[1]])
    black_pixels_down   = np.count_nonzero(mask_black[(frame.shape[0]//2)+40:(frame.shape[0]//2)+50, 0:frame.shape[1]])
    black_pixels_left   = np.count_nonzero(mask_black[0:frame.shape[0], (frame.shape[1]//2)-50:(frame.shape[1]//2)-40])
    black_pixels_right  = np.count_nonzero(mask_black[0:frame.shape[0], (frame.shape[1]//2)+40:(frame.shape[1]//2)+50])
    black_threshold = 500
    
    if direction == 'down':
        if black_pixels_down > black_threshold:
            foundOnce = True
        if foundOnce:
            if black_pixels_up > black_threshold:
                location[0] = location[0]+1
                foundOnce = False
    if direction == 'up':
        if black_pixels_up > black_threshold:
            foundOnce = True
        if foundOnce:
            if black_pixels_down > black_threshold:
                location[0] = location[0]-1
                foundOnce = False
    if direction == 'left':
        if black_pixels_left > black_threshold:
            foundOnce = True
        if foundOnce:
            if black_pixels_right > black_threshold:
                location[1] = location[1]-1
                foundOnce = False
    if direction == 'right':
        if black_pixels_right > black_threshold:
            foundOnce = True
        if foundOnce:
            if black_pixels_left > black_threshold:
                location[1] = location[1]+1
                foundOnce = False
    return location, foundOnce

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    direction = 'right'
    location = [0, 0]
    found = False
    while True:
        ret, frame = video.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        location, found = black_line_detection(hsv, location, found, direction)
        print(location)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == 27:
            break

    # When everything done, release the capture
    video.release()
    cv2.destroyAllWindows()