# coding=utf-8

"""Here we use the SNAPPY package ardavin (AR Davinci) to show base AR, using SNAPPY"""
import sys
from PySide2.QtWidgets import QApplication
from ardavin.ui.VTKRenderer import get_VTK_data
from ardavin.ui.Viewers import MonoViewer



app = QApplication([])

#you can set the video source, 0 for the first webcam you find.
video_source=0
vtk_models = get_VTK_data('/home/thompson/src/ardavin/inputs/demo')

viewer = MyMonoViewer(0)

viewer.add_VTK_models(vtk_models)

camera_file=False
if camera_file:
    viewer.load_camera_view(camera_file)
viewer.start()

sys.exit(app.exec_())
    
