import os
from PyQt4 import QtGui
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
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
        self.log.debug("#-- Setup Tree Project --#")
        self.twTree = Tree(self)
        self.vlTree.insertWidget(-1, self.twTree)
        self.rbTreeMode.clicked.connect(self.twTree.rf_tree)
        self.rbStepMode.clicked.connect(self.twTree.rf_tree)
        self.rbAsset.clicked.connect(self.twTree.rf_tree)
        self.rbShot.clicked.connect(self.twTree.rf_tree)

    def _refresh(self):
        self.log.debug("#-- Refresh Tree Project --#")
        self.twTree.rf_tree()

    def getSelMode(self):
        """ Get selected display mode
            @return: (str) : Selected tree display mode """
        if self.rbTreeMode.isChecked():
            return 'treeMode'
        elif self.rbStepMode.isChecked():
            return 'stepMode'

    def getSelTree(self):
        """ Get selected tree
            @return: (str) : Selected tree name """
        if self.rbAsset.isChecked():
            return 'asset'
        elif self.rbShot.isChecked():
            return 'shot'

    def _newRadioButton(self, treeName):
        """ Create new QRadioButton
            @param treeName: (str) : Button label
            @return: (object) : QRadioButton """
        newButton = QtGui.QRadioButton()
        newButton.setText(treeName)
        newButton.clicked.connect(self.twTree.rf_tree)
        return newButton


class Tree(QtGui.QTreeWidget):
    """ QTreeWidget used by ProjectTree
        @param parent: (object) : Parent QWidget """

    def __init__(self, parent):
        self._parent = parent
        self.mainUi = self._parent.mainUi
        self.pm = self._parent.pm
        self.log = self._parent.log
        super(Tree, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup projectTree QTreeWidget """
        self.log.debug("\t Setup mainTree widget ...")
        self.header().setVisible(False)
        self.itemClicked.connect(self.on_treeNode)

    def rf_tree(self):
        """ Refresh mainTree """
        self.clear()
        if self._parent.getSelTree() is not None:
            selTree = self._parent.getSelTree()
            treeDict = self.pm.prodTrees[selTree]
            if self._parent.getSelMode() == 'treeMode':
                self.log.debug("\t Refreshing main tree (Tree Mode) ...")
                self.rf_treeMode(selTree, treeDict)
            elif self._parent.getSelMode() == 'stepMode':
                self.log.debug("\t Refreshing main tree (Step Mode) ...")
                self.rf_stepMode(selTree, treeDict)

    def rf_treeMode(self, selTree, treeDict):
        """ Refresh main tree with treeMode listing
            @param treeDict: (dict) : Tree dict """
        for node in treeDict['tree']['_order']:
            newItem = TreeNode(**treeDict['tree'][node])
            if len(node.split('/')) == 1:
                self.addTopLevelItem(newItem)
            else:
                parent = self._getItemFromTreePath('/'.join(node.split('/')[:-1]))
                parent.addChild(newItem)
            if getattr(newItem, 'nodeType') == 'shotNode':
                newItem._itemPath = node
                newItem._dataPath = os.path.join(self.pm._treePath, selTree)
                for fld in node.split('/'):
                    newItem._dataPath = os.path.join(newItem._dataPath, fld)
                newItem._dataPath = pFile.conformPath(newItem._dataPath)
                newItem._dataFile = "%s.py" % newItem._dataPath
                for step in treeDict['steps']:
                    newStep = TreeNode(nodeType='step', nodeLabel=step, nodeName=step)
                    newStep._tree = selTree
                    newStep._step = step
                    newStep._dataPath = newItem._dataPath
                    newStep._ltPath = pFile.conformPath(os.path.join(newStep._dataPath, 'lt', step))
                    newStep._dataFile = newItem._dataFile
                    newItem.addChild(newStep)

    def rf_stepMode(self, selTree, treeDict):
        """ Refresh main tree with stepMode listing
            @param treeDict: (dict) : Tree dict """
        for step in treeDict['steps']:
            newStep = TreeNode(nodeType='step', nodeLabel=step, nodeName=step)
            self.addTopLevelItem(newStep)
            for node in treeDict['tree']['_order']:
                newItem = TreeNode(**treeDict['tree'][node])
                if len(node.split('/')) == 1:
                    newStep.addChild(newItem)
                else:
                    rootPath = "%s/%s" % (step, '/'.join(node.split('/')[:-1]))
                    parent = self._getItemFromTreePath(rootPath)
                    parent.addChild(newItem)
                if getattr(newItem, 'nodeType') == 'shotNode':
                    newItem._tree = selTree
                    newItem._step = step
                    newItem._itemPath = node
                    newItem._dataPath = os.path.join(self.pm._treePath, selTree)
                    for fld in node.split('/'):
                        newItem._dataPath = os.path.join(newItem._dataPath, fld)
                    newItem._dataPath = pFile.conformPath(newItem._dataPath)
                    newItem._ltPath = pFile.conformPath(os.path.join(newItem._dataPath, 'lt', step))
                    newItem._dataFile = "%s.py" % newItem._dataPath

    def on_treeNode(self):
        """ Command launch when shotNode is clicked """
        if self.mainUi.getSelTab() == 'Shots':
            self.mainUi.wgShots._refresh()
        elif self.mainUi.getSelTab() == 'LineTest':
            self.mainUi.wgLineTest._refresh()

    def addTopLevelItem(self, QTreeWidgetItem):
        super(Tree, self).addTopLevelItem(QTreeWidgetItem)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        super(Tree, self).addTopLevelItems(list_of_QTreeWidgetItem)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        super(Tree, self).insertTopLevelItem(p_int, QTreeWidgetItem)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        super(Tree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)

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
        self._setupUi()

    def _setupUi(self):
        """ Setup treeNode QTreeWidgetItem """
        self.setText(0, getattr(self, 'nodeLabel'))
        if hasattr(self, 'nodeType'):
            if getattr(self, 'nodeType') == 'shotNode':
                self.setTextColor(0, QtGui.QColor(125, 255, 255))

    def addChild(self, QTreeWidgetItem):
        super(TreeNode, self).addChild(QTreeWidgetItem)

    def addChildren(self, list_of_QTreeWidgetItem):
        super(TreeNode, self).addChildren(list_of_QTreeWidgetItem)

    def insertChild(self, p_int, QTreeWidgetItem):
        super(TreeNode, self).insertChild(p_int, QTreeWidgetItem)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        super(TreeNode, self).insertChildren(p_int, list_of_QTreeWidgetItem)
