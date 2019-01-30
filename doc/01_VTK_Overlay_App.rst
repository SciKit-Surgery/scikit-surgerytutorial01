.. highlight:: shell

.. _SimpleOverlayApp:

===============================================
Making a simple overlay application
===============================================

This is tutorial 01 for the SNAPPY software collection. SNAPPY aims to support users in 
developing software applications for surgery. The aim of the tutorial is to 
introduce the user to SNAPPY. After completing the tutorial the user will have; 

- made a small augmented reality that shows a rendered surface model overlaid on a 
  live video,
- written an algorithm to move the rendered model,
- written an algorithm to track an aruco tag in the live video and "attach" the rendered moel
  to the feature.

The tutorial makes use of the SNAPPY library scikit-surgeryvtk. The tutorial has been tested with
Python 3.6. It may also work with Python 2.7, though has not been tested.

Installation
~~~~~~~~~~~~
Step 1:
::
  pip install scikit-surgeryvtk

Step 2: if you have git installed you can get the complete tutorial with;
::
  git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01

otherwise you should be able to copy files directly from 
https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/SNAPPYTutorial01





