import sys
from tools.apps import archiver
from lib.qt.scripts import dialog
from PyQt4 import QtGui, QtCore, uic
from tools.apps.archiver.scripts import acCmds


mainClass, uiClass = uic.loadUiType(archiver.uiList['archiver'])
class MainWindow(mainClass, uiClass):

    def __init__(self):
        print "##### Launch Archiver #####"
        self.bankPath = archiver.bankPath
        self.archPath = archiver.archPath
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._setupUi()
        self.rf_mainUi()

    def _setupUi(self):
        """ Setup Archiver main ui """
        self._setupMenu()
        self._setupArchivage()
        self._setupStat()

    def _setupMenu(self):
        """ Setup Archiver menu """
        self.miRefresh.triggered.connect(self.rf_mainUi)
        self.miRefresh.setShortcut("F5")

    def _setupArchivage(self):
        """ Setup Archivage """
        self.tabArchiver.currentChanged.connect(self.rf_mainUi)
        self.twArchivage.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.twArchivage.itemClicked.connect(self.rf_archives)
        self.twArchives.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.twArchives.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.twArchives.itemClicked.connect(self.rf_comment)
        self.bArchivage.clicked.connect(self.on_archivage)

    def _setupStat(self):
        """ Setup Stat """
        self.rbPy.toggled.connect(self.rf_stat)
        self.rbUi.toggled.connect(self.rf_stat)
        self.rbXml.toggled.connect(self.rf_stat)
        self.rbTxt.toggled.connect(self.rf_stat)
        self.rbMel.toggled.connect(self.rf_stat)
        self.rbMa.toggled.connect(self.rf_stat)
        self.rbNk.toggled.connect(self.rf_stat)
        self.bExpand.clicked.connect(self.twStat.expandAll)
        self.bCollapse.clicked.connect(self.twStat.collapseAll)
        self.twStat.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.twStat.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

    def rf_mainUi(self):
        """ Refresh Archiver main ui """
        posX, posY = self.getUiPosition
        if self.getActiveTab == 'Archivage':
            self.rf_archivage()
            self.rf_archives()
            self.rf_comment()
            self.splitArchInfo.setVisible(True)
            self.setGeometry(QtCore.QRect(posX, posY, 700, 500))
        elif self.getActiveTab == 'Stat':
            self.rf_stat()
            self.splitArchInfo.setVisible(False)
            self.setGeometry(QtCore.QRect(posX, posY, 500, 700))

    def rf_archivage(self):
        """ Refresh Archivage QTreeWidget """
        self.twArchivage.clear()
        acCmds.PopulateArchivage(self.bankPath, self.twArchivage).populate()

    def rf_archives(self):
        """ Refresh Archives QTreeWidget """
        self.twArchives.clear()
        self.teComment.clear()
        selItems = self.twArchivage.selectedItems()
        if len(selItems) == 1:
            if selItems[0].type == 'tool':
                acCmds.PopulateArchives(selItems[0], self.twArchives).populate()

    def rf_comment(self):
        """ Refresh Archive Comment QTextEdit """
        self.teComment.clear()
        selItems = self.twArchives.selectedItems()
        if len(selItems) == 1:
            self.teComment.append(selItems[0].comment)

    def rf_stat(self):
        """ Refresh Stat QTreeWidget """
        self.twStat.clear()
        acCmds.PopulateStat(self, self.twStat).populate()

    def on_archivage(self):
        """ Command launch when bArchivage is clicked """
        selItems = self.getArchSelItems
        if len(selItems):
            mess = "Add Comment !!!"
            self.cdArchivage = dialog.CommentDialog(mess, self._archDialogAccept,
                                                          self._archDialogCancel)
            self.cdArchivage.exec_()

    def _archDialogAccept(self):
        """ Command launch when 'Ok' of Comment Dialog is clicked """
        comm = str(self.cdArchivage.teUserText.toPlainText())
        if not len(comm):
            warn = "!!! WARNING: Comment needed for archivage:\nAdd Comment !!!"
            self.cdArchivage.lMessage.setText(warn)
        else:
            selItems = self.getArchSelItems
            acCmds.Archivage(self).archive(selItems, comm)
            self.cdArchivage.close()

    def _archDialogCancel(self):
        """ Command launch when 'Cancel' of Comment Dialog is clicked """
        self.cdArchivage.close()

    @property
    def getUiPosition(self):
        """ Get window position
            @return: posX, posY
            @rtype: int """
        geom = self.geometry()
        posX = geom.x()
        posY = geom.y()
        if posX < 30:
            posX = 30
        if posY < 30:
            posY = 30
        return posX, posY

    @property
    def getActiveTab(self):
        """ Get Archiver active tab
            @return: Active tab text
            @rtype: str """
        return self.tabArchiver.tabText(self.tabArchiver.currentIndex())

    @property
    def getArchSelItems(self):
        """ Get selected tools from 'archivage'
            @return: Selected QTreeWidgetItems
            @rtype: list """
        selItems = []
        allItems = QtGui.QTreeWidgetItemIterator(self.twArchivage,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None:
            while allItems.value():
                item = allItems.value()
                if item.type == 'tool':
                    if item.Active.isChecked():
                        selItems.append(item)
                allItems += 1
        return selItems


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
