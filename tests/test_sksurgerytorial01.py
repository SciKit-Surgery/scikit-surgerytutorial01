# coding=utf-8

"""sksurgerytutorial01 vtkoverlay tests"""

import pytest

from sksurgerytutorial01.vtk_aruco_app import OverlayApp as aruco
from sksurgerytutorial01.vtkoverlay_app import OverlayApp as vtkoverlay
from sksurgerytutorial01.vtkoverlay_with_movement_app import OverlayApp as vtkmovingoverlay


def test_vtk_aruco_app(setup_qt):
    pass
    viewer = aruco(image_source='data/output.avi')
    viewer.add_vtk_models_from_dir('models')
    viewer.show()
    viewer.start()
    viewer.stop()


def test_vtkoverlay_app(setup_qt):
    pass
    viewer = vtkoverlay(video_source='data/output.avi')
    viewer.add_vtk_models_from_dir('models')
    viewer.show()
    viewer.start()
    viewer.stop()


def test_vtkoverlay_with_movement_app(setup_qt):
    pass
    viewer = vtkmovingoverlay(video_source='data/output.avi')
    viewer.add_vtk_models_from_dir('models')
    viewer.show()
    viewer.start()
    viewer.stop()
