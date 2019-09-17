.. highlight:: shell

.. _OverlayAppWithArUco:

===============================================
Detecting a feature to control model motion
===============================================

So far we haven't performed any data processing, which is a key
element of any surgical AR system. Typically we might get tracking
information from an external tracking system, for example using
`scikit-surgerynditracker`_. Alternatively computer vision can
be used to estimate the location of anatomy relative to the camera.

For this example we're going to use computer vision to track an
ArUco tag, using OpenCV's implementation of the ArUco library.
We should end up with a 3D rendering that follows a tag as you move
it in front of the camera. Something like ...

.. figure:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/raw/master/doc/vtk_overlay_aruco_example.gif

02 - Add a feature detector and follower
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**You'll need an ArUco tag to track, print out**
`this one`_ .

Create a copy of vtkoverlay_with_movement_app.py and call it
vtk_aruco_app.py or similar.

Add an import statement for the ArUco detectors in OpenCV

::

  import cv2.aruco as aruco

OpenCV provides numerous computer vision tools, and integrates seamlessly
with SNAPPY using NumPy data structures, which we must also import

::

  import numpy


Now we need some member variables to use with the ArUco tag detector. In our
OverlayApp we will create a new __init__ function to override the one in the base
class and define the member variables we will need

::

   def __init__(self, image_source):
        #the aruco tag dictionary to use. DICT_4X4_50 will work with the tag in
        #../tags/tag_sheet_snappy01.pdf
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        # The size of the aruco tag in mm
        self.marker_size = 50

        #we'll use opencv to estimate the pose of the visible aruco tags.
        #for that we need a calibrated camera. For now let's just use a
        #a hard coded estimate. Maybe you could improve on this.
        self.camera_projection_mat = numpy.array([[560.0, 0.0, 320.0],
                                                  [0.0, 560.0, 240.0],
                                                  [0.0, 0.0, 1.0]])
        self.camera_distortion = numpy.zeros((1, 4), numpy.float32)

        #and call the constructor for the base class
        if sys.version_info > (3, 0):
            super().__init__(image_source)
        else:
            #super doesn't work the same in py2.7
            OverlayBaseApp.__init__(self, image_source)


Edit the update method for the OverlayApp class, to call a new
method called _aruco_detect_and_follow. Replace the call to method
self._move_model() with self._aruco_detect_and_follow().

.. code-block:: python
   :emphasize-lines: 4,5

   def update(self):
        _, image = self.video_source.read()

        #add a method to move the rendered models
        self._aruco_detect_and_follow()

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window._RenderWindow.Render()

Then add a new method called _aruco_detect_and_follow to the class.
The tag detection code is taken from the `OpenCV ArUco tutorial`_.

::

  def _aruco_detect_and_follow(self):
        #detect any markers
        marker_corners, _, _ = aruco.detectMarkers(image, self.dictionary)

        if marker_corners:
            #if any markers found, try and determine their pose
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(marker_corners,
                                                              self.marker_size,
                                                              self.camera_projection_mat,
                                                              self.camera_distortion)

            self._move_model(rvecs[0][0], tvecs[0][0])


Delete the _move_model method and replace it with the one
below, which takes two position arguments.

.. code-block:: python

  def _move_model(self, rotation, translation):

        #because the camera won't normally be at the origin,
        #we need to find it and make movement relative to it
        camera = self.vtk_overlay_window.get_foreground_camera()

        #Iterate through the rendered models
        for actor in self.vtk_overlay_window.get_foreground_renderer().GetActors():
            #opencv and vtk seem to have different x-axis, flip the x-axis
            translation[0] = -translation[0]

            #set the position, relative to the camera
            actor.SetPosition(camera.GetPosition() - translation)


Leave the rest of the file as is, and try running the application with

::

  python vtk_aruco_app.py

or similar. If successful you should see a live video stream overlaid with
a rendered surface model, similar to the video at the top of the page.
When you hold the printed ArUco tag in front of the
camera, the model should approximately follow it.

You may notice that the model appears and disappears at certain distances from the
camera. This is because we haven't updated the renderer's clipping planes to
match the new model position. This can be easily fixed by adding the following
code to the update method

::

  self.vtk_overlay_window.set_camera_state({"ClippingRange": [10, 800]})

Maybe you can do something more sophisticated.

Also, you may notice that the model does not change orientation. You could add the following
to the _move_model method

::

  rotation = 180 * rotation/3.14
  actor.SetOrientation( rotation)

You will see that a further rotation is required to get a sensible result. See if you can
work it out.

Lastly you will notice that the model doesn't precisely follow the tag. This may be
because we haven't calibrated the camera, we just took a guess, so the pose estimation
will be wrong. Also we have not set the camera parameters for the VTK renderer, so this
will not match the video view.

You can download a
`finished example`_ of this tutorial file.

You can also download the completed tutorial, either using git;
::

  git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

or by downloading the files directly from

https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

That completes this tutorial. Please get in touch with any feedback or issues. You can
use the issue tracker at the `Project homepage`_.

.. _`scikit-surgeryutils`: https://pypi.org/project/scikit-surgeryutils
.. _`scikit-surgerynditracker`: https://pypi.org/project/scikit-surgerynditracker
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`OverlayBaseApp` : https://scikit-surgeryutils.readthedocs.io/en/latest/sksurgeryutils.common_overlay_apps.html#module-sksurgeryutils.common_overlay_apps.OverlayBaseApp
.. _`finished example` : https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/blob/master/snappytutorial01/vtk_aruco_app.py
.. _`OpenCV ArUco tutorial` : https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
.. _`Project homepage` : https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01
.. _`this one`: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/blob/master/tags/tag_sheet_snappy01.pdf
