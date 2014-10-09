import os
from functools import partial
from appli import prodManager
from lib.qt import textEditor
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.prodManager.ui import tabLineTestUI, wgtLtNodeUI, wgtLtCmtNodeUI, wgtLtShotNodeUI


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
        self.bLtDel.clicked.connect(self.on_delLt)
        self.rf_tabVis()

    def _refresh(self):
        """ Refresh lineTest tabWidget """
        self.log.debug("#-- Refresh Tab LineTest --#")
        selItems = self.mainUi.wgTree.twTree.selectedItems()
        self.twLtTree.clear()
        if selItems:
            if self.mainUi.getSelMode() == 'treeMode':
                if selItems[0].nodeType == 'step':
                    self.rf_tabVis(state=True)
                    self.rf_ltTree()
                else:
                    self.rf_tabVis(state=False)
            elif self.mainUi.getSelMode() == 'stepMode':
                if selItems[0].nodeType == 'shotNode':
                    self.rf_tabVis(state=True)
                    self.rf_ltTree()
                else:
                    self.rf_tabVis(state=False)

    def rf_tabVis(self, state=False):
        """ Refresh project tab ui visibility
            @param state: (bool) : Visibility state """
        self.log.debug("\t Refreshing Tab LineTest Visibility ...")
        self.bLtNew.setEnabled(state)
        self.bLtDel.setEnabled(state)

    def rf_ltTree(self):
        """ Refresh lineTest treeWidget """
        self.log.debug("\t Refreshing Tree LineTest ...")
        selItem = self.mainUi.wgTree.twTree.selectedItems()[0]
        if os.path.exists(selItem._ltPath):
            ltList = os.listdir(selItem._ltPath) or []
            ltList.reverse()
            for lt in ltList:
                ltPath = os.path.join(selItem._ltPath, lt)
                if os.path.isdir(ltPath) and lt.startswith('lt__'):
                    ltFile = os.path.join(ltPath, 'ltData.py')
                    newLtItem = self._newLtItem(ltFile)
                    self.twLtTree.addTopLevelItem(newLtItem)
                    self.twLtTree.setItemWidget(newLtItem, 0, newLtItem._widget)
                    newLtItem.setExpanded(True)
                    comments = newLtItem._widget.ltComments['_order']
                    comments.reverse()
                    for cmt in comments:
                        newCmtItem = self._newCommentItem(ltFile, newLtItem._widget.ltComments[cmt])
                        newLtItem.addChild(newCmtItem)
                        self.twLtTree.setItemWidget(newCmtItem, 0, newCmtItem._widget)

    def on_newLt(self):
        """ Command launch when 'NewLt' QPushButton is clicked """
        item = self.mainUi.wgTree.twTree.selectedItems()[0]
        ltDate = pFile.getDate()
        ltTime = pFile.getTime()
        ltName = "lt__%s__%s" % (ltDate, ltTime)
        ltFile = pFile.conformPath(os.path.join(item._ltPath, ltName, 'ltData.py'))
        ltDict = {'ltTitle': "New LineTest", 'ltDate': ltDate, 'ltTime': ltTime,
                  'ltUser': prodManager.user, 'ltComments': {'_order': []}}
        ltData = []
        for k, v in ltDict.iteritems():
            if isinstance(v, str):
                ltData.append("%s = %r" % (k, v))
            else:
                ltData.append("%s = %s" % (k, v))
        if self.pm.writeLineTest(ltFile, '\n'.join(ltData)):
            self.twLtTree.clear()
            self.rf_ltTree()

    def on_delLt(self):
        """ Command launch when 'DelLt' QPushButton is clicked """
        selItems = self.twLtTree.selectedItems()
        if selItems:
            self.delConf = pQt.ConfirmDialog("Delete ?", ['Delete'], [self.delLt])
            self.delConf.exec_()

    def delLt(self):
        """ Delete selected lineTest """
        ltItem = self.twLtTree.selectedItems()[0]
        if self.pm.deleteLt(os.path.dirname(ltItem._ltFile)):
            self.delConf.close()
            self.twLtTree.clear()
            self._refresh()

    def _newLtItem(self, ltFile):
        """ Create new lineTest QTreeWidgetItem
            @param ltFile: (str) : LtFile absolut path
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem._ltFile = ltFile
        newItem._wgParent = self
        newItem._widget = LtNode(newItem)
        return newItem

    def _newCommentItem(self, ltFile, cmtData):
        """ Create new lineTest QTreeWidgetItem
            @param ltFile: (str) : LtFile absolut path
            @param cmtData: (dict) : Comments data
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem._ltFile = ltFile
        newItem._wgParent = self
        newItem._widget = LtCommentNode(newItem, cmtData)
        return newItem


