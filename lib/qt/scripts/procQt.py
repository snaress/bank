from PyQt4 import QtGui


def getAllItems(twTree):
    """ Get all QTreeWidgetItem of given QTreeWidget
        @param twTree: (object) : QTreeWidget object
        @return: (list) : All QTreeWidgetItem list """
    items = []
    allItems = QtGui.QTreeWidgetItemIterator(twTree, QtGui.QTreeWidgetItemIterator.All) or None
    if allItems is not None:
        while allItems.value():
            item = allItems.value()
            items.append(item)
            allItems += 1
    return items

def getTopItems(twTree):
    """ Get all topLevelItems of given QTreeWidget
        @param twTree: (object) : QTreeWidget object
        @return: (list) : All topLevelItem list """
    items = []
    nTop = twTree.topLevelItemCount()
    for n in range(nTop):
        items.append(twTree.topLevelItem(n))
    return items
