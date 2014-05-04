from PyQt4 import QtGui, QtCore


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

def resizePixmap(maxWidth, maxHeight, pixMap, item):
    """ Resize given pixmap of given label
        @param maxWidth: (int) : Pixmap max width
        @param maxHeight: (int) : Pixmap maxHeight
        @param pixMap: (object) : QPixmap
        @param item: (object) : QLabel """
    imaWidth = pixMap.width()
    imaHeight = pixMap.height()
    maxRatio = float(maxWidth)/float(maxHeight)
    imaRatio = float(imaWidth)/float(imaHeight)
    if imaRatio < maxRatio:
        newWidth = int(maxHeight*imaRatio)
        item.setMinimumSize(QtCore.QSize(newWidth, maxHeight))
        item.setMaximumSize(QtCore.QSize(newWidth, maxHeight))
    elif imaRatio == maxRatio:
        item.setMinimumSize(QtCore.QSize(maxWidth, maxHeight))
        item.setMaximumSize(QtCore.QSize(maxWidth, maxHeight))
    elif imaRatio > maxRatio:
        newHeight = int(maxWidth/imaRatio)
        item.setMinimumSize(QtCore.QSize(maxWidth, newHeight))
        item.setMaximumSize(QtCore.QSize(maxWidth, newHeight))
