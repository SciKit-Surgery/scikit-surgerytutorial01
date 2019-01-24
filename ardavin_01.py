# coding=utf-8

"""Now we try and implement Aruco tag tracking in the library"""
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import *
from ardavin.ui.VTKRenderer import get_VTK_data
from ardavin.ui.Viewers import MonoViewer

#A new import statement to get access to the VTKRender's image update
from ardavin.ui.VTKRenderer import UI, VTKOverlayWindow

class MyVTKOverlayWindow (VTKOverlayWindow):
    """Same as ardavin.ui.VTKRenderer.VTKOverlayWindow, but we overwrite
    get_next_frame, with our own function"""
    def get_next_frame(self):
        super(MyVTKOverlayWindow, self).get_next_frame()
        self.aruco_detect()

    def aruco_detect(self):
        #put detection code in here
        print ("Overidden")
        pass

class MyUI (UI):
    def add_vtk_overlay_window(self, video_source):
        """ Create a new VTKOverlayWindow and add it to widget list"""
        self.interactor_layout = QHBoxLayout()
        self.VTK_interactor = MyVTKOverlayWindow(video_source)
        #self.VTK_interactor.resize(300, 300)
        self.VTK_interactor.setFixedSize(self.width(), self.height())

        self.interactor_layout.addWidget(self.VTK_interactor, 0)
        self.layout.addLayout(self.interactor_layout)

        self.VTK_interactor.set_stereo_right()

        self.VTK_interactor.Initialize()
        self.VTK_interactor.Start()

class MyMonoViewer ( MonoViewer ):
    def __init__(self,video_source):
        self.UI = MyUI(video_source)
        self.UI.exit_signal.connect(self.run_before_quit)
    #here we could modify our own mono viewer
    pass


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
    
