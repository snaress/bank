import os
from PyQt4 import QtGui
from lib.qt import textEditor
from appli import prodManager
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
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

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup project tabWidget """
        self.setupUi(self)
        self.log.debug("#-- Setup Tab Shots --#")
        self.twShotNodes = ShotTree(self)
        self.vlTreeShots.insertWidget(0, self.twShotNodes)
        self.leWorkDir.editingFinished.connect(self.on_workDir)
        self.wgComment = Comment()
        self.glShotComment.addWidget(self.wgComment)
        self.bEditShotParams.clicked.connect(self.on_editShotsTab)
        self.bCancelEdit.clicked.connect(self.on_cancelShotsTab)

    def _refresh(self):
        """ Refresh shots tabWidget """
        self.log.debug("#-- Refresh Tab Shots --#")
        self.twShotNodes._refresh()
        self.rf_treeParams()
        self.rf_tabVis()

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
        if self.twShotNodes.selectedItems():
            self.bEditShotParams.setEnabled(True)
        else:
            self.bEditShotParams.setEnabled(False)

    def rf_workDir(self):
        """ Refresh workDir lineEdit """
        self.leWorkDir.clear()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            itemDict = selItems[0].__dict__
            if selItems[0].workDir is None:
                defaultWorkDir = os.path.join(self.pm.prodWorkDir, itemDict['_shotType'])
                for fld in itemDict['_dataPath'].split('/'):
                    defaultWorkDir = os.path.join(defaultWorkDir, fld)
                self.leWorkDir.setText(pFile.conformPath(defaultWorkDir))
            else:
                self.leWorkDir.setText(selItems[0].workDir)

    def rf_imaDir(self):
        """ Refresh imaDir lineEdit """
        self.leImaDir.clear()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            if selItems[0].imaDir is None:
                self.leImaDir.setText('')
            else:
                self.leImaDir.setText(selItems[0].imaDir)

    def rf_treeParams(self):
        """ Refresh paramsTree """
        self.log.debug("\t Refreshing tree params ...")
        self.twShotParams.clear()
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            attrDict = selItems[0].__getDict__()['attr']
            for attr in attrDict['_order']:
                newItem = ShotParamItem(selItems[0], attr, attrDict[attr]['type'],
                                        attrDict[attr]['value'])
                self.twShotParams.addTopLevelItem(newItem)
                self.twShotParams.setItemWidget(newItem, 1, newItem._widget)

    def on_shotNodeItem(self):
        """ Command launch when twShotNodes item is clicked """
        self.rf_workDir()
        self.rf_imaDir()
        self.rf_treeParams()
        self.rf_tabVis()

    def on_editShotsTab(self):
        """ Command launch when bEditShotParams is clicked """
        checkState = self.bEditShotParams.isChecked()
        if checkState:
            self.bEditShotParams.setText("Save")
            self.bEditShotParams.selIndex = self.twShotNodes.selectedIndexes()[0].row()
            self.setStyleSheet(self.mainUi.applyStyle(styleName='redGrey'))
            self.twShotNodes.setEnabled(False)
        else:
            self.bEditShotParams.setText("Edit")
            self.twShotNodes.setEnabled(True)
            self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
            item = pQt.getTopItems(self.twShotNodes)[self.bEditShotParams.selIndex]
            self.twShotNodes.setItemSelected(item, True)
        self.rf_tabVis(state=checkState)

    def on_cancelShotsTab(self):
        """ Command launch when bCancelEdit is clicked """
        self.bEditShotParams.setText("Edit")
        self.bEditShotParams.setChecked(False)
        self.twShotNodes.setEnabled(True)
        self._refresh()
        item = pQt.getTopItems(self.twShotNodes)[self.bEditShotParams.selIndex]
        self.twShotNodes.setItemSelected(item, True)
        self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))

    def on_workDir(self):
        """ Store workDir in shotNode """
        self.log.debug("Storing WorkDir ...")
        selItems = self.twShotNodes.selectedItems()
        if selItems:
            selItems[0].workDir = str(self.leWorkDir.text())

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

    def _getNodeDict(self, itemDict):
        """ Init nodeDict
            @param itemDict: (dict) : QTreeWidgetItem dict
            @return: (dict) : Node dict """
        nodeDict = {'workDir': None, 'imaDir': None, 'comment': None, 'attr': {'_order': []}}
        for k, v in self._itemDictToNodeDict(itemDict).iteritems():
            nodeDict[k] = v
        attrs = self.pm.prodTrees[self.mainUi.getSelTree()]['attr']
        nodeDict['attr']['_order'] = attrs['_order']
        for attr in attrs['_order']:
            nodeDict['attr'][attr] = {}
            nodeDict['attr'][attr]['type'] = attrs[attr]
            if not os.path.exists(nodeDict['_dataFile']):
                nodeDict['attr'][attr]['value'] = None
        return nodeDict

    def _itemDictToNodeDict(self, itemDict):
        """ Convert itemDict to nodeDict
            @param itemDict: (dict) : QTreeWidgetItem dict
            @return: (dict) : Converted dict """
        newDict = {}
        for k, v in itemDict.iteritems():
            newDict['_%s' % k] = v
        newDict['_shotType'] = self.mainUi.wgTree.getSelTree()
        return newDict


class ShotTree(QtGui.QTreeWidget):
    """ ShotNodes QTreeWidget used by ShotsTab()
        @param parent: (object) : Parent QWidget """

    def __init__(self, parent):
        self._parent = parent
        self.mainUi = self._parent.mainUi
        self.log = self.mainUi.log
        super(ShotTree, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup shotTree QTreeWidget """
        self.setIndentation(0)
        self.header().setVisible(False)
        self.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.itemClicked.connect(self._parent.on_shotNodeItem)

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
                        itemDict = self._parent._getNodeDict(rootNode.child(n).__dict__)
                        newShotItem = ShotItem(self, **itemDict)
                        shotItems.append(newShotItem)
                self.addTopLevelItems(shotItems)

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


