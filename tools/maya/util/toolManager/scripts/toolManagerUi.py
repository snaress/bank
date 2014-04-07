import sys
from PyQt4 import QtGui, uic
from tools.maya.util import toolManager
from tools.maya.util.toolManager.scripts import uiRefresh


toolManagerClass, toolManagerUiClass = uic.loadUiType(toolManager.uiList['toolManager'])
class ToolManagerUi(toolManagerClass, toolManagerUiClass):
    """ Class containing all toolManager's Ui actions """

    def __init__(self):
        print "##### Launching ToolManager Ui #####"
        self.rootPath = toolManager.mayaToolsPath
        self.populate = uiRefresh.PopulateTree(self)
        super(ToolManagerUi, self).__init__()
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



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ToolManagerUi()
    window.show()
    sys.exit(app.exec_())