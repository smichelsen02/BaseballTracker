# import the necessary packages and files
from imutils import paths
import numpy as np
import imutils
import cv2 as cv
import CircleFinder
import triangulation as tri


#create correction matrices from calibration step
cv_file = cv.FileStorage()
cv_file.open('stereoMap.xml', cv.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()
#pull each frame for each camera from an mp4

capR = cv.VideoCapture('images/videos/tests_S0001.mp4')
capL = cv.VideoCapture('images/videos/tests_S0002.mp4')
count = 0
while capR.isOpened() and capL.isOpened():
    count +=1
    retR, frameR = capR.read()
    retL, frameL = capL.read()
    # if frame is read correctly ret is True
    if not retL or not retR:
        print("Can't receive frame. Exiting ...")
        break

#applies calibration values to correct views
    frameRCorrected = cv.remap(frameR, stereoMapR_x, stereoMapR_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    frameLCorrected = cv.remap(frameL, stereoMapL_x, stereoMapL_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)


#displays each actual corrected frame
    cv.imshow('Left', frameL)
    cv.imshow('Right', frameR)


#mask frames for white of the ball
    #The values here are the RGB value for white. a snapshot of a frame can be used with an
    #online color selector to adjust these values as needed
    upperMaskLimit = np.array([255,255,255])
    lowerMaskLimit = np.array([200,200,200])
    maskR = cv.inRange(frameRCorrected, lowerMaskLimit, upperMaskLimit)
    maskL = cv.inRange(frameLCorrected, lowerMaskLimit, upperMaskLimit)


#find circular contour of ball in each frame
    # #right contours
    # circleRight = CircleFinder.findCircle(frameRCorrected, maskR, count)
    # #left contours
    # circleLeft = CircleFinder.findCircle(frameLCorrected, maskL, count)


#run the find depth on the contours of ball

    #I need to figure out the color issues to be able to adress this part. there is not a way i know of to isolate
    #for a circular contour, just largest or smallest. Currently, the ball is neither of those. if i can isolate
    #the ball by itself in the mask, then that solves the issue entirely.


    # #calculate depth
    # #defines needed knowns
    # knownWidth = 6 #units are mm currently
    # alpha = 46 #field of view in degrees
    # baseline = 12.7 #cm
    # #get right and left camera focal lengths from xml files
    # cv_file = cv.FileStorage()
    # cv_file.open('intrinsics.xml', cv.FileStorage_READ)
    # rightIntrinsics = cv_file.getNode('Right_Intrinsics').mat()
    # focalLengthRight = rightIntrinsics[0,0]
    # leftIntrinsics = cv_file.getNode('Left_Intrinsics').mat()
    # focalLengthLeft = leftIntrinsics[0,0]


    # #run find depth function
    # if np.all(circleRight) == None or np.all(circleLeft) == None:
    #     print("Tracking lost")
    #
    # else:
    #     depth = tri.findDepth(circleRight, circleLeft, frameR, frameL, baseline, focalLengthRight, alpha)
    #     print("Depth: " + str(depth))

#display depth, x and y of center in a print

#add them to the list then export as a csv
    xList = []
    yList = []
    zList = []

    cv.imshow('maskR', maskR)
    cv.imshow('maskL', maskL)
capR.release()
capL.release()
cv.destroyAllWindows()
print(count)