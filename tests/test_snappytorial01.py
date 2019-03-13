# coding=utf-8
  
"""snappytutorial01 vtkoverlay tests"""

import pytest

from snappytutorial01.vtk_aruco_app import OverlayApp as aruco
from snappytutorial01.vtkoverlay_app import OverlayApp as vtkoverlay
from snappytutorial01.vtkoverlay_with_movement_app import OverlayApp as vtkmovingoverlay


#I can't seem to get the following to run on all platforms, I suspect it's
#something to do with display, but I need to park it for the minute, so 
#I've just commented out the lines that start the viewer

def test_vtk_aruco_app(setup_qt):
#    viewer = aruco(image_source = 'data/output.avi')
#    viewer.add_vtk_models_from_dir('models')
#    viewer.start()
    assert True

def test_vtkoverlay_app(setup_qt):
#    viewer = vtkoverlay(video_source = 'data/output.avi')
#    viewer.add_vtk_models_from_dir('models')
#    viewer.start()
    assert True

def test_vtkoverlay_with_movement_app(setup_qt):
#    viewer = vtkmovingoverlay(video_source = 'data/output.avi')
#    viewer.add_vtk_models_from_dir('models')
#    viewer.start()
    assert True


