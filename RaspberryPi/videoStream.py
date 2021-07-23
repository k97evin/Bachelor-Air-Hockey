# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Importing packages """
#from pymunk import vec2d
from globfile import *
#import cv2.aruco as aruco
import pickle
#import numpy as np
#from datetime import datetime


class VideoStream():
    def __init__(self, src = 0, width = 640, height = 480, framerate = 30.0, buffersize = 1) :
        self.stream = cv2.VideoCapture(src)

        """ CAMERA SETTINGS """
        #self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        #self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_FPS, framerate)
        #self.stream.set(cv2.CAP_PROP_AUTOFOCUS,0)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, buffersize)

        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

        self.current_time = None

        """ COLOR CONSTRUCTORS """
        # BLUE
        #self.lower_range_puck_color = np.array([99,186,130])
        #self.upper_range_puck_color = np.array([159,255,255])        
        # GREEN
        self.lower_range_puck_color = np.array([41,81,71])
        self.upper_range_puck_color = np.array([84,255,255])

        """ READING PICKLE-FILE AND IMPORT CAMERA CALIBRATION MATRICES """
        calib_result_pickle = pickle.load(open("camera_calib_pickle.p", "rb" ))
        self.old_camera_matrix = calib_result_pickle["mtx"]
        self.optimal_camera_matrix = calib_result_pickle["optimal_camera_matrix"]
        self.distortion_matrix = calib_result_pickle["dist"]

        """ ARUCO DICTIONARY AND PARAMETERS """
        self.ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        self.arucoParameters = aruco.DetectorParameters_create()

        """ ROI LIMITS """
        self.max_x = 0
        self.max_y = 0
        self.min_x = 10000
        self.min_y = 10000

        """ PIXEL CONVERSION """
        self.world_unit_px_conversion = 0
        self.world_unit_py_conversion = 0



    def start(self):
        # Start camera and dedicated thread
        if self.started:
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self


    def update(self):
        # Grab frames from camera
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            #self.current_time = datetime.now().time()
            self.current_time = datetime.now()
            #print(self.current_time)
            self.read_lock.release()


    def undistort_camera(self):
        # Undistort camera with camera calibration matrices
        self.read_lock.acquire()
        frame = self.frame.copy()
        time = self.current_time
        self.read_lock.release()
        undistorted_frame = cv2.undistort(frame, self.old_camera_matrix, self.distortion_matrix, None, self.optimal_camera_matrix)
        return undistorted_frame, time


    def puck_color(self, min_hue, min_saturation, min_value, max_hue, max_saturation, max_value):
        # Getting HSV-color range for puck needed for puck detection
        self.lower_range_puck_color = np.array[(min_hue, min_saturation, min_value)]
        self.upper_range_puck_color = np.array[(max_hue, max_saturation, max_value)]

    def robot_detection(self):

        frame, _ = self.undistort_camera()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = aruco.detectMarkers(gray, dictionary=self.ARUCO_DICT, parameters=self.arucoParameters)

        if np.all(ids is not None):
            for i in range(len(ids)):
                if ids[i] == 4:
                    return True
        else: return False

    def corner_detection(self):
        """ Detect corners """
        frame, _ = self.undistort_camera()

        # Convert into gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find all the aruco markers in the frame
        corners, ids, rejected = aruco.detectMarkers(gray, dictionary=self.ARUCO_DICT, parameters=self.arucoParameters)

        # Removing robots ID if it found
        if np.all(ids is not None):     
            remove_pos = -1
            for i in range(len(ids)):
                if ids[i] == 4:
                    remove_pos = i
                    
            if remove_pos != -1:
                ids = np.delete(ids,remove_pos)
                corners.pop(remove_pos)
                
                
        if np.all(ids is not None and len(ids) == 4):           
            for id, corner in zip(ids, corners):

                # Playing area + offset
                if corner[0][0][0] < self.min_x: self.min_x = int(corner[0][0][0]) - 35 #35
                if corner[0][0][0] > self.max_x: self.max_x = int(corner[0][0][0]) + 5  #8
                if corner[0][0][1] < self.min_y: self.min_y = int(corner[0][0][1]) - 6
                if corner[0][0][1] > self.max_y: self.max_y = int(corner[0][0][1]) + 5

                # Playing area
                # if corner[0][0][0] < self.min_x: self.min_x = int(corner[0][0][0]) - 9 
                # if corner[0][0][0] > self.max_x: self.max_x = int(corner[0][0][0]) + 5 
                # if corner[0][0][1] < self.min_y: self.min_y = int(corner[0][0][1]) - 6
                # if corner[0][0][1] > self.max_y: self.max_y = int(corner[0][0][1]) + 5
                                
            if self.min_x < 0: self.min_x = 0
            if self.min_y < 0: self.mix_y = 0
            
            #roi = frame[self.min_y:self.max_y, self.min_x:self.max_x]

            roi_px = self.max_x - self.min_x
            roi_py = self.max_y - self.min_y
            # Relationship between pixel and millimetres
            self.world_unit_px_conversion = table_width/roi_px
            self.world_unit_py_conversion = table_height/roi_py
           
            return _, True

        else:
            # Checking which corners is missing
            aruco_verification = [False, False, False, False]

            if np.all(ids is not None):
                for i in range(len(ids)):
                    if ids[i] == 0: aruco_verification[0] = True
                    if ids[i] == 1: aruco_verification[1] = True
                    if ids[i] == 2: aruco_verification[2] = True
                    if ids[i] == 3: aruco_verification[3] = True                    

            return aruco_verification, False



    def region_of_interest(self):
        # Cropping frame to ROI
        frame, time = self.undistort_camera()
        roi = frame[self.min_y:self.max_y, self.min_x:self.max_x]
        return roi, time

    def pixel_to_mm(self,pixel_x,pixel_y):
        # Pixel units to millimetres
        pos_px = pixel_x * self.world_unit_px_conversion
        pos_py = pixel_y * self.world_unit_py_conversion
        pos_world_unit = Vec2d(pos_px, pos_py)
        return pos_world_unit


    def get_robot_coordinates_roi(self):
        """ Gets robots coordinate from ArUco ID 4 in ROI """
        frame, _ = self.region_of_interest()
        
        # Convert into grey scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejected = aruco.detectMarkers(gray, dictionary=self.ARUCO_DICT, parameters=self.arucoParameters)
        
        center = -1
        if np.all(ids is not None): 
            for id, corner in zip(ids, corners):              
                if id == 4:
                    pixel_x = (corner[0][0][0] + corner[0][1][0] + corner[0][2][0] + corner[0][3][0]) / 4
                    pixel_y = (corner[0][0][1] + corner[0][1][1] + corner[0][2][1] + corner[0][3][1]) / 4
                    
                    center = self.pixel_to_mm(pixel_x-20,pixel_y)

                    # Adding offset because the pusher is at a higher position than the playing surface
                    offset_x = pusher_height/camera_height * (table_center_x-center.x)
                    offset_y = pusher_height/camera_height * (table_center_y-center.y)
                    offset = Vec2d(offset_x,offset_y)
                    
                    center = center + offset

        return center

    def get_robot_coordinates_full_fov(self):
        """ Gets robots coordinate from ArUco ID 4 in full FOV"""
        frame, _ = self.undistort_camera()

        # Convert into grey scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejected = aruco.detectMarkers(gray, dictionary=self.ARUCO_DICT, parameters=self.arucoParameters)
        
        center = -1
        pixel_x = -1
        if np.all(ids is not None): 
            for id, corner in zip(ids, corners):              
                if id == 4:
                    pixel_x = (corner[0][0][0] + corner[0][1][0] + corner[0][2][0] + corner[0][3][0]) / 4
                    pixel_y = (corner[0][0][1] + corner[0][1][1] + corner[0][2][1] + corner[0][3][1]) / 4
                    
                    center = Vec2d(pixel_x,pixel_y)

        return pixel_x

    def get_robot(self, frame, roi):
        frame, _ = self.undistort_camera()
        
        # Convert into grey scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, rejected = aruco.detectMarkers(gray, dictionary=self.ARUCO_DICT, parameters=self.arucoParameters)
        
        #center = -1
        pixel_x = -1
        if np.all(ids is not None): 
            for id, corner in zip(ids, corners):              
                if id == 4:
                    pixel_x = (corner[0][0][0] + corner[0][1][0] + corner[0][2][0] + corner[0][3][0]) / 4
                    pixel_y = (corner[0][0][1] + corner[0][1][1] + corner[0][2][1] + corner[0][3][1]) / 4
                    
                    #center = Vec2d(pixel_x,pixel_y)
                    Vec2d(pixel_x,pixel_y)

        return pixel_x



    def get_puck_coordinates(self):
        """ Gets pucks coordinates by masking the puck with values for HSV-color range """  
        roi, time = self.region_of_interest()
        #roi = cv2.bitwise_and(roi, roi)

        # Convert frame from RGB to HSV colorscale
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Masking the object with defined color range
        mask = cv2.inRange(hsv, self.lower_range_puck_color, self.upper_range_puck_color)

        # Enlarge the mask
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(mask, kernel)

        # Finding the contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            # Finds the biggest object with defined color
            obj = max(contours, key=cv2.contourArea)
            # Draw contour on object
            cv2.drawContours(roi, obj, -1, (0, 255, 0), 2)
            # Calculate center-coordinates of the object
            moments = cv2.moments(obj)

            pixel_x = int(moments["m10"] / moments["m00"]) -20
            pixel_y = int(moments["m01"] / moments["m00"])
            # Convert from pixel to millimetres
            center_pos = self.pixel_to_mm(pixel_x, pixel_y)

        else:
            center_pos = -1

        return roi, time, center_pos
        


    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()


