#! /usr/bin/python3.6

"""This is a script that uses only opencv functions in python 
to track Aruco markers in a live webcam image."""

import numpy 
import cv2

cap = cv2.VideoCapture(0)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(frame, dictionary)
    if len(marker_corners) > 0:
        cv2.aruco.drawDetectedMarkers(frame, marker_corners)# marker_ids)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
