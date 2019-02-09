import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
# read the video capture frame
_, frame = cap.read()

frameContrast = np.zeros(frame.shape, frame.dtype)
alpha = 1.5
beta = 20.0
for y in range(frame.shape[0]):
    for x in range(frame.shape[1]):
        for c in range(frame.shape[2]):
            frameContrast[y,x,c] = np.clip(alpha*frame[y,x,c] + beta, 0, 255)

frameGray = cv.cvtColor(frameContrast, cv.COLOR_BGR2GRAY)


while(True):
    cv.imshow('frame', frame)
    cv.imshow('contrast', frameContrast)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
cap.release()