class ShotItem(QtGui.QTreeWidgetItem):
    """ ShotNode QTreeWidgetItem used by ShotTree()
        @param ui: (object) : Parent QWidget
        @param kwargs: (dict) : ShotItem params (itemDict and nodeDict) """

    def __init__(self, ui, **kwargs):
        self._ui = ui
        super(ShotItem, self).__init__()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self._widget = ShotNode(self._ui, self)

    def __getDict__(self):
        """ Get ShotItem params writtable dict
            @return: (dict) : ShotItem params """
        itemDict = {}
        for k, v in self.__dict__.iteritems():
            if not k.startswith('_'):
                itemDict[k] = v
        return itemDict

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
        @param ui: (object) : Parent QWidget
        @param parent: (object) : Parent QTreeWidgetItem """

    def __init__(self, ui, parent):
        self._ui = ui
        self._parent = parent
        super(ShotNode, self).__init__()
        self._setupUi()
        self._refresh()

    def _setupUi(self):
        """ Setup shotNode QWidget """
        self.setupUi(self)

    def _refresh(self):
        """ Refresh shotNode """
        self.lLabelVal.setText(self._parent._nodeLabel)
        self.lNameVal.setText(self._parent._nodeName)
        self.lTypeVal.setText(self._parent._shotType)
        self.rf_shotNodeIma()

    def rf_shotNodeIma(self, ima=None):
        if ima is None:
            ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')
        qIma = QtGui.QPixmap(ima)
        self.lPreview.setPixmap(qIma)


class ShotParamItem(QtGui.QTreeWidgetItem):

    def __init__(self, shotItem, attrName, attrType, attrValue):
        self._shotItem = shotItem
        self.attrName = attrName
        self.attrType = attrType
        self.attrValue = attrValue
        super(ShotParamItem, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup ShotParamItem QTreeWidgetItem """
        self.setText(0, self.attrName)
        if self.attrType == 'str':
            self._widget = self._newStrItem()
        elif self.attrType == 'int':
            self._widget = self._newIntItem()
        elif self.attrType == 'float':
            self._widget = self._newFloatItem()

    def storeParams(self):
        """ Store attribute params """
        if self.attrType == 'str':
            self._shotItem.attr[self.attrName]['value'] = str(self._widget.text())
        else:
            self._shotItem.attr[self.attrName]['value'] = self._widget.value()

    # noinspection PyUnresolvedReferences
    def _newStrItem(self):
        """ Create new QLineEdit
            @return: (object) : QLineEdit """
        newItem = QtGui.QLineEdit()
        if self.attrValue is not None:
            newItem.setText(self.attrValue)
        newItem.editingFinished.connect(self.storeParams)
        return newItem

    def _newIntItem(self):
        """ Create new QSpinBox
            @return: (object) : QSpinBox """
        newItem = QtGui.QSpinBox()
        if self.attrValue is not None:
            newItem.setValue(self.attrValue)
        newItem.editingFinished.connect(self.storeParams)
        return newItem

    def _newFloatItem(self):
        """ Create new QDoubleSpinBox
            @return: (object) : QDoubleSpinBox """
        newItem = QtGui.QDoubleSpinBox()
        if self.attrValue is not None:
            newItem.setValue(self.attrValue)
        newItem.editingFinished.connect(self.storeParams)
        return newItem


class Comment(textEditor.TextEditor):

    def __init__(self):
        super(Comment, self).__init__()
