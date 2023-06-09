# import the necessary packages and files
from imutils import paths
import numpy as np
import imutils
import cv2 as cv
import CircleFinder
import triangulation as tri
import copy
import cvzone



#initial storage lists
xList = []
yList = []
zList = []
frameList = []
csvRowList = []
csvRowList.append(['Frame', 'X Position', 'Y Position', 'Z position', 'Disparity', 'Center Left X', 'Center Left Y',
                   'Center Right X', 'Center Right X'])

#create correction matrices from calibration step
cv_file = cv.FileStorage()
cv_file.open('stereoMap.xml', cv.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()
#pull each frame for each camera from an mp4

capR = cv.VideoCapture('images/videos/trial3_C001H001S0001.mp4')
capL = cv.VideoCapture('images/videos/trial3_C002H001S0001.mp4')
count = 0
while capR.isOpened() and capL.isOpened():
    count +=1
    retR, frameR = capR.read()
    retL, frameL = capL.read()
    # if frame is read correctly ret is True
    if not retL or not retR:
        print("Can't receive frame. Exiting ...")
        break
    template = cv.resize(cv.imread('images/Templates/ScaleTestTemplate.png', 0), (0,0),fx = (87/42), fy = (87/42))
    scaleFactor = 87/42
#applies calibration values to correct views
    frame_Right = cv.remap(frameR, stereoMapR_x, stereoMapR_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    frame_Left = cv.remap(frameL, stereoMapL_x, stereoMapL_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
    # frame_Right = frameR
    # frame_Left = frameL

#displays each actual corrected frame
    #note it is showing the uncorrected frames due to the calibration issues caused by the paper being loose





    #calculate depth
    #defines needed knowns
    knownWidth = 6 #units are mm currently
    alpha = 46 #field of view in degrees
    baseline = 107.95 #mm
    #get and store left intrinsics
    cv_file = cv.FileStorage()
    cv_file.open('intrinsics.xml', cv.FileStorage_READ)
    leftIntrinsics = cv_file.getNode('Left_Intrinsics').mat()
    focalxLengthLeft = leftIntrinsics[0,0]
    focalyLengthLeft = leftIntrinsics[1,1]
    OxLeft = leftIntrinsics[0,2]
    OyLeft = leftIntrinsics[1,2]
    print('oxLeft' + str(OxLeft))
    print('oyLeft' + str(OyLeft))

    #run find depth function
    # if np.all(circleRight) == None or np.all(circleLeft) == None:
    #     print("Tracking lost")
    #
    # else:
    #     depth , xLocation, yLocation= tri.findDepth(circleRight, circleLeft, frameR, frameL, baseline, focalxLengthLeft, focalyLengthLeft,OxLeft, OyLeft, alpha)
    #     print("Depth: " + str(depth))

    methods = [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR,
               cv.TM_CCORR_NORMED, cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]
    print(count)
    h, w = template.shape
    print(h, w)
    scaleFactor = 1-((1-(35/87))/1361)*(count-1)
    template = cv.resize(template, (0,0), fx = scaleFactor, fy = scaleFactor)
    h, w = template.shape
    print(h, w)
    imgL = cv.cvtColor(frame_Left, cv.COLOR_BGR2GRAY)
    imgR = cv.cvtColor(frame_Right, cv.COLOR_BGR2GRAY)

    method = methods[3]

    #run template matching
    resultL = cv.matchTemplate(imgL, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(resultL)
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        locationL = min_loc
    else:
        locationL = max_loc

    centerL = (locationL[0] + w/2, locationL[1] + h/2)
    bottomCornerL = (locationL[0] + w, locationL[1] + h)

    resultR = cv.matchTemplate(imgR, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(resultR)
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        locationR = min_loc
    else:
        locationR = max_loc
    centerR = (locationR[0] + w/2, locationR[1] + h/2)
    bottomCornerR = (locationR[0] + w, locationR[1] + h)

    cv.rectangle(frame_Left, locationL, bottomCornerL, 255, 5)
    cv.rectangle(frame_Right, locationR, bottomCornerR, 255, 5)
    cv.circle(frame_Left, (round(centerL[0]), round(centerL[1])), 5, (222,222,0), -1)
    cv.circle(frame_Right, (round(centerR[0]), round(centerR[1])), 5, (222,222,0), -1)
    cv.putText(frame_Left, str(count), (75,50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
    xDisparity = centerL[0] - centerR[0]


    zDepth = (baseline * focalxLengthLeft) / xDisparity
    xLocation = (baseline * (centerL[0] - OxLeft )) / (xDisparity)
    yLocation = (baseline * focalxLengthLeft * (centerL[1] - OyLeft)) / (focalyLengthLeft * (xDisparity))

#Add depth, x, y, and frame number to lists
    row = []
    row.append(count)
    row.append(abs(xLocation))
    row.append(abs(yLocation))
    row.append(abs(zDepth))
    row.append(xDisparity)
    row.append(centerL[0])
    row.append(centerL[1])
    row.append(centerR[0])
    row.append(centerR[1])
    csvRowList.append(row)

    imgStack = cvzone.stackImages([frame_Left,frame_Right, frameL, frameR],2,0.5)
    cv.imshow('Left', imgStack)

    if cv.waitKey(1) == ord('q'):
        break

#end of loop and final code bits before end of program


np.savetxt("PositionData.csv", csvRowList, delimiter =", ", fmt ='% s')



capR.release()
capL.release()
cv.destroyAllWindows()
print(count)