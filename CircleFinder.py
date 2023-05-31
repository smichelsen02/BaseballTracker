import sys
import cv2 as cv
import numpy
import time
import imutils

def findCircle(frame, mask, count):
    contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    #check that contour was found
    if len(contours) > 0:
        #pick largest contour to avoid catching noise
        c = max(contours, key=cv.contourArea)
        ((x,y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #Proceed if radius is greater than specified value. can be used to break between camera sets
        #10 is arbitrary for now, value will need to be determined from testing
        if radius > 10:
            #draw circle and centroid on frame
            cv.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv.circle(frame, center, 5, (0,0,0), -1)
        else:
            print("No object found on frame " + str(count))

    return center
