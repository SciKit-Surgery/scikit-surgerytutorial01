# coding=utf-8

"""Script to create a viewer window with a static surface
model overlaid in a live video feed"""

import sys
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseWidget

#create an OverlayApp class, that inherits from OverlayBaseApp
class OverlayApp(OverlayBaseWidget):
    """Inherits from OverlayBaseApp, and adds a minimal
    implementation of update. """
    def update_view(self):
        """Update the background renderer with a new frame,
        and render"""
        _, image = self.video_source.read()
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

#the following line prevents the code below from running unless
#this file is executed. It enables us to import this file for
#unit testing
if __name__ == '__main__':
    #first we create an application
    app = QApplication([])

    #then an instance of OverlayApp. The video source
    #is set when we create the instance. This is an index
    #starting at 0. If you have more than one webcam, you can
    #try using different numbered sources
    video_source = 0
    viewer = OverlayApp(video_source)

    #Set a model directory containing the models you wish
    #to render and optionally a colours.txt defining the
    #colours to render in.
    model_dir = '../models'
    viewer.add_vtk_models_from_dir(model_dir)

    #start the viewer
    viewer.show()
    viewer.start()

    #start the application
    sys.exit(app.exec_())
