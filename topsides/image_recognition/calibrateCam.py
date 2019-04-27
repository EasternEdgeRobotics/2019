import numpy as np
import cv2 as cv
import glob

def calibrateCam():
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (6,9), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (6,9), corners2, ret)
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
            img2 = cv.imread('test.jpg')
            h,  w = img2.shape[:2]
            newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
            # undistort
            dst = cv.undistort(img2, mtx, dist, None, newcameramtx)
            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv.imwrite('calibresult.png', dst)
            np.savez('camsettings', mtx=mtx, dist=dist, newcameramtx=newcameramtx)
            while True:
                cv.imshow('img', img)
                cv.imshow('dst', dst)
                k = cv.waitKey(5) & 0xFF
                if k == 27:
                    break
    cv.destroyAllWindows()

if __name__ == "__main__":
    calibrateCam()