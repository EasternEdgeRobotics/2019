import numpy as np
import cv2 as cv
import glob

npzfile = np.load('camsettings.npz')
img2 = cv.imread('test.jpg')
dst = cv.undistort(img2, npzfile['mtx'], npzfile['dist'], None, npzfile['newcameramtx'])
while True:
    cv.imshow('img', img2)
    cv.imshow('dst', dst)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
