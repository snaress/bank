import sys
from PyQt4 import QtGui, uic
from tools.maya.util import toolManager


toolManagerClass, toolManagerUiClass = uic.loadUiType(toolManager.uiList['toolManager'])
class ToolManagerUi(toolManagerClass, toolManagerUiClass):
    """ Class containing all toolManager's Ui actions """

    def __init__(self):
        print "##### Launching ToolManager Ui #####"
        super(ToolManagerUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ToolManagerUi()
    window.show()
    sys.exit(app.exec_())