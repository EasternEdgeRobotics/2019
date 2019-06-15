import cv2
import numpy as np
import math
import time
import colorsys
from detectCracks import detectCracks
import detectGridPosition
import topsidesComms
from TopsidesGlobals import GLOBALS
import sys

#camera and frame variables
cam = None
cam_connection = "udpsrc port=5004 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER"
frameWidth = 0
frameHeight = 0
OGframeWidth = 0
OGframeHeight = 0
centerbox = {"x": None, "y": None, "width": 25, "height": 25}

isRunning = False

#track current state of task
currentLocation = [-1, 3]
crackPosition = [0, 0]
currentDirection = None
currentAdjust = None

ADJ_THRESH = 5

#direction switching control values
stopDirectionSwitch = False
stopDirectionSwitchTime = 0

#distance from dam initialization
distanceWidth = 80 #80
distanceDeadZone = 10
distanceIndicator = ""

cornerFixVert = 0
cornerFixHorz = 0
cornerFixNum = 0.1

#red hsv threshold values
red2HSV = {"low": (0, 50, 57), "high": (30, 255, 210)}
redHSV = {"low": (149, 50, 57), "high": (179, 255, 210)}

red = {"low": (), "high": ()} #when ran, hsv is converted to rgb80
red2 = {"low": (), "high": ()} #when ran, hsv is converted to rgb80
#hsv
black = {"low": (0,0,0), "high": (360,100,60)}


CROP_WIDTH = 300
CROP_HEIGHT = 300


def start():
    global isRunning, cam, frameWidth, frameHeight, centerbox, OGframeHeight, OGframeWidth
    isRunning = True
    cam = cv2.VideoCapture(cam_connection)

    if(cam.isOpened()):
        OGframeWidth = int(cam.get(3))
        OGframeHeight = int(cam.get(4))
        frameWidth = int(cam.get(3))
        frameHeight = int(cam.get(4))
        centerbox["x"] = int(frameWidth/2 - centerbox["width"]/2)
        centerbox["y"] = int(frameHeight/2 - centerbox["height"]/2)
        
        loop()
    else:
        print("Unable to open video feed.")

def end():
    global isRunning, cam
    isRunning = False

    print("WOOOOOO WE DID IT!!!")

    cam.release()
    cv2.destroyAllWindows()

