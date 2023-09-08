import cv2
import numpy as np


image = cv2.imread('test/cropped_image.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
# _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

mask = np.zeros_like(image)

cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

cv2.imshow('Original Image', image)
cv2.imwrite('test/mask.jpg', mask)
cv2.imshow('Mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()