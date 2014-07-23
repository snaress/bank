import sys
from PyQt4 import QtGui, uic
from tools.maya.util import toolManager
from tools.maya.util.proc.scripts import procUi as pUi
from tools.maya.util.toolManager.scripts import uiRefresh
try:
    import pymel.core as pm
    import maya.OpenMayaUI as mOpen
except:
    pass


toolManagerClass, toolManagerUiClass = uic.loadUiType(toolManager.uiList['toolManager'])
class ToolManagerUi(toolManagerClass, toolManagerUiClass):
    """ Class containing all toolManager's Ui actions """

    def __init__(self, _parent=pUi.getMayaMainWindow()):
        print "##### Launching ToolManager Ui #####"
        self.rootPath = toolManager.mayaToolsPath
        self.populate = uiRefresh.PopulateTree(self)
        super(ToolManagerUi, self).__init__(_parent)
        self._setupUi()
        self.rf_toolsTree()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)
        self.bLaunchTool.clicked.connect(self.launchTool)

    def rf_toolsTree(self):
        """ Refresh tools QTreeWidget """
        self.twTools.clear()
        self.populate.toolsTree()

    def launchTool(self):
        """ Launch selected tool """
        selTool = self.twTools.selectedItems()
        if selTool:
            print "#-- Launch From ToolManager: %s --#" % selTool[0].nodeName
            execfile(selTool[0].launchFile, globals())


def launch():
    toolName = 'toolManagerUi'
    if pm.window(toolName, q=True, ex=True):
        pm.deleteUI(toolName)
    tool = ToolManagerUi()
    tool.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ToolManagerUi()
    window.show()
    sys.exit(app.exec_())