def loop():
    global cam, currentDirection, stopDirectionSwitchTime, stopDirectionSwitch, stopMoveGrid, lastMoveGrid, currentLocation, currentAdjust, distanceIndicator,cornerFixHorz, cornerFixVert, frameHeight, frameWidth, centerbox

    cornerCount = 0

    while(isRunning and cam.isOpened()):
        
        ret, frame = cam.read()
        frame = cv2.GaussianBlur(frame,(5,5),0)
        
        frame = frame[int(OGframeHeight/2 - CROP_HEIGHT/2):int(OGframeHeight/2 + CROP_HEIGHT/2), int(OGframeWidth/2 - CROP_WIDTH/2):int(OGframeWidth/2+CROP_WIDTH/2)]
        frameWidth = CROP_WIDTH
        frameHeight = CROP_HEIGHT
        
        centerbox["x"] = int(frameWidth/2 - centerbox["width"]/2)
        centerbox["y"] = int(frameHeight/2 - centerbox["height"]/2)
        
        imgShow = frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        try:
            crack = detectCracks(frame)

            maskRed = cv2.inRange(hsv, redHSV["low"], redHSV["high"])
            maskRed2 = cv2.inRange(hsv, red2HSV["low"], red2HSV["high"])

            maskRed = maskRed + maskRed2

            isOnLine = redInsideRectangle(hsv, centerbox["x"], centerbox["y"], centerbox["width"], centerbox["height"])
            
            currentOrientation = ""
            currentLocation = detectGridPosition.black_line_detection(frame, currentLocation, currentDirection)

            contours, h = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            if(len(contours) > 0):
                x = frameWidth
                y = frameHeight
                x2 = -1
                y2 = -1
                width = None
                height = None
                
                centerX = 0
                centerY = 0
                
                fullcontour = None
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if(area > 500 and area < frameWidth*frameHeight - 2000):
                        cv2.drawContours(frame, contour, -1, (255,0,0), 3)
                        M = cv2.moments(contour)
                        cx = 0
                        cy = 0
                        if(M["m00"] > 0):
                            cx = int(M["m10"]/M["m00"])
                            cy = int(M["m01"]/M["m00"])
                            cv2.circle(frame, (cx,cy), 5, (255,255,0), -1)
                            #centerX = (centerX + cx) / 2
                            #centerY = (centerY + cy) / 2

                        xTemp,yTemp,widthTemp,heightTemp = cv2.boundingRect(contour)
                        x = min(x, xTemp)
                        y = min(y, yTemp)
                        x2 = max(x2, xTemp + widthTemp)
                        y2 = max(y2, yTemp + heightTemp)
                        
                        if(fullcontour is None):
                            fullcontour = contour
                        else:
                            fullcontour = fullcontour + contour

                if(x2 != -1):
                    width = x2 - x
                    height = y2 - y
                    
                    M = cv2.moments(contour)
                    if(M["m00"] > 0):
                        centerX = int(M["m10"]/M["m00"])
                        centerY = int(M["m01"]/M["m00"])
                    
                    ((Bx,By), (Bw,Bh), Brot) = cv2.minAreaRect(fullcontour)
                    
                    if(currentDirection == None):
                        currentDirection = input()
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
                        #checkDistance(width, height)
                        checkDistance(Bw, Bh)
                    else:
                        distanceIndicator = ""

                    if(stopDirectionSwitchTime <= 0):
                        stopDirectionSwitch = False

                    if(cornerCount > 10):
                        findNextLine(frame, frameWidth, frameHeight, int(x + width/2), int(y + height/2))
                    print(frameWidth/2, centerX)
                    currentAdjust = ""
                    if(currentOrientation == "vertical"):
                        if(centerX > int(frameWidth/2 + ADJ_THRESH)):
                            print("R")
                            currentAdjust = "right"
                        elif(centerX < int(frameWidth/2 - ADJ_THRESH)):
                            print("L")
                            currentAdjust = "left"
                        else:
                            currentAdjust = ""
                    elif(currentOrientation == "horizontal"):
                        if(centerY > int(frameHeight/2 + ADJ_THRESH)):
                            currentAdjust = "down"
                        elif(centerY < int(frameheight/2 - ADJ_THRESH)):
                            currentAdjust = "up"
                        else:
                            currentAdjust = ""
                    else:
                        currentAdjust = ""
                    
                    
                    cv2.putText(frame, "orientation: " + str(currentOrientation), (20, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))
                    cv2.putText(frame, "move: " + str(currentDirection), (20, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))
                    cv2.putText(frame, str(distanceIndicator), (20, 130), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))
                    cv2.putText(frame, str(currentLocation), (20, 160), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))
                    cv2.putText(frame, "ADJUST: " + str(currentAdjust), (20, 190), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255))
                    
                    #fullBoundingBox
                    cv2.rectangle(frame, (x,y), (x2,y2), (255, 0, 255), 3)
                
                #crosshair
                cv2.rectangle(frame, (int(frameWidth/2 - 1), int(frameHeight/2 - 10)), (int(frameWidth/2 + 1), int(frameHeight/2 +10)), (80,80,80), -1)
                cv2.rectangle(frame, (int(frameWidth/2 - 10), int(frameHeight/2-1)), (int(frameWidth/2 + 10), int(frameHeight/2 + 1)), (80,80,80), -1)
                imgShow = frame
                
                heave = 0
                if(currentDirection == "up"):
                    heave = -0.6
                elif(currentDirection == "down"):
                    heave = 0.6

                sway = 0
                if(currentDirection == "right"):
                    sway = 0.6
                elif(currentDirection == "left"):
                    sway = -0.6
                
                surge = 0
                """
                if(distanceIndicator == "move forward"):
                    surge = -0.10
                elif(distanceIndicator == "move back"):
                    surge = 0.10
                """
                if(currentAdjust == "up"):
                    heave = -0.3
                elif(currentAdjust == "down"):
                    heave = 0.3

                if(currentAdjust == "right"):
                    sway = 0.3
                elif(currentAdjust == "left"):
                    sway = -0.3
                
                #sway = -0.5
                #heave += cornerFixVert
                #sway += cornerFixHorz
                
                #yaw = (0.03) if heave < 0 else 0
                #yaw = 0
                
                
                thrusterData = {
                    "fore-port-vert": +heave,
                    "fore-star-vert": -heave,
                    "aft-port-vert": -heave,
                    "aft-star-vert": -heave,

                    #"fore-port-horz": -surge  + (sway if sway < 0 else 0),
                    #"fore-star-horz": +surge + (sway if sway > 0 else 0),
                    "aft-port-horz": -sway,
                    "aft-star-horz": - sway,
                }
                
                if(cornerFixHorz != 0):
                    cornerFixHorz -= cornerFixHorz/abs(cornerFixHorz)*0.001
                
                if(abs(cornerFixHorz) <= 0.01):
                    cornerFixHorz = 0
                
                if(cornerFixVert != 0):
                    cornerFixVert -= cornerFixVert/abs(cornerFixVert)*0.001
                    
                if(abs(cornerFixVert) <= 0.01):
                    cornerFixVert = 0
                
                for control in thrusterData:
                    print(control + "   " + str(thrusterData))
                    val = thrusterData[control]
                    topsidesComms.putMessage("runThruster.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
                

        except Exception as e:
            print(e, sys.exc_info()[-1].tb_lineno)

        cv2.imshow("frame", imgShow)
        if cv2.waitKey(1) == 27:
            break

    end()

def findNextLine(frame, frameWidth, frameHeight, cx, cy):
    global currentDirection, directionHistory, stopDirectionSwitch, cornerFixVert, cornerFixHorz

    if(stopDirectionSwitch):
        return

    dx = cx - (frameWidth / 2)
    dy = cy - (frameHeight / 2)
    #print(dx)
    #print(dy)
    if (currentDirection == None):
        if (abs(dx) > abs(dy) and currentDirection is not "horizontal"):
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
        cornerFixVert = (cornerFixNum if currentDirection is "down" else -cornerFixNum)
        if (dx > 0):
            currentDirection = "right"
        else:
            currentDirection = "left"
    else:
        cornerFixHorz = (cornerFixNum if currentDirection is "left" else -cornerFixNum)
        if (dy > 0):
            currentDirection = "down"
        else:
            currentDirection = "up"
    stopDirectionSwitch = True

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

def checkDistance(width, height):
    global distanceIndicator, distanceWidth, distanceDeadZone
    v = min(width, height)
    #print(width)
    print(height)
    if(v > distanceWidth + distanceDeadZone):
        distanceIndicator = "move back"
    elif(v < distanceWidth - distanceDeadZone):
        distanceIndicator = "move forward"
    else:
        distanceIndicator = ""
        

if __name__ == "__main__":
    start()
