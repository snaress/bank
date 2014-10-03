from PyQt4 import QtGui
from appli.prodManager.ui import tabLineTestUI, wgtLtNodeUI


class LineTestTab(QtGui.QWidget, tabLineTestUI.Ui_ltTab):
    """ LineTest ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(LineTestTab, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup lineTest tabWidget """
        self.setupUi(self)
        self.log.debug("#-- Setup Tab LineTest --#")
        self.bLtNew.clicked.connect(self.on_newLt)
        self.wgLtTree = LtTree(self)
        self.vlLtZone.insertWidget(-1, self.wgLtTree)
        self.rf_tabVis()

    def _refresh(self):
        """ Refresh lineTest tabWidget """
        self.log.debug("#-- Refresh Tab LineTest --#")
        selItems = self.mainUi.wgTree.twTree.selectedItems()
        if selItems:
            if self.mainUi.getSelMode() == 'treeMode':
                if selItems[0].nodeType == 'step':
                    self.rf_tabVis(state=True)
                else:
                    self.rf_tabVis(state=False)
            elif self.mainUi.getSelMode() == 'stepMode':
                if selItems[0].nodeType == 'shotNode':
                    self.rf_tabVis(state=True)
                else:
                    self.rf_tabVis(state=False)

    def rf_tabVis(self, state=False):
        """ Refresh project tab ui visibility
            @param state: (bool) : Visibility state """
        self.log.debug("#-- Refresh Tab LineTest Visibility --#")
        self.bLtNew.setEnabled(state)
        self.bLtDel.setEnabled(state)

    def on_newLt(self):
        """ Command launch when bLtNew is clicked """
        item = self.mainUi.wgTree.twTree.selectedItems()[0]
        print item.__dict__
        newLtItem = LtItem(self)
        self.wgLtTree.addTopLevelItem(newLtItem)


class LtTree(QtGui.QTreeWidget):

    def __init__(self, tab):
        self._tab = tab
        super(LtTree, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup lineTest treeWidget """
        self.header().setVisible(False)
        self.setIndentation(0)

    def addTopLevelItem(self, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(LtTree, self).addTopLevelItem(QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(LtTree, self).addTopLevelItems(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(LtTree, self).insertTopLevelItem(p_int, QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(LtTree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)


class LtItem(QtGui.QTreeWidgetItem):

    def __init__(self, tab):
        self._tab = tab
        super(LtItem, self).__init__()
        self._widget = LtNode(self)

    def addChild(self, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(LtItem, self).addChild(QTreeWidgetItem)
        QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addChildren(self, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(LtItem, self).addChildren(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertChild(self, p_int, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(LtItem, self).insertChild(p_int, QTreeWidgetItem)
        QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(LtItem, self).insertChildren(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)


class LtNode(QtGui.QWidget, wgtLtNodeUI.Ui_LineTest):

    def __init__(self, item):
        self._item = item
        self._tab = self._item._tab
        self.mainUi = self._tab.mainUi
        super(LtNode, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup lineTest itemWidget """
        self.setupUi(self)