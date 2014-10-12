import os
from functools import partial
from appli import prodManager
from lib.qt import textEditor
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.prodManager.ui import tabLineTestUI, wgtLtNodeUI, wgtLtShotNodeUI, dialLtEditorUI


class LineTestTab(QtGui.QWidget, tabLineTestUI.Ui_ltTab):
    """ LineTest ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(LineTestTab, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup lineTest tabWidget """
        self.setupUi(self)
        self.log.debug("#-- Setup Tab LineTest --#")
        self.bLtNew.clicked.connect(self.on_newLt)
        self.bLtDel.clicked.connect(self.on_delLt)
        self.twLtTree.itemClicked.connect(self.on_ltNode)
        self.sbLtColumns.editingFinished.connect(self.rf_shotTree)
        self.rf_tabVis()

    def _refresh(self):
        """ Refresh lineTest tabWidget """
        self.log.debug("#-- Refresh Tab LineTest --#")
        selItems = self.mainUi.wgTree.twTree.selectedItems()
        if selItems:
            self.twLtTree.clear()
            self.twShotTree.clear()
            if self.mainUi.getSelMode() == 'treeMode':
                if selItems[0].nodeType == 'step':
                    self.rf_tabVis(state=True)
                    self.rf_ltTree()
                    self.rf_shotTree()
                else:
                    self.rf_tabVis(state=False)
            elif self.mainUi.getSelMode() == 'stepMode':
                if selItems[0].nodeType == 'shotNode':
                    self.rf_tabVis(state=True)
                    self.rf_ltTree()
                    self.rf_shotTree()
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
        self.twLtTree.clear()
        selItem = self.mainUi.wgTree.twTree.selectedItems()[0]
        if os.path.exists(selItem._ltPath):
            ltList = os.listdir(selItem._ltPath) or []
            ltList.reverse()
            for lt in ltList:
                ltPath = os.path.join(selItem._ltPath, lt)
                if os.path.isdir(ltPath) and lt.startswith('lt__'):
                    ltFile = os.path.join(ltPath, 'ltData.py')
                    newLtItem = self._newLtItem(selItem._dataFile, ltFile)
                    self.twLtTree.addTopLevelItem(newLtItem)
                    self.twLtTree.setItemWidget(newLtItem, 0, newLtItem._widget)
                    newLtItem.setExpanded(True)
                    comments = newLtItem._widget.ltComments['_order']
                    comments.reverse()
                    for cmt in comments:
                        newCmtItem = self._newCommentItem(ltFile, newLtItem._widget.ltComments[cmt])
                        newLtItem.addChild(newCmtItem)
                        self.twLtTree.setItemWidget(newCmtItem, 0, newCmtItem._widget)

    def rf_shotTree(self):
        """ Refresh ltShots treeWidget """
        self.log.debug("\t Refreshing Tree Shots ...")
        self.twShotTree.clear()
        self.rf_shotTreeColumnSize()
        selItem = self.mainUi.wgTree.twTree.selectedItems()[0]
        rootItem = self.getRootItem(selItem)
        if rootItem is not None:
            newItems = self._initShotItem(rootItem, selItem._step)
            self.twShotTree.addTopLevelItems(newItems)
            for item in newItems:
                for n, widget in enumerate(item.shotNodes):
                    self.twShotTree.setItemWidget(item, n, widget)
                self.adjustShotNodeHeight(item)

    def rf_shotTreeColumnSize(self):
        """ Adjust shotTree column size """
        self.twShotTree.setColumnCount(self.sbLtColumns.value())
        for n in range(self.sbLtColumns.value()):
            self.twShotTree.setColumnWidth(n, int(self.twShotTree.width() / self.sbLtColumns.value()))

    def on_newLt(self):
        """ Command launch when 'NewLt' QPushButton is clicked """
        item = self.mainUi.wgTree.twTree.selectedItems()[0]
        ltDate = pFile.getDate()
        ltTime = pFile.getTime()
        ltName = "lt__%s__%s" % (ltDate, ltTime)
        ltFile = pFile.conformPath(os.path.join(item._ltPath, ltName, 'ltData.py'))
        ltDict = {'ltTitle': "New LineTest", 'ltDate': ltDate, 'ltTime': ltTime,
                  'ltUser': prodManager.user, 'ltImaPath': "", 'ltSeqPath': "", 'ltMovPath': "",
                  'ltComments': {'_order': []}}
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

    def on_ltNode(self):
        """ Command launched when 'ltNode' QTreeWidgetItem is clicked """
        selItems = self.twLtTree.selectedItems()
        if selItems:
            iconeFile = os.path.join(os.path.dirname(selItems[0]._ltFile), 'previewIcone.png')
            if os.path.exists(iconeFile):
                self.mainUi.wgPreview._ima = iconeFile
            else:
                self.mainUi.wgPreview._ima = None
            ltData = selItems[0]._widget.getLtData()
            self.mainUi.wgPreview.pIma = ltData['ltImaPath']
            self.mainUi.wgPreview.pSeq = ltData['ltSeqPath']
            self.mainUi.wgPreview.pMov = ltData['ltMovPath']
            if os.path.exists(selItems[0]._dataFile):
                data = pFile.readPyFile(selItems[0]._dataFile)
                self.mainUi.wgPreview.pXplor = data['workDir']
                self.mainUi.wgPreview.pXterm = data['workDir']
            self.mainUi.wgPreview.rf_preview()

    def delLt(self):
        """ Delete selected lineTest """
        ltItem = self.twLtTree.selectedItems()[0]
        if self.pm.deleteLt(os.path.dirname(ltItem._ltFile)):
            self.delConf.close()
            self.twLtTree.clear()
            self._refresh()

    def getRootItem(self, selItem):
        """ Get given item's rootItem
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

    def adjustShotNodeHeight(self, item):
        """ Adjust QTreeWidgetItem maximum height
            @param item: (object) : QTreeWidgetItem """
        maxHeight = 0
        for node in item.shotNodes:
            if node.lPreview.height() > maxHeight:
                maxHeight = node.lPreview.height()
        for node in item.shotNodes:
            node.lPreview.setMinimumHeight(maxHeight)
            node.lPreview.setMaximumHeight(maxHeight)

    def _initShotItem(self, rootItem, step):
        """ Initialize shotItem
            @param rootItem: (object) : QTreeWidgetItem
            @return: (list) : List of QTreeWidgetItems """
        nc = 0
        newItems = []
        newItem = None
        for n in range(rootItem.childCount()):
            if nc == 0:
                newItem = self._newShotItem()
                newItems.append(newItem)
            nc += 1
            if newItem is not None:
                newNode = LtShotNode(self, step, **rootItem.child(n).__dict__)
                newItem.shotNodes.append(newNode)
            if nc == self.sbLtColumns.value():
                nc = 0
        return newItems

    def _newLtItem(self, dataFile, ltFile):
        """ Create new lineTest QTreeWidgetItem
            @param dataFile: (str) : DataFile absolut path
            @param ltFile: (str) : LtFile absolut path
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem._dataFile = dataFile
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

    def _newShotItem(self):
        """ Create new ltShot QTreeWidgetItem
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.shotNodes = []
        newItem._wgParent = self
        return newItem


class LtNode(QtGui.QWidget, wgtLtNodeUI.Ui_ltNode):

    def __init__(self, parent):
        self._parent = parent
        self._dataFile = self._parent._dataFile
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
        self.bEdit.clicked.connect(self.on_editLt)
        self.bEdition.setText("AddCmt")
        self.bEdition.clicked.connect(self.on_addComment)
        self.teComment.setVisible(False)
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
        self.bEdit.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.bEdition.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))

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

    def on_editLt(self):
        """ Command launched when 'edit' QPushButton is clicked """
        self.dialLt = LineTestEditor(self.mainUi, self)
        self.dialLt.exec_()

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


class LtCommentNode(QtGui.QWidget, wgtLtNodeUI.Ui_ltNode):

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
        self.leTitle.setVisible(False)
        self.bEdit.clicked.connect(self.on_edit)
        self.bEdition.setText("DelCmt")
        self.bEdition.clicked.connect(self.on_delComment)
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
        self.rf_commentSize()

    def rf_commentSize(self):
        """ Refresh QTextEdit sizeHeight """
        nLines = len(self.cmtText.split('\n'))
        height = (12 + (nLines * 20))
        if height < 50:
            height = 50
        elif height > 250:
            height = 250
        self.teComment.setMinimumHeight(height)
        self.teComment.setMaximumHeight(height)

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


class LtShotNode(QtGui.QWidget, wgtLtShotNodeUI.Ui_LineTestShot):

    def __init__(self, tab, step, **kwargs):
        self._tab = tab
        self.pm = self._tab.pm
        self.mainUi = self._tab.mainUi
        self.log = self.mainUi.log
        self._dataPath = kwargs['_dataPath']
        self._dataFile = kwargs['_dataFile']
        self._step = step
        self._ltPath = os.path.join(self._dataPath, 'lt', self._step)
        self._taskFile = pFile.conformPath(os.path.join(self._ltPath, 'ltTask.py'))
        self._ima = None
        self.shotName = kwargs['nodeName']
        super(LtShotNode, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup lineTest itemWidget """
        self.setupUi(self)
        self.bShotName.setText(self.shotName)
        self.bShotName.clicked.connect(self.on_shotNode)
        self.qIma = None
        self.rf_shotNodeIma()
        self.rf_task()
        self._popUpMenu()

    def _popUpMenu(self):
        """ Init shotNode popUp menu """
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popUpMenu)
        self.tbMenu = QtGui.QToolBar()
        self.pMenu = QtGui.QMenu(self)
        self.menuTask = self._menuTask()
        self.pMenu.addMenu(self.menuTask)

    def _menuTask(self):
        """ Create menu 'Task'
            @return: (object) : QMenu """
        taskDict = self.pm.prodTasks
        menuTask = QtGui.QMenu(self.pMenu)
        menuTask.setTitle("Task")
        for task in taskDict['_order']:
            newMenuItem = self.tbMenu.addAction(task, partial(self.on_task, task))
            newMenuItem.setChecked(True)
            menuTask.addAction(newMenuItem)
        return menuTask

    def rf_shotNodeIma(self):
        """ Refresh shotNode preview image """
        self.storeImaFile()
        self.qIma = QtGui.QPixmap(self._ima)
        self.lPreview.setMinimumSize(20, 20)
        self.lPreview.setMaximumSize(20, 20)
        self.lPreview.setPixmap(self.qIma)
        self.resizePreview()

    def rf_task(self):
        """ Refresh current task """
        taskDict = self.pm.prodTasks
        if not os.path.exists(self._taskFile):
            self.lTask.setText("ToDo")
            col1 = taskDict['ToDo']['color']
        else:
            taskData = pFile.readPyFile(self._taskFile)
            self.lTask.setText(taskData['task'])
            col1 = taskDict[taskData['task']]['color']
        checkCol = float((col1[0] + col1[1] + col1[2]) / 3)
        if checkCol > float(255 / 3):
            col2 = (30, 30, 30)
        else:
            col2 = (220, 220, 220)
        self.lTask.setStyleSheet("background-color:rgb(%s, %s, %s);"
                                 "color:rgb(%s, %s, %s)" % (col1[0], col1[1], col1[2],
                                                            col2[0], col2[1], col2[2]))

    def on_popUpMenu(self, point):
        """ Show popUp menu
            @param point: (object) : QPoint """
        selItems = self.mainUi.wgTree.twTree.selectedItems()
        self.pMenu.setEnabled(False)
        if selItems:
            item = selItems[0]
            if self.mainUi.getSelMode() == 'treeMode':
                if item.nodeType == 'step':
                    if item._step == self._step and item.parent().nodeName == self.shotName:
                        self.pMenu.setEnabled(True)
            else:
                if item.nodeType == 'shotNode':
                    if item._step == self._step and item.nodeName == self.shotName:
                        self.pMenu.setEnabled(True)
        self.pMenu.exec_(self.mapToGlobal(point))

    def on_shotNode(self):
        """ Command launched when a shotNode is clicked """
        allItems = pQt.getAllItems(self.mainUi.wgTree.twTree)
        itemToSelect = None
        for item in allItems:
            if self.mainUi.getSelMode() == 'treeMode':
                if item.nodeType == 'step':
                    if item._step == self._step and item.parent().nodeName == self.shotName:
                        itemToSelect = item
                        break
            elif self.mainUi.getSelMode() == 'stepMode':
                if item.nodeType == 'shotNode':
                    if item._step == self._step and item.nodeName == self.shotName:
                        itemToSelect = item
                        break
        if itemToSelect is not None:
            self.mainUi.wgTree.twTree.setCurrentItem(itemToSelect)
            self._tab.rf_ltTree()

    def on_task(self, task):
        """ Command launched when task QMenuItem is clicked
            @param task: (str) : task name """
        taskTxt = ["task = %r" % task, "user = %r" % prodManager.user,
                   "date = %r" % pFile.getDate(), "time = %r" % pFile.getTime()]
        try:
            pFile.writeFile(self._taskFile, '\n'.join(taskTxt))
            self.log.info("Write task for %s" % self.shotName)
            self.rf_task()
        except:
            self.log.error("Can not write task for %s" % self.shotName)

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
            width = self._tab.twShotTree.columnWidth(0)
            height = int(float(width) / ratio)
        else:
            height = self._tab.twShotTree.columnWidth(0)
            width = int(float(height) / ratio)
        if 'prodManager' in os.path.basename(self._ima):
            height = int(height / 2)
        self.lPreview.setMinimumSize(width, height)
        self.lPreview.setMaximumSize(width, height)


