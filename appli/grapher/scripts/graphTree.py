from appli import grapher
from functools import partial
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import procQt as pQt
from appli.grapher.scripts import core


class GraphTree(QtGui.QTreeWidget):
    """ Class used by the grapherUi for graph tree edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.columns = 10
        self.cpBuffer = None
        super(GraphTree, self).__init__()
        self._setupUi()
        self._setupMainUi()
        self._popUpMenu()

    def __repr__(self):
        treeDict = {'_order': []}
        allItems = pQt.getAllItems(self)
        for item in allItems:
            nodeDict = item.__repr__()
            treeDict['_order'].append(nodeDict['nodeName'])
            treeDict[nodeDict['nodeName']] = nodeDict
        return treeDict

    def __str__(self):
        treeDict = self.__repr__()
        text = ["#-- Graph Tree --#"]
        for node in treeDict['_order']:
            text.append("%s:" % node)
            for k, v in treeDict[node].iteritems():
                text.append("%s %s = %s" % (' '*len(node), k, v))
        return '\n'.join(text)

    def _setupUi(self):
        #-- Columns --#
        self.setHeaderHidden(True)
        self.setColumnCount(self.columns)
        #-- Items --#
        self.setSelectionMode(QtGui.QTreeWidget.ExtendedSelection)
        self.setItemsExpandable(True)
        self.setIndentation(0)
        #-- Drag & Drop --#
        self.setAcceptDrops(False)
        self.setDragEnabled(False)
        self.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.setDefaultDropAction(QtCore.Qt.LinkAction)

    def _setupMainUi(self):
        self.mainUi.miNewGraphNode.triggered.connect(self.on_newNode)
        self.mainUi.miNewGraphNode.setShortcut("Alt+N")
        self.mainUi.miDelGraphNode.triggered.connect(self.on_delNode)
        self.mainUi.miDelGraphNode.setShortcut("Del")
        self.mainUi.miCopyNodes.triggered.connect(self.on_copyNode)
        self.mainUi.miCopyNodes.setShortcut("Ctrl+C")
        self.mainUi.miPasteNodes.triggered.connect(self.on_pasteNode)
        self.mainUi.miPasteNodes.setShortcut("Ctrl+V")

    def _popUpMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popUpMenu)
        self.tbGraph = QtGui.QToolBar()
        self.pMenu = QtGui.QMenu(self.mainUi)
        #-- New Graph Node --#
        self.miNewGraphNode = self.tbGraph.addAction("New Node", self.on_newNode)
        self.miNewGraphNode.setShortcut("Alt+N")
        self.pMenu.addAction(self.miNewGraphNode)
        #-- Delete Graph Node --#
        self.miDelGraphNode = self.tbGraph.addAction("Delete", self.on_delNode)
        self.miDelGraphNode.setShortcut("Del")
        self.pMenu.addAction(self.miDelGraphNode)
        self.pMenu.addSeparator()
        #-- Cut Nodes --#
        self.miCutNodes = self.tbGraph.addAction("Cut")
        self.miCutNodes.setShortcut("Ctrl+X")
        self.pMenu.addAction(self.miCutNodes)
        #-- Copy Nodes --#
        self.miCopyNodes = self.tbGraph.addAction("Copy", self.on_copyNode)
        self.miCopyNodes.setShortcut("Ctrl+C")
        self.pMenu.addAction(self.miCopyNodes)
        #-- Paste Nodes --#
        self.miPasteNodes = self.tbGraph.addAction("Paste", self.on_pasteNode)
        self.miPasteNodes.setShortcut("Ctrl+V")
        self.pMenu.addAction(self.miPasteNodes)
        #-- Instanciate Nodes --#
        self.miInstanceNodes = self.tbGraph.addAction("Instanciate")
        self.miInstanceNodes.setShortcut("Shift+C")
        self.pMenu.addAction(self.miInstanceNodes)
        self.pMenu.addSeparator()
        #-- Push Nodes --#
        self.miPushNodes = self.tbGraph.addAction("Push")
        self.miPushNodes.setShortcut("Ctrl+P")
        self.pMenu.addAction(self.miPushNodes)
        #-- Pull Nodes --#
        self.miPullNodes = self.tbGraph.addAction("Pull")
        self.miPullNodes.setShortcut("Shift+P")
        self.pMenu.addAction(self.miPullNodes)

    def addTopLevelItem(self, QTreeWidgetItem):
        super(GraphTree, self).addTopLevelItem(QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        super(GraphTree, self).addTopLevelItems(list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self.setItemWidget(item, 0, item._widget)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        super(GraphTree, self).insertTopLevelItem(p_int, QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        super(GraphTree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self.setItemWidget(item, 0, item._widget)

    def rf_graphBgc(self):
        """ Refresh graph background color """
        if not self.mainUi._lock:
            self.setStyleSheet(self.mainUi.graphBgc)
        else:
            self.setStyleSheet(self.mainUi.lockColor)

    def rf_graphColumns(self):
        """ Refresh graph columns size """
        for column in range(self.columns):
            self.resizeColumnToContents(column)

    def rf_graph(self):
        """ Refresh graph tree """
        self.resetGraph()
        for node in self.grapher.graphTree['_order']:
            nodeDict = self.grapher.graphTree[node]
            _parent = self.getItemFromNodeName(nodeDict['nodeParent'])
            self.addGraphNode(nodeDict['nodeName'], nodeDict['nodeEnabled'], _parent)
        self.rf_graphColumns()

    def on_popUpMenu(self, point):
        """ Show popup menu
            @param point: (object) : QPoint """
        self.pMenu.exec_(self.mapToGlobal(point))

    def on_newNode(self):
        """ Command launch when menuItem 'New Node' is clicked
            @return: (object) : QTreeWidgetItem """
        selItems = self.selectedItems()
        if not len(selItems) > 1:
            if selItems:
                newItem = self.addGraphNode('NewNode', nodeParent=selItems[0])
            else:
                newItem = self.addGraphNode('NewNode', nodeParent=None)
            return newItem
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)

    def on_delNode(self):
        """ Command launch when menuItem 'Delete Node' is clicked """
        selItems = self.selectedItems()
        if selItems:
            self.confUi = pQt.ConfirmDialog('Delete Selected Nodes ?', ['Delete'],
                                            [partial(self.delGraphNodes, selItems)])
            self.confUi.exec_()

    def on_cutNode(self):
        """ Store selected items dict and remove selection """
        self.on_copyNode()
        selItems = self.selectedItems()

    def on_copyNode(self):
        """ Store selected items dict """
        selItems = self.selectedItems()
        if selItems:
            self.cpBuffer = []
            for item in selItems:
                self.cpBuffer.append(item.__repr__())

    def on_pasteNode(self):
        """ Paste stored items dict """
        selItems = self.selectedItems()
        if not len(selItems) > 1:
            if self.cpBuffer is not None:
                for nodeDict in self.cpBuffer:
                    if selItems:
                        parentItem = selItems[0]
                    else:
                        parentItem = None
                    valideName = self._checkNodeName(nodeDict['nodeName'])
                    self.addGraphNode(valideName, nodeEnable=nodeDict['nodeEnabled'],
                                      nodeParent=parentItem)
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)

    def addGraphNode(self, nodeName, nodeEnable=True, nodeParent=None):
        """ Add new QTreeWidgetItem
            @param nodeName: (str) : New node name
            @param nodeEnable: (bool) : New node state
            @param nodeParent: (object) : Parent QTreeWidgetItem
            @return: (object) : QTreeWidgetItem """
        valideName = self._checkNodeName(nodeName)
        newItem = GraphItem(self, nodeParent)
        if nodeParent is None:
            self.addTopLevelItem(newItem)
        else:
            nodeParent.addChild(newItem)
        newItem._widget.setGraphNodeName(valideName)
        newItem._widget.setGraphNodeEnabled(nodeEnable)
        self.rf_graphColumns()
        return newItem

    def delGraphNodes(self, QTreeWidgetItems):
        """ Delete given QTreeWidgetItems
            @param QTreeWidgetItems: (list) : List of QTreeWidgetItem to remove"""
        for item in QTreeWidgetItems:
            if item.parent() is None:
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))
            else:
                item.parent().removeChild(item)
        try:
            self.confUi.close()
        except:
            pass

    def _checkNodeName(self, nodeName):
        """ Check if new name is valide
            @param nodeName: (str) : Node name
            @return: (str) : Valide node name """
        #-- Check Suffixe --#
        if len(nodeName.split('_')) < 2:
            tmpName = '%s_1' % nodeName
            tmpBaseName = nodeName
        else:
            if not nodeName.split('_')[-1].isdigit():
                tmpName = '%s_1' % nodeName
                tmpBaseName = nodeName
            else:
                tmpName = nodeName
                tmpBaseName = '_'.join(nodeName.split('_')[:-1])
        #-- Get Valide Name --#
        allItems = pQt.getAllItems(self)
        if not allItems:
            return tmpName
        else:
            indexes = []
            nodeExists = False
            for item in allItems:
                treeNodeName = item._widget.__repr__()['nodeName']
                if treeNodeName == tmpName:
                    nodeExists = True
                if treeNodeName.startswith('%s_' % tmpBaseName):
                    indexes.append(int(treeNodeName.split('_')[-1]))
            if not nodeExists:
                return nodeName
            else:
                return '%s_%s' % (tmpBaseName, (max(indexes) + 1))

    def getItemFromNodeName(self, nodeName):
        """ Get QTreeWidgetItem from given nodeName
            @param nodeName: (str) : Node name
            @return: (object) : QTreeWidgetItem """
        if nodeName is None:
            return None
        else:
            allItems = pQt.getAllItems(self)
            for item in allItems:
                if item._widget.__repr__()['nodeName'] == nodeName:
                    return item

    def resetGraph(self):
        """ Reset graph tree """
        self.clear()


class GraphItem(QtGui.QTreeWidgetItem):

    def __init__(self, tree, parent):
        self._tree = tree
        self._parent = parent
        self._widget = GraphNode(self._tree, self)
        if self._parent is None:
            self._widgetIndex = 0
        else:
            self._widgetIndex = (self._parent._widgetIndex + 1)
        super(GraphItem, self).__init__()

    def __repr__(self):
        itemDict = self._widget.__repr__()
        if self.parent() is None:
            itemDict['nodeParent'] = None
        else:
            parentName = self.parent()._widget.__repr__()['nodeName']
            itemDict['nodeParent'] = parentName
        return itemDict

    def addChild(self, QTreeWidgetItem):
        super(GraphItem, self).addChild(QTreeWidgetItem)
        self._tree.setItemWidget(QTreeWidgetItem, (self._widgetIndex + 1), QTreeWidgetItem._widget)

    def addChildren(self, list_of_QTreeWidgetItem):
        super(GraphItem, self).addChildren(list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self._tree.setItemWidget(item, (self._widgetIndex + 1), item._widget)

    def insertChild(self, p_int, QTreeWidgetItem):
        super(GraphItem, self).insertChild(p_int, QTreeWidgetItem)
        self._tree.setItemWidget(QTreeWidgetItem, (self._widgetIndex + 1), QTreeWidgetItem._widget)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        super(GraphItem, self).insertChildren(p_int, list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self._tree.setItemWidget(item, (self._widgetIndex + 1), item._widget)


graphNodeClass, graphNodeUiClass = uic.loadUiType(grapher.uiList['graphNode'])
class GraphNode(graphNodeClass, graphNodeUiClass, core.Style):

    def __init__(self, tree, item):
        self._tree = tree
        self._item = item
        super(GraphNode, self).__init__()
        self._setupUi()

    def __repr__(self):
        return {'nodeName': str(self.pbNode.text()),
                'nodeEnabled': self.cbNode.isChecked()}

    def _setupUi(self):
        self.setupUi(self)
        self.setStyleSheet(self.graphNodeBgc)
        self.pbExpand.clicked.connect(self.on_expandNode)
        self.cbNode.clicked.connect(self.on_enableNode)

    def on_expandNode(self):
        """ Expand or collapse item """
        if str(self.pbExpand.text()) == '+':
            self._item.setExpanded(True)
            self.pbExpand.setText('-')
            self._tree.rf_graphColumns()
        else:
            self._item.setExpanded(False)
            self.pbExpand.setText('+')

    def on_enableNode(self):
        """ Enable or disable graphNode """
        self.pbNode.setEnabled(self.cbNode.isChecked())

    def setGraphNodeName(self, nodeName):
        """ Edit graphNode button name
            @param nodeName: (str) : Node name"""
        self.pbNode.setText(nodeName)

    def setGraphNodeEnabled(self, nodeEnable):
        """ Edit graphNode checkBox state
            @param nodeEnable: (bool) : Node state """
        self.cbNode.setChecked(nodeEnable)
