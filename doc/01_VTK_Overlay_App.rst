.. highlight:: shell

.. _SimpleOverlayApp:

===============================================
Making a simple model overlay application
===============================================

Making an augmented reality application can be complicated. The developer
requires an application framework to handle display, threading and user interface, something
to provide video streaming, and finally a model renderer. The SNAPPY package
`scikit-surgeryutils`_ simplifies the process by integrating QT (`PySide2`_),
`OpenCV`_, and `VTK`_ into a simple to use library.

00 - Simple overlay application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Using your favourite text editor or Python development environment,
create a new file called vtkoverlay_app.py or similar.

Start with some import statements

::

  import sys
  from PySide2.QtWidgets import QApplication
  from sksurgeryutils.common_overlay_apps import OverlayBaseApp

scikit-surgery provides an `OverlayBaseApp`_ module that creates a qtwidget showing
a live stream from a video source, overlaid with a rendered surface model.
scikit-surgery leaves the update method unimplemented so that the user
can implement their own version in an child class.

::

  #create an OverlayApp class, that inherits from OverlayBaseApp
  class OverlayApp(OverlayBaseApp):

and implement a minimal update method

::

    def update(self):

        #read a new image from the video source
        _, image = self.video_source.read()

        #copy the image to the overlay window
        self.vtk_overlay_window.set_video_image(image)

        #and render
        self.vtk_overlay_window.Render()

Now we build the application itself.

::

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
  viewer.start()

  #start the application
  sys.exit(app.exec_())

Now run the application with

::

  python vtkoverlay_app.py

or similar. If successful you should see a live video stream overlaid with
a rendered surface model, some thing like this... 

.. figure:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/raw/7-screenshots/doc/vtk_overlay_example.gif

. Congratulations. If not you can download a
`finished example`_ and compare. Play around with it, see what happens if
you delete some line or change part of the update method.

Next we will add some code to the update loop to move the rendered model
for each frame update.

.. _`scikit-surgeryutils`: https://pypi.org/project/scikit-surgeryutils
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`OverlayBaseApp` : https://scikit-surgeryutils.readthedocs.io/en/latest/sksurgeryutils.common_overlay_apps.html#module-sksurgeryutils.common_overlay_apps.OverlayBaseApp
.. _`finished example` : https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/blob/master/snappytutorial01/vtkoverlay_app.py
