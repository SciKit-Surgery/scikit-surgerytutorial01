#! /usr/bin/python3.6
# coding=utf-8

"""Now we try and implement Aruco tag tracking in the library"""
import sys
import cv2
import numpy
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import *
from ardavin.ui.VTKRenderer import get_VTK_data
from ardavin.ui.Viewers import MonoViewer

#A new import statement to get access to the VTKRender's image update
from ardavin.ui.VTKRenderer import UI, VTKOverlayWindow

class MyVTKOverlayWindow (VTKOverlayWindow):
    """Same as ardavin.ui.VTKRenderer.VTKOverlayWindow, but we overwrite
    get_next_frame, with our own function to do tag exraction."""
    def get_next_frame(self):
        #It's good practice to call the parent's overwritten function 
        # if possible.
        super(MyVTKOverlayWindow, self).get_next_frame()
        self.aruco_detect()

    def aruco_detect(self):
        """Detect any aruco tags present."""
        #hard code the tag variety for simplicity
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
        #detect
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(self.img, dictionary)
        #hard code the camera calibration for now. This should really load any camera 
        #parameters from the class
        camera_matrix = numpy.zeros((3,3), numpy.float32)
        camera_matrix[0][0] = 560.0
        camera_matrix[1][1] = 560.0
        camera_matrix[0][2] = 320.0
        camera_matrix[1][2] = 240.0
        camera_matrix[2][2] = 1.0
        distortion = numpy.zeros((1,4),numpy.float32)
        marker_size = 15 ## mm same units as camera calibration

        if len(marker_corners) > 0:
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, 15.0, camera_matrix, distortion)
            #do some drawing
            cv2.aruco.drawDetectedMarkers(self.img, marker_corners)# marker_ids)
            cv2.aruco.drawAxis(self.img, camera_matrix, distortion, rvecs, tvecs, 15.0)

            camera = self.get_model_camera()
            print (camera.GetPosition())
            
            #move the actors onto the tag.
            for actor in self.foreground_renderer.GetActors():
                actor.SetPosition(camera.GetPosition() - tvecs[0][0])
                print (actor.GetPosition())


class MyUI (UI):
    """Same as ardavin.ui.VTKRenderer.VTKOverlayWindow, but we overwrite
    add_vtk_overlay_window, to tell it to use our MyVTKOverlayWindow"""

    def add_vtk_overlay_window(self, video_source):
        """ Create a new VTKOverlayWindow and add it to widget list"""
        self.interactor_layout = QHBoxLayout()
        self.VTK_interactor = MyVTKOverlayWindow(video_source)
        #self.VTK_interactor.resize(300, 300)
        self.VTK_interactor.setFixedSize(self.width(), self.height())

        self.interactor_layout.addWidget(self.VTK_interactor, 0)
        self.layout.addLayout(self.interactor_layout)

        self.VTK_interactor.set_stereo_right()

        self.VTK_interactor.Initialize()
        self.VTK_interactor.Start()

class MyMonoViewer ( MonoViewer ):
    """Same as ardavin.ui.Viewers.VTKOverlayWindow, but we overwrite
    __init, to tell it to use our MyUI"""
    def __init__(self,video_source):
        self.UI = MyUI(video_source)
        self.UI.exit_signal.connect(self.run_before_quit)
    #here we could modify our own mono viewer
    pass


app = QApplication([])

#you can set the video source, 0 for the first webcam you find.
video_source=0
vtk_models = get_VTK_data('models')

viewer = MyMonoViewer(0)

viewer.add_VTK_models(vtk_models)

camera_file=False
if camera_file:
    viewer.load_camera_view(camera_file)
viewer.start()

sys.exit(app.exec_())
    
