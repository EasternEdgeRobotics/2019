import cv2
import numpy as np

cap = cv2.VideoCapture('udpsrc port=5002 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

while True:
	
	ret, img = cap.read()
	
	cv2.imshow('test', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
cap.release()
cv2.destroyAllWindows()