#! /usr/bin/python3.6
# coding=utf-8
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
        self.vtk_overlay_window._RenderWindow.Render()
            
        #move the actors onto the tag.
        for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
            orientation=actor.GetOrientation()
            orientation = [orientation[0] , orientation[1], orientation[2] + 0.5]
            actor.SetOrientation(orientation)
            
           # tvecs[0][0][0] = -tvecs[0][0][0]
           # actor.SetPosition(camera.GetPosition() - tvecs[0][0])
           # print (actor.GetPosition())


app = QApplication([])

#you can set the video source, 0 for the first webcam you find.
video_source=0
viewer = ArucoApp(video_source)

model_dir = 'models'
viewer.add_vtk_models_from_dir(model_dir)

viewer.start()

sys.exit(app.exec_())
    
