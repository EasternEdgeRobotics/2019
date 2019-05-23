import cv2
import numpy as np
import math
import time
import colorsys
from detectCracks import detectCracks
import detectGridPosition

cam = None
#cam_connection = 0
cam_connection = "udpsrc port=4444 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER"
#cam_connection = "static/video/lineVideo.MOV"

frameWidth = 0
frameHeight = 0

centerbox = {"x": None, "y": None, "width": 25, "height": 25}

isRunning = False

##|, _, |_, _|, -|, |-
#grid = []
currentLocation = [-1, 3]
crackPosition = [0, 0]

#directionHistory = []
currentDirection = None

stopDirectionSwitch = False
stopDirectionSwitchTime = 0

#distanceWidth = 110
distanceWidth = 70
distanceDeadZone = 15
distanceIndicator = ""

#stopMoveGrid = False
#lastMoveGrid = None


#B,G,R
#red = {"low": (0,0,100), "high": (30,10,255)}
#H,S,V
#redHSV = {"low": (330, 60, 10), "high": (360, 255, 120)}
red2HSV = {"low": (0, 35, 57), "high": (30, 255, 170)}
redHSV = {"low": (149, 35, 57), "high": (179, 255, 170)}
#red2HSV = {"low": (0, 60, 10), "high": (30, 255, 120)}

red = {"low": (), "high": ()} #when ran, hsv is converted to rgb80
red2 = {"low": (), "high": ()} #when ran, hsv is converted to rgb80
#hsv
black = {"low": (0,0,0), "high": (360,100,60)}

def start():
    global isRunning, cam, frameWidth, frameHeight, centerbox
    isRunning = True
    cam = cv2.VideoCapture(cam_connection)

    if(cam.isOpened()):
        frameWidth = int(cam.get(3))
        frameHeight = int(cam.get(4))
        centerbox["x"] = int(frameWidth/2 - centerbox["width"]/2)
        centerbox["y"] = int(frameHeight/2 - centerbox["height"]/2)

        loop()
    else:
        print("Unable to open video feed.")

def end():
    global isRunning, cam
    #isRunning = False

    print("WOOOOOO WE DID IT!!!")

    #cam.release()
    #cv2.destroyAllWondows()

