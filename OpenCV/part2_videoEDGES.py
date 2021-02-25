import cv2
import numpy as np

cap = cv2.VideoCapture(0)


while True:
    success, img = cap.read()

    kernel = np.ones((5,5), np.uint8)

    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (7,7), 0)
    # Detect edges
    imgCanny = cv2.Canny(img, 100, 100) 
    # Increase egde thickness
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1) # iterations = 1,2,3,...
    # Decrease edge thickenss
    imgEroded = cv2.erode(imgDialation, kernel, iterations=1)

    cv2.imshow("Video grey", imgGrey)
    cv2.imshow("Video blur", imgBlur)
    cv2.imshow("Video cany", imgCanny)
    cv2.imshow("Video dialation", imgDialation)
    cv2.imshow("Video eroded", imgEroded)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break