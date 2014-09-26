from PyQt4 import QtGui
from appli.prodManager.ui import wgtMainTreeUI


class ProjectTree(QtGui.QWidget, wgtMainTreeUI.Ui_mainTree):
    """ Project settings ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(ProjectTree, self).__init__()
        self._setupUi()
        self.rf_treeSwitch()

    def _setupUi(self):
        """ Setup projectTree Widget """
        self.setupUi(self)
        self.log.info("#-- Setup Tree Project --#")
        self.twTree = Tree(self)
        self.vlTree.insertWidget(-1, self.twTree)

    def rf_treeSwitch(self):
        for n in range(self.hlTreeSwitch.count()):
            self.hlTreeSwitch.takeAt(0)
        for tree in self.pm.prodTrees['_order']:
            self.hlTreeSwitch.insertWidget(-1, self._newRadioButton(tree))
        self.hlTreeSwitch.itemAt(0).widget().setChecked(True)

    def getSelTree(self):
        for n in range(self.hlTreeSwitch.count()):
            if self.hlTreeSwitch.itemAt(n).widget().isChecked():
                return str(self.hlTreeSwitch.itemAt(n).widget().text())

    def _newRadioButton(self, treeName):
        newButton = QtGui.QRadioButton()
        newButton.setText(treeName)
        newButton.clicked.connect(self.twTree.rf_tree)
        return newButton


class Tree(QtGui.QTreeWidget):

    def __init__(self, parent):
        self._parent = parent
        self.mainUi = self._parent.mainUi
        self.pm = self._parent.pm
        self.log = self._parent.log
        super(Tree, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup projectTree QTreeWidget """
        self.log.debug("\t Setup mainTree widget ...")
        self.header().setVisible(False)

    def rf_tree(self):
        self.clear()
        treeDict = self.pm.prodTrees[self._parent.getSelTree()]['tree']
        for node in treeDict['_order']:
            print node