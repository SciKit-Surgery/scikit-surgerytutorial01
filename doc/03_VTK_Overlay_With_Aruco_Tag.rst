.. highlight:: shell

.. _SimpleOverlayApp:

===============================================
Detecting a feature to control model motion
===============================================

So far we haven't performed any data processing, which is a key 
element of any surgical AR system. Typically we might get tracking 
information from an external tracking system, for example using
`scikit-surgerynditracker`_. However this isn't practical for a 
tutorial, so let's just use the video feed itself. 

02 - Add a feature detector and follower
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a copy of vtkoverlay_with_movement_app.py and call it 
vtk_aruco_app.py or similar.

Add an import statement for opencv

::

  import cv2

OpenCV provides numerous computer vision tools, and integrates seamlessly 
with SNAPPY using numpy data structures, which we must also import

::

  import numpy


Now we need some member variables to use with the aruco tag detector. In our 
OverlayApp we will create a new __init__ function to override the one in the base
class and define the member variables we will need

::

  def __init__(self, video_source):

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
        super().__init__(video_source)



Edit the update method for the OverlayApp class, to call a new 
method called _aruco_detect_and_follow.

.. code-block:: python
   :emphasize-lines: 4,5

   def update(self):
        ret, self.img = self.video_source.read()

        #add a method to move the rendered models
        self._aruco_detect_and_follow()

        self.vtk_overlay_window.set_video_image(self.img)
        self.vtk_overlay_window._RenderWindow.Render()

Then add a new method called _aruco_detect_and_follow to the class.  
The tag detection code is taken from the `OpenCV aruco tutorial`_.

::

  def _aruco_detect_and_follow(self):
        #detect any markers
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(self.img, self.dictionary)

        if len(marker_corners) > 0:
            #if any markers found, estmate their pose
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners,
                    self.marker_size, self.camera_projection_matrix, self.camera_distortion)
            
            #and move the model to suit
            self._move_model(rvecs[0][0], tvecs[0][0])


Then edit the _move_model method to take two position arguments.  

.. code-block:: python

  def _move_model(self, rotation, translation):

        #because the camera won't normally be at the origin, 
        #we need to find it and make movement relative to it
        camera=self.vtk_overlay_window.get_foreground_camera()

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
a rendered surface model. When you hold the printed aruco tag in front of the
camera, the model should approximately follow it.

You may notice that the model appears and disappears at certain distances from the 
camera. This is because we haven't updated the renderer's clipping planes to 
match the new model position. This can be easily fixed by adding the following
code to the update method

::

  self.vtk_overlay_window.set_camera_state({"ClippingRange": [10,800]})

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

That completes this tutorial. Please get in touch with any feedback or issues. You can 
use the issue tracker at the `Project homepage`_. 

.. _`scikit-surgeryvtk`: https://pypi.org/project/scikit-surgeryvtk
.. _`scikit-surgerynditracker`: https://pypi.org/project/scikit-surgerynditracker
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`OverlayBaseApp` : https://scikit-surgeryvtk.readthedocs.io/en/latest/sksurgeryvtk.widgets.OverlayBaseApp.html#module-sksurgeryvtk.widgets.OverlayBaseApp
.. _`finished example` : https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/blob/master/snappytutorial01/02_vtk_aruco_app.py
.. _`OpenCV aruco tutorial` : https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
.. _`Project homepage` : https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01
