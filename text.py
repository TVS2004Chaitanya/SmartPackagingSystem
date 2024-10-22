import pytesseract
import cv2 as cv
from PIL import Image

img = cv.imread("ExpiryDate4.jpg")
cv.namedWindow('Image', cv.WINDOW_NORMAL)  # Allows resizing
cv.resizeWindow('Image', 800, 600)  # Adjust the window size as needed

# Display the image
cv.imshow('Image', img)

custom_config = r" --oem 3 --psm 11"
text = pytesseract.image_to_string(img, config = custom_config)
print(text)

cv.waitKey(0)