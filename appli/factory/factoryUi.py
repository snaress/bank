import os, sys
from PyQt4 import QtGui
from lib.qt import preview
from functools import partial
from lib.qt import procQt as pQt
from appli.factory import factory
from lib.system import procFile as pFile
from appli.factory.ui import factoryUI, wgtThumbnailUI


class FactoryUi(QtGui.QMainWindow, factoryUI.Ui_factory, pQt.Style):
    """ FactoryUi MainWindow
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="Factory-ui", level=logLvl)
        self.log.info("#-- Launching Factory --#")
        self.factory = factory.Factory()
        super(FactoryUi, self).__init__()
        self._setupUi()
        self.rf_tree()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup main ui """
        self.log.debug("#-- Setup Factory Ui --#")
        self.setupUi(self)
        self.setStyleSheet(self.applyStyle(styleName='darkOrange'))
        self.mPreview.aboutToShow.connect(self.rf_previewMenu)
        self.miCreateSelPreviews.triggered.connect(partial(self.on_createIcone, 'sel', 'preview'))
        self.miCreateAllPreviews.triggered.connect(partial(self.on_createIcone, 'all', 'preview'))
        self.mThumbnail.aboutToShow.connect(self.rf_thumbnailMenu)
        self.miCreateSelIcons.triggered.connect(partial(self.on_createIcone, 'sel', 'icon'))
        self.miCreateAllIcons.triggered.connect(partial(self.on_createIcone, 'all', 'icon'))
        self.wgPreview = Preview(self)
        self.vlLeftZone.insertWidget(0, self.wgPreview)
        self.rbTexture.clicked.connect(self.on_switch)
        self.rbShader.clicked.connect(self.on_switch)
        self.rbStockShot.clicked.connect(self.on_switch)
        self.twTree.itemClicked.connect(self.rf_thumbnail)
        self.sbColumns.editingFinished.connect(self.rf_thumbnail)
        self.twThumbnail.header().setStretchLastSection(False)

    def rf_tree(self):
        """ Refresh factory tree """
        self.twTree.clear()
        selTree = getattr(self.factory, self.getSelTree())
        if selTree is not None:
            for node in getattr(selTree, 'tree'):
                newItem = self._newTreeItem(node)
                self.twTree.addTopLevelItem(newItem)
                for child in node._children:
                    newChild = self._newTreeItem(child)
                    newItem.addChild(newChild)

    def rf_thumbnail(self):
        """ Refresh factory thumbnail """
        self.twThumbnail.clear()
        self.rf_thumbnailColumns()
        selTreeItems = self.twTree.selectedItems()
        if selTreeItems:
            node = selTreeItems[0].node
            if node.nodeType == 'subCategory':
                NC = self.twThumbnail.columnCount()
                nc = 0
                for child in node._children:
                    if nc == 0:
                        newItem = self._newThumbnailItem()
                        self.twThumbnail.addTopLevelItem(newItem)
                    newPreview = Thumbnail(self, newItem, child)
                    newItem._widgets.append(newPreview)
                    self.twThumbnail.setItemWidget(newItem, nc, newPreview)
                    nc += 1
                    if nc == NC:
                        nc = 0

    def rf_previewMenu(self):
        """ Refresh preview menu """
        self.miCreateSelPreviews.setEnabled(False)
        self.miCreateAllPreviews.setEnabled(False)
        selItems = self.twTree.selectedItems()
        if selItems:
            if selItems[0].node.nodeType == 'subCategory':
                self.miCreateAllPreviews.setEnabled(True)
                if self.getSelThumbnails():
                    self.miCreateSelPreviews.setEnabled(True)

    def rf_thumbnailMenu(self):
        """ Refresh thumbnail menu """
        self.miCreateSelIcons.setEnabled(False)
        self.miCreateAllIcons.setEnabled(False)
        selItems = self.twTree.selectedItems()
        if selItems:
            if selItems[0].node.nodeType == 'subCategory':
                self.miCreateAllIcons.setEnabled(True)
                if self.getSelThumbnails():
                    self.miCreateSelIcons.setEnabled(True)

    def rf_thumbnailColumns(self):
        """ Refresh factory thumbnail columns """
        self.twThumbnail.setColumnCount(self.sbColumns.value())
        for n in range(self.twThumbnail.columnCount()):
            self.twThumbnail.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)

    def on_switch(self):
        """ Command launched when treeSwitch QRadioButton is clicked """
        self.rf_tree()
        self.rf_thumbnail()

    def on_createIcone(self, mode, _type):
        """ Command launched when 'Create Icons' menuItems are clicked
            @param mode: (str) : 'sel' or 'all'
            @param _type: (str) : 'icon' or 'preview' """
        if mode == 'sel':
            wList = self.getSelThumbnails()
        else:
            wList = self.getAllThumbnails()
        for w in wList:
            self.factory.ud_thumbnailImages(w.node.nodePath, _type)

    def getSelTree(self):
        """ Get selected tree
            @return: (str) : Selected tree """
        if self.rbTexture.isChecked():
            return 'texture'
        elif self.rbShader.isChecked():
            return 'shader'
        elif self.rbStockShot.isChecked():
            return 'stockShot'

    def getAllThumbnails(self):
        """ Get all thumbnail widgets
            @return: (list) : Thumbnail QWidgets list """
        allItems = pQt.getTopItems(self.twThumbnail)
        allWidgets = []
        for item in allItems:
            for w in item._widgets:
                allWidgets.append(w)
        return allWidgets

    def getSelThumbnails(self):
        """ Get selected thumbnail widgets
            @return: (list) : Thumbnail QWidgets list """
        selWidgets = []
        for w in self.getAllThumbnails():
            if w.cbPreview.isChecked():
                selWidgets.append(w)
        return selWidgets

    @staticmethod
    def _newTreeItem(node):
        """ Create new treeItem
            @param node: (object) : Factory node
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, node.nodeName)
        newItem.node = node
        return newItem

    @staticmethod
    def _newThumbnailItem():
        """ Create new thumbnailItem
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem._widgets = []
        return newItem


class Thumbnail(QtGui.QWidget, wgtThumbnailUI.Ui_thumbnail):

    def __init__(self, mainUi, item, node):
        self.mainUi = mainUi
        self.noImage = os.path.join(self.mainUi.factory.libPath, 'ima', 'noImage_100.jpg')
        self._item = item
        self.node = node
        super(Thumbnail, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup widget """
        self.setupUi(self)
        self.bPreview.clicked.connect(self.on_icon)
        self.rf_icon()

    @property
    def iconFile(self):
        """ Get icon file
            @return: (str) : Icon absolute path """
        iconPath = os.path.join(os.path.dirname(self.node.nodePath), '_icon')
        return pFile.conformPath(os.path.join(iconPath, '%s.png' % self.node.nodeName))

    @property
    def previewFile(self):
        """ Get preview file
            @return: (str) : Preview absolute path """
        previewPath = os.path.join(os.path.dirname(self.node.nodePath), '_preview')
        return pFile.conformPath(os.path.join(previewPath, '%s.png' % self.node.nodeName))

    def rf_icon(self):
        """ Refresh thumbnail icon """
        #-- Icone --#
        if not os.path.exists(self.iconFile):
            self.bPreview.setIcon(QtGui.QIcon(self.noImage))
        else:
            self.bPreview.setIcon(QtGui.QIcon(self.iconFile))
        #-- Preview --#
        if not os.path.exists(self.previewFile):
            self.cbPreview.setText("No Preview")
        else:
            self.cbPreview.setText("")

    def on_icon(self):
        """ Command launched when thumbnail icon is clicked """
        if os.path.exists(self.previewFile):
            self.mainUi.wgPreview.previewFile = self.previewFile
            self.mainUi.wgPreview.imagePath = self.node.nodePath
        else:
            self.mainUi.wgPreview.previewFile = None
            self.mainUi.wgPreview.imagePath = None
        self.mainUi.wgPreview.rf_preview()
        self.mainUi.wgPreview.rf_btnsVisibility()


class Preview(preview.Preview):

    def __init__(self, mainUi):
        self.mainUi = mainUi
        super(Preview, self).__init__(widgetSize=(250, 250), previewSize=(245, 245))
        self._setupWidget()

    def _setupWidget(self):
        """ Setup widget """
        self.qfButtonsDn.setVisible(False)
        self.bImage.setEnabled(False)
        self.bSequence.setEnabled(False)
        self.bMovie.setEnabled(False)


def launch(logLvl='info'):
    """ Factory launcher
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """
    app = QtGui.QApplication(sys.argv)
    window = FactoryUi(logLvl=logLvl)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()