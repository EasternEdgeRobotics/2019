import cv2
import numpy as np
import math
import time
import colorsys
from detectCracks import detectCracks

cam = None
#cam_connection = 0
cam_connection = "udpsrc port=4444 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER"
#cam_connection = "static/video/lineVideo.MOV"

frameWidth = 0
frameHeight = 0

centerbox = {"x": None, "y": None, "width": 25, "height": 25}
lines = {
    "up": {"x": None, "y": 0, "width": 30, "height": None},
    "right": {"x": None, "y": None, "width": None, "height": 30},
    "down": {"x": None, "y": None, "width": 30, "height": None},
    "left": {"x": 0, "y": None, "width": None, "height": 30}
}
lineDeadzone = 100

isRunning = False

#|, _, |_, _|, -|, |-
grid = []
currentPosition = [0,0]

directionHistory = []
currentDirection = None

stopDirectionSwitch = False
stopDirectionSwitchTime = 0

distanceWidth = 110
distanceDeadZone = 15
distanceIndicator = ""

stopMoveGrid = False
lastMoveGrid = None


#B,G,R
#red = {"low": (0,0,100), "high": (30,10,255)}
#H,S,V
redHSV = {"low": (330, 60, 30), "high": (360, 100, 80)}
red = {"low": (), "high": ()} #when ran, hsv is converted to rgb80
#hsv
black = {"low": (0,0,0), "high": (360,100,60)}

def start():
    global isRunning, cam, frameWidth, frameHeight, centerbox, lines, lineDeadzone, red
    isRunning = True
    cam = cv2.VideoCapture(cam_connection)

    rgbLow = colorsys.hsv_to_rgb(redHSV["low"][0]/360, redHSV["low"][1]/100,redHSV["low"][2]/100)
    rgbHigh = colorsys.hsv_to_rgb(redHSV["high"][0]/360,redHSV["high"][1]/100,redHSV["high"][2]/100)

    red["low"] = (int(min(rgbLow[2]*255, rgbHigh[2]*255)) , int(min(rgbLow[1]*255, rgbHigh[1]*255)), int(min(rgbLow[0]*255, rgbHigh[0]*255)))
    red["high"] = (int(max(rgbLow[2]*255, rgbHigh[2]*255)) , int(max(rgbLow[1]*255, rgbHigh[1]*255)), int(max(rgbLow[0]*255, rgbHigh[0]*255)))

    #print(red["low"])
    #print(red["high"])
    if(cam.isOpened()):
        frameWidth = int(cam.get(3))
        frameHeight = int(cam.get(4))
        centerbox["x"] = int(frameWidth/2 - centerbox["width"]/2)
        centerbox["y"] = int(frameHeight/2 - centerbox["height"]/2)

        lines["up"]["x"] = int(frameWidth/2 - lines["up"]["width"]/2)
        lines["up"]["height"] = int(frameHeight/2) - lineDeadzone

        lines["right"]["x"] = int(frameWidth/2) + lineDeadzone
        lines["right"]["width"] = int(frameWidth/2) - lineDeadzone - 2
        lines["right"]["y"] = int(frameHeight/2 - lines["right"]["height"]/2)

        lines["down"]["x"] = int(frameWidth/2 - lines["down"]["width"]/2)
        lines["down"]["height"] = int(frameHeight/2) - lineDeadzone
        lines["down"]["y"] = int(frameHeight/2) + lineDeadzone

        lines["left"]["width"] = int(frameWidth/2) - lineDeadzone
        lines["left"]["y"] = int(frameHeight/2 - lines["left"]["height"]/2)

        loop()
    else:
        print("Unable to open video feed.")

def end():
    global isRunning, cam
    isRunning = False

    print("WOOOOOO WE DID IT!!!")

    cam.release()
    cv2.destroyAllWondows()

def loop():
    global cam, currentDirection, stopDirectionSwitchTime, stopDirectionSwitch, stopMoveGrid, lastMoveGrid

    cornerCount = 0

    while(isRunning and cam.isOpened()):
        ret, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        crack = detectCracks(frame)
        print(crack)

        maskRed = cv2.inRange(frame, red["low"], red["high"])

        maskRed = cv2.cvtColor(maskRed, cv2.COLOR_GRAY2BGR)
        maskRed = cv2.cvtColor(maskRed, cv2.COLOR_BGR2GRAY)

        isOnLine = redInsideRectangle(frame, centerbox["x"], centerbox["y"], centerbox["width"], centerbox["height"])

        directionToMove = ""
        
        currentOrientation = ""
        currentRatio = ""

        contours, h = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if(area > 10000):
                cv2.drawContours(frame, contour, -1, (255,0,0), 3)
                M = cv2.moments(contour)
                if(M["m00"] > 0):
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    cv2.circle(frame, (cx,cy), 5, (255,255,0), -1)

                x,y,width,height = cv2.boundingRect(contour)
                #print(width)

                currentRatio = str(width/height)

                if(currentDirection == None):
                    findNextLine(frame, frameWidth, frameHeight)
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

        #maskBlack = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #blackhsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #maskBlack = cv2.inRange(blackhsv, black["low"], black["high"])
        #maskBlack = cv2.GaussianBlur(maskBlack,(5,5),0)
        
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


        if(stopDirectionSwitchTime <= 0):
            stopDirectionSwitch = False

        if(cornerCount > 10):
            findNextLine(frame, frameWidth, frameHeight)


        cv2.putText(frame, "orientation: " + str(currentOrientation), (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
        cv2.putText(frame, "ratio: " + str(currentRatio), (20, 140), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
        cv2.putText(frame, "move: " + str(currentDirection), (20, 210), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
        cv2.putText(frame, str(distanceIndicator), (20, 280), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0))
        
        #imgShow = np.hstack((frame, maskRed))
        imgShow = frame

        cv2.imshow("frame", imgShow)
        if cv2.waitKey(1) == 27:
            break
        
        #time.sleep(0.02)

    end()

def findNextLine(frame, frameWidth, frameHeight):
    global currentDirection, directionHistory, stopDirectionSwitch

    if(stopDirectionSwitch):
        return

    #print("woop")

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

    
    cv2.rectangle(frame, (0, frameHeight-10), (frameWidth, frameHeight-10+2), (255,0,0), -1)
        
    

def redInsideRectangle(matRed, x, y, w, h):
    for xx in range(x,x+w-1):
        for yy in range(y, y+h-1):
            #print(yy)
            if(inColorRange(matRed[yy,xx], red["low"], red["high"])):
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

def inColorRangeRedHSV(val, min, max):
    if(val[0] > max[0] or val[0] < min[0]):
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