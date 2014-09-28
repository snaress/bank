import os
from PyQt4 import QtGui
from lib.qt import textEditor
from appli import prodManager
from appli.prodManager.ui import tabShotsUI, wgtShotNodeUI


class ShotsTab(QtGui.QWidget, tabShotsUI.Ui_shotsTab):
    """ ShotNode settings ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(ShotsTab, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup project tabWidget """
        self.setupUi(self)
        self.log.info("#-- Setup Tab Shots --#")
        self.twShotNodes = ShotTree(self)
        self.vlTreeShots.insertWidget(0, self.twShotNodes)
        self.wgComment = Comment()
        self.glShotComment.addWidget(self.wgComment)

    def _refresh(self):
        """ Refresh shots tabWidget """
        self.log.info("#-- Refresh Tab Shots --#")
        self.rf_treeShot()

    def rf_treeShot(self):
        """ Refresh shotTree """
        self.log.debug("\t Refreshing tree shot ...")
        self.twShotNodes.clear()
        selItems = self.mainUi.wgTree.twTree.selectedItems()
        if selItems:
            rootNode = self.twShotNodes.getItemRootNode(selItems[0])
            if rootNode is not None:
                shotItems = []
                for n in range(rootNode.childCount()):
                    if rootNode.child(n).nodeType == 'shotNode':
                        itemDict = rootNode.child(n).__dict__
                        itemDict['shotType'] = self.mainUi.wgTree.getSelTree()
                        newShotItem = ShotItem(self, **itemDict)
                        shotItems.append(newShotItem)
                self.twShotNodes.addTopLevelItems(shotItems)


class ShotTree(QtGui.QTreeWidget):

    def __init__(self, parent):
        self._parent = parent
        self.mainUi = self._parent.mainUi
        super(ShotTree, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup shotTree QTreeWidget """
        self.setIndentation(0)
        self.header().setVisible(False)
        self.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

    def addTopLevelItem(self, QTreeWidgetItem):
        super(ShotTree, self).addTopLevelItem(QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        super(ShotTree, self).addTopLevelItems(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        super(ShotTree, self).insertTopLevelItem(p_int, QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        super(ShotTree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def getItemRootNode(self, item):
        """ Get given item rootNode
            @param item: (object) : QTreeWidgetItem
            @return: (object) : QTreeWidgetItem """
        rootNode = None
        if item.nodeType == 'container':
            rootNode = item
        elif item.nodeType == 'shotNode':
            rootNode = item.parent()
        elif item.nodeType == 'step':
            if self.mainUi.wgTree.getSelMode() == 'treeMode':
                rootNode = item.parent().parent()
        return rootNode


class ShotItem(QtGui.QTreeWidgetItem):

    def __init__(self, ui, **kwargs):
        self.ui = ui
        super(ShotItem, self).__init__()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self._widget = ShotNode(self.ui, self)

    def addChild(self, QTreeWidgetItem):
        super(ShotItem, self).addChild(QTreeWidgetItem)
        tree = QTreeWidgetItem.treeWidget()
        tree.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addChildren(self, list_of_QTreeWidgetItem):
        super(ShotItem, self).addChildren(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            tree = QTreeWidgetItem.treeWidget()
            tree.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertChild(self, p_int, QTreeWidgetItem):
        super(ShotItem, self).insertChild(p_int, QTreeWidgetItem)
        tree = QTreeWidgetItem.treeWidget()
        tree.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        super(ShotItem, self).insertChildren(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            tree = QTreeWidgetItem.treeWidget()
            tree.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)


class ShotNode(QtGui.QWidget, wgtShotNodeUI.Ui_shotNode):

    def __init__(self, ui, parent):
        self.ui = ui
        self._parent = parent
        super(ShotNode, self).__init__()
        self._setupUi()
        self._refresh()

    def _setupUi(self):
        """ Setup shotNode QWidget """
        self.setupUi(self)

    def _refresh(self):
        self.lLabelVal.setText(self._parent.nodeLabel)
        self.lNameVal.setText(self._parent.nodeName)
        self.lTypeVal.setText(self._parent.shotType)
        self.rf_shotNodeIma()

    def rf_shotNodeIma(self, ima=None):
        if ima is None:
            ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')
        qIma = QtGui.QPixmap(ima)
        self.lPreview.setPixmap(qIma)


class Comment(textEditor.TextEditor):

    def __init__(self):
        super(Comment, self).__init__()