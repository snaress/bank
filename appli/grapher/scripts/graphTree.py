from PyQt4 import QtGui, QtCore
from lib.qt.scripts import procQt as pQt


class GraphTree(QtGui.QTreeWidget):
    """ Class used by the grapherUi for graph tree edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.columns = 10
        super(GraphTree, self).__init__()
        self._setupUi()

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

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        self.setHeaderHidden(True)
        self.setColumnCount(self.columns)
        self.setSelectionMode(QtGui.QTreeWidget.ExtendedSelection)
        self.setItemsExpandable(True)
        self.setIndentation(0)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.itemClicked.connect(self.rf_graphColumns)

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

    def resetGraph(self):
        """ Reset graph tree """
        self.clear()
