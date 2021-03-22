# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Crops the frame of top left corners of the markers
Setup ARUCO with IDs:
                0   1

                2   3

"""



# Import packages
import numpy as np
import cv2
import cv2.aruco as aruco
import pickle



""" READING PICKLE-FILE AND IMPORT CALIBRATION MATRICES"""
calib_result_pickle = pickle.load(open("camera_calib_pickle.p", "rb" ))
old_camera_matrix = calib_result_pickle["mtx"]
optimal_camera_matrix = calib_result_pickle["optimal_camera_matrix"]
dist_matrix = calib_result_pickle["dist"]

# Print matrices
print("old: \n", old_camera_matrix)
print("new: \n", optimal_camera_matrix)
print("dist: \n", dist_matrix)


# Define aruco dictionary
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
arucoParameters = aruco.DetectorParameters_create()

# ROI limits
max_x = 0
max_y = 0
min_x = 10000
min_y = 10000

# Capture the videocamera
cap = cv2.VideoCapture(0)

while True:
    # Read the camera frame
    ret, frame = cap.read()

    undistorted_frame = cv2.undistort(frame, old_camera_matrix, dist_matrix, None, optimal_camera_matrix)

    # Convert into grey scale
    gray = cv2.cvtColor(undistorted_frame, cv2.COLOR_BGR2GRAY)

    # Find all the aruco markers in the image
    corners, ids, rejected = aruco.detectMarkers(gray, dictionary=ARUCO_DICT, parameters=arucoParameters)
    if np.all(ids is not None and len(ids) == 4):
        for id, corner in zip(ids, corners):
            if corner[0][0][0] < min_x: min_x = int(corner[0][0][0])
            if corner[0][0][0] > max_x: max_x = int(corner[0][0][0])
            if corner[0][0][1] < min_y: min_y = int(corner[0][0][1])
            if corner[0][0][1] > max_y: max_y = int(corner[0][0][1])
        break
    
    cv2.imshow('Display', undistorted_frame)
    
    # Break loop if ESC-key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

while True:
    # Read the camera frame
    ret, frame = cap.read()
    undistorted_frame = cv2.undistort(frame, old_camera_matrix, dist_matrix, dst=None, newCameraMatrix=optimal_camera_matrix)
    # Defining ROI
    roi = undistorted_frame[min_y:max_y, min_x:max_x]


    """ Detect puck"""
    roi = cv2.bitwise_and(roi, roi)
    
    # Convert frame from RGB to HSV colorscale
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Set lower and upper range for color
    # In this case: detect color BLUE
    lower_range = np.array([110,50,50])
    upper_range = np.array([130,255,255])

    # Masking the object with defined color range
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Enlarge the mask
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(mask, kernel)
    #_, thresh = cv2.threshold(mask, 127, 255, 0)

     # Finding the contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Finds the biggest object with defined color
        obj = max(contours, key=cv2.contourArea)
        # Draw contour on object
        cv2.drawContours(roi, obj, -1, (0, 255, 0), 2)
        # Calculate center-coordinates of the object 
        moments = cv2.moments(obj)
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
        # Print coordinates
        print(center)

    else:
        print("(0, 0)")
    

    # Display windows
    cv2.imshow('ROI', roi)  
    cv2.imshow('Display', undistorted_frame)
    #cv2.imshow("Dilation", dilation)
    
    
    # Break loop if ESC-key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv_file.release()
cv2.destroyAllWindows()
