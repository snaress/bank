from PyQt4 import QtGui
from lib.qt import procQt as pQt
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
        self._refresh()

    def _setupUi(self):
        """ Setup projectTree Widget """
        self.setupUi(self)
        self.log.info("#-- Setup Tree Project --#")
        self.twTree = Tree(self)
        self.vlTree.insertWidget(-1, self.twTree)
        self.rbTreeMode.clicked.connect(self.twTree.rf_tree)
        self.rbStepMode.clicked.connect(self.twTree.rf_tree)

    def _refresh(self):
        self.log.info("#-- Refresh Tree Project --#")
        self.rf_treeSwitch()
        self.twTree.rf_tree()

    def rf_treeSwitch(self):
        """ Refresh mainTree switch """
        self.log.debug("\t Refreshing tree switch ...")
        for n in range(self.hlTreeSwitch.count()):
            self.hlTreeSwitch.takeAt(0)
        for tree in self.pm.prodTrees['_order']:
            newButton = self._newRadioButton(tree)
            self.hlTreeSwitch.insertWidget(-1, newButton)
        self.hlTreeSwitch.itemAt(0).widget().setChecked(True)

    def getSelTree(self):
        """ Get selected tree
            @return: (str) : Selected tree name """
        for n in range(self.hlTreeSwitch.count()):
            if self.hlTreeSwitch.itemAt(n).widget().isChecked():
                return str(self.hlTreeSwitch.itemAt(n).widget().text())

    def _newRadioButton(self, treeName):
        """ Create new QRadioButton
            @param treeName: (str) : Button label
            @return: (object) : QRadioButton """
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
        """ Refresh mainTree """
        self.clear()
        treeDict = self.pm.prodTrees[self._parent.getSelTree()]
        if self._parent.rbTreeMode.isChecked():
            self.log.debug("\t Refreshing main tree (Tree Mode) ...")
            for node in treeDict['tree']['_order']:
                print treeDict['tree'][node]
                newItem = TreeNode(**treeDict['tree'][node])
                if len(node.split('/')) == 1:
                    self.addTopLevelItem(newItem)
                else:
                    parent = self._getItemFromTreePath('/'.join(node.split('/')[:-1]))
                    parent.addChild(newItem)
                if newItem.nodeType == 'shotNode':
                    for step in treeDict['steps']:
                        newStep = TreeNode(nodeLabel=step)
                        newItem.addChild(newStep)
        else:
            self.log.debug("\t Refreshing main tree (Step Mode) ...")

    @staticmethod
    def _getItemTreePath(item):
        """ Get given QTreeWidgetItem tree path
            @param item: (object) : QTreeWidgetItem
            @return: (str) : Item tree path """
        if item.parent() is None:
            root = item.nodeLabel
        else:
            root = ""
            parents = pQt.getAllParent(item)
            parents.reverse()
            for n, p in enumerate(parents[:-1]):
                if n == 0:
                    root = p.nodeLabel
                else:
                    root = "%s/%s" % (root, p.nodeLabel)
            root = "%s/%s" % (root, item.nodeLabel)
        return root

    def _getItemFromTreePath(self, treePath):
        """ Get item from given tree path
            @param treePath: (str) : Tree path
            @return: (object) : QTreeWidgetItem """
        for item in pQt.getAllItems(self):
            if self._getItemTreePath(item) == treePath:
                return item


class TreeNode(QtGui.QTreeWidgetItem):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        super(TreeNode, self).__init__()
        self.setText(0, getattr(self, 'nodeLabel'))