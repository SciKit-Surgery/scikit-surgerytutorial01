.. highlight:: shell

.. _Introduction:

===============================================
Introduction
===============================================

This the SNAPPY Augmented Reality Tutorial. SNAPPY aims to support users in
developing software applications for surgery. The aim of this tutorial is to
introduce the user to SNAPPY. After completing the tutorial the user will be able to;

- make a small augmented reality that shows a rendered surface model overlaid on a
  live video,
- write an algorithm to move the rendered model,
- write an algorithm to track an ArUco tag in the live video and "attach" the rendered model
  to the feature.

The tutorial makes use of the SNAPPY library scikit-surgeryutils. The tutorial has been tested with
Python 3.6 and 3.7 on Linux, Windows, and Mac. and Python 2.7 on Linux.

Installation
~~~~~~~~~~~~
Step 1:
You'll need scikit-surgeryutils installed on your system. Provided you have Python installed on 
your system you should be able to run ...
::
  pip install scikit-surgeryutils

to install scikit-surgeryutils and its dependencies. If you don't have Python installed, we 
recommend downloading an installer for your platform from `Python Downloads`_

Step 2: 
You should now be able to follow the tutorial, using the code snippets contained herein.
You can also download a completed tutorial, either using git;
::
  git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

or by downloading the files directly from 
https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

.. _`Python Downloads`: https://python downloads



