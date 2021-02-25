import cv2
import numpy as np

img = cv2.imread('Resources/kings.jpg', -1)

width, height = 250,350
pts1 = np.float32([[950,200],[1250,330],[733,578],[1100, 780]])
pts2 = np.float32([[0,0],[width, 0],[0, height],[width, height]])

matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img, matrix,(width,height))

cv2.imshow("Image", img)
cv2.imshow("OUTPUT", imgOutput)

cv2.waitKey(0)