.. highlight:: shell

.. _SimpleOverlayApp:

===============================================
Adding some model motion to overlay
===============================================

For image guided interventions we typically need some control over
the position of model elements. Here we add a few lines of code to
our update function to make the overlaid model move. You should end up 
with something like this ...

.. figure:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/raw/7-screenshots/doc/vtk_overlay_with_movement_example.gif


01 - Add some movement to the models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a copy of vtkoverlay_app.py and call it
vtkoverlay_with_movement_app.py or similar.

Edit the update method for the OverlayApp class, to call a new
method called _move_model.

.. code-block:: python
   :emphasize-lines: 4,5

   def update(self):
        _, image = self.video_source.read()
        
        #add a method to move the rendered models
        self._move_model()

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()


Then add a new method called _move_model to the class.

.. code-block:: python

   def _move_model(self):
        #Iterate through the rendered models
        for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
            #get the current orientation
            orientation = actor.GetOrientation()
            #increase the rotation around the z-axis by 1.0 degrees
            orientation = [orientation[0] , orientation[1], orientation[2] + 1.0]
            #add update the model's orientation
            actor.SetOrientation(orientation)


Leave the rest of the file as is, and try running the application with

::

  python vtkoverlay_with_movement_app.py

or similar. If successful you should see a live video stream overlaid with
a rendered surface model. The surface model should slowly rotate, like in the 
video at the top of the page. Congratulations.
Note that you can still use the VTK interactor to move the camera around or change the
model representation. Have a play around and see how it interacts with the model rotation.

You can download a
`finished example`_ and compare.
Play around with it, experiment with different ways to move the model or
to change the opacity etc.

Next we will add some code to detect an ArUco marker and "pin" the model to it

.. _`scikit-surgeryutils`: https://pypi.org/project/scikit-surgeryutils
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`OverlayBaseApp` : https://scikit-surgeryutils.readthedocs.io/en/latest/sksurgeryutils.common_overlay_apps.html#module-sksurgeryutils.common_overlay_apps.OverlayBaseApp
.. _`finished example` : https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/blob/master/snappytutorial01/vtkoverlay_with_movement_app.py
