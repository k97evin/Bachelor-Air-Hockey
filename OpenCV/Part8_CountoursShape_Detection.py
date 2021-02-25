import cv2
import numpy as np


def getCountours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Retrieves the extreme outer contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 100:
            cv2.drawContours(imgContour, cnt, -1, (255,0,0), 3)
            perimetre = cv2.arcLength(cnt, True)
            #print(perimetre)
            approx = cv2.approxPolyDP(cnt, 0.02*perimetre, True)
            print(len(approx))
            objCorneres = len(approx)
            x,y,w,h = cv2.boundingRect(approx)

            if objCorneres == 3: objectType = "Triangle"
            elif objCorneres == 4: 
                aspectRatio = w/float(h)
                if aspectRatio > 0.95 and aspectRatio < 1.05: objectType = "Square"
                else: objectType = "Rectangle"
            elif objCorneres > 4: objectType = "Circle"
            else: objectType = "NONE"

            cv2.rectangle(imgContour,(x,y), (x+w, y+h), (0,255,0), 2) # Create rectangle around each object
            cv2.putText(imgContour,objectType, 
                                (x+(w//2)- 10, y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0),2)


path = 'Assets/Shapes.jpg'
img = cv2.imread(path)
img = cv2.resize(img, (0,0), fx=0.5,fy=0.5)
imgContour = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,150,100)

getCountours(imgCanny)

cv2.imshow("Original", img)
cv2.imshow("Gray", imgGray)
cv2.imshow("Blur", imgBlur)
cv2.imshow("Canny", imgCanny)
cv2.imshow("Contours", imgContour)

cv2.waitKey(0)