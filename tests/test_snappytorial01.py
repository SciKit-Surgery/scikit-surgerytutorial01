# coding=utf-8
  
"""snappytutorial01 vtkoverlay tests"""

from snappytutorial01.vtk_aruco_app import OverlayApp as aruco
from snappytutorial01.vtkoverlay_app import OverlayApp as vtkoverlay
from snappytutorial01.vtkoverlay_with_movement_app import OverlayApp as vtkmovingoverlay
from PySide2.QtWidgets import QApplication

def test_vtk_aruco_app():
    app = QApplication([])
    viewer = aruco(image_source = 0)
    assert True


def test_vtkoverlay_app():
    viewer = vtkoverlay(video_source = 0)
    assert True

def test_vtkoverlay_with_movement_app():
    viewer = vtkmovingoverlay(video_source = 0)
    assert True

