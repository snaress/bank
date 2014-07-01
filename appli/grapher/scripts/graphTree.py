from appli import grapher
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
        super(GraphTree, self).__init__()
        self._setupUi()
        self._setupMainUi()
        self._popUpMenu()

    def __repr__(self):
        treeDict = {'_order': []}
        allItems = pQt.getAllItems(self)
        for item in allItems:
            nodeDict = item._widget.__repr__()
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
        self.mainUi.miNewGraphNode.triggered.connect(self.on_newGraphNode)
        self.mainUi.miNewGraphNode.setShortcut("N")

    def _popUpMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popUpMenu)
        self.tbGraph = QtGui.QToolBar()
        self.pMenu = QtGui.QMenu(self.mainUi)
        self.miNewGraphNode = self.tbGraph.addAction("New Node", self.on_newGraphNode)
        self.miNewGraphNode.setShortcut("N")
        self.pMenu.addAction(self.miNewGraphNode)

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
            newItem, newWidget = self.new_graphItem(_parent=_parent)
            if _parent is None:
                self.addTopLevelItem(newItem)
                self.setItemWidget(newItem, 0, newWidget)
                newItem._widgetInd = 0
            else:
                _parent.addChild(newItem)
                ind = (_parent._widgetInd + 1)
                self.setItemWidget(newItem, ind, newWidget)
                newItem._widgetInd = ind
        self.rf_graphColumns()

    def on_popUpMenu(self, point):
        """ Show popup menu
            @param point: (object) : QPoint """
        self.pMenu.exec_(self.mapToGlobal(point))

    def on_newGraphNode(self):
        """ Create new graphNode item """
        selItems = self.selectedItems()
        #-- Add Top Item --#
        if not selItems:
            newItem, newWidget = self.new_graphItem()
            self.addTopLevelItem(newItem)
            self.setItemWidget(newItem, 0, newWidget)
            newItem._widgetInd = 0
        #-- Add Child Item --#
        else:
            if len(selItems) > 1:
                self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)
            else:
                newItem, newWidget = self.new_graphItem(_parent=selItems[0])
                selItems[0].addChild(newItem)
                ind = (selItems[0]._widgetInd + 1)
                self.setItemWidget(newItem, ind, newWidget)
                newItem._widgetInd = ind
        self.rf_graphColumns()

    def new_graphItem(self, _parent=None):
        """ New graphNode item
            @return: (object), (object) : QTreeWidgetItem, QWidget """
        newItem = QtGui.QTreeWidgetItem()
        newWidget = GraphNode(self, newItem, _parent)
        newWidget.pbNode.setText(self.newNodeName())
        newItem._widget = newWidget
        return newItem, newWidget

    def newNodeName(self):
        """ Get new default node name
            @return: (str) : default node name """
        allItems = pQt.getAllItems(self)
        if not allItems:
            return 'NewNode_1'
        else:
            names = []
            for item in allItems:
                nodeName = item._widget.__repr__()['nodeName']
                if nodeName.startswith('NewNode_'):
                    names.append(nodeName)
            names.sort()
            return 'NewNode_%s' % (int(names[-1].split('_')[-1]) + 1)

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


graphNodeClass, graphNodeUiClass = uic.loadUiType(grapher.uiList['graphNode'])
class GraphNode(graphNodeClass, graphNodeUiClass, core.Style):

    def __init__(self, tree, item, _parent):
        self.tree = tree
        self.item = item
        self._parent = _parent
        super(GraphNode, self).__init__()
        self._setupUi()

    def __repr__(self):
        if self._parent is None:
            _parentItem = None
        else:
            _parentItem = self._parent._widget.__repr__()['nodeName']
        return {'nodeName': str(self.pbNode.text()), 'nodeParent': _parentItem,
                'nodeEnabled': self.cbNode.isChecked()}

    def _setupUi(self):
        self.setupUi(self)
        self.setStyleSheet(self.graphNodeBgc)
        self.pbExpand.clicked.connect(self.on_expandNode)
        self.cbNode.clicked.connect(self.on_enableNode)

    def on_expandNode(self):
        """ Expand or collapse item """
        if str(self.pbExpand.text()) == '+':
            self.item.setExpanded(True)
            self.pbExpand.setText('-')
            self.tree.rf_graphColumns()
        else:
            self.item.setExpanded(False)
            self.pbExpand.setText('+')

    def on_enableNode(self):
        """ Enable or disable graphNode """
        self.pbNode.setEnabled(self.cbNode.isChecked())
