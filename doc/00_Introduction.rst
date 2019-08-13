.. highlight:: shell

.. _Introduction:

===============================================
Introduction
===============================================

This is the SNAPPY Augmented Reality Tutorial. SNAPPY aims to support users in
developing software applications for surgery. The aim of this tutorial is to
introduce the user to SNAPPY. After completing the tutorial the user will be able to;

- make a small augmented reality that shows a rendered surface model overlaid on a
  live video,
- write an algorithm to move the rendered model,
- write an algorithm to track an ArUco tag in the live video and "attach" the rendered model
  to the feature.

The tutorial makes use of the SNAPPY library `scikit-surgeryutils`_. The tutorial has been tested with
Python 3.6 and 3.7 on Linux, Windows, and Mac. and Python 2.7 on Linux.

Augmented Reality in Surgery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmented reality is the process of overlaying virtual models onto
live video. Augmented reality has useful applications in surgery, where 
unseen anatomy can be overlaid on the surgical scene, to help the surgeon 
find anatomy of interest. The example below is from the `SmartLiver`_ system, 
developed using the `NifTK`_ platform.

.. figure:: https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01/raw/master/doc/croppedOverlayVideo.gif

Making an augmented reality application from scratch can be quite complicated.
The developer will require an
application framework to handle display, threading and user interface, something
to provide video streaming, and finally a model renderer. The SNAPPY package
`scikit-surgeryutils`_ simplifies the process by integrating QT (`PySide2`_),
`OpenCV`_, and `VTK`_ into a simple to use Python library. This tutorial will
guide the user in creating an augmented reality application in around 70 lines of code.

Installation
~~~~~~~~~~~~
Step 1:
You'll need scikit-surgeryutils installed on your system. Provided you have Python installed on 
your system you should be able to run ...
::
  pip install scikit-surgeryutils

to install scikit-surgeryutils and its dependencies. If you don't have Python installed, we 
recommend downloading an installer for your platform directly from `python.org`_

Step 2: 
You should now be able to follow the tutorial, using the code snippets contained herein.
You can also download a completed tutorial, either using git;
::
  git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

or by downloading the files directly from 

https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

.. _`python.org`: https://www.python.org/downloads/
.. _`SmartLiver`: https://link.springer.com/article/10.1007/s11548-018-1761-3
.. _`NifTK`: https://link.springer.com/article/10.1007/s11548-014-1124-7
.. _`scikit-surgeryutils`: https://pypi.org/project/scikit-surgeryutils/
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk

