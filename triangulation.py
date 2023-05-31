import sys
import cv2 as cv
import numpy as np
import time

def findDepth(circleRight, circleLeft, frameR, frameL, baseline, Fx, Fy, Ox, Oy, alpha):
    heightR, widthR, depthR = frameR.shape
    heightL, widthL, depthL = frameL.shape

    if widthR == widthL:
        fPixel = (widthR * 0.5) / np.tan(alpha * np.pi / 180)

    else:
        print("Left and Right frames do not have the same pixel width")

    xRight = circleRight[0]
    xLeft = circleLeft[0]
    yRight = circleRight[1]
    yLeft = circleLeft[1]
    #Disparity in pixels, cancels out with pixels in focal lengths
    xDisparity = xLeft - xRight


    zDepth = (baseline * Fx) / xDisparity
    xLocation = (baseline * (xLeft - Ox )) / (xDisparity)
    yLocation = (baseline * Fx * (yLeft - Oy)) / (Fy * (xDisparity))


    return abs(zDepth) , xLocation, yLocation