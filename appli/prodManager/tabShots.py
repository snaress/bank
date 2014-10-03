import os
from lib.qt import textEditor
from appli import prodManager
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.prodManager import pmCore
from appli.prodManager.ui import tabShotsUI, wgtShotNodeUI


class ShotsTab(QtGui.QWidget, tabShotsUI.Ui_shotsTab):
    """ ShotNode settings ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(ShotsTab, self).__init__()
        self._setupUi()

    def __getDict__(self):
        """ Get shots params writtable dict
            @return: (dict) : Shots params """
        shotDict = {}
        shotDict['workDir'] = str(self.leWorkDir.text())
        shotDict['imaDir'] = str(self.leImaDir.text())
        for item in pQt.getTopItems(self.twShotParams):
            if item.attrType == 'str':
                shotDict[str(item.text(0))] = str(item._widget.text())
            else:
                shotDict[str(item.text(0))] = item._widget.value()
        for k, v in self.wgComment.__getDict__().iteritems():
            shotDict[k] = v
        return shotDict

    def __getStr__(self):
        """ Get shots params writtable string
            @return: (str) : Shots Params """
        shotDict = self.__getDict__()
        txt = []
        for k, v in shotDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup project tabWidget """
        self.setupUi(self)
        self.log.debug("#-- Setup Tab Shots --#")
        self.twShotNodes = ShotTree(self)
        self.vlTreeShots.insertWidget(0, self.twShotNodes)
        self.wgComment = Comment(self)
        self.glShotComment.addWidget(self.wgComment)
        self.bEditShotParams.clicked.connect(self.on_editShotsTab)
        self.bCancelEdit.clicked.connect(self.on_cancelShotsTab)
        self.bOpenWorkDir.clicked.connect(self.on_openWorkDir)
        self.leImaDir.editingFinished.connect(self.on_imaDir)
        self.bOpenImaDir.clicked.connect(self.on_openImaDir)

    def _refresh(self):
        """ Refresh shots tabWidget """
        self.log.debug("#-- Refresh Tab Shots --#")
        self.rf_workDir()
        self.rf_imaDir()
        self.twShotNodes._refresh()
        self.rf_treeParams()
        self.rf_comment()
        self.rf_tabVis()

    def _update(self):
        """ Update pmObject with tabWidget values """
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            self.pm.writeShotData(selItems[0]._dataFile, self.__getStr__())

    def rf_tabVis(self, state=False):
        """ Refresh project tab ui visibility
            @param state: (bool) : Visibility state """
        self.log.debug("#-- Refresh Tab Shots Visibility --#")
        self.bCancelEdit.setVisible(state)
        self.leWorkDir.setReadOnly(not state)
        self.leImaDir.setReadOnly(not state)
        self.bOpenWorkDir.setEnabled(state)
        self.bOpenImaDir.setEnabled(state)
        for item in pQt.getAllItems(self.twShotParams):
            item._widget.setReadOnly(not state)
        self.wgComment.setEnabled(state)
        if self.twShotNodes.selectedItems():
            self.bEditShotParams.setEnabled(True)
        else:
            self.bEditShotParams.setEnabled(False)

    def rf_workDir(self):
        """ Refresh workDir lineEdit """
        self.leWorkDir.clear()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            defaultWorkDir = os.path.join(self.pm.prodWorkDir, selItems[0].shotType)
            for fld in selItems[0]._itemPath.split('/'):
                defaultWorkDir = os.path.join(defaultWorkDir, fld)
            if not os.path.exists(selItems[0]._dataFile):
                self.leWorkDir.setText(pFile.conformPath(defaultWorkDir))
            else:
                data = pFile.readPyFile(selItems[0]._dataFile)
                if 'workDir' in data.keys():
                    self.leWorkDir.setText(data['workDir'])
                else:
                    self.leWorkDir.setText(pFile.conformPath(defaultWorkDir))

    def rf_imaDir(self):
        """ Refresh imaDir lineEdit """
        self.leImaDir.clear()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            if not os.path.exists(selItems[0]._dataFile):
                self.leImaDir.setText('')
            else:
                data = pFile.readPyFile(selItems[0]._dataFile)
                if 'imaDir' in data.keys():
                    self.leImaDir.setText(data['imaDir'])
                else:
                    self.leImaDir.setText('')

    def rf_treeParams(self):
        """ Refresh paramsTree """
        self.log.debug("\t Refreshing tree params ...")
        self.twShotParams.clear()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            #-- Get Datas --#
            attrDict = self.pm.prodTrees[selItems[0].shotType]['attr']
            if os.path.exists(selItems[0]._dataFile):
                data = pFile.readPyFile(selItems[0]._dataFile)
            else:
                data = None
            #-- Refresh --#
            for attr in attrDict['_order']:
                if data is None:
                    newItem = self._newParamItem(attr, attrDict[attr], None)
                else:
                    if attr in data.keys():
                        newItem = self._newParamItem(attr, attrDict[attr], data[attr])
                    else:
                        newItem = self._newParamItem(attr, attrDict[attr], None)
                self.twShotParams.addTopLevelItem(newItem)
                self.twShotParams.setItemWidget(newItem, 1, newItem._widget)

    def rf_comment(self):
        """ Refresh comment """
        self.log.debug("\t Refreshing comment ...")
        self.wgComment.resetComment()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            if os.path.exists(selItems[0]._dataFile):
                data = pFile.readPyFile(selItems[0]._dataFile)
                if 'commentHtml' in data.keys():
                    self.wgComment.rf_comment(data['commentHtml'])

    def on_shotNodeItem(self):
        """ Command launch when twShotNodes item is clicked """
        self.rf_workDir()
        self.rf_imaDir()
        self.rf_treeParams()
        self.rf_comment()
        self.rf_tabVis()

    def on_editShotsTab(self):
        """ Command launch when bEditShotParams is clicked """
        checkState = self.bEditShotParams.isChecked()
        if checkState:
            self.bEditShotParams.setText("Save")
            self.bEditShotParams.selIndex = self.twShotNodes.selectedIndexes()[0].row()
            self.setStyleSheet(self.mainUi.applyStyle(styleName='redGrey'))
            self.twShotNodes.setEnabled(False)
            self.mainUi.wgTree.setEnabled(False)
        else:
            self.bEditShotParams.setText("Edit")
            self._update()
            self.twShotNodes.setEnabled(True)
            self.mainUi.wgTree.setEnabled(True)
            self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
            item = pQt.getTopItems(self.twShotNodes)[self.bEditShotParams.selIndex]
            self.twShotNodes.setItemSelected(item, True)
        self.rf_tabVis(state=checkState)

    def on_cancelShotsTab(self):
        """ Command launch when bCancelEdit is clicked """
        self.bEditShotParams.setText("Edit")
        self.bEditShotParams.setChecked(False)
        self.twShotNodes.setEnabled(True)
        self.mainUi.wgTree.setEnabled(True)
        self._refresh()
        item = pQt.getTopItems(self.twShotNodes)[self.bEditShotParams.selIndex]
        self.twShotNodes.setItemSelected(item, True)
        self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))

    def on_openWorkDir(self):
        """ Command launch when bOpenWorkDir is clicked """
        root = str(self.leWorkDir.text())
        if not os.path.exists(root):
            if self.pm.prodWorkDir == '':
                root = prodManager.rootDisk
            else:
                root = self.pm.prodWorkDir
        self.fdWorkDir = pQt.fileDialog(fdRoot=root, fdCmd=self.ud_workDir)
        self.fdWorkDir.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        self.fdWorkDir.exec_()

    def ud_workDir(self):
        """ Update Work dir with selected path from dialog """
        selPath = self.fdWorkDir.selectedFiles()
        if selPath:
            self.leWorkDir.setText(str(selPath[0]))

    def on_openImaDir(self):
        """ Command launch when bOpenImaDir is clicked """
        root = str(self.leImaDir.text())
        if not os.path.exists(root):
            root = str(self.leWorkDir.text())
            if not os.path.exists(str(self.leWorkDir.text())):
                if self.pm.prodWorkDir == '':
                    root = prodManager.rootDisk
                else:
                    root = self.pm.prodWorkDir
        self.fdImaDir = pQt.fileDialog(fdRoot=root, fdCmd=self.ud_imaDir)
        self.fdImaDir.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdImaDir.exec_()

    def on_imaDir(self):
        """ Command launch when imaDir edition is finished """
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            selItems[0]._widget.ud_shotNodeIcone(str(self.leImaDir.text()))

    def ud_imaDir(self):
        """ Update Ima dir with selected path from dialog """
        selPath = self.fdImaDir.selectedFiles()
        selItems = self.twShotNodes.selectedItems()
        if selPath and selItems:
            self.leImaDir.setText(str(selPath[0]))
            selItems[0]._widget.ud_shotNodeIcone(str(selPath[0]))

    def _newParamItem(self, attrName, attrType, attrValue):
        """ Create paramsTree QTreeWidgetItem
            @param attrName: (str) : Attribute label
            @param attrType: (str) : 'str', 'int' or 'float'
            @param attrValue: (str) or (int) or (float) : Attribute value
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, attrName)
        newItem.attrName = attrName
        newItem.attrType = attrType
        newItem.attrValue = attrValue
        newItem._widget = self._newParamWidget(attrType, attrValue)
        return newItem

    # noinspection PyUnresolvedReferences
    @staticmethod
    def _newParamWidget(attrType, attrValue):
        """ Create new QSpinBox
            @param attrType: (str) : 'str', 'int' or 'float'
            @param attrValue: (str) or (int) or (float) : Attribute value
            @return: (object) : QSpinBox or QDoubleSpinBox """
        #-- Create Widget --#
        if attrType == 'str':
            newWidget = QtGui.QLineEdit()
        elif attrType == 'int':
            newWidget = QtGui.QSpinBox()
        else:
            newWidget = QtGui.QDoubleSpinBox()
            newWidget.setDecimals(3)
        #-- Init Widget --#
        if not attrType == 'str':
            newWidget.setMinimum(-999999)
            newWidget.setMaximum(999999)
            newWidget.setMaximumWidth(80)
            newWidget.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        #-- Edit Widget --#
        if attrValue is not None:
            if attrType == 'str':
                newWidget.setText(attrValue)
            else:
                newWidget.setValue(attrValue)
        return newWidget


class ShotTree(QtGui.QTreeWidget):
    """ ShotNodes QTreeWidget used by ShotsTab()
        @param parent: (object) : Parent QWidget """

    def __init__(self, parent):
        self._tab = parent
        self.mainUi = self._tab.mainUi
        self.pm = self._tab.pm
        self.log = self.mainUi.log
        super(ShotTree, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup shotTree QTreeWidget """
        self.setIndentation(0)
        self.header().setVisible(False)
        self.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.itemClicked.connect(self._tab.on_shotNodeItem)

    def _refresh(self):
        """ Refresh shotTree """
        self.log.debug("\t Refreshing tree shots ...")
        self.clear()
        selItems = self.mainUi.wgTree.twTree.selectedItems()
        if selItems:
            rootNode = self.getItemRootNode(selItems[0])
            if rootNode is not None:
                shotItems = []
                for n in range(rootNode.childCount()):
                    if rootNode.child(n).nodeType == 'shotNode':
                        itemDict = rootNode.child(n).__dict__
                        itemDict['shotType'] = self.mainUi.wgTree.getSelTree()
                        newShotItem = ShotItem(self, **itemDict)
                        shotItems.append(newShotItem)
                self.addTopLevelItems(shotItems)
            self.reselectFromMainTree(selItems[0])
            self._tab.on_shotNodeItem()

    def addTopLevelItem(self, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(ShotTree, self).addTopLevelItem(QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(ShotTree, self).addTopLevelItems(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(ShotTree, self).insertTopLevelItem(p_int, QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(ShotTree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def getItemRootNode(self, item):
        """ Get given item rootNode
            @param item: (object) : QTreeWidgetItem
            @return: (object) : QTreeWidgetItem """
        rootNode = None
        if item.nodeType == 'container':
            rootNode = item
        elif item.nodeType == 'shotNode':
            rootNode = item.parent()
        elif item.nodeType == 'step':
            if self.mainUi.wgTree.getSelMode() == 'treeMode':
                rootNode = item.parent().parent()
        return rootNode

    def reselectFromMainTree(self, selItem):
        """ Link mainTree selection to shotNodeTree selection
            @param selItem: (object) : Selected mainTree QTreeWidgetItem """
        for item in pQt.getTopItems(self):
            if self.mainUi.getSelMode() == 'treeMode':
                if selItem.nodeType == 'shotNode':
                    if item.nodeName == selItem.nodeName:
                        self.setCurrentItem(item)
                elif selItem.nodeType == 'step':
                    if item.nodeName == selItem.parent().nodeName:
                        self.setCurrentItem(item)
            elif self.mainUi.getSelMode() == 'stepMode':
                if selItem.nodeType == 'shotNode':
                    if item.nodeName == selItem.nodeName:
                        self.setCurrentItem(item)


class ShotItem(QtGui.QTreeWidgetItem):
    """ ShotNode QTreeWidgetItem used by ShotTree()
        @param ui: (object) : Parent QWidget
        @param kwargs: (dict) : ShotItem params (itemDict and nodeDict) """

    def __init__(self, ui, **kwargs):
        self._tree = ui
        super(ShotItem, self).__init__()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self._widget = ShotNode(self._tree, self)

    def addChild(self, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(ShotItem, self).addChild(QTreeWidgetItem)
        QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addChildren(self, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(ShotItem, self).addChildren(list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertChild(self, p_int, QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param QTreeWidgetItem: (object) : QTreeWidgetItem """
        super(ShotItem, self).insertChild(p_int, QTreeWidgetItem)
        QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        """ Override function and add itemWidget
            @param p_int: (int) : Column index
            @param list_of_QTreeWidgetItem: (list) : List of QTreeWidgetItems """
        super(ShotItem, self).insertChildren(p_int, list_of_QTreeWidgetItem)
        for QTreeWidgetItem in list_of_QTreeWidgetItem:
            QTreeWidgetItem.treeWidget().setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)


class ShotNode(QtGui.QWidget, wgtShotNodeUI.Ui_shotNode):
    """ ShotNode WQidget used by ShotItem()
        @param tree: (object) : Parent QWidget
        @param parent: (object) : Parent QTreeWidgetItem """

    def __init__(self, tree, parent):
        self._tree = tree
        self._item = parent
        self.pm = self._tree.pm
        self.log = self._tree.log
        super(ShotNode, self).__init__()
        self._setupUi()
        self._refresh()

    def _setupUi(self):
        """ Setup shotNode QWidget """
        self.qIma = None
        self.setupUi(self)

    def _refresh(self):
        """ Refresh shotNode """
        self.lLabelVal.setText(self._item.nodeLabel)
        self.lNameVal.setText(self._item.nodeName)
        self.lTypeVal.setText(self._item.shotType)
        self.rf_shotNodeIma()

    def rf_shotNodeIma(self, ima=None):
        """ Refresh shotNode preview image
            @param ima: (str) : Image absolut path """
        if ima is None:
            ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')
            iconeFile = os.path.join(self._item._dataPath, 'shotNodeIcone.png')
            if os.path.exists(iconeFile):
                ima = iconeFile
        if ima == '' or ima == ' ':
            ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')
        self.qIma = QtGui.QPixmap(ima)
        self.lPreview.setPixmap(self.qIma)
        self.lPreview.setMinimumSize(self.qIma.width()/2, self.qIma.height()/2)
        self.lPreview.setMaximumSize(self.qIma.width()/2, self.qIma.height()/2)

    def ud_shotNodeIcone(self, ima):
        """ Update shotNode icone file
            @param ima: (str) : Image absolut path """
        root = os.path.join(self.pm._prodPath, self.pm._prodId)
        iconeFile = os.path.join(self._item._dataPath, 'shotNodeIcone.png')
        if ima == '' or ima == ' ':
            self.rf_shotNodeIma(ima='')
            self.removeShotNodeIcone(iconeFile)
        else:
            self.rf_shotNodeIma(ima=ima)
            img = self.resizeImage()
            if pmCore.Manager.checkDataPath(root, os.path.dirname(iconeFile)):
                try:
                    img.save(iconeFile, 'png', 100)
                    self.rf_shotNodeIma(ima=iconeFile)
                    self.log.info("Saving shotNode icone: %s ..." % pFile.conformPath(iconeFile))
                except:
                    self.log.error("Can't save shotNode icone: %s !!!" % pFile.conformPath(iconeFile))

    def removeShotNodeIcone(self, iconeFile):
        """ Remove shotNode icone file
            @param iconeFile: (str) : Icone absolut path """
        if os.path.exists(iconeFile):
            try:
                os.remove(iconeFile)
                self.log.info("Remove shotNode icone: %s" % pFile.conformPath(iconeFile))
            except:
                self.log.error("Can't remove shotNode icone: %s !!!" % pFile.conformPath(iconeFile))

    def resizeImage(self):
        """ Resize image to icone size
            @return: (object) : QPixmap """
        ratio = float(self.qIma.width()) / float(self.qIma.height())
        if self.qIma.width() > self.qIma.height():
            maxWidth = 300
            maxHeight = int(300 / ratio)
        else:
            maxWidth = int(300 / ratio)
            maxHeight = 300
        img = self.qIma.toImage().scaled(maxWidth, maxHeight, QtCore.Qt.KeepAspectRatio)
        return img


class Comment(textEditor.TextEditor):
    """ Comment Widget used by ShotsTab()
        @param parent: (object) : Parent widget """

    def __init__(self, parent):
        self._parent = parent
        super(Comment, self).__init__()
        self._setupWidget()

    def __getDict__(self):
        """ Get shot comment writtable dict
            @return: (dict) : Shot comment """
        return {'commentHtml': str(self.teText.toHtml()),
                'commentTxt': str(self.teText.toPlainText())}

    def __getStr__(self):
        """ Get shot comment writtable string
            @return: (str) : Shot comment """
        return self.__getDict__()['commentTxt']

    def _setupWidget(self):
        """ Setup widegt ui """
        self.bLoadFile.setEnabled(False)
        self.bSaveFile.setEnabled(False)

    def rf_comment(self, textHtml):
        """ Refresh comment
            @param textHtml: (str) : Comment in html form """
        self.teText.setHtml(textHtml)

    def resetComment(self):
        """ Reset comment """
        self.teText.clear()
