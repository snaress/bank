import os, sys
from PyQt4 import QtGui
from lib.qt import procQt as pQt
from tools.maya.util import toolManager
from lib.system import procFile as pFile
from tools.maya.util.proc import procUi as pUi
try:
    import pymel.core as pm
    import maya.OpenMayaUI as mOpen
    __inMaya__ = True
    pQt.CompileUi(uiDir=os.path.join(toolManager.toolPath, 'ui'))
except:
    __inMaya__ = False
from tools.maya.util.toolManager.ui import toolManagerUI


class ToolManagerUi(QtGui.QMainWindow, toolManagerUI.Ui_toolManager):

    def __init__(self, parent=None, logLvl='info'):
        self.log = pFile.Logger(title="Factory-ui", level=logLvl)
        self.log.info("#-- Launching ToolManager --#")
        self.log.info("Mode StandAlone: %s" % __inMaya__)
        super(ToolManagerUi, self).__init__(parent)
        self._setupUi()

    def _setupUi(self):
        self.setupUi(self)



def launch():
    if __inMaya__:
        _parent = pUi.getMayaMainWindow()
    else:
        _parent = None
    toolName = 'factory'
    if pm.window(toolName, q=True, ex=True):
        pm.deleteUI(toolName)
    tool = ToolManagerUi(parent=_parent)
    tool.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ToolManagerUi(parent=None)
    window.show()
    sys.exit(app.exec_())