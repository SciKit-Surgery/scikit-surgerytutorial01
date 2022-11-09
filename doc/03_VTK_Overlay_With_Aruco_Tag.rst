.. highlight:: shell

.. _OverlayAppWithArUco:

===============================================
Detecting a feature to control model motion
===============================================

So far we haven't performed any data processing, which is a key
element of any surgical AR system. Typically we might get tracking
information from an external tracking system, for example using
`SciKit-SurgeryNDITracker`_. For this demo, as you're unlikely to 
have an NDI tracker, we'll use `SciKit-SurgeryArUcoTracker`_ which
uses computer vision to track a tag.

We should end up with a 3D rendering that follows a tag as you move
it in front of the camera. Something like ...

.. figure:: https://github.com/SciKit-Surgery/SciKit-SurgeryTutorial01/raw/master/doc/vtk_overlay_aruco_example.gif

02 - Add a feature detector and follower
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**You'll need an ArUco tag to track, print it out in A4**
`this one`_ .

Create a copy of vtkoverlay_with_movement_app.py and call it
vtk_aruco_app.py or similar.

Add an import statement for SciKit-SurgeryArUcoTracker,

::

  from sksurgeryarucotracker.arucotracker import ArUcoTracker

And an import statement for SciKit-Surgery's transform manager.

::

  from sksurgerycore.transforms.transform_manager import TransformManager

We'll also need NumPy to handle arrays;

::
 
  import numpy


Set up SciKit-SurgeryArUcoTracker in the __init__ function of OverlayApp Class.

::

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

Edit the update method for the OverlayApp class, to call a new
method called _aruco_detect_and_follow. Replace the call to method
self._move_model() with self._aruco_detect_and_follow().

.. code-block:: python
   :emphasize-lines: 4,5

   def update_view(self):
        _, image = self.video_source.read()

        #add a method to move the rendered models
        self._aruco_detect_and_follow(image)

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window._RenderWindow.Render()

Then add a new method called _aruco_detect_and_follow to the class.

.. code-block:: python

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



Delete the _move_model method and replace it with a new _move_camera method

.. code-block:: python

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


Lastly you will notice that the model doesn't precisely follow the tag. This may be
because we haven't calibrated the camera, we just took a guess, so the pose estimation
will be wrong. Also we have not set the camera parameters for the VTK renderer, so this
will not match the video view.

You can download a
`finished example`_ of this tutorial file.

You can also download the completed tutorial, either using git;
::

  git clone https://github.com/SciKit-Surgery/scikit-surgerytutorial01

or by downloading the files directly from

https://github.com/SciKit-Surgery/scikit-surgerytutorial01

That completes this tutorial. Please get in touch with any feedback or issues. You can
use the issue tracker at the `Project homepage`_.

.. _`scikit-surgeryutils`: https://pypi.org/project/scikit-surgeryutils
.. _`scikit-surgerynditracker`: https://pypi.org/project/scikit-surgerynditracker
.. _`SciKit-SurgeryArUcoTracker`: https://pypi.org/project/scikit-surgeryarucotracker
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`OverlayBaseApp` : https://scikit-surgeryutils.readthedocs.io/en/latest/sksurgeryutils.common_overlay_apps.html#module-sksurgeryutils.common_overlay_apps.OverlayBaseApp
.. _`finished example` : https://github.com/SciKit-Surgery/SciKit-SurgeryTutorial01/blob/master/sksurgerytutorial01/vtk_aruco_app.py
.. _`OpenCV ArUco tutorial` : https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
.. _`Project homepage` : https://github.com/SciKit-Surgery/SciKit-SurgeryTutorial01
.. _`this one`: https://github.com/SciKit-Surgery/scikit-surgerytutorial01/blob/master/tags/tag_sheet_snappy01.pdf