def loop():
    global cam, currentDirection, stopDirectionSwitchTime, stopDirectionSwitch, stopMoveGrid, lastMoveGrid, currentLocation

    cornerCount = 0

    while(isRunning and cam.isOpened()):
        ret, frame = cam.read()
        frame = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        crack = detectCracks(frame)
        #print(crack)

        maskRed = cv2.inRange(hsv, redHSV["low"], redHSV["high"])
        maskRed2 = cv2.inRange(hsv, red2HSV["low"], red2HSV["high"])

        maskRed = maskRed + maskRed2

        isOnLine = redInsideRectangle(hsv, centerbox["x"], centerbox["y"], centerbox["width"], centerbox["height"])
        
        currentOrientation = ""


        currentLocation = detectGridPosition.black_line_detection(frame, currentLocation, currentDirection)

        contours, h = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if(len(contours) <= 0):
            continue

        x = frameWidth
        y = frameHeight
        x2 = -1
        y2 = -1
        width = None
        height = None

        
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > 10000 and area < frameWidth*frameHeight - 2000):
                cv2.drawContours(frame, contour, -1, (255,0,0), 3)
                M = cv2.moments(contour)
                cx = 0
                cy = 0
                if(M["m00"] > 0):
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    cv2.circle(frame, (cx,cy), 5, (255,255,0), -1)

                xTemp,yTemp,widthTemp,heightTemp = cv2.boundingRect(contour)
                x = min(x, xTemp)
                y = min(y, yTemp)
                x2 = max(x2, xTemp + widthTemp)
                y2 = max(y2, yTemp + heightTemp)      

        if(x2 != -1):
            width = x2 - x
            height = y2 - y
            
            if(currentDirection == None):
                findNextLine(frame, frameWidth, frameHeight, int(x + width/2), int(y + height/2))
            if(width/height > 0.6 and width/height < 2):
                currentOrientation = "corner"
                cornerCount+=1
                stopDirectionSwitchTime = 10
            elif(width > height):
                currentOrientation = "horizontal"
                cornerCount = 0
                stopDirectionSwitchTime -= 1
            else:
                currentOrientation = "vertical"
                cornerCount = 0
                stopDirectionSwitchTime -= 1

            if(currentOrientation != "corner"):
                checkDistance(contour)
            """
            if(blackInsideRectangle(frame, int(frameWidth/2 - 200), 0, 2, int(frameHeight/2) - 100) and currentOrientation == "vertical"):
                if(stopMoveGrid and lastMoveGrid is not "up"):
                    stopMoveGrid = False
                elif(currentDirection == "up" and not stopMoveGrid):
                    lastMoveGrid = "up"
                    stopMoveGrid = True
                    print("moved up")

            elif (blackInsideRectangle(frame, int(frameWidth/2 - 200), int(frameHeight/2 + 100), 2, int(frameHeight/2 - 100)) and currentOrientation == "vertical"):
                if(stopMoveGrid and lastMoveGrid is not "down"):
                    stopMoveGrid = False
                elif(currentDirection == "down" and not stopMoveGrid):
                    lastMoveGrid = "down"
                    stopMoveGrid = True
                    print("moved down")

            elif(blackInsideRectangle(frame, 0, int(frameHeight/2 - 200), int(frameWidth/2 - 00), 2) and currentOrientation == "horizontal"):
                if(stopMoveGrid and lastMoveGrid is not "left"):
                    stopMoveGrid = False
                elif(currentDirection == "left" and not stopMoveGrid):
                    lastMoveGrid = "left"
                    stopMoveGrid = True
                    print("moved left")

            elif(blackInsideRectangle(frame, int(frameWidth/2 + 100), int(frameHeight/2 - 200), int(frameWidth/2 - 100), 2) and currentOrientation == "horizontal"):
                if(stopMoveGrid and lastMoveGrid is not "right"):
                    stopMoveGrid = False
                elif(currentDirection == "right" and not stopMoveGrid):
                    lastMoveGrid = "right"
                    stopMoveGrid = True
                    print("moved right")
            """

            if(stopDirectionSwitchTime <= 0):
                stopDirectionSwitch = False

            if(cornerCount > 10):
                findNextLine(frame, frameWidth, frameHeight, int(x + width/2), int(y + height/2))


            cv2.putText(frame, "orientation: " + str(currentOrientation), (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
            cv2.putText(frame, "move: " + str(currentDirection), (20, 210), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
            cv2.putText(frame, str(distanceIndicator), (20, 280), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
            cv2.putText(frame, str(currentLocation), (20, 350), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
            
            #fullBoundingBox
            cv2.rectangle(frame, (x,y), (x2,y2), (255, 0, 255), 3)
        
        #crosshair
        cv2.rectangle(frame, (int(frameWidth/2 - 1), int(frameHeight/2 - 10)), (int(frameWidth/2 + 1), int(frameHeight/2 +10)), (80,80,80), -1)
        cv2.rectangle(frame, (int(frameWidth/2 - 10), int(frameHeight/2-1)), (int(frameWidth/2 + 10), int(frameHeight/2 + 1)), (80,80,80), -1)
        #imgShow = np.hstack((frame, maskRed))
        imgShow = frame

        cv2.imshow("frame", imgShow)
        if cv2.waitKey(1) == 27:
            break
        
        #time.sleep(0.02)

    end()

def findNextLine(frame, frameWidth, frameHeight, cx, cy):
    global currentDirection, directionHistory, stopDirectionSwitch

    if(stopDirectionSwitch):
        return

    dx = cx - (frameWidth / 2)
    dy = cy - (frameHeight / 2)
    print(dx)
    print(dy)
    if (currentDirection == None):
        if (abs(dx) > abs(dy)):
            if (dx > 0):
                currentDirection = "right"
            else:
                currentDirection = "left"
        else:
            if (dy > 0):
                currentDirection = "down"
            else:
                currentDirection = "up"
    elif (currentDirection == "down" or currentDirection == "up"):
        if (dx > 0):
            currentDirection = "right"
        else:
            currentDirection = "left"
    else:
        if (dy > 0):
            currentDirection = "down"
        else:
            currentDirection = "up"
    stopDirectionSwitch = True

    '''
    if(redInsideRectangle(frame, frameWidth - 10, 0, 2, frameHeight) and currentDirection is not "left" and currentDirection is not "right"):
        directionHistory.append(currentDirection)
        currentDirection = "right"
        stopDirectionSwitch = True
    elif(redInsideRectangle(frame, 10, 0, 2, frameHeight) and currentDirection is not "left" and currentDirection is not "right"):
        directionHistory.append(currentDirection)
        currentDirection = "left"
        stopDirectionSwitch = True
    elif(redInsideRectangle(frame, 0, 10, frameWidth, 2) and currentDirection is not "down" and currentDirection is not "up"):
        directionHistory.append(currentDirection)
        currentDirection = "up"
        stopDirectionSwitch = True
    elif(redInsideRectangle(frame, 0, frameHeight - 10, frameWidth, 2) and currentDirection is not "down" and currentDirection is not "up"):
        #print("wwp")
        directionHistory.append(currentDirection)
        currentDirection = "down"
        stopDirectionSwitch = True
    else:
        end()
    '''
    cv2.rectangle(frame, (0, frameHeight-10), (frameWidth, frameHeight-10+2), (255,0,0), -1)
        
    

def redInsideRectangle(matRed, x, y, w, h):
    for xx in range(x,x+w-1):
        for yy in range(y, y+h-1):
            #print(yy)
            if(inColorRange(matRed[yy,xx], redHSV["low"], redHSV["high"])):
                return True
    return False

def blackInsideRectangle(frame, x, y, w, h):
    for xx in range(x,x+w-1):
        for yy in range(y, y+h-1):
            if(inColorRange(frame[yy,xx], black["low"], black["high"])):
                return True
    return False

def inColorRange(val, min, max):
    if(val[0] > min[0] and val[0] < max[0]):
        if(val[1] > min[1] and val[1] < max[1]):
            if(val[2] > min[2] and val[2] < max[2]):
                return True
    return False

def checkDistance(contour):
    global distanceIndicator
    x,y,w,h = cv2.boundingRect(contour)
    v = min(w,h)
    if(v > distanceWidth + distanceDeadZone):
        distanceIndicator = "move back"
    elif(v < distanceWidth - distanceDeadZone):
        distanceIndicator = "move forward"
    else:
        distanceIndicator = ""
        

if __name__ == "__main__":
    start()