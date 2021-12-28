import cv2
import numpy as np

img = cv2.imread("input.jpg")

# 1) Edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur= cv2.medianBlur(gray, 5)
edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)


# 2) Color
color = cv2.bilateralFilter(img, d=9, sigmaColor=300, sigmaSpace=300)

# 3) Cartoon
cartoon = cv2.bitwise_and(color, color, mask=edges)

cv2.imwrite('output.jpg',cartoon);
cv2.imshow("Image", img)
cv2.imshow("Blured Gray",blur)
cv2.imshow("color",color)
cv2.imshow("Cartoon", cartoon)
cv2.imshow("gray", gray)
cv2.imshow("edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows(1)
