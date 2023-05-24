import numpy as np
import cv2 as cv
from matplotlib import pyplot as py


def backgroundMask(captureName):
    #team
    print("into background masking")
    backSub = cv.createBackgroundSubtractorMOG2()
    capture = cv.VideoCapture((str(captureName)))
    if not capture.isOpened():
        print('Unable to open: ' + str(captureName))
        exit(0)
    while True:
        print('while loop')
        ret, frame = capture.read()
        if frame is None:
            break

        fgMask = backSub.apply(frame)

        cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
        cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)

        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break

backgroundMask('output1.mp4v')