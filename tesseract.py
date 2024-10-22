import pytesseract
import cv2 as cv
from PIL import Image

img = cv.imread("LogoCheck.jpg")
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
cv.imshow("PreProcessed", img)
# print(pytesseract.image_to_string(img))

#Note: OpenCV assumes origin to be at top-left corner but pytesseract assumes origin is at bottom-left corner. This is only for img_to_string, this changes for img_to_data. 

# #Detecting Characters
# hImg, wImg, _ = img.shape
# boxes = pytesseract.image_to_boxes(img)
# if boxes:
#     for b in boxes.splitlines():
#         # print(b)
#         b = b.split(' ')
#         print(b)
#         x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
#         y = hImg - y
#         h = hImg - h
#         cv.rectangle(img, (x,y), (w, h),(0,0,255), 2)
#         cv.putText(img, b[0], (x,h+5), cv.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 2)

#Detecting Words
hImg, wImg, _ = img.shape
boxes = pytesseract.image_to_data(img)
print(boxes)
if boxes:
    for x,b in enumerate(boxes.splitlines()):
        # print(b)
        if x!=0:
            b = b.split()
            # print(b)
            if len(b)==12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv.rectangle(img, (x,y), (w+x,h+y), (0,0,255), 3)
                cv.putText(img, b[11], (x,y), cv.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 2)



cv.imshow("Result", img)
cv.waitKey(0)