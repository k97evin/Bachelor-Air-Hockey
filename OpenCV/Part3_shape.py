import cv2

img = cv2.imread('Resources/logo.png', -1)
print(img.shape)

imgResize = cv2.resize(img,(300,200))
print(imgResize.shape)

imgCropped = img[0: 400, 200:600]
print(imgCropped.shape)

cv2.imshow("Image", img)
cv2.imshow("Image Resize", imgResize)
cv2.imshow("Image Resize", imgCropped)

cv2.waitKey(0)