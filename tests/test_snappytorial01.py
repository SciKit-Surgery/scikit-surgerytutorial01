# coding=utf-8
  
"""snappytutorial01 vtkoverlay tests"""

import pytest

from snappytutorial01.vtk_aruco_app import OverlayApp as aruco
from snappytutorial01.vtkoverlay_app import OverlayApp as vtkoverlay
from snappytutorial01.vtkoverlay_with_movement_app import OverlayApp as vtkmovingoverlay

def test_vtk_aruco_app(setup_qt):
    pass
    viewer = aruco(image_source = 'data/output.avi')
    viewer.add_vtk_models_from_dir('models')
    viewer.start()
    viewer.stop()

def test_vtkoverlay_app(setup_qt):
    pass
    viewer = vtkoverlay(video_source = 'data/output.avi')
    viewer.add_vtk_models_from_dir('models')
    viewer.start()
    viewer.stop()

def test_vtkoverlay_with_movement_app(setup_qt):
    pass
    viewer = vtkmovingoverlay(video_source = 'data/output.avi')
    viewer.add_vtk_models_from_dir('models')
    viewer.start()
    viewer.stop()


