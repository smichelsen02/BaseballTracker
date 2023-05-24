import sys
import cv2 as cv
import numpy as np
import time

def findDepth(circleRight, circleLeft, frameR, frameL, baseline, f, alpha):
    heightR, widthR, depthR = frameR.shape
    heightL, widthL, depthL = frameL.shape

    if widthR == widthL:
        fPixel = (widthR * 0.5) / np.tan(alpha * np.pi / 180)

    else:
        print("Left and Right frames do not have the same pixel width")

    xRight = circleRight[0]
    xLeft = circleLeft[0]

    disparity = xLeft - xRight

    zDepth = (baseline * fPixel) / disparity

    return abs(zDepth)