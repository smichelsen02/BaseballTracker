# import the necessary packages and files
from imutils import paths
import numpy as np
import imutils
import cv2 as cv
import CircleFinder
import triangulation as tri
import copy


#initial storage lists
xList = []
yList = []
zList = []
frameList = []
csvRowList = []
csvRowList.append(['Frame', 'X Position', 'Y Position', 'Z position'])

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
    frame_Right = cv.remap(frameR, stereoMapR_x, stereoMapR_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    frame_Left = cv.remap(frameL, stereoMapL_x, stereoMapL_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)


#displays each actual corrected frame
    #note it is showing the uncorrected frames due to the calibration issues caused by the paper being loose
    cv.imshow('Left', frameL)
    cv.imshow('Right', frameR)


#mask frames for white of the ball
    #The values here are the RGB value for white. a snapshot of a frame can be used with an
    #online color selector to adjust these values as needed
    upperMaskLimit = np.array([255,255,255])
    lowerMaskLimit = np.array([200,200,200])
    maskR = cv.inRange(frameR, lowerMaskLimit, upperMaskLimit)
    maskL = cv.inRange(copy.copy(frameL), lowerMaskLimit, upperMaskLimit)
    cv.imwrite('images/maskImages/frameL' + str(count) + '.png', frameL)

#find circular contour of ball in each frame
    #right contours
    circleRight = CircleFinder.findCircle(frameR, maskR, count)
    #left contours
    circleLeft = CircleFinder.findCircle(frameL, maskL, count)


#run the find depth on the contours of ball

    #I need to figure out the color issues to be able to adress this part. there is not a way i know of to isolate
    #for a circular contour, just largest or smallest. Currently, the ball is neither of those. if i can isolate
    #the ball by itself in the mask, then that solves the issue entirely.


    #calculate depth
    #defines needed knowns
    knownWidth = 6 #units are mm currently
    alpha = 46 #field of view in degrees
    baseline = 12.7 #cm
    #get and store left intrinsics
    cv_file = cv.FileStorage()
    cv_file.open('intrinsics.xml', cv.FileStorage_READ)
    leftIntrinsics = cv_file.getNode('Left_Intrinsics').mat()
    focalxLengthLeft = leftIntrinsics[0,0]
    focalyLengthLeft = leftIntrinsics[1,1]
    OxLeft = leftIntrinsics[2,0]
    OyLeft = leftIntrinsics[2,1]


    #run find depth function
    if np.all(circleRight) == None or np.all(circleLeft) == None:
        print("Tracking lost")

    else:
        depth , xLocation, yLocation= tri.findDepth(circleRight, circleLeft, frameR, frameL, baseline, focalxLengthLeft, focalyLengthLeft,OxLeft, OyLeft, alpha)
        print("Depth: " + str(depth))

#Add depth, x, y, and frame number to lists
    row = []
    row.append(count)
    row.append(xLocation)
    row.append(yLocation)
    row.append(depth)
    csvRowList.append(row)


    cv.imshow('maskR', maskR)
    cv.imshow('maskL', maskL)
    if cv.waitKey(1) == ord('q'):
        break

#end of loop and final code bits before end of program
print(zList)

np.savetxt("PositionData.csv", csvRowList, delimiter =", ", fmt ='% s')



capR.release()
capL.release()
cv.destroyAllWindows()
print(count)