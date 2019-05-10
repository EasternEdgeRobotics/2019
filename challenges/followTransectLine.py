import cv2
import numpy as np
import math
import socket

# sys.path.append.("../topsides/")
from detectCracks import detectCracks

ipSend = '192.168.88.5'
ipHost = '192.168.88.2'

portSend = 5000
portHost = 5001

# Try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Failed To Create Socket")
    sys.exit()
except Exception as e:
    print("failed")
# Bind the ip and port of topsides to the socket and loop coms
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(ipHost)
print(portHost)
s.bind((ipHost, portHost))

def sendData(inputData):
    global s
    s.sendto(inputData.encode('utf-8'), (ipSend, portSend))

def run_lineFollower():
    videoFeed = 'lineVideo.mov'
    video = VideoStream(videoFeed)
    video.update()
    video.stop()

class VideoStream:

    def __init__(self, source):
        #self.video = cv2.VideoCapture(source)
        self.video = cv2.VideoCapture('udpsrc port=5002 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

        dir = self.program_start()

        direction =   { 'w':'up',
                'a':'left',
                's':'down',
                'd':'right'}

        self.last_line = ''
        self.main_dir = direction[dir]
        self.checkOne = False
        self.blue_boi = False
        self.isBlueFound = False
        self.blue_line_location = [0,0]
        self.blue_line_location_str = ''
        self.crack_length = ''

        self.heave = 0
        self.surge = 0
        self.sway = 0

        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def program_start(self):
        '''Initialize starting position and direction'''

        while True:
            print('Enter Initial Row', end = ' ')
            location_y = input()
            if location_y.isdigit() != True or int(location_y) > 3:
                print('\nNot a valid number!!!\n')
                continue
            else:
                location_y = int(location_y)

            print('Enter Initial Column', end = ' ')
            location_x = input()
            if location_x.isdigit() != True or int(location_x) > 5:
                print('\nNot a valid number!!!\n')
                continue
            else:
                location_x = int(location_x)
            self.location = [location_y, location_x]
            starting_locations = [[0,1],[1,0],[0,4],[1,5],[3,5]]

            if self.location in starting_locations:
                print('Initial Position Chosen: {}'.format(self.location))
                break
            else:
                print('\nNot a valid starting position!!!\n ')
                continue

        print('Enter Initial Direction', end = ' ')
        dir = input()
        print('Initial Direction Chosen:', dir)

        return dir

    def update(self):
        while True: 
            # Read camera frames
            ret, frame = self.video.read()
            frame_height = frame.shape[0] # 480
            frame_width = frame.shape[1]  # 640
            frame = cv2.resize(frame, (frame_width//2,frame_height//2))
            if not ret:
                #self.video = cv2.VideoCapture(source)
                self.video = cv2.VideoCapture('udpsrc port=5002 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
                continue

            self.heave = 0
            self.surge = 0
            self.sway = 0

            edges, mask, mask_ne, mask_blue, mask_black = self.preprocess(frame)
            line_image, ver, hor = self.hough_line_detection(mask, frame)
            line_image = self.drive_logic(frame, mask, mask_ne, ver, hor, mask_blue, mask_black, line_image)
            line_image = self.draw_map(line_image)
            MotorControl.update_motor_signal(self.heave, self.surge, self.sway, self.pitch, self.roll, self.yaw)

            cv2.imshow("Front Camera", line_image)

            key = cv2.waitKey(25)
            if key == 27:
                break

    def preprocess(self, orig_frame):

        # Blurs image using a gaussian filter kernal, (n,m) are width and height, must be + and odd #'s, 0 is border type
        frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)

        # Converts from bgr colorspace to hsv colorspace
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define hsv bounds for red
        low_red1 = np.array([0,80,0])
        up_red1 = np.array([40,255,255])
        low_red2 = np.array([130,80,0])
        up_red2 = np.array([180,255,255])

        # Define hsv bounds for blue
        low_blue = np.array([110,50,50])
        up_blue = np.array([130,255,255])

        # Define hsv bounds for black
        low_black = np.array([0,0,0])
        up_black = np.array([180,255,80])

        # Threshold the hsv image for red
        mask1 = cv2.inRange(hsv, low_red1, up_red1)
        mask2 = cv2.inRange(hsv, low_red2, up_red2)
        mask_ne = cv2.bitwise_or(mask1, mask2)
        mask_inv = cv2.bitwise_not(mask_ne)

        # Threshold the hsv image for blue
        mask_blue = cv2.inRange(hsv, low_blue, up_blue)

        # Threshold the hsv image for black
        mask_black = cv2.inRange(hsv, low_black, up_black)
        mask_black = cv2.bitwise_and(mask_black, mask_black, mask=mask_inv)

        # kernel = np.ones((10,10),np.uint8)
        kernel = np.ones((25,25),np.uint8)
        mask = cv2.erode(mask_ne,kernel,iterations = 1)

        kernel_blue = np.ones((3,3),np.uint8)
        mask_blue = cv2.erode(mask_blue,kernel_blue,iterations = 1)

        # Canny edge detection to get a binary output of edges
        edges = cv2.Canny(mask, 75, 150)

        return edges, mask, mask_ne, mask_blue, mask_black

    def hough_line_detection(self, mask, frame):
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

    def drive_logic(self, frame, mask, mask_ne, ver, hor, mask_blue, mask_black, line_image):        
        # Transverse error bounds
        self.height = frame.shape[0] # 480
        self.width = frame.shape[1]  # 640
        self.mid_height = self.height//2  # 240
        self.mid_width = self.width//2    # 320
        error_bounds = 40

        # Bounds for line width
        size_l_bound = 60
        size_h_bound = 120

        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(line_image, (cX,cY), 6, (255,255,0), -1)
            cv2.line(line_image, (cX, cY), (self.mid_width, self.mid_height), (255, 255, 0), 3)

            self.line_detection(frame, size_l_bound, size_h_bound, cX, cY, ver, hor, error_bounds, mask, mask_ne, mask_blue, mask_black)

        return line_image
    
    def line_detection(self, frame, size_l_bound, size_h_bound, cX, cY, ver, hor, error_bounds, mask, mask_ne, mask_blue, mask_black):
        # Red line direction detection
        if ver == 0:
            self.horizontal_line(size_l_bound, size_h_bound, cY, error_bounds, mask_ne)
        elif hor == 0:
            self.vertical_line(size_l_bound, size_h_bound,cX, error_bounds, mask_ne)         
        elif hor > 10 and ver > 10 and self.location[0] > 0 and self.location[1] > 0:
            self.corner_line(mask, cX, cY)
        else:
            print('.')

        # BLue line detection
        self.blue_crack_detection(frame, mask_blue)

        # Black line detection
        self.black_line_detection(mask_black)

    def horizontal_line(self, size_l_bound, size_h_bound, cY, bounds, mask_ne):
        if self.main_dir == 'down':
            self.main_dir = 'Left'
        self.last_line = 'horizontal'
        error = abs(cY - self.mid_height)
        transv_speed = 0.1
        drive_speed = 0.1

        # Line size conditionals
        line_size = np.count_nonzero(mask_ne[0:self.height, 0:1])
        if line_size < size_l_bound:
            self.surge = transv_speed
            size_error = 'In'
        elif line_size > size_h_bound:
            self.surge = -transv_speed
            size_error = 'Out'
        else:
            self.surge = 0
            size_error = 'None'
            
        # Left/Right error conditionals
        if cY > self.mid_height + bounds:
            self.heave = transv_speed
            error_dir = 'Up'
        elif cY < self.mid_height - bounds:
            self.heave = -transv_speed
            error_dir = 'Down'
        else:
            self.heave = 0
            error_dir = 'None'

        if self.main_dir == 'Left':
            self.sway = -drive_speed
        if self.main_dir == 'Right':
            self.sway = drive_speed
        
        print('Horizontal line | Drive: {} | Vertical error: {} | Correct: {} | Line size: {} | Correct: {}'.format(self.main_dir, error, error_dir, line_size, size_error))

    def vertical_line(self, size_l_bound, size_h_bound, cX, bounds, mask_ne):
        self.last_line = 'vertical'
        error = abs(cX - self.mid_width)
        transv_speed = 0.1
        drive_speed = 0.1

        # Line size conditionals
        line_size = np.count_nonzero(mask_ne[79:80])
        if line_size < size_l_bound:
            self.surge = transv_speed
            size_error = 'In'
        elif line_size > size_h_bound:
            self.surge = -transv_speed
            size_error = 'Out'
        else:
            self.surge = 0
            size_error = 'None'

        # Left/Right error conditionals
        if cX > self.mid_width + bounds:
            self.sway = -transv_speed
            error_dir = 'Left'
        elif cX < self.mid_width - bounds:
            self.sway = transv_speed
            error_dir = 'Right'
        else:
            self.sway = 0
            error_dir = 'None'

        if self.main_dir == 'Up':
            self.heave = drive_speed
        if self.main_dir == 'Down':
            self.heave = -drive_speed

        print('Vertical Line | Drive: {} | Horizontal Error: {} | Correct: {} | Line size: {} | Correct: {}'.format(self.main_dir, error, error_dir, line_size, size_error))

    def corner_line(self, mask, cX, cY):
        corner_dir = ''
        error = 0
        transv_speed = 0.1
        drive_speed = 0.1

        # Corner inlet: Horizontal, Determine corner outlet: Up or Down
        if self.last_line == 'horizontal':
            top_roi = mask[0 : 1].any()
            bot_roi = mask[self.height-1 : self.height].any()
            # print('top_roi',top_roi,'bot_roi',bot_roi, 'np.count_nonzero bot', np.count_nonzero(mask[419:420]))
            corner_dir = 'vertical'
            error = abs(cX - self.mid_width)

            if top_roi:
                self.main_dir = 'up'
                self.heave = drive_speed
            if bot_roi:
                self.main_dir = 'down'
                self.heave = -drive_speed

        # Corner inlet: Vertical, Determine corner outlet: Left or Right
        elif self.last_line == 'vertical':
            left_roi = mask[0 : self.height, 0 : 1].any()
            right_roi = mask[0 : self.height, self.width-1 : self.width].any()
            print('left_roi',left_roi,'right_roi',right_roi)
            corner_dir = 'horizontal'
            error = abs(cY - self.mid_height)

            if left_roi:
                self.main_dir = 'left'
                self.sway = -drive_speed
            if right_roi:
                self.main_dir = 'right'
                self.sway = drive_speed

        elif self.last_line == 'corner':
            pass

        print('Corner | Drive: {} | Error: {}'.format(self.main_dir,error))
        self.last_line = 'corner'

    def draw_map(self, frame):
        x1_map, x2_map = self.width-60, self.width
        y1_map, y2_map = 0, 60
        xrange, yrange = [1,2,3,4], [1,2,3]

        for i in yrange:
            for j in xrange:
                cv2.rectangle(frame,(x1_map,y1_map),(x2_map,y2_map),(0,255,100),1)
                x1_map = x1_map - 60
                x2_map = x2_map - 60
            x2_map = self.width - 1
            x1_map = self.width - 60
            y1_map = y1_map + 60
            y2_map = y2_map + 60
            text = 'Current Square'
            text2 = 'Blue Line Location'

            cv2.putText(frame, text, (self.width - 400, 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,100), 1)
            cv2.putText(frame, str(self.location), (self.width - 350, 40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,100), 1)
            cv2.putText(frame, text2, (self.width - 400, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,100), 1)
            cv2.putText(frame, self.blue_line_location_str, (self.width - 350, 130), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,100), 1)
            cv2.circle(frame,  ((self.width-270)+self.location[1]*60, -30+self.location[0]*60), 6, (0,255,100), -1)

            if self.blue_boi:
                self.blue_line_location = self.location[:] # passes by value
                self.blue_line_location_str = str(self.location)
                self.blue_boi = False
            if self.blue_line_location != '':
                cv2.putText(frame, self.crack_length[0:3]+'cm', ((self.width-300)+self.blue_line_location[1]*60, -30+self.blue_line_location[0]*60), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,0,0), 1)

        return frame

    def blue_crack_detection(self, frame, mask_blue):
        left_roi_blue = mask_blue[0:self.height, 0:10].any()
        right_roi_blue = mask_blue[0:self.height, self.width-10:self.width].any()
        top_roi_blue = mask_blue[0:10, 0:self.width].any()
        bot_roi_blue = mask_blue[self.height-10:self.height, 0:self.width].any()
        blue_pixels = np.count_nonzero(mask_blue[180:320,100:540])  

        if left_roi_blue != True and right_roi_blue != True and top_roi_blue != True and bot_roi_blue != True and blue_pixels > 1000 and self.isBlueFound == False:
            print('Blue boi')
            self.crack_length = detectCracks(frame)
            self.blue_boi = True
            self.isBlueFound = True

    def black_line_detection(self,mask_black):              
            black_pixels_up     = np.count_nonzero(mask_black[self.mid_height-50:self.mid_height-40, 0:self.width])
            black_pixels_down   = np.count_nonzero(mask_black[self.mid_height+40:self.mid_height+50, 0:self.width])
            black_pixels_left   = np.count_nonzero(mask_black[0:self.height, self.mid_width-50:self.mid_width-40])
            black_pixels_right  = np.count_nonzero(mask_black[0:self.height, self.mid_width+40:self.mid_width+50])
            black_threshold = 500
            
            if self.main_dir == 'down':
                if black_pixels_down > black_threshold:
                    self.checkOne = True
                if self.checkOne:
                    if black_pixels_up > black_threshold:
                        self.location[0] = self.location[0]+1
                        self.checkOne = False
            if self.main_dir == 'up':
                if black_pixels_up > black_threshold:
                    self.checkOne = True
                if self.checkOne:
                    if black_pixels_down > black_threshold:
                        self.location[0] = self.location[0]-1
                        self.checkOne = False
            if self.main_dir == 'left':
                if black_pixels_left > black_threshold:
                    self.checkOne = True
                if self.checkOne:
                    if black_pixels_right > black_threshold:
                        self.location[1] = self.location[1]-1
                        self.checkOne = False
            if self.main_dir == 'right':
                if black_pixels_right > black_threshold:
                    self.checkOne = True
                if self.checkOne:
                    if black_pixels_left > black_threshold:
                        self.location[1] = self.location[1]+1
                        self.checkOne = False

    def stop():
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class MotorControl:
    
    def update_motor_signal(heave, surge, sway, pitch, roll, yaw):
        thrusterData = {
                "fore-port-vert": -heave - pitch + roll,
                "fore-star-vert": -heave - pitch - roll,
                "aft-port-vert": -heave + pitch + roll,
                "aft-star-vert": -heave + pitch - roll,

                "fore-port-horz": -surge + yaw + sway,
                "fore-star-horz": -surge - yaw - sway,
                "aft-port-horz": +surge - yaw + sway,
                "aft-star-horz": -surge - yaw + sway,
            }
        thrusterPorts = [1,2,5,0,4,3,6,7,8,9]
        i = 0
        for control in thrusterData:
            val = thrusterData[control]
            sendData("fControl.py " + str(thrusterPorts[i]) + " " + str(val))
            print("value:", val)
            i += 1


if __name__ == '__main__':
    run_lineFollower()