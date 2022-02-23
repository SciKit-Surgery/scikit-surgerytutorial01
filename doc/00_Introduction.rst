.. highlight:: shell

.. _Introduction:

===============================================
Introduction
===============================================

This is the SciKit-Surgery Augmented Reality Tutorial. SciKit-Surgery aims to support users in
developing software applications for surgery. The aim of this tutorial is to
introduce the user to SciKit-Surgery. After completing the tutorial the user will be able to;

- make a small augmented reality that shows a rendered surface model overlaid on a
  live video,
- write an algorithm to move the rendered model,
- write an algorithm to track an ArUco tag in the live video and "attach" the rendered model
  to the feature.

The tutorial makes use of the SciKit-Surgery library `SciKit-SurgeryUtils`_ to create a simple overlay
window, showing a VTK model over a video stream. The last part of the tutorial uses `SciKit-SurgeryArUcoTracker`_ and `SciKit-SurgeryCore`_ to use the motion of a tracked marker to 
move the model. The tutorial has been tested with
Python 3.6 and 3.7 on Linux, Windows, and Mac. and Python 2.7 on Linux.

Augmented Reality in Surgery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmented reality is the process of overlaying virtual models onto
live video. Augmented reality has useful applications in surgery, where 
unseen anatomy can be overlaid on the surgical scene, to help the surgeon 
find anatomy of interest. The example below is from the `SmartLiver`_ system, 
developed using the `NifTK`_ platform.

.. figure:: https://github.com/SciKit-Surgery/SciKit-SurgeryTutorial01/raw/master/doc/croppedOverlayVideo.gif

Making an augmented reality application from scratch can be quite complicated.
The developer will require an
application framework to handle display, threading and user interface, something
to provide video streaming, and finally a model renderer. The SciKit-Surgery package
`scikit-surgeryutils`_ simplifies the process by integrating QT (`PySide2`_),
`OpenCV`_, and `VTK`_ into a simple to use Python library. This tutorial will
guide the user in creating an augmented reality application in around 70 lines of code.

Installation
~~~~~~~~~~~~
Step 1:
You'll need SciKit-SurgeryUtils installed on your system. Provided you have Python installed on 
your system you should be able to run ...
::
 
  pip install scikit-surgeryutils

to install SciKit-SurgeryUtils and its dependencies (including SciKit-SurgeryCore).
For the third part of the tutorial you'll also need SciKit-SurgeryArUcoTracker

::

  pip install scikit-surgeryarucotracker

If you don't have Python installed, we 
recommend downloading an installer for your platform directly from `python.org`_.

You can also use a virtual environment to run the tutorial without altering your system's Python 
installation, see our instructions for `virtual environments`_.

Step 2: 
You should now be able to follow the tutorial, using the code snippets contained herein.

.. _`python.org`: https://www.python.org/downloads/
.. _`SmartLiver`: https://link.springer.com/article/10.1007/s11548-018-1761-3
.. _`NifTK`: https://link.springer.com/article/10.1007/s11548-014-1124-7
.. _`SciKit-SurgeryUtils`: https://pypi.org/project/scikit-surgeryutils/
.. _`SciKit-SurgeryCore`: https://pypi.org/project/scikit-surgerycore/
.. _`SciKit-SurgeryArUcoTracker`: https://pypi.org/project/scikit-surgeryarucotracker/
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`virtual environments` : https://weisslab.cs.ucl.ac.uk/WEISS/wiki/wikis/Creating-Python-Virtual-Environment-using-Anaconda/Minicoda-and-Virtualenv

