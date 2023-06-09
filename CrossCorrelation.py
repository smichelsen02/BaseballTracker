import numpy as np
import cv2 as cv

img = cv.imread('images/maskImages/frameL680.png', 0)
template = cv.imread('images/Templates/template2.png', 0)

#mid range for template should be around 42x42
h, w = template.shape
print(h, w)

#test template is best so far
template = cv.imread('images/Templates/8APTTemplate.tif', 0)
h, w = template.shape
print(h, w)


methods = [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR,
           cv.TM_CCORR_NORMED, cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]

for method in methods:
    img2 = img.copy()

    result = cv.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc
    bottomRightLocation = (location[0] + w, location[1] + h)
    cv.rectangle(img2, location, bottomRightLocation, 255, 5)
    cv.imshow('Match', img2)
    cv.waitKey(0)
    cv.destroyAllWindows()


cap = cv.VideoCapture('images/videos/tests_C002H001S0001.mp4')
while cap.isOpened():
    ret, imgV = cap.read()
    imgVG = cv.cvtColor(imgV, cv.COLOR_BGR2GRAY)
    method = methods[3]

    #run template matching
    result = cv.matchTemplate(imgVG, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    location = max_loc
    bottomRightLocation = (location[0] + w, location[1] + h)
    center = (location[0] + w/2, location[1] + h/2)
    print(center)
    cv.rectangle(imgVG, location, bottomRightLocation, 255, 5)

    cv.imshow('Video Frame', imgVG)
    if cv.waitKey(1) == ord('q'):
        break
cv.destroyAllWindows()