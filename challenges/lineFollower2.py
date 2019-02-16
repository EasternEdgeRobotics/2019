import cv2
import numpy as np
import math

class VideoStream:
    def __init__(self, source):
        self.video = cv2.VideoCapture(source)
        print('Enter Initial Row')
        location_y = int(input())
        print('Enter Initial Column')
        location_x = int(input())
        self.location = [location_y, location_x]
        print('Enter Initial Direction')
        dir = input()
        print('Initial direction chosen:', dir)
        direction =   { 'w':'up',
                        'a':'left',
                        's':'down',
                        'd':'right'}
        self.last_line = ''
        self.main_dir = direction[dir]
        self.checkOne = False
        self.blue_boi = False
        self.blue_line_location = [0,0]
        self.blue_line_location_str = ''

    def update(self):
        while True: 
            # Read camera frames
            ret, frame = self.video.read()
            if not ret:
                self.video = cv2.VideoCapture(source)
                # video = cv2.VideoCapture('udpsrc port=420 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
                continue

            edges, mask, mask_ne, mask_blue, mask_black = self.preprocess(frame)
            line_image, ver, hor = self.linesHough(mask, frame)
            self.logic(frame, mask, mask_ne, ver, hor, mask_blue)
            line_image = self.drawMap(line_image, mask_black)
            cv2.imshow("Frame", line_image)
            cv2.imshow("Mask Black", mask)

            key = cv2.waitKey(25)
            if key == 27:
                break

    def preprocess(self, orig_frame):
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

        # Define hsv bounds for black
        low_black    = np.array([0,0,0])
        up_black     = np.array([180,255,80])

        # Threshold the hsv image to get only red colors
        mask1 = cv2.inRange(hsv, low_red1, up_red1)
        mask2 = cv2.inRange(hsv, low_red2, up_red2)
        mask_ne = cv2.bitwise_or(mask1, mask2)
        mask_inv = cv2.bitwise_not(mask_ne)

        # Threshold the hsv image to get only blue colors
        mask_blue = cv2.inRange(hsv, low_blue, up_blue)

        mask_black = cv2.inRange(hsv, low_black, up_black)
        mask_black = cv2.bitwise_and(mask_black,mask_black,mask = mask_inv)


        # kernel = np.ones((10,10),np.uint8)
        kernel = np.ones((70,70),np.uint8)
        mask = cv2.erode(mask_ne,kernel,iterations = 1)

        kernel_blue = np.ones((10,10),np.uint8)

        mask_blue = cv2.erode(mask_blue,kernel_blue,iterations = 1)

        # Apply Canny edge detection algorithm to get a binary output of edges
        edges = cv2.Canny(mask, 75, 150)

        return edges, mask, mask_ne, mask_blue, mask_black

    def linesHough(self, mask, frame):
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
        weighted_image = cv2.addWeighted(frame, 0.8, line_image, 0.5, 1)
        return weighted_image, ver, hor

    def linesLSD(self, frame):
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

    def logic(self, frame, mask, mask_ne, ver, hor, mask_blue):
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
                self.last_line = 'horizontal'
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

                print('Horizontal line','| Drive:', self.main_dir,'| Vertical error:', error, '| Correct:', error_dir, '| Line size:', line_size, '| Correct:', size_error)
            # Vertical line
            elif hor == 0:
                if self.main_dir == 'right':
                    self.main_dir = 'down'
                self.last_line = 'vertical'
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

                print('Vertical Line','| Drive:', self.main_dir, '| Horizontal Error:', error, '| Correct:', error_dir, '| Line size:', line_size, '| Correct:', size_error)
            # Corner            
            elif hor > 10 and ver > 10:
                corner_dir = ''
                error = 0
                # Corner inlet: Horizontal, Determine corner outlet: Up or Down
                if self.last_line == 'horizontal':
                    top_roi = mask[height_start:height_start+1].any()
                    bot_roi = mask[height_end-1:height_end].any()
                    # print('top_roi',top_roi,'bot_roi',bot_roi, 'np.count_nonzero bot', np.count_nonzero(mask[419:420]))
                    corner_dir = 'vertical'
                    error = abs(cX - mid_width)
                    if top_roi:
                        self.main_dir = 'up'
                    if bot_roi:
                        self.main_dir = 'down'
                        print('maindir1', self.main_dir)
                    print('maindir2', self.main_dir)
                # Corner inlet: Vertical, Determine corner outlet: Left or Right
                elif self.last_line == 'vertical':
                    left_roi = mask[0:height,0:1].any()
                    right_roi = mask[0:height,639:640].any()
                    print('left_roi',left_roi,'right_roi',right_roi)
                    corner_dir = 'horizontal'
                    error = abs(cY - mid_height)
                    if left_roi:
                        self.main_dir = 'left'
                    if right_roi:
                        self.main_dir = 'right'
                elif self.last_line == 'corner':
                    pass
                # print('Corner from',self.last_line,'to',corner_dir,'| Drive:', self.main_dir,'| Error:', error)
                print('Corner | Drive:', self.main_dir,'| Error:', error)
                self.last_line = 'corner'
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
                self.blue_boi = True

    def drawMap(self, frame, mask_black):
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
            text2 = 'Blue Line Location'

            height = frame.shape[0]
            width = frame.shape[1] 
            mid_height = height//2 
            mid_width = width//2 

            if self.blue_boi == True:
                self.blue_line_location = self.location[:] # passes by value
                self.blue_line_location_str = str(self.location)
                self.blue_boi = False
                

            black_pixels_up = np.count_nonzero(mask_black[mid_height-50:mid_height-40,0:width])
            black_pixels_down = np.count_nonzero(mask_black[mid_height+40:mid_height+50,0:width])
            black_pixels_left = np.count_nonzero(mask_black[0:height,mid_width-50:mid_width-40])
            black_pixels_right = np.count_nonzero(mask_black[0:height+50,mid_width+40:mid_width+50])

            
            if self.main_dir == 'down':
                if black_pixels_down > 1000:
                    self.checkOne = True
                if self.checkOne == True:
                    if black_pixels_up > 1000:
                        self.location[0] = self.location[0]+1
                        self.checkOne = False
            if self.main_dir == 'up':
                if black_pixels_up > 1000:
                    self.checkOne = True
                if self.checkOne == True:
                    if black_pixels_down > 1000:
                        self.location[0] = self.location[0]-1
                        self.checkOne = False
            if self.main_dir == 'left':
                if black_pixels_left > 1000:
                    self.checkOne = True
                if self.checkOne == True:
                    if black_pixels_right > 1000:
                        self.location[1] = self.location[1]-1
                        self.checkOne = False
            if self.main_dir == 'right':
                if black_pixels_right > 1000:
                    self.checkOne = True
                if self.checkOne == True:
                    if black_pixels_left > 1000:
                        self.location[1] = self.location[1]+1
                        self.checkOne = False

            cv2.putText(frame, text, (width - 400, 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1)
            cv2.putText(frame, str(self.location), (width - 350, 40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1)
            cv2.putText(frame, text2, (width - 400, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1)
            cv2.putText(frame, self.blue_line_location_str, (width - 350, 130), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1)

            cv2.circle(frame, ((width-270)+self.location[1]*60, -30+self.location[0]*60), 6, (255,0,0), -1)
            if self.blue_line_location != '':
                cv2.circle(frame, ((width-270)+self.blue_line_location[1]*60, -30+self.blue_line_location[0]*60), 6, (255,255,0), -1)
            

        return frame

    def stop():
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    videoFeed = 'lineVideo.mov'
    video = VideoStream(videoFeed)
    video.update()
    video.stop()