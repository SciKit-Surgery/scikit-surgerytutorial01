# coding=utf-8

"""Script to create a viewer window with a movable surface
model overlaid in a live video feed"""

import sys
#add an import for opencv, so we can use its aruco functions
import cv2.aruco as aruco
#add an import for numpy, to manipulate arrays
import numpy
from PySide2.QtWidgets import QApplication
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy
from sksurgeryarucotracker.arucotracker import ArUcoTracker

class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, image_source):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        #the aruco tag dictionary to use. DICT_4X4_50 will work with the tag in
        #../tags/aruco_4by4_0.pdf

        #we'll use opencv to estimate the pose of the visible aruco tags.
        #for that we need a calibrated camera. For now let's just use a
        #a hard coded estimate. Maybe you could improve on this.

        ar_config={
                "tracker type": "aruco",
                "video source": 'none',
                "debug": False,
                "dictionary" : 'DICT_4X4_50',
                "marker size": 50,
                "camera projection": numpy.array([[560.0, 0.0, 320.0],
                                                  [0.0, 560.0, 240.0],
                                                  [0.0, 0.0, 1.0]],
                                                  dtype=numpy.float32),
                "camera distortion": numpy.zeros((1, 4), numpy.float32)

                  }

        #and call the constructor for the base class
        if sys.version_info > (3, 0):
            super().__init__(image_source)
        else:
            #super doesn't work the same in py2.7
            OverlayBaseApp.__init__(self, image_source)
        
        self.tracker = ArUcoTracker(ar_config)
        self.tracker.start_tracking()

    def update(self):
        """Update the background render with a new frame and
        scan for aruco tags"""
        _, image = self.video_source.read()
        self._aruco_detect_and_follow(image)

        #Without the next line the model does not show as the clipping range
        #does not change to accommodate model motion. Uncomment it to
        #see what happens.
        self.vtk_overlay_window.set_camera_state({"ClippingRange": [10, 800]})
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

    def _aruco_detect_and_follow(self, image):
        """Detect any aruco tags present using sksurgeryarucotracker
        """
        
        port_handles, _, _, tag2camera, _ = self.tracker.get_frame(image)
        if tag2camera is not None:
            self._move_model(tag2camera[0])


    def _move_model(self, tag2camera):
        """Internal method to move the rendered models in
        some interesting way"""

        #because the camera won't normally be at the origin,
        #we need to find it and make movement relative to it
        transform_manager = TransformManager()
        camera_vtk = self.vtk_overlay_window.get_foreground_camera().GetModelViewTransformMatrix()
       
        camera2world = numpy.eye(4, dtype = numpy.float64)
        camera_vtk.DeepCopy(camera2world.ravel(), camera_vtk)
        transform_manager.add("camera2world", camera2world)
        transform_manager.add("camera2tag", tag2camera)
        tag2world = transform_manager.get("tag2world")
        #Iterate through the rendered models
        for actor in \
                self.vtk_overlay_window.get_foreground_renderer().GetActors():
            #opencv and vtk seem to have different x-axis, flip the x-axis
            actor.SetUserMatrix(create_vtk_matrix_from_numpy(tag2world))
            #translation[0] = -translation[0]

            #set the position, relative to the camera
            #actor.SetPosition(camera.GetPosition() - translation)

            #rvecs are in radians, VTK in degrees.
            #rotation = 180 * rotation/3.14

            #for orientation, opencv axes don't line up with VTK,
            #uncomment the next line for some interesting results.
            #actor.SetOrientation( rotation)

if __name__ == '__main__':
    app = QApplication([])

    video_source = 0
    viewer = OverlayApp(video_source)

    model_dir = '../models'
    viewer.add_vtk_models_from_dir(model_dir)

    viewer.start()

    sys.exit(app.exec_())
