#! /usr/bin/python3.6
# coding=utf-8
import sys
#add an import for opencv, so we can use its aruco functions
import cv2
#add an import for numpy, to manipulate arrays
import numpy
from PySide2.QtWidgets import QApplication
from sksurgeryvtk.widgets.OverlayBaseApp import OverlayBaseApp

class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, video_source):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        #the aruco tag dictionary to use. DICT_4X4_50 will work with the tag in
        #../tags/aruco_4by4_0.pdf
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        # The size of the aruco tag in mm
        self.marker_size = 50

        #we'll use opencv to estimate the pose of the visible aruco tags.
        #for that we need a calibrated camera. For now let's just use a
        #a hard coded estimate. Maybe you could improve on this.
        self.camera_projection_matrix = numpy.array([[560.0 , 0.0 , 320.0],
                                                      [0.0, 560.0 , 240.0],
                                                      [0.0, 0.0, 1.0]])
        self.camera_distortion = numpy.zeros((1,4),numpy.float32)

        #and call the constructor for the base class
        if (sys.version_info > (3, 0)):
            super().__init__(video_source)
        else:
            #super doesn't work the same in py2.7
            OverlayBaseApp.__init__(self,video_source)

    def update(self):
        """Update the background render with a new frame and
        scan for aruco tags"""

        ret, self.img = self.video_source.read()
        self._aruco_detect_and_follow()

        #Without the next line the model does not show as the clipping range
        #does not change to accommodate model motion. Uncomment it to
        #see what happens.
        self.vtk_overlay_window.set_camera_state({"ClippingRange": [10,800]})
        self.vtk_overlay_window.set_video_image(self.img)
        self.vtk_overlay_window._RenderWindow.Render()

    def _aruco_detect_and_follow(self):
        """Detect any aruco tags present. Based on;
        https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
        """
        #detect any markers
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(self.img, self.dictionary)

        if len(marker_corners) > 0:
            #if any markers found, try and determine their pose
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners,
                    self.marker_size, self.camera_projection_matrix, self.camera_distortion)

            self._move_model(rvecs[0][0], tvecs[0][0])


    def _move_model(self, rotation, translation):
        """Internal method to move the rendered models in
        some interesting way"""

        #because the camera won't normally be at the origin,
        #we need to find it and make movement relative to it
        camera=self.vtk_overlay_window.get_foreground_camera()

        #Iterate through the rendered models
        for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
             #opencv and vtk seem to have different x-axis, flip the x-axis
             translation[0] = -translation[0]

             #set the position, relative to the camera
             actor.SetPosition(camera.GetPosition() - translation)

             #for orientation, opencv axes don't line up with VTK, and
             #rvecs are in radians, VTK in degrees.
             #uncomment the next two lines for some interesting results.
             #rotation = 180 * rotation/3.14
             #actor.SetOrientation( rotation)


app = QApplication([])

video_source=0
viewer = OverlayApp(video_source)

model_dir = '../models'
viewer.add_vtk_models_from_dir(model_dir)

viewer.start()

sys.exit(app.exec_())

