import numpy as np
import cv2 as cv
from matplotlib import pyplot as py
def cameras():
    #define camera inputs, index starts at 0 not 1
    cap1 = cv.VideoCapture(0)
    cap2 = cv.VideoCapture(1)
    # cap3 = cv.VideoCapture(2)
    # cap4 = cv.VideoCapture(3)
    # cap5 = cv.VideoCapture(4)
    # cap6 = cv.VideoCapture(5)


    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')


    #output files are named here and the file type is defined
    #first is file name, then the videoWriter object, then framerate, then capture size
    #once framerate is determined update it for each camera
    out1 = cv.VideoWriter('output1.mp4v', fourcc, 20.0, (640,  480))
    out2 = cv.VideoWriter('output2.mp4v', fourcc, 20.0, (640,  480))
    # out3 = cv.VideoWriter('output3.mp4', fourcc, 20.0, (640,  480))
    # out4 = cv.VideoWriter('output4.mp4', fourcc, 20.0, (640,  480))
    # out5 = cv.VideoWriter('output5.mp4', fourcc, 20.0, (640,  480))
    # out6 = cv.VideoWriter('output6.mp4', fourcc, 20.0, (640,  480))


    #loop to run capture until key break is triggered
    while cap1.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        # ret3, frame3 = cap3.read()
        # ret4, frame4 = cap4.read()
        # ret5, frame5 = cap5.read()
        # ret6, frame6 = cap6.read()


        if not ret1:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if not ret2:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        #the number here defines how the frame is flipped. 1 flips along vertical, 0 along x, -1 flips along both
        frame1 = cv.flip(frame1, 1)
        frame2 = cv.flip(frame2, 1)
        # frame3 = cv.flip(frame3, 1)
        # frame4 = cv.flip(frame4, 1)
        # frame5 = cv.flip(frame5, 1)
        # frame6 = cv.flip(frame6, 1)

        #Gray scale each frame for each input. if already gray scaled by camera, comment this out
        frame1g = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        frame2g = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        # frame3g = cv.cvtColor(frame3, cv.COLOR_BGR2GRAY)
        # frame4g = cv.cvtColor(frame4, cv.COLOR_BGR2GRAY)
        # frame5g = cv.cvtColor(frame5, cv.COLOR_BGR2GRAY)
        # frame6g = cv.cvtColor(frame6, cv.COLOR_BGR2GRAY)

        #write frames to the outputs. Note i could write either the grayscale or the color here
        out1.write(frame1g)
        out2.write(frame2g)
        # out3.write(frame3g)
        # out4.write(frame4g)
        # out5.write(frame5g)
        # out6.write(frame6g)

        #display frames while capturing
        #only show one to confirm that capture is happening while limiting processing
        cv.imshow('frame', frame1g)


        #break statement based off keyboard input
        #currently bound to escape
        #i will need to figure out how to automatically end video capture
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    #release captures and outputs when video cap is finished
    cap1.release()
    cap2.release()
    out1.release()
    out2.release()
    cv.destroyAllWindows()



cameras()

