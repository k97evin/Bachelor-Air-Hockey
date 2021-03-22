#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import packages
import numpy as np
import cv2 as cv
import glob
import pickle

# square constants
IMG_WIDTH = 9
IMG_HEIGHT = 6


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((IMG_HEIGHT*IMG_WIDTH,3), np.float32)
objp[:,:2] = np.mgrid[0:IMG_WIDTH,0:IMG_HEIGHT].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space.
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (IMG_WIDTH,IMG_HEIGHT), None)

    # If found, add object points, image points (after refining them)
    if ret is True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (IMG_WIDTH,IMG_HEIGHT), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
cv.destroyAllWindows()


# Calibration
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Obtain new optimal cameramatrix and ROI
img = cv.imread('image2.jpg')
h,  w = img.shape[:2]
optimal_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))


# Save the camera calibration results to pickle file
calib_result_pickle = {}
calib_result_pickle["mtx"] = mtx
calib_result_pickle["optimal_camera_matrix"] = optimal_camera_matrix
calib_result_pickle["dist"] = dist
calib_result_pickle["rvecs"] = rvecs
calib_result_pickle["tvecs"] = tvecs
pickle.dump(calib_result_pickle, open("camera_calib_pickle.p", "wb" )) 


# Print the camera calibration
#print("mtx: ", mtx)
#print("\noptimal camera matrix: ", optimal_camera_matrix)
#print("\ndist: ", dist)

