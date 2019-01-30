#! /usr/bin/python3.6
# coding=utf-8
import cv2
import sys
import numpy as np
from PySide2.QtWidgets import QWidget, QApplication
from sksurgeryvtk.widgets.OverlayBaseApp import OverlayBaseApp

class ArucoApp(OverlayBaseApp):

    def __init__(self, video_source):
        super().__init__(video_source)

    def update(self):
        """Update the background render with a new frame and
        scan for aruco tags"""
        #pylint: disable=attribute-defined-outside-init

        ret, self.img = self.video_source.read()
        self.vtk_overlay_window.set_video_image(self.img)
        self.aruco_detect()
        self.vtk_overlay_window._RenderWindow.Render()

    def aruco_detect(self):
        """Detect any aruco tags present."""
        #hard code the tag variety for simplicity
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        #detect
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(self.img, dictionary)
        #hard code the camera calibration for now. This should really load any camera 
        #parameters from the class
        camera_matrix = np.zeros((3,3), np.float32)
        camera_matrix[0][0] = 560.0
        camera_matrix[1][1] = 560.0
        camera_matrix[0][2] = 320.0
        camera_matrix[1][2] = 240.0
        camera_matrix[2][2] = 1.0
        distortion = np.zeros((1,4),np.float32)
        marker_size = 50 ## mm same units as camera calibration

        if len(marker_corners) > 0:
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, marker_size, camera_matrix, distortion)
            #do some drawing
            cv2.aruco.drawDetectedMarkers(self.img, marker_corners)# marker_ids)
            cv2.aruco.drawAxis(self.img, camera_matrix, distortion, rvecs, tvecs, 15.0)

            camera = self.vtk_overlay_window.get_foreground_camera()
            self.vtk_overlay_window.set_camera_state({"ClippingRange": [10,400]})
            #print (camera.GetPosition())
            
            #move the actors onto the tag.
            for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
                tvecs[0][0][0] = -tvecs[0][0][0]

                actor.SetPosition(camera.GetPosition() - tvecs[0][0])
                
                #for orientation, opencv axes don't line up with VTK, and 
                #rvecs are in radians, VTK in degrees
                #rvecs[0][0] = 180 * rvecs[0][0]/3.14
                #actor.SetOrientation( rvecs[0][0])
                print (actor.GetPosition(), actor.GetOrientation())


app = QApplication([])

#you can set the video source, 0 for the first webcam you find.
video_source=0
viewer = ArucoApp(video_source)

model_dir = 'models'
viewer.add_vtk_models_from_dir(model_dir)

viewer.start()

sys.exit(app.exec_())
    