class LineTestEditor(QtGui.QDialog, dialLtEditorUI.Ui_editLt):

    def __init__(self, mainUi, ltNode):
        self.mainUi = mainUi
        self.ltNode = ltNode
        self.pm = self.ltNode.pm
        super(LineTestEditor, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup widget """
        self.setupUi(self)
        self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.bImaOpen.clicked.connect(partial(self.on_open, 'ima'))
        self.bSeqOpen.clicked.connect(partial(self.on_open, 'seq'))
        self.bMovOpen.clicked.connect(partial(self.on_open, 'mov'))
        self.bSave.clicked.connect(self.on_save)
        self.bCancel.clicked.connect(self.close)
        self._refresh()

    def _refresh(self):
        """ Refresh widget """
        ltData = self.ltNode.getLtData()
        self.leImaPath.setText(ltData['ltImaPath'])
        self.leSeqPath.setText(ltData['ltSeqPath'])
        self.leMovPath.setText(ltData['ltMovPath'])

    def on_open(self, pathType):
        """ Command launched when 'Open' QPushButton is clicked
            @param pathType: (str) : 'ima', 'seq' or 'mov' """
        QLineEdit = None
        if pathType == 'ima':
            QLineEdit = self.leImaPath
        elif pathType == 'seq':
            QLineEdit = self.leSeqPath
        elif pathType == 'mov':
            QLineEdit = self.leMovPath
        root = os.path.dirname(str(QLineEdit.text()))
        if root is None or root in ['', ' ']:
            if os.path.exists(self.ltNode._dataFile):
                data = pFile.readPyFile(self.ltNode._dataFile)
                if not data['workDir'] in ['', ' ']:
                    root = data['workDir']
                else:
                    if not self.pm.prodWorkDir in ['', ' ']:
                        root = self.pm.prodWorkDir
                    else:
                        root = prodManager.rootDisk
            else:
                if not self.pm.prodWorkDir in ['', ' ']:
                    root = self.pm.prodWorkDir
                else:
                    root = prodManager.rootDisk
        self.fdPath = pQt.fileDialog(fdRoot=root, fdCmd=partial(self.ud_path, QLineEdit))
        self.fdPath.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdPath.exec_()

    def ud_path(self, QLineEdit):
        """ Update given widget
            @param QLineEdit: (object) : QLineEdit """
        selPath = self.fdPath.selectedFiles()
        if selPath:
            QLineEdit.setText(str(selPath[0]))

    def on_save(self):
        """ Command launched when 'Save' QPushButton is clicked """
        ltData = self.ltNode.getLtData()
        ltData['ltImaPath'] = str(self.leImaPath.text())
        ltData['ltSeqPath'] = str(self.leSeqPath.text())
        ltData['ltMovPath'] = str(self.leMovPath.text())
        if self.ltNode.writeLt(ltData):
            iconeFile = os.path.join(os.path.dirname(self.ltNode._ltFile), 'previewIcone.png')
            self.mainUi.wgPreview.ud_previewIcone(pFile.conformPath(str(self.leImaPath.text())),
                                                  pFile.conformPath(iconeFile))
            self.close()

    def getRootDir(self):
        """ Get root directory from selected node
            @return: (str) : Root path """
        if os.path.exists(self.ltNode._dataFile):
            dataDict = pFile.readPyFile(self.ltNode._dataFile)
            if 'workDir' in dataDict.keys():
                return dataDict['workDir']


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
        if self._ltNode.writeLt(data):
            self._cmtNode.teComment.setHtml(self.teText.toHtml())
            self.close()

    def closeEvent(self, *args, **kwargs):
        """ Unfreeze mainUi """
        self.mainUi.setEnabled(True)
