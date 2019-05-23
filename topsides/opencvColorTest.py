import cv2
import numpy as np

hLow = 0
sLow = 0
vLow = 0

hHigh = 360
sHigh = 255
vHigh = 255

cam = cv2.VideoCapture("udpsrc port=4444 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink", cv2.CAP_GSTREAMER)

title = "video"


video = "sliders" 
def on_h_l(val):
    global hLow
    print(val)
    hLow = int(val)

def on_h_h(val):
    global hHigh
    hHigh = int(val)

def on_s_l(val):
    global sLow
    sLow = int(val)

def on_s_h(val):
    global sHigh
    sHigh = int(val)

def on_v_l(val):
    global vLow
    vLow = int(val)

def on_v_h(val):
    global vHigh
    vHigh = int(val)


cv2.namedWindow(video)
cv2.createTrackbar("h - min", video, 0, 360, on_h_l)
cv2.createTrackbar("h - max", video, 0, 360, on_h_h)
cv2.createTrackbar("s - min", video, 0, 255, on_s_l)
cv2.createTrackbar("s - max", video, 0, 255, on_s_h)
cv2.createTrackbar("v - min", video, 0, 255, on_v_l)
cv2.createTrackbar("v - max", video, 0, 255, on_v_h)

while True:   
    
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (hLow, sLow, vLow), (hHigh, sHigh, vHigh))

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        if(cv2.contourArea(c) > 1000):
            cv2.drawContours(frame, c, -1, (255,0,0), 3)
    
    cv2.imshow("video", frame)
    cv2.imshow("mask", mask)
    if cv2.waitKey(1) == 27:
            break