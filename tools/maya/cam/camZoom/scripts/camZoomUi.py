from PyQt4 import uic
import maya.cmds as mc
from functools import partial
from tools.maya.cam import camZoom
from tools.maya.util.proc.scripts import procUi as pUi
try:
    import pymel.core as pm
    import maya.OpenMayaUI as mOpen
except:
    pass


camZoomClass, camZoomUiClass = uic.loadUiType(camZoom.uiList['camZoom'])
class CamZoomUi(camZoomClass, camZoomUiClass):

    def __init__(self, _parent=pUi.getMayaMainWindow()):
        print "##### Launching camZoom Ui #####"
        super(CamZoomUi, self).__init__(_parent)
        self._setupUi()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)
        self.bInit.clicked.connect(self.on_initCam)
        self.hsCamZoom.valueChanged.connect(partial(self.on_slider, self.hsCamZoom, self.dsbCamZoom))
        self.hsVertPan.valueChanged.connect(partial(self.on_slider, self.hsVertPan, self.dsbVertPan))
        self.hsHoriPan.valueChanged.connect(partial(self.on_slider, self.hsHoriPan, self.dsbHoriPan))
        self.dsbCamZoom.valueChanged.connect(partial(self.on_spinBox, self.hsCamZoom,
                                                     self.dsbCamZoom, 'zoom'))
        self.dsbVertPan.valueChanged.connect(partial(self.on_spinBox, self.hsVertPan,
                                                     self.dsbVertPan, 'verticalPan'))
        self.dsbHoriPan.valueChanged.connect(partial(self.on_spinBox, self.hsHoriPan,
                                                     self.dsbHoriPan, 'horizontalPan'))
        self.bReset.clicked.connect(self.on_reset)
        self.bRestoreInit.clicked.connect(self.on_restore)

    def on_initCam(self):
        """ Init selected camera, store initial cam attributes """
        if not len(mc.ls(sl=True)) == 1:
            self.leCam.setText("Warning: Select only one camera !!!")
        else:
            selCam = mc.ls(sl=True)[0]
            if mc.nodeType(selCam) == 'camera':
                self.leCam.setText(selCam)
                self.storeParams(selCam)
            else:
                if mc.listRelatives(selCam, s=True, ni=True):
                    selShape = mc.listRelatives(selCam, s=True, ni=True)[0]
                    if mc.nodeType(selShape) == 'camera':
                        self.leCam.setText(selShape)
                        self.storeParams(selShape)
                    else:
                        self.leCam.setText("Warning: Selection is not a valide camera !!!")
                else:
                    self.leCam.setText("Warning: Selection is not a valide camera !!!")

    def storeParams(self, camShape):
        """ Store selected camera attributes
            @param camShape: (str) : Camera shape name """
        #-- Store Params --3
        self.leCam.params = {'panZoomEnabled': mc.getAttr('%s.panZoomEnabled' % camShape),
                             'zoom': mc.getAttr('%s.zoom' % camShape),
                             'horizontalPan': mc.getAttr('%s.horizontalPan' % camShape),
                             'verticalPan': mc.getAttr('%s.verticalPan' % camShape)}
        #-- Init Cam --#
        mc.setAttr('%s.panZoomEnabled' % camShape, True)
        mc.setAttr('%s.zoom' % camShape, self.dsbCamZoom.value())
        mc.setAttr('%s.verticalPan' % camShape, self.dsbVertPan.value())
        mc.setAttr('%s.horizontalPan' % camShape, self.dsbHoriPan.value())

    def on_slider(self, slider, spinBox):
        """ Get given slider position and translate value to the given spinBox
            @param slider: (object) : QSlider
            @param spinBox: (object) : QDoubleSpinBox """
        spinBox.setValue(float(slider.value())/100)

    def on_spinBox(self, slider, spinBox, camAttr):
        """ Get given spinBox value and translate position to the given slider,
            Apply value to the given camera
            @param slider: (object) : QSlider
            @param spinBox: (object) : QDoubleSpinBox
            @param camAttr: (str) : Cam attribute name """
        value = spinBox.value()
        slider.setValue(int(value*100))
        self.editCam(camAttr, value)

    def editCam(self, camAttr, value):
        """ Edit selected camera shape
            @param camAttr: (str) : Cam attribute name
            @param value: (str) : Cam attribute value """
        cam = str(self.leCam.text())
        if mc.objExists(cam) and mc.nodeType(cam) == 'camera':
            mc.setAttr('%s.%s' % (str(self.leCam.text()), camAttr), value)
        else:
            mc.warning("Warning: Initialized camera is not a valide camera (%s) !!!" % cam)

    def on_reset(self):
        """ Reset params """
        self.dsbCamZoom.setValue(1)
        self.dsbVertPan.setValue(0)
        self.dsbHoriPan.setValue(0)

    def on_restore(self):
        """ Restore init camera attributes """
        cam = str(self.leCam.text())
        if mc.objExists(cam) and mc.nodeType(cam) == 'camera':
            if hasattr(self.leCam, 'params'):
                self.on_reset()
                for k, v in self.leCam.params.iteritems():
                    mc.setAttr('%s.%s' % (cam, k), v)
                self.leCam.clear()
                delattr(self.leCam, 'params')
            else:
                mc.warning("Warning: Stored params not found !!!" % cam)
        else:
            mc.warning("Warning: Initialized camera is not a valide camera (%s) !!!" % cam)


def launch():
    toolName = 'camZoomUi'
    if pm.window(toolName, q=True, ex=True):
        pm.deleteUI(toolName)
    tool = CamZoomUi()
    tool.show()