class LtNode(QtGui.QWidget, wgtLtNodeUI.Ui_LineTest):

    def __init__(self, parent):
        self._parent = parent
        self._ltFile = self._parent._ltFile
        self._tabUi = self._parent._wgParent
        self.mainUi = self._tabUi.mainUi
        self.log = self.mainUi.log
        self.pm = self._tabUi.pm
        for k, v in self.getLtData().iteritems():
            setattr(self, k, v)
        super(LtNode, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup lineTest itemWidget """
        self.setupUi(self)
        self._initStyle()
        self.leTitle.returnPressed.connect(self.on_title)
        self.bAddCmt.clicked.connect(self.on_addComment)
        self._refresh()
        self.dtDate.dateChanged.connect(partial(self.on_dateTime, 'date'))
        self.dtTime.timeChanged.connect(partial(self.on_dateTime, 'time'))

    def _initStyle(self):
        """ Init lineTest node style """
        self.setStyleSheet("background-color: rgb(255,0,0)")
        self.leTitle.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.lUser.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.lUserName.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.lDate.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.dtDate.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.lTime.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.dtTime.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.bAddCmt.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))

    def _refresh(self):
        """ Refresh lineTest node """
        self.leTitle.setText(self.ltTitle)
        self.lUserName.setText(self.ltUser)
        self.dtDate.setDate(QtCore.QDate(int(self.ltDate.split('_')[0]),
                                         int(self.ltDate.split('_')[1]),
                                         int(self.ltDate.split('_')[2])))
        self.dtTime.setTime(QtCore.QTime(int(self.ltTime.split('_')[0]),
                                         int(self.ltTime.split('_')[1]),
                                         int(self.ltTime.split('_')[2])))

    def on_title(self):
        """ Command launched when 'Title' QLineEdit is edited """
        if self.leTitle.isModified():
            dataDict = self.getLtData()
            dataDict['ltTitle'] = str(self.leTitle.text())
            self.writeLt(dataDict)

    def on_dateTime(self, _type):
        """ Command launched when 'Date' or 'time' QDateTime is edited
            @param _type: (str) : 'date' or 'time' """
        self.log.debug("\t Updating LineTest Date Time ...")
        dataDict = self.getLtData()
        if dataDict is not None:
            w, sep, key = self.getTypeParams(_type)
            if not dataDict['lt%s' % key] == str(w.text()).replace(sep, '_'):
                dataDict['lt%s' % key] = str(w.text()).replace(sep, '_')
                if self.writeLt(dataDict):
                    newLtPath = self.pm.editLtDateTime(self._ltFile, dataDict)
                    if newLtPath is not None:
                        self._tabUi.twLtTree.clear()
                        self._tabUi.rf_ltTree()
                        self.log.debug("\t Update LineTest Date successfully done.")

    def on_addComment(self):
        """ Command launched when 'NewCmt' QPushButton is clicked """
        cmtDate = pFile.getDate()
        cmtTime = pFile.getTime()
        cmtName = "%s__%s" % (cmtDate, cmtTime)
        data = self.getLtData()
        data['ltComments']['_order'].append(cmtName)
        data['ltComments'][cmtName] = {'cmtUser': prodManager.user, 'cmtDate': cmtDate,
                                       'cmtTime': cmtTime, 'cmtHtml': "", 'cmtText': ""}
        if self.writeLt(data):
            self._tabUi.twLtTree.clear()
            self._tabUi.rf_ltTree()

    def getTypeParams(self, _type):
        """ Get type params
            @param _type: (str) : 'date' or 'time'
            @return: (object, str, str): QDateTime, separator, key """
        if _type == 'date':
            return self.dtDate, '/', 'Date'
        elif _type == 'time':
            return self.dtTime, ':', 'Time'

    def getLtData(self):
        """ Get ltData from ltFile
            @return: (dict) : LtData """
        if os.path.exists(self._ltFile):
            return pFile.readPyFile(self._ltFile)

    def writeLt(self, dataDict):
        """ Write lineTest
            @param dataDict: (dict) : LineTest data """
        ltData = []
        for k, v in dataDict.iteritems():
            if isinstance(v, str):
                ltData.append("%s = %r" % (k, v))
            else:
                ltData.append("%s = %s" % (k, v))
        result = self.pm.writeLineTest(self._ltFile, '\n'.join(ltData))
        return result


class LtCommentNode(QtGui.QWidget, wgtLtCmtNodeUI.Ui_ltComment):

    def __init__(self, parent, cmtData):
        self._parent = parent
        self._ltFile = self._parent._ltFile
        self._tabUi = self._parent._wgParent
        self.mainUi = self._tabUi.mainUi
        self.log = self.mainUi.log
        self.pm = self._tabUi.pm
        for k, v in cmtData.iteritems():
            setattr(self, k, v)
        self.cmtName = "%s__%s" % (self.cmtDate, self.cmtTime)
        super(LtCommentNode, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup comment node """
        self.setupUi(self)
        self.bEdit.clicked.connect(self.on_edit)
        self.bDelCmt.clicked.connect(self.on_delComment)
        self._refresh()
        self.dtDate.dateChanged.connect(partial(self.on_dateTime, 'date'))
        self.dtTime.timeChanged.connect(partial(self.on_dateTime, 'time'))

    def _refresh(self):
        """ Refresh comment node """
        self.lUserName.setText(self.cmtUser)
        self.dtDate.setDate(QtCore.QDate(int(self.cmtDate.split('_')[0]),
                                         int(self.cmtDate.split('_')[1]),
                                         int(self.cmtDate.split('_')[2])))
        self.dtTime.setTime(QtCore.QTime(int(self.cmtTime.split('_')[0]),
                                         int(self.cmtTime.split('_')[1]),
                                         int(self.cmtTime.split('_')[2])))
        self.teComment.setHtml(self.cmtHtml)

    def on_dateTime(self, _type):
        """ Command launched when 'Date' or 'time' QDateTime is edited
            @param _type: (str) : 'date' or 'time' """
        w, sep, key = self.getTypeParams(_type)
        newValue = str(w.text()).replace(sep, '_')
        if _type == 'date':
            newCmtName = "%s__%s" % (newValue, self.cmtName.split('__')[-1])
        else:
            newCmtName = "%s__%s" % (self.cmtName.split('__')[0], newValue)
        data = self.getLtData()
        cmtDict = data['ltComments']
        index = cmtDict['_order'].index(self.cmtName)
        cmtDict['_order'].pop(index)
        cmtDict['_order'].append(newCmtName)
        cmtDict['_order'].sort()
        cmtDict.pop(self.cmtName)
        cmtDict[newCmtName] = {'cmtUser': prodManager.user,
                               'cmtDate': str(self.dtDate.text()).replace('/', '_'),
                               'cmtTime': str(self.dtTime.text()).replace(':', '_'),
                               'cmtHtml': str(self.teComment.toHtml()),
                               'cmtText': str(self.teComment.toPlainText())}
        self._parent.parent()._widget.writeLt(data)
        self._tabUi.twLtTree.clear()
        self._tabUi.rf_ltTree()

    def on_edit(self):
        """ Command launched when 'Edit' QPushButton is clicked """
        ltNode = self._parent.parent()._widget
        self.cmtEditor = CommentEditor(self.mainUi, self, self._ltFile, ltNode)
        self.mainUi.setEnabled(False)
        self.cmtEditor.show()

    def on_delComment(self):
        """ Command launch when 'DelLt' QPushButton is clicked """
        self.delConf = pQt.ConfirmDialog("Delete ?", ['Delete'], [self.delComment])
        self.delConf.exec_()

    def delComment(self):
        """ Delete selected comment """
        data = self.getLtData()
        data['ltComments']['_order'].pop(data['ltComments']['_order'].index(self.cmtName))
        data['ltComments'].pop(self.cmtName)
        if self._parent.parent()._widget.writeLt(data):
            self.delConf.close()
            self._tabUi.twLtTree.clear()
            self._tabUi.rf_ltTree()

    def getTypeParams(self, _type):
        """ Get type params
            @param _type: (str) : 'date' or 'time'
            @return: (object, str, str): QDateTime, separator, key """
        if _type == 'date':
            return self.dtDate, '/', 'Date'
        elif _type == 'time':
            return self.dtTime, ':', 'Time'

    def getLtData(self):
        """ Get ltData from ltFile
            @return: (dict) : LtData """
        if os.path.exists(self._ltFile):
            return pFile.readPyFile(self._ltFile)


class CommentEditor(textEditor.TextEditor):

    def __init__(self, mainUi, cmtNode, ltFile, ltNode):
        self.mainUi = mainUi
        self._cmtNode = cmtNode
        self._ltFile = ltFile
        self._ltNode = ltNode
        super(CommentEditor, self).__init__()
        self._setupWidget()

    def _setupWidget(self):
        """ Setup comment editor """
        self.bLoadFile.setEnabled(False)
        self.teText.setHtml(str(self._cmtNode.teComment.toHtml()))

    def on_saveFile(self):
        """ Save comment """
        data = self._ltNode.getLtData()
        data['ltComments'][self._cmtNode.cmtName]['cmtHtml'] = str(self.teText.toHtml())
        data['ltComments'][self._cmtNode.cmtName]['cmtText'] = str(self.teText.toPlainText())
        self._cmtNode.teComment.setHtml(self.teText.toHtml())
        if self._ltNode.writeLt(data):
            self.close()

    def closeEvent(self, *args, **kwargs):
        """ Unfreeze mainUi """
        self.mainUi.setEnabled(True)


class LtShotTree(QtGui.QTreeWidget):
    def __init__(self, tab):
        self._tab = tab
        self.log = self._tab.log
        self.mainUi = self._tab.mainUi
        super(LtShotTree, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup lineTest treeWidget """
        self.log.debug("\t Setup Tree ShotLineTest ...")
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.header().setVisible(False)
        self.setIndentation(0)

    def _refresh(self):
        """ Refresh lineTest tabWidget """
        self.log.debug("\t Refreshing Tree ShotLineTest ...")
        self.clear()
        self.rf_columnSize()
        selItem = self.mainUi.wgTree.twTree.selectedItems()[0]
        rootItem = self._getRootItem(selItem)
        if rootItem is not None:
            nc = 0
            newItems = []
            newItem = None
            for n in range(rootItem.childCount()):
                if nc == 0:
                    newItem = LtShotItem(self._tab)
                    newItems.append(newItem)
                nc += 1
                if newItem is not None:
                    newNode = LtShotNode(self._tab, **rootItem.child(n).__dict__)
                    newItem.shotNodes.append(newNode)
                if nc == self._tab.sbLtColumns.value():
                    nc = 0
            self.addTopLevelItems(newItems)

    def rf_columnSize(self):
        """ Adjust shotTree column size """
        self.setColumnCount(self._tab.sbLtColumns.value())
        for n in range(self._tab.sbLtColumns.value()):
            self.setColumnWidth(n, int(self.width() / self._tab.sbLtColumns.value()))

    def _getRootItem(self, selItem):
        """ Get refresh rootItem
            @param selItem: (object) : QTreeWidgetItem
            @return: (object) : QTreeWidgetItem """
        rootItem = None
        if self.mainUi.getSelMode() == 'treeMode':
            if selItem.nodeType == 'step':
                rootItem = selItem.parent().parent()
        if selItem.nodeType == 'shotNode':
            rootItem = selItem.parent()
        if selItem.nodeType == 'container':
            for n in range(selItem.childCount()):
                if selItem.child(n).nodeType == 'shotNode':
                    rootItem = selItem
                    break
        return rootItem

    def addTopLevelItem(self, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(LtShotTree, self).addTopLevelItem(QTreeWidgetItem)
        for n, widget in enumerate(QTreeWidgetItem.shotNodes):
            self.setItemWidget(QTreeWidgetItem, n, widget)
        QTreeWidgetItem.adjustMaxHeight()

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(LtShotTree, self).addTopLevelItems(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            for n, widget in enumerate(QTreeWidgetItem.shotNodes):
                self.setItemWidget(QTreeWidgetItem, n, widget)
            QTreeWidgetItem.adjustMaxHeight()

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(LtShotTree, self).insertTopLevelItem(p_int, QTreeWidgetItem)
        for n, widget in enumerate(QTreeWidgetItem.shotNodes):
            self.setItemWidget(QTreeWidgetItem, n, widget)
        QTreeWidgetItem.adjustMaxHeight()

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(LtShotTree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            for n, widget in enumerate(QTreeWidgetItem.shotNodes):
                self.setItemWidget(QTreeWidgetItem, n, widget)
            QTreeWidgetItem.adjustMaxHeight()


class LtShotItem(QtGui.QTreeWidgetItem):

    def __init__(self, tab):
        self._tab = tab
        self.shotNodes = []
        super(LtShotItem, self).__init__()
    
    def adjustMaxHeight(self):
        """ Adjust QTreeWidgetItem maximum height """
        maxHeight = 0
        for node in self.shotNodes:
            if node.lPreview.height() > maxHeight:
                maxHeight = node.lPreview.height()
        for node in self.shotNodes:
            node.lPreview.setMinimumHeight(maxHeight)
            node.lPreview.setMaximumHeight(maxHeight)


class LtShotNode(QtGui.QWidget, wgtLtShotNodeUI.Ui_LineTestShot):

    def __init__(self, tab, **kwargs):
        self._tab = tab
        self._dataPath = kwargs['_dataPath']
        self._dataFile = kwargs['_dataFile']
        self._ltPath = os.path.join(self._dataPath, 'lt')
        self._ltFile = os.path.join(self._ltPath, 'lt_%s' % os.path.basename(self._dataFile))
        self._ima = None
        self.shotName = kwargs['nodeName']
        super(LtShotNode, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup lineTest itemWidget """
        self.setupUi(self)
        self.bShotName.setText(self.shotName)
        self.qIma = None
        self.rf_shotNodeIma()

    def rf_shotNodeIma(self):
        """ Refresh shotNode preview image """
        self.storeImaFile()
        self.qIma = QtGui.QPixmap(self._ima)
        self.lPreview.setMinimumSize(20, 20)
        self.lPreview.setMaximumSize(20, 20)
        self.lPreview.setPixmap(self.qIma)
        self.resizePreview()

    def storeImaFile(self):
        """ Store image file """
        if self._ima is None:
            self._ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')
            iconeFile = os.path.join(self._dataPath, 'shotNodeIcone.png')
            if os.path.exists(iconeFile):
                self._ima = iconeFile
        if self._ima == '' or self._ima == ' ':
            self._ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')

    def resizePreview(self):
        """ Resize previw icone QLabel """
        ratio = float(self.qIma.width()) / float(self.qIma.height())
        if self.qIma.width() >= self.qIma.height():
            width = self._tab.twLtShotTree.columnWidth(0)
            height = int(float(width) / ratio)
        else:
            height = self._tab.twLtShotTree.columnWidth(0)
            width = int(float(height) / ratio)
        if 'prodManager' in os.path.basename(self._ima):
            height = int(height / 2)
        self.lPreview.setMinimumSize(width, height)
        self.lPreview.setMaximumSize(width, height)
