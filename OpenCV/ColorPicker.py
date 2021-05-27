import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640,240)
cv2.createTrackbar("Hue Min", "HSV", 0, 179, empty)
cv2.createTrackbar("Saturation Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Value Min", "HSV", 0, 255, empty)
cv2.createTrackbar("Hue Max", "HSV", 179, 179, empty)
cv2.createTrackbar("Saturation Max", "HSV", 255, 255, empty)
cv2.createTrackbar("Value Max", "HSV", 255, 255, empty)

while True:
    #img = cv2.imread()
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min","HSV")
    h_max = cv2.getTrackbarPos("Hue Max","HSV")
    s_min = cv2.getTrackbarPos("Saturation Min","HSV")
    s_max = cv2.getTrackbarPos("Saturation Max","HSV")
    v_min = cv2.getTrackbarPos("Value Min","HSV")
    v_max = cv2.getTrackbarPos("Value Max","HSV")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)

    imgResult = cv2.bitwise_and(img, img, mask=mask) # compares two pictures and adds to all white


    
    cv2.imshow("Original", img)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", imgResult)
    cv2.imwrite('test.png', mask)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break