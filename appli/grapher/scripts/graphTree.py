import os
from appli import grapher
from functools import partial
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import procFile as pFile
from appli.grapher.scripts import nodeEditor, gpCore


class GraphTree(QtGui.QTreeWidget):
    """ Class used by the grapherUi for graph tree edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.columns = 10
        self.cpBuffer = None
        super(GraphTree, self).__init__()
        self._setupUi()
        self._setupMainUi()
        self._popUpMenu()

    def __repr2__(self):
        treeDict = {'_order': []}
        allItems = pQt.getAllItems(self)
        for item in allItems:
            nodeDict = item.__repr2__()
            treeDict['_order'].append(nodeDict['nodeName'])
            treeDict[nodeDict['nodeName']] = nodeDict
        return treeDict

    def __str__(self):
        treeDict = self.__repr2__()
        text = ["#-- Graph Tree --#"]
        for node in treeDict['_order']:
            text.append("%s:" % node)
            for k, v in sorted(treeDict[node].iteritems()):
                text.append("%s %s = %s" % (' '*len(node), k, v))
        return '\n'.join(text)

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        #-- Columns --#
        self.setHeaderHidden(True)
        self.setColumnCount(self.columns)
        #-- Items --#
        self.setSelectionMode(QtGui.QTreeWidget.ExtendedSelection)
        self.setItemsExpandable(True)
        self.setIndentation(0)
        self.itemClicked.connect(self.mainUi.nodeEditor.resetUi)
        #-- Drag & Drop --#
        self.setAcceptDrops(False)
        self.setDragEnabled(False)
        self.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.setDefaultDropAction(QtCore.Qt.LinkAction)

    def _setupMainUi(self):
        #-- Menu Create --#
        self.mainUi.miNewGraphNode.triggered.connect(self.on_newNode)
        self.mainUi.miNewGraphNode.setShortcut("Alt+N")
        self.mainUi.miRenameGraphNode.triggered.connect(self.on_renameNode)
        self.mainUi.miRenameGraphNode.setShortcut("F2")
        self.mainUi.miInstanceGraphNode.triggered.connect(self.on_instanceNode)
        self.mainUi.miInstanceGraphNode.setShortcut("F3")
        self.mainUi.miDelGraphNode.triggered.connect(self.on_delNode)
        self.mainUi.miDelGraphNode.setShortcut("Del")
        #-- Menu Move --#
        self.mainUi.miMoveNodesUp.triggered.connect(partial(self.on_moveNodes, 'up'))
        self.mainUi.miMoveNodesUp.setShortcut("Ctrl+Up")
        self.mainUi.miMoveNodesDn.triggered.connect(partial(self.on_moveNodes, 'down'))
        self.mainUi.miMoveNodesDn.setShortcut("Ctrl+Down")
        #-- Menu Edit --#
        self.mainUi.miCutNodes.triggered.connect(partial(self.on_cutSelection, 'node'))
        self.mainUi.miCutNodes.setShortcut("Ctrl+X")
        self.mainUi.miCutBranch.triggered.connect(partial(self.on_cutSelection, 'branch'))
        self.mainUi.miCutBranch.setShortcut("Shift+X")
        self.mainUi.miCopyNodes.triggered.connect(partial(self.on_copySelection, 'node'))
        self.mainUi.miCopyNodes.setShortcut("Ctrl+C")
        self.mainUi.miCopyBranch.triggered.connect(partial(self.on_copySelection, 'branch'))
        self.mainUi.miCopyBranch.setShortcut("Shift+C")
        self.mainUi.miPasteNodes.triggered.connect(self.on_pasteNode)
        self.mainUi.miPasteNodes.setShortcut("Ctrl+V")
        #-- Menu Storage --#
        self.mainUi.miPushNodes.triggered.connect(partial(self.on_pushSelection, 'node'))
        self.mainUi.miPushNodes.setShortcut("Ctrl+P")
        self.mainUi.miPushBranch.triggered.connect(partial(self.on_pushSelection, 'branch'))
        self.mainUi.miPushBranch.setShortcut("Shift+P")
        self.mainUi.miPullNodes.triggered.connect(self.on_pullNodes)
        self.mainUi.miPullNodes.setShortcut("Alt+P")

    def _popUpMenu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popUpMenu)
        self.tbGraph = QtGui.QToolBar()
        self.pMenu = QtGui.QMenu(self.mainUi)
        self.miCleanCheckFiles1 = self.tbGraph.addAction("Clean Check Files", self.on_cleanCheckFiles)
        self.miCleanCheckFiles2 = self.tbGraph.addAction("Clean Check Files", self.on_cleanCheckFiles)
        self.pMenu.addAction(self.miCleanCheckFiles1)
        self.pMenu.addSeparator()
        self._menuCreate()
        self._menuMove()
        self._menuEdit()
        self._menuStorage()
        self.pMenu.addSeparator()
        self.pMenu.addAction(self.miCleanCheckFiles2)

    def _menuCreate(self):
        #-- New Graph Node --#
        self.miNewGraphNode = self.tbGraph.addAction("New Node", self.on_newNode)
        self.miNewGraphNode.setShortcut("Alt+N")
        self.pMenu.addAction(self.miNewGraphNode)
        #-- Rename Graph Node --#
        self.miRenameGraphNode =  self.tbGraph.addAction("Rename Node", self.on_renameNode)
        self.miRenameGraphNode.setShortcut("F2")
        self.pMenu.addAction(self.miRenameGraphNode)
        #-- Instanciate Graph Node --#
        self.miInstanceGraphNode = self.tbGraph.addAction("Instanciate Node", self.on_instanceNode)
        self.miInstanceGraphNode.setShortcut("F3")
        self.pMenu.addAction(self.miInstanceGraphNode)
        #-- Delete Graph Node --#
        self.miDelGraphNode = self.tbGraph.addAction("Delete Nodes", self.on_delNode)
        self.miDelGraphNode.setShortcut("Del")
        self.pMenu.addAction(self.miDelGraphNode)
        self.pMenu.addSeparator()

    def _menuMove(self):
        #-- Move Nodes Up --#
        self.miMoveNodesUp = self.tbGraph.addAction("Move Up", partial(self.on_moveNodes, 'up'))
        self.miMoveNodesUp.setShortcut("Ctrl+Up")
        self.pMenu.addAction(self.miMoveNodesUp)
        #-- Move Nodes Down --#
        self.miMoveNodesDn = self.tbGraph.addAction("Move Down", partial(self.on_moveNodes, 'down'))
        self.miMoveNodesDn.setShortcut("Ctrl+Down")
        self.pMenu.addAction(self.miMoveNodesDn)
        self.pMenu.addSeparator()

    def _menuEdit(self):
        #-- Cut Nodes --#
        self.miCutNodes = self.tbGraph.addAction("Cut Nodes", partial(self.on_cutSelection, 'node'))
        self.miCutNodes.setShortcut("Ctrl+X")
        self.pMenu.addAction(self.miCutNodes)
        #-- Cut Branch --#
        self.miCutBranch = self.tbGraph.addAction("Cut Branch", partial(self.on_cutSelection, 'branch'))
        self.miCutBranch.setShortcut("Shift+X")
        self.pMenu.addAction(self.miCutBranch)
        #-- Copy Nodes --#
        self.miCopyNodes = self.tbGraph.addAction("Copy Nodes", partial(self.on_copySelection, 'node'))
        self.miCopyNodes.setShortcut("Ctrl+C")
        self.pMenu.addAction(self.miCopyNodes)
        #-- Copy Branch --#
        self.miCopyBranch = self.tbGraph.addAction("Copy Branch", partial(self.on_copySelection, 'branch'))
        self.miCopyBranch.setShortcut("Shift+C")
        self.pMenu.addAction(self.miCopyBranch)
        #-- Paste Nodes --#
        self.miPasteNodes = self.tbGraph.addAction("Paste", self.on_pasteNode)
        self.miPasteNodes.setShortcut("Ctrl+V")
        self.pMenu.addAction(self.miPasteNodes)
        self.pMenu.addSeparator()

    def _menuStorage(self):
        #-- Push Nodes --#
        self.miPushNodes = self.tbGraph.addAction("Push Nodes", partial(self.on_pushSelection, 'node'))
        self.miPushNodes.setShortcut("Ctrl+P")
        self.pMenu.addAction(self.miPushNodes)
        #-- Push Branch --#
        self.miPushBranch = self.tbGraph.addAction("Push Branch", partial(self.on_pushSelection, 'branch'))
        self.miPushBranch.setShortcut("Shift+P")
        self.pMenu.addAction(self.miPushBranch)
        #-- Pull Nodes --#
        self.miPullNodes = self.tbGraph.addAction("Pull", self.on_pullNodes)
        self.miPullNodes.setShortcut("Alt+P")
        self.pMenu.addAction(self.miPullNodes)

    def addTopLevelItem(self, QTreeWidgetItem):
        super(GraphTree, self).addTopLevelItem(QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        super(GraphTree, self).addTopLevelItems(list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self.setItemWidget(item, 0, item._widget)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        super(GraphTree, self).insertTopLevelItem(p_int, QTreeWidgetItem)
        self.setItemWidget(QTreeWidgetItem, 0, QTreeWidgetItem._widget)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        super(GraphTree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self.setItemWidget(item, 0, item._widget)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass

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
        for item in pQt.getAllItems(self):
            item._widget.rf_childIndicator()

    def rf_graph(self):
        """ Refresh graph tree """
        self.resetGraph()
        for node in self.grapher.graphTree['_order']:
            nodeDict = self.grapher.graphTree[node]
            nodeDict['nodeParent'] = self.getItemFromNodeName(nodeDict['nodeParent'])
            nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
            self.addGraphNode(**nodeDict)
        self.rf_graphColumns()

    def on_popUpMenu(self, point):
        """ Show popup menu
            @param point: (object) : QPoint """
        selItems = self.selectedItems()
        if selItems[0]._instanceFrom is None:
            nodeType = selItems[0]._widget._data.nodeType
            self.miInstanceGraphNode.setVisible(True)
        else:
            nodeType = selItems[0]._instanceFrom.__repr2__()['nodeType']
            self.miInstanceGraphNode.setVisible(False)
        if len(selItems) == 1 and nodeType == 'loop':
            self.miCleanCheckFiles1.setVisible(True)
            self.miCleanCheckFiles2.setVisible(True)
            self.miInstanceGraphNode.setVisible(False)
        else:
            self.miCleanCheckFiles1.setVisible(False)
            self.miCleanCheckFiles2.setVisible(False)
        self.pMenu.exec_(self.mapToGlobal(point))

    def on_newNode(self):
        """ Command launch when menuItem 'New Node' is clicked
            @return: (object) : QTreeWidgetItem """
        selItems = self.selectedItems()
        attrs = {'nodeName': 'NewNode', 'nodeType': 'modul', 'currentVersion': '001',
                 'versionTitle': {'001': 'New Version'}, 'instanceFrom': None}
        if not len(selItems) > 1:
            if selItems:
                attrs['nodeParent'] = selItems[0]
                newItem = self.addGraphNode(**attrs)
            else:
                attrs['nodeParent'] = None
                newItem = self.addGraphNode(**attrs)
            return newItem
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)

    def on_renameNode(self):
        """ Command launch when menuItem 'Rename Node' is clicked """
        selItems = self.selectedItems()
        if len(selItems) == 1:
            message = "Enter New Node Name"
            self.renameDialog = pQt.PromptDialog(message, partial(self.renameNode, selItems[0]))
            self.renameDialog.exec_()

    def on_instanceNode(self):
        """ Command launch when menuItem 'Instanciate Node' is clicked
            @return: (object) : QTreeWidgetItem """
        selItems = self.selectedItems()
        if len(selItems) == 1:
            if selItems[0]._instanceFrom is None:
                nodeDict = selItems[0].__repr2__()
                if nodeDict['nodeParent'] is not None:
                    nodeDict['nodeParent'] = self.getItemFromNodeName(nodeDict['nodeParent'])
                    nodeDict['nodeName'] = self._checkInstanceName("[i1]_%s" % nodeDict['nodeName'])
                    nodeDict['instanceFrom'] = selItems[0]
                newItem = self.addGraphNode(**nodeDict)
                newItem._widget.setGraphNodeBgc()
                return newItem

    def on_delNode(self):
        """ Command launch when menuItem 'Delete Node' is clicked """
        selItems = self.selectedItems()
        if selItems:
            self.confUi = pQt.ConfirmDialog('Delete Selected Nodes ?', ['Delete'],
                                            [partial(self.delGraphNodes, selItems)])
            self.confUi.exec_()

    def on_moveNodes(self, side):
        """ Command launch when miMoveNodes up or down is clicked
            @param side: (str) : 'up' or 'down' """
        selItems = self.selectedItems()
        if len(selItems) == 1:
            #-- Store Info --#
            _parent = selItems[0].parent()
            nodeDict = selItems[0].__repr2__()
            children = selItems[0].getChildren()
            childDict = []
            for item in children:
                childDict.append(item.__repr2__())
            #-- Move Node --#
            if _parent is None:
                reparentChild = self._moveTopItem(selItems, side, **nodeDict)
            else:
                reparentChild = self._moveChildItem(selItems, _parent, side, **nodeDict)
            #-- Reparent Children --#
            if reparentChild:
                for node in childDict:
                    if not node['nodeName'] == nodeDict['nodeName']:
                        node['nodeParent'] = self.getItemFromNodeName(node['nodeParent'])
                        self.addGraphNode(**node)
            #-- Reselect Node --#
            nodesList = []
            for selItem in selItems:
                nodesList.append(selItem.__repr2__()['nodeName'])
            self._reselectNodes(nodesList)
            self.rf_graphColumns()
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)

    def on_cutSelection(self, mode):
        """ Store selected items dict and remove selection
            @param mode: (str) : 'node' or 'branch' """
        selItems = self.selectedItems()
        if selItems:
            if mode == 'node':
                checkChildren = True
                for item in selItems:
                    if item.childCount() > 0:
                        checkChildren = False
                if checkChildren:
                    self.on_copySelection(mode)
                    self.delGraphNodes(selItems)
                    self.rf_graphColumns()
                else:
                    mess = "!!! Warning: Node with children can not be cut !!!"
                    self.mainUi._defaultErrorDialog(mess, self.mainUi)
            elif mode == 'branch':
                if len(selItems) == 1:
                    self.cpBuffer = {'mode': mode, 'nodeList': []}
                    children = selItems[0].getChildren()
                    for child in children:
                        self.cpBuffer['nodeList'].append(child.__repr2__())
                    self.delGraphNodes(selItems)
                    self.rf_graphColumns()
                else:
                    mess = "!!! Warning: Select only one node !!!"
                    self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select at least one node !!!", self.mainUi)

    def on_copySelection(self, mode):
        """ Store selected items dict
            @param mode: (str) : 'node' or 'branch' """
        selItems = self.selectedItems()
        if selItems:
            self.cpBuffer = {'mode': mode, 'nodeList': []}
            if mode == 'node':
                for item in selItems:
                    if item._instanceFrom is None:
                        self.cpBuffer['nodeList'].append(item.__repr2__())
                    else:
                        self.cpBuffer['nodeList'].append(self.getInstanceDict(item))
            elif mode == 'branch':
                if len(selItems) == 1:
                    children = selItems[0].getChildren()
                    for child in children:
                        if child._instanceFrom is None:
                            self.cpBuffer['nodeList'].append(child.__repr2__())
                        else:
                            self.cpBuffer['nodeList'].append(self.getInstanceDict(child))
                else:
                    message = "!!! Warning: Select only one node !!!"
                    self.mainUi._defaultErrorDialog(message, self.mainUi)

    def on_pasteNode(self):
        """ Paste stored items dict """
        selItems = self.selectedItems()
        if not len(selItems) > 1:
            if self.cpBuffer is not None:
                if self.cpBuffer['mode'] == 'node':
                    self._pasteNode(selItems)
                elif self.cpBuffer['mode'] == 'branch':
                    self._pasteBranch(selItems)
                self.rf_graphColumns()
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)

    def on_pushSelection(self, mode):
        """ Push selected nodes into buffer
            @param mode: (str) : 'node' or 'branch' """
        if not os.path.exists(grapher.binPath):
            mess = "!!! ERROR: rndBin path not found, check __init__.py !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            tmpPath = os.path.join(self.grapher.userBinPath, 'tmp')
            pFile.mkPathFolders(grapher.binPath, tmpPath)
            tmpFile = os.path.join(tmpPath, 'nodeBuffer.py')
            selItems = self.selectedItems()
            txt = ["pushMode = %r" % mode]
            if mode == 'node':
                for n, item in enumerate(selItems):
                    if item._instanceFrom is None:
                        txt.append("selNode_%s = %s" % ((n + 1), item.__repr2__()))
                    else:
                        txt.append("selNode_%s = %s" % ((n + 1), self.getInstanceDict(item)))
            elif mode == 'branch':
                if len(selItems) == 1:
                    children = selItems[0].getChildren()
                    for n, child in enumerate(children):
                        if child._instanceFrom is None:
                            txt.append("selNode_%s = %s" % ((n + 1), child.__repr2__()))
                        else:
                            txt.append("selNode_%s = %s" % ((n + 1), self.getInstanceDict(child)))
                else:
                    message = "!!! Warning: Select only one node !!!"
                    self.mainUi._defaultErrorDialog(message, self.mainUi)
            try:
                pFile.writeFile(tmpFile, '\n'.join(txt))
                print "[grapherUI] : Nodes successfully pushed in user buffer with mode %r." % mode
            except:
                mess = "!!! ERROR: Can not store nodes in buffer !!!"
                self.mainUi._defaultErrorDialog(mess, self.mainUi)

    def on_pullNodes(self):
        """ Pull nodes from buffer """
        selItems = self.selectedItems()
        if not len(selItems) > 1:
            if not os.path.exists(grapher.binPath):
                mess = "!!! ERROR: rndBin path not found, check user pref !!!"
                self.mainUi._defaultErrorDialog(mess, self.mainUi)
            else:
                tmpPath = os.path.join(self.grapher.userBinPath, 'tmp')
                tmpFile = os.path.join(tmpPath, 'nodeBuffer.py')
                nodesDict = pFile.readPyFile(tmpFile)
                if nodesDict['pushMode'] == 'node':
                    self._pullNodes(nodesDict, selItems)
                elif nodesDict['pushMode'] == 'branch':
                    self._pullBranch(nodesDict, selItems)
                self.rf_graphColumns()
        else:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one node !!!", self.mainUi)

    def on_cleanCheckFiles(self):
        """ Clean check files from selected loop node """
        selItems = self.selectedItems()
        if not len(selItems) == 1:
            self.mainUi._defaultErrorDialog("!!! Warning: Select only one loop node !!!", self.mainUi)
        else:
            checkFile =  "checkFile__%s" % selItems[0].__repr2__()['nodeLoop']['checkFile']
            tmpPath = pFile.conformPath(self.grapher.tmpPath)
            if os.path.exists(tmpPath):
                print "Clean check files ..."
                files = os.listdir(tmpPath) or []
                for f in files:
                    if f.startswith('%s.' % checkFile) and f.endswith('.py'):
                        os.remove(os.path.join(tmpPath, f))

    def addGraphNode(self, index=None, **kwargs):
        """ Add new QTreeWidgetItem
            @param index: (int) : Index of insertion
            @param kwargs: (dict) : Node params
                @keyword nodeName: (str) : New node name
                @keyword nodeParent: (object) : Parent QTreeWidgetItem
                @keyword nodeEnabled: (bool) : New node state
                @keyword nodeExpanded: (bool) : New node expanded or collapsed
            @return: (object) : QTreeWidgetItem """
        #-- Create New QTreeWidgetItem --#
        kwargs['nodeName'] = self._checkNodeName(kwargs['nodeName'])
        newItem = GraphItem(self, kwargs['nodeParent'])
        if kwargs['nodeParent'] is None:
            if index is None:
                self.addTopLevelItem(newItem)
            else:
                self.insertTopLevelItem(index, newItem)
        else:
            if index is None:
                kwargs['nodeParent'].addChild(newItem)
            else:
                kwargs['nodeParent'].insertChild(index, newItem)
        if kwargs['instanceFrom'] is not None:
            newItem._instanceFrom = kwargs['instanceFrom']
        #-- Edit New QTreeWidgetItem --#
        nodeParams = self._checkNodeDict(**kwargs)
        newItem.setParams(**nodeParams)
        if newItem._instanceFrom is not None:
            newItem._widget._data = None
        else:
            newItem.setDatas(**nodeParams)
        self.rf_graphColumns()
        newItem._widget.setGraphNodeBgc()
        return newItem

    def delGraphNodes(self, QTreeWidgetItems):
        """ Delete given QTreeWidgetItems
            @param QTreeWidgetItems: (list) : List of QTreeWidgetItem to remove"""
        for item in QTreeWidgetItems:
            if item.parent() is None:
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))
            else:
                item.parent().removeChild(item)
        try:
            self.confUi.close()
            self.rf_graphColumns()
        except:
            pass

    def renameNode(self, selNode):
        """ Rename selected node
            @param selNode: (object) : QTreeWidgetItem to rename """
        result = self.renameDialog.result()['result_1']
        newNodeName = self._checkNodeName(result)
        print "\n[grapherUi] : Renaming %s ---> %s" % (selNode.__repr2__()['nodeName'], newNodeName)
        oldName = selNode._widget.__repr2__()['nodeName']
        selNode._widget.setGraphNodeName(newNodeName)
        self.renameDialog.close()
        #-- Refresh UI --#
        if self.mainUi.miNodeEditor.isChecked():
            if str(self.mainUi.nodeEditor.leNodeName.text()) == oldName:
                self.mainUi.nodeEditor.leNodeName.setText(newNodeName)
        #-- Refresh Instance --#
        allItems = pQt.getAllItems(self)
        for item in allItems:
            if item._instanceFrom is not None:
                if item._instanceFrom.__repr2__()['nodeName'] == newNodeName:
                    iName = item.__repr2__()['nodeName']
                    iNewName = "%s]_%s" % (iName.split(']')[0], newNodeName)
                    print "[grapherUi] : Renaming %s ---> %s" % (iName, iNewName)
                    item._widget.setGraphNodeName(iNewName)

    def getItemFromNodeName(self, nodeName):
        """ Get QTreeWidgetItem from given nodeName
            @param nodeName: (str) : Node name
            @return: (object) : QTreeWidgetItem """
        if nodeName is None:
            return None
        else:
            allItems = pQt.getAllItems(self)
            for item in allItems:
                if item._widget.__repr2__()['nodeName'] == nodeName:
                    return item

    def getAllInstance(self):
        """ Get graph instance node
            @return: (list) : Instance node """
        instances = []
        allItems = pQt.getAllItems(self)
        for item in allItems:
            if item._instanceFrom is not None:
                instances.append(item)
        return instances

    def getInstanceDict(self, instance):
        """ Get given instance dict
            @param instance: (object) : QTreeWidgetItem
            @return: (dict) : Instance dict """
        instDict = instance.__repr2__()
        refDict = instance._instanceFrom.__repr2__()
        for k, v in instDict.iteritems():
            refDict[k] = v
        return refDict

    def resetGraph(self):
        """ Reset graph tree """
        self.clear()

    def _checkNodeName(self, nodeName):
        """ Check if new name is valide
            @param nodeName: (str) : Node name
            @return: (str) : Valide node name """
        #-- Check Suffixe --#
        if len(nodeName.split('_')) < 2:
            tmpName = '%s_1' % nodeName
            tmpBaseName = nodeName
        else:
            if not nodeName.split('_')[-1].isdigit():
                tmpName = '%s_1' % nodeName
                tmpBaseName = nodeName
            else:
                tmpName = nodeName
                tmpBaseName = '_'.join(nodeName.split('_')[:-1])
        #-- Get Valide Name --#
        allItems = pQt.getAllItems(self)
        if not allItems:
            return tmpName
        else:
            indexes = []
            nodeExists = False
            for item in allItems:
                treeNodeName = item._widget.__repr2__()['nodeName']
                if treeNodeName == tmpName:
                    nodeExists = True
                if treeNodeName.startswith('%s_' % tmpBaseName):
                    indexes.append(int(treeNodeName.split('_')[-1]))
            if not nodeExists:
                return tmpName
            else:
                return '%s_%s' % (tmpBaseName, (max(indexes) + 1))

    def _checkInstanceName(self, instName):
        """ Check if new instance name is valide
            @param instName: (str) : Instance node name
            @return: (str) : Valide instance Name """
        baseName = instName.split(']')[-1]
        allInstance = self.getAllInstance()
        indexList = []
        for instance in allInstance:
            iName = instance.__repr2__()['nodeName']
            if iName.endswith(']%s' % baseName):
                index = iName.split(']')[0].replace('[', '')
                indexList.append(index)
        if not indexList:
            return instName
        else:
            i = sorted(indexList)[-1].replace('i', '')
            newIndex = 'i%s' % (int(i) + 1)
            return "[%s]%s" % (newIndex, baseName)

    def _checkNodeDict(self, **kwargs):
        """ Check and fill node params with default value
            @param kwargs: (dict) : Node params
            @return: (dict) : Node params """
        keyList = kwargs.keys()
        if not 'nodeEnabled' in keyList:
            kwargs['nodeEnabled'] = True
        if not 'nodeExpanded' in keyList:
            kwargs['nodeExpanded'] = False
        if not 'nodeType' in keyList:
            kwargs['nodeType'] = 'modul'
        if not 'instanceFrom' in keyList:
            kwargs['instanceFrom'] = None
        if not 'currentVersion' in keyList:
            kwargs['currentVersion'] = '001'
        if not 'versionTitle' in keyList:
            kwargs['versionTitle'] = {'001': 'New Version'}
        if not 'nodeComment' in keyList:
            kwargs['nodeComment'] = {'001': {'txt': "Add Comment", 'html': ""}}
        if not 'nodeVariables' in keyList:
            kwargs['nodeVariables'] = {'001': {}}
        if not 'nodeLoop' in keyList:
            kwargs['nodeLoop'] = {'type': 'range', 'iter': 'i', 'checkFile': 'tmpCheck',
                                          'start': '1', 'stop': '10', 'step': '1',
                                          'list': '2,3,4', 'single': '1'}
        if not 'nodeCmd' in keyList:
            kwargs['nodeCmd'] = ""
        if not 'nodeCmdInit' in keyList:
            kwargs['nodeCmdInit'] = ""
        if not 'nodeScript' in keyList:
            kwargs['nodeScript'] = {'001': ""}
        if not 'nodeNotes' in keyList:
            kwargs['nodeNotes'] = {'001': ""}
        return kwargs

    def _moveTopItem(self, selItems, side, **nodeDict):
        """ Move top level items
            @param selItems: (list) : List of QTreeWidgetItem
            @param side: (str) : 'up' or 'down'
            @param nodeDict: (dict) : Node params
            @return: (bool) : True if success, False if failed """
        currentIndex = self.indexOfTopLevelItem(selItems[0])
        topItemCount = self.topLevelItemCount()
        if side == 'up':
            if currentIndex > 0:
                self.takeTopLevelItem(currentIndex)
                self.addGraphNode(index=(currentIndex - 1), **nodeDict)
            else:
                return False
        elif side == 'down':
            newIndex = (currentIndex + 1)
            if newIndex < topItemCount:
                self.takeTopLevelItem(currentIndex)
                self.addGraphNode(index=newIndex, **nodeDict)
            else:
                return False
        return True

    def _moveChildItem(self, selItems, _parent, side, **nodeDict):
        """ Move child items
            @param selItems: (list) : List of QTreeWidgetItem
            @param _parent: (object) : QTreeWidgetItem
            @param side: (str) : 'up' or 'down'
            @param nodeDict: (dict) : Node params
            @return: (bool) : True if success, False if failed """
        currentIndex = None
        childCount = _parent.childCount()
        nodeDict['nodeParent'] = _parent
        for n in range(childCount):
            childItem = _parent.child(n)
            if childItem.__repr2__()['nodeName'] == selItems[0].__repr2__()['nodeName']:
                currentIndex = n
                break
        if side == 'up':
            if currentIndex > 0:
                _parent.removeChild(selItems[0])
                self.addGraphNode(index=(currentIndex - 1), **nodeDict)
            else:
                return False
        elif side == 'down':
            newIndex = (currentIndex + 1)
            if newIndex < childCount:
                _parent.removeChild(selItems[0])
                self.addGraphNode(index=newIndex, **nodeDict)
            else:
                return False
        return True

    def _pasteNode(self, selItems):
        """ Paste stored items with mode 'node'
            @param selItems: (list) : List of QTreeWidgetItem """
        for nodeDict in self.cpBuffer['nodeList']:
            if selItems:
                nodeDict['nodeParent'] = selItems[0]
            else:
                nodeDict['nodeParent'] = None
            if nodeDict['instanceFrom'] is not None:
                nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
            self.addGraphNode(**nodeDict)

    def _pasteBranch(self, selItems):
        """ Paste stored items with mode 'branch'
            @param selItems: (list) : List of QTreeWidgetItem """
        convertedDict = {}
        for n, nodeDict in enumerate(self.cpBuffer['nodeList']):
            if n == 0:
                if selItems:
                    nodeDict['nodeParent'] = selItems[0]
                else:
                    nodeDict['nodeParent'] = None
                if nodeDict['instanceFrom'] is not None:
                    nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
                newNode = self.addGraphNode(**nodeDict)
                convertedDict[nodeDict['nodeName']] = newNode.__repr2__()
            else:
                _parent = self.getItemFromNodeName(convertedDict[nodeDict['nodeParent']]['nodeName'])
                nodeDict['nodeParent'] = _parent
                if nodeDict['instanceFrom'] is not None:
                    nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
                newNode = self.addGraphNode(**nodeDict)
                convertedDict[nodeDict['nodeName']] = newNode.__repr2__()

    def _pullNodes(self, nodesDict, selItems):
        """ Pull nodes from buffer with mode 'node'
            @param nodesDict: (list) : List of dict to pull
            @param selItems: (list) : Parent item """
        for node in sorted(nodesDict.keys()):
            if node.startswith('selNode_'):
                nodeDict = nodesDict[node]
                if selItems:
                    nodeDict['nodeParent'] = selItems[0]
                else:
                    nodeDict['nodeParent'] = None
                if nodeDict['instanceFrom'] is not None:
                    nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
                self.addGraphNode(**nodeDict)

    def _pullBranch(self, nodesDict, selItems):
        """ Pull nodes from buffer with mode 'branch'
            @param nodesDict: (list) : List of dict to pull
            @param selItems: (list) : Parent item """
        convertedDict = {}
        nodesDict.pop('pushMode')
        for n, node in enumerate(sorted(nodesDict.keys())):
            nodeDict = nodesDict[node]
            if n == 0:
                if selItems:
                    nodeDict['nodeParent'] = selItems[0]
                else:
                    nodeDict['nodeParent'] = None
                if nodeDict['instanceFrom'] is not None:
                    nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
                newNode = self.addGraphNode(**nodeDict)
                convertedDict[nodeDict['nodeName']] = newNode.__repr2__()
            else:
                _parent = self.getItemFromNodeName(convertedDict[nodeDict['nodeParent']]['nodeName'])
                nodeDict['nodeParent'] = _parent
                if nodeDict['instanceFrom'] is not None:
                    nodeDict['instanceFrom'] = self.getItemFromNodeName(nodeDict['instanceFrom'])
                newNode = self.addGraphNode(**nodeDict)
                convertedDict[nodeDict['nodeName']] = newNode.__repr2__()

    def _reselectNodes(self, nodes):
        """ Reselect given nodes
            @param nodes: (list) : List of node names """
        for item in pQt.getAllItems(self):
            if item.__repr2__()['nodeName'] in nodes:
                self.setItemSelected(item, True)
            else:
                self.setItemSelected(item, False)


class GraphItem(QtGui.QTreeWidgetItem):
    """ Class used by GraphTree(), overriding QTreeWidgetItem
        @param tree: (object) : Parent QTreeWidget
        @param parent: (object) : Parent QTreeWidgetItem """

    def __init__(self, tree, parent):
        self._tree = tree
        self._parent = parent
        self._widget = GraphNode(self._tree, self)
        self._instanceFrom = None
        if self._parent is None:
            self._widgetIndex = 0
        else:
            self._widgetIndex = (self._parent._widgetIndex + 1)
        super(GraphItem, self).__init__()

    def __repr2__(self):
        itemDict = self._widget.__repr2__()
        #-- Add Parent Item --#
        if self.parent() is None:
            itemDict['nodeParent'] = None
        else:
            parentName = self.parent()._widget.__repr2__()['nodeName']
            itemDict['nodeParent'] = parentName
        #-- Add Instance Info --#
        if self._instanceFrom is not None:
            itemDict['instanceFrom'] = self._instanceFrom.__repr2__()['nodeName']
        else:
            itemDict['instanceFrom'] = None
        return itemDict

    def __str__(self):
        txt = []
        for k, v in self.__repr2__().iteritems():
            txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def addChild(self, QTreeWidgetItem):
        super(GraphItem, self).addChild(QTreeWidgetItem)
        self._tree.setItemWidget(QTreeWidgetItem, (self._widgetIndex + 1), QTreeWidgetItem._widget)

    def addChildren(self, list_of_QTreeWidgetItem):
        super(GraphItem, self).addChildren(list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self._tree.setItemWidget(item, (self._widgetIndex + 1), item._widget)

    def insertChild(self, p_int, QTreeWidgetItem):
        super(GraphItem, self).insertChild(p_int, QTreeWidgetItem)
        self._tree.setItemWidget(QTreeWidgetItem, (self._widgetIndex + 1), QTreeWidgetItem._widget)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        super(GraphItem, self).insertChildren(p_int, list_of_QTreeWidgetItem)
        for item in list_of_QTreeWidgetItem:
            self._tree.setItemWidget(item, (self._widgetIndex + 1), item._widget)

    def getChildren(self, depth=-1):
        """ Get all children items with given recursion
            @param depth: (int) : Number of recursion (-1 = infinite)
            @return: (list) : QTreeWigdetItem list """
        return pQt.getAllChildren(self, depth=depth)

    def getParents(self, depth=-1):
        """ Get all parent items with given recursion
            @param depth: (int) : Number of recursion (-1 = infinite)
            @return: (list) : QTreeWigdetItem list """
        return pQt.getAllParent(self, depth=depth)

    def setParams(self, **kwargs):
        """ Edit widget params
            @param kwargs: (dict) : Node params
                @keyword nodeName: (str) : New node name
                @keyword nodeEnabled: (bool) : New node state
                @keyword nodeExpanded: (bool) : New node expanded or collapsed """
        self._widget.setGraphNodeName(kwargs['nodeName'])
        self._widget.setGraphNodeEnabled(kwargs['nodeEnabled'])
        self._widget.setGraphNodeExpanded(kwargs['nodeExpanded'])

    def setDatas(self, **kwargs):
        """ Edit widget params
            @param kwargs: (dict) : Node datas
                @keyword nodeType: (str) : 'modul', 'loop', 'sysData', 'cmdData', 'purData'
                @keyword currentVersion: (str) : Current node version
                @keyword versionTitle: (dict) : Version titles"""
        for k, v in kwargs.iteritems():
            if hasattr(self._widget._data, k):
                setattr(self._widget._data, k, v)


graphNodeClass, graphNodeUiClass = uic.loadUiType(grapher.uiList['graphNode'])
class GraphNode(graphNodeClass, graphNodeUiClass, gpCore.Style):
    """ Class used by GraphItem(), adding widgets to QTreeWidgetItem
        @param tree: (object) : Parent QTreeWidget
        @param item: (object) : Parent QTreeWidgetItem """

    def __init__(self, tree, item):
        self._tree = tree
        self._item = item
        self._data = GraphNodeData()
        self.mainUi = self._tree.mainUi
        super(GraphNode, self).__init__()
        self._setupUi()

    def __repr2__(self):
        nodeDict = {'nodeName': str(self.pbNode.text()),
                    'nodeEnabled': self.cbNode.isChecked(),
                    'nodeExpanded': self._item.isExpanded()}
        if self._data is not None:
            for k, v in self._data.__repr2__().iteritems():
                nodeDict[k] = v
        return nodeDict

    def __str__(self):
        txt = []
        for k, v in self.__repr2__().iteritems():
            txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def _setupUi(self):
        self.setupUi(self)
        self.setStyleSheet(self.graphNodeBgc('modul'))
        self.pbExpand.clicked.connect(self.on_expandNode)
        self.cbNode.clicked.connect(self.on_enableNode)
        click_handler = pQt.ClickHandler(singleClickCmd=self._singleClick,
                                         doubleClickCmd=self._doubleClick)
        self.pbNode.clicked.connect(click_handler)

    def rf_childIndicator(self):
        """ Refresh children indicator """
        if self._item.childCount() > 0:
            self.lChildIndicator.setText("F")
        else:
            self.lChildIndicator.setText("")

    def on_expandNode(self):
        """ Expand or collapse item """
        self.setGraphNodeExpanded(not self._item.isExpanded())

    def on_enableNode(self):
        """ Enable or disable graphNode """
        self.setGraphNodeEnabled(self.cbNode.isChecked())

    def _singleClick(self):
        """ Connect graphNode to nodeEditor """
        if self.mainUi.miNodeEditor.isChecked():
            if self._item._instanceFrom is None:
                self.mainUi.nodeEditor.connectGraphNode(self)
            else:
                self.mainUi.nodeEditor.connectGraphNode(self._item._instanceFrom._widget)
            self.mainUi.nodeEditor.bClose.setVisible(False)

    def _doubleClick(self):
        """ Connect graphNode in an external nodeEditor """
        self.nodeEditor = nodeEditor.NodeEditor(self.mainUi)
        self.nodeEditor.show()
        if self._item._instanceFrom is None:
            self.nodeEditor.connectGraphNode(self)
        else:
            self.nodeEditor.connectGraphNode(self._item._instanceFrom._widget)
        self.nodeEditor.bClose.setVisible(True)

    def setGraphNodeBgc(self):
        """ Edit graphNode color """
        if self._item._instanceFrom is None:
            if self._data.nodeType is not None:
                self.setStyleSheet(self.graphNodeBgc(self._data.nodeType))
        else:
            self.setStyleSheet(self.graphInstanceBgc)

    def setGraphNodeName(self, nodeName):
        """ Edit graphNode button name
            @param nodeName: (str) : Node name"""
        self.pbNode.setText(nodeName)

    def setGraphNodeEnabled(self, nodeEnable):
        """ Edit graphNode checkBox state
            @param nodeEnable: (bool) : Node state """
        self.cbNode.setChecked(nodeEnable)
        self.pbNode.setEnabled(nodeEnable)

    def setGraphNodeExpanded(self, nodeExpanded):
        """ Edit graphNode QTreeWidgetItem state
            @param nodeExpanded: (bool) : QTreeWidgetItem state """
        self._item.setExpanded(nodeExpanded)
        if nodeExpanded:
            self.pbExpand.setText('-')
        else:
            self.pbExpand.setText('+')
        self._tree.rf_graphColumns()


class GraphNodeData(object):
    """ Class used by Grapher for graphNode data storage """

    def __init__(self):
        self.nodeType = None
        self.currentVersion = None
        self.versionTitle = {}
        self.nodeComment = {}
        self.nodeVariables = {}
        self.nodeLoop = {}
        self.nodeCmd = None
        self.nodeCmdInit = None
        self.nodeScript = {}
        self.nodeNotes = {}

    def __repr2__(self):
        return self.__dict__

    def __str__(self):
        txt = []
        for k, v in self.__repr2__().iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)
