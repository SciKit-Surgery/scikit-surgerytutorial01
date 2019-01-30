#! /usr/bin/python3.6
# coding=utf-8
import sys
from PySide2.QtWidgets import QApplication
from sksurgeryvtk.widgets.OverlayBaseApp import OverlayBaseApp

class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds a minimal
    implementation of update. """

    def update(self):
        """Update the background renderer with a new frame,
        move the model and render"""
        ret, self.img = self.video_source.read()

        #add a method to move the rendered models
        self._move_model()

        self.vtk_overlay_window.set_video_image(self.img)
        self.vtk_overlay_window._RenderWindow.Render()

    def _move_model(self):
        """Internal method to move the rendered models in
        some interesting way"""
        #Iterate through the rendered models
        for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
            #get the current orientation
            orientation=actor.GetOrientation()
            #increase the rotation around the z-axis by 1.0 degrees
            orientation = [orientation[0] , orientation[1], orientation[2] + 1.0]
            #add update the model's orientation
            actor.SetOrientation(orientation)


app = QApplication([])

video_source=0
viewer = OverlayApp(video_source)

model_dir = '../models'
viewer.add_vtk_models_from_dir(model_dir)

viewer.start()

sys.exit(app.exec_())

