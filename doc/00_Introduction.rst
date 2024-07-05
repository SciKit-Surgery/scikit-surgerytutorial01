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

Packages, other requirements, and virtual environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python virtual environments
~~~~~~~~~~~~
Virtualenv, venv, conda or pyenv can be used to create virtual environments to manage python packages.
If you don't have Python installed, we recommend downloading an installer for your platform directly from `python.org`_.
For the case of conda, please create a VE using the following commands in your terminal:

::

   conda update -n base -c defaults conda
   conda create -n sst01VE python=3.8 pip -c conda-forge #try3.7
   conda activate sst01VE
   pip install -r requirements.txt
   pip install -r requirements-dev.txt


.. _`python.org`: https://www.python.org/downloads/
.. _`SmartLiver`: https://link.springer.com/article/10.1007/s11548-018-1761-3
.. _`NifTK`: https://link.springer.com/article/10.1007/s11548-014-1124-7
.. _`SciKit-SurgeryUtils`: https://pypi.org/project/scikit-surgeryutils/
.. _`SciKit-SurgeryCore`: https://pypi.org/project/scikit-surgerycore/
.. _`SciKit-SurgeryArUcoTracker`: https://pypi.org/project/scikit-surgeryarucotracker/
.. _`PySide2`: https://pypi.org/project/PySide2
.. _`OpenCV` : https://pypi.org/project/opencv-contrib-python
.. _`VTK` : https://pypi.org/project/vtk
.. _`conda_installation` : https://conda.io/projects/conda/en/latest/user-guide/install/index.html
