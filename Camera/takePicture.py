# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("Frame")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break
    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "testPic{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{}".format(img_name))
        img_counter += 1


cam.release()
cv2.destroyAllWindows()