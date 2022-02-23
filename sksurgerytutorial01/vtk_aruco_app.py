# coding=utf-8

"""Script to create a viewer window with a movable surface
model overlaid in a live video feed"""

import sys
#add an import for numpy, to manipulate arrays
import numpy
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryarucotracker.arucotracker import ArUcoTracker

class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, image_source):
        """override the default constructor to set up sksurgeryarucotracker"""

        #we'll use SciKit-SurgeryArUcoTracker to estimate the pose of the
        #visible ArUco tag relative to the camera. We use a dictionary to
        #configure SciKit-SurgeryArUcoTracker

        ar_config = {
            "tracker type": "aruco",
            #Set to none, to share video source with OverlayBaseApp
            "video source": 'none',
            "debug": False,
            #the aruco tag dictionary to use. DICT_4X4_50 will work with
            #../tags/aruco_4by4_0.pdf
            "aruco dictionary" : 'DICT_4X4_50',
            "marker size": 50, # in mm
            #We need a calibrated camera. For now let's just use a
            #a hard coded estimate. Maybe you could improve on this.
            "camera projection": numpy.array([[560.0, 0.0, 320.0],
                                              [0.0, 560.0, 240.0],
                                              [0.0, 0.0, 1.0]],
                                             dtype=numpy.float32),
            "camera distortion": numpy.zeros((1, 4), numpy.float32)
            }
        self.tracker = ArUcoTracker(ar_config)
        self.tracker.start_tracking()

        #and call the constructor for the base class
        if sys.version_info > (3, 0):
            super().__init__(image_source)
        else:
            #super doesn't work the same in py2.7
            OverlayBaseApp.__init__(self, image_source)

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

        #tracker.get_frame(image) returns 5 lists of tracking data.
        #we'll only use the tracking matrices (tag2camera)
        _port_handles, _timestamps, _frame_numbers, tag2camera, \
                        _tracking_quality = self.tracker.get_frame(image)

        #If no tags are detected tag2camera will be an empty list, which
        #Python interprets as False
        if tag2camera:
            #pass the first entry in tag2camera. If you have more than one tag
            #visible, you may need to do something cleverer here.
            self._move_camera(tag2camera[0])

    def _move_camera(self, tag2camera):
        """Internal method to move the rendered models in
        some interesting way"""

        #SciKit-SurgeryCore has a useful TransformManager that makes
        #chaining together and inverting transforms more intuitive.
        #We'll just use it to invert a matrix here.
        transform_manager = TransformManager()
        transform_manager.add("tag2camera", tag2camera)
        camera2tag = transform_manager.get("camera2tag")

        #Let's move the camera, rather than the model this time.
        self.vtk_overlay_window.set_camera_pose(camera2tag)

if __name__ == '__main__':
    app = QApplication([])

    video_source = 0
    viewer = OverlayApp(video_source)

    model_dir = '../models'
    viewer.add_vtk_models_from_dir(model_dir)

    viewer.start()

    sys.exit(app.exec_())
