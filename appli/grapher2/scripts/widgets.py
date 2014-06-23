from appli import grapher2
from functools import partial
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import textEditor
from lib.qt.scripts import procQt as pQt


class Style(object):
    """ Class used for grapher2 style settings """

    @property
    def lockColor(self):
        return "background-color:Tomato;"

    @property
    def graphBgc(self):
        return "background-color:Black;"

    @property
    def graphNodeBgc(self):
        return "background-color:LightGrey;"


class TextEditor(textEditor.TextEditor):
    """ Class used by the grapherUi for text edition
        @param parent: (object) : QWidget parent """

    def __init__(self, parent):
        self.parent = parent
        self.stored = None
        super(TextEditor, self).__init__()
        self._setupWidget()
        self.rf_widgetVis()

    def _setupWidget(self):
        self.bClearText.setToolTip("Cancel Edition")
        self.bLoadFile.setToolTip("Start Edition")
        self.bSaveFile.setToolTip("Save Edition")

    def rf_widgetVis(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.bClearText.setEnabled(state)
        self.bLoadFile.setEnabled(not state)
        self.bSaveFile.setEnabled(state)
        for grp in [self.editActionGrp, self.textActionGrp, self.fontActionGrp]:
            for widget in grp:
                widget.setEnabled(state)
        self.teText.setReadOnly(not state)

    def rf_comment(self, textHtml):
        """ Refresh Grapher comment
            @param textHtml: (str) : Comment in html form """
        self.teText.setHtml(textHtml)

    def on_clearText(self):
        """ Switch widget visibility to disable edition and restore text """
        super(TextEditor, self).on_clearText()
        self.teText.setHtml(self.stored)
        self.rf_widgetVis()
        self.stored = None

    def on_loadFile(self):
        """ Switch widget visibility to enable edition """
        self.stored = self.teText.toHtml()
        self.rf_widgetVis(state=True)

    def on_saveFile(self):
        """ Switch widget visibility to disable edition and save text """
        self.stored = None
        self.rf_widgetVis()
        if str(self.parent.objectName()) == 'grapherUi':
            self.parent.grapher.ud_commentFromUi(self.parent)

    def resetComment(self):
        """ Reset Grapher comment """
        self.teText.clear()


varEditorClass, varEditorUiClass = uic.loadUiType(grapher2.uiList['varEditor'])
class VarEditor(varEditorClass, varEditorUiClass):
    """ Class used by the grapherUi for variable edition
        @param parent: (object) : QWidget parent """

    def __init__(self, parent):
        self.parent = parent
        super(VarEditor, self).__init__()
        self._setupUi()

    def __repr__(self):
        items = pQt.getTopItems(self.twVariables)
        varDict = {}
        for n, item in enumerate(items):
            varDict['var%s' % (n + 1)] = self.getItemDict(item)
        return varDict

    def __str__(self):
        text = ["#-- Variables --#"]
        for var in sorted(self.__repr__().keys()):
            text.append("%s = %s" % (var, self.__repr__()[var]))
        return '\n'.join(text)

    def _setupUi(self):
        self.setupUi(self)
        self._setupMain()
        self.rf_variablesBg()

    def _setupMain(self):
        self.bAddVar.clicked.connect(partial(self.on_addVar, index=None))
        self.bDelVar.clicked.connect(self.on_delVar)
        self.bVarUp.clicked.connect(partial(self.on_moveVar, 'up'))
        self.bVarDn.clicked.connect(partial(self.on_moveVar, 'down'))

    def rf_variablesBg(self):
        """ Refresh variables background form and color """
        self.twVariables.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.twVariables.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.twVariables.header().setResizeMode(3, QtGui.QHeaderView.ResizeToContents)

    def rf_variables(self, **kwargs):
        """ Refresh variables values
            @param kwargs: (dict) : Variables dict """
        self.resetVariables()
        for var in sorted(kwargs.keys()):
            newItem = self.on_addVar()
            self.setItem(newItem, **kwargs[var])
            self.on_varEnable(newItem)

    def on_addVar(self, index=None):
        """ Add new variable
            @param index: (int) : Index for item insertion
            @return: (object) : QTreeWidgetItem """
        newItem = self.new_varItem()
        if index is None:
            self.twVariables.addTopLevelItem(newItem)
        else:
            self.twVariables.insertTopLevelItem(index, newItem)
            self.reindexVar()
        self.twVariables.setItemWidget(newItem, 1, newItem.wdgEnabled)
        self.twVariables.setItemWidget(newItem, 2, newItem.wdgLabel)
        self.twVariables.setItemWidget(newItem, 3, newItem.wdgType)
        self.twVariables.setItemWidget(newItem, 4, newItem.wdgValue)
        self.twVariables.setItemWidget(newItem, 5, newItem.wdgComment)
        newItem.wdgEnabled.clicked.connect(partial(self.on_varEnable, newItem))
        return newItem

    def on_delVar(self):
        """ Delete selected variables """
        selItems = self.twVariables.selectedItems()
        selItems.reverse()
        if selItems:
            for item in selItems:
                ind = self.twVariables.indexOfTopLevelItem(item)
                self.twVariables.takeTopLevelItem(ind)
        self.reindexVar()

    def on_moveVar(self, side):
        """ Move selected variables
            @param side: (str) : 'up' or 'down' """
        selItems = self.twVariables.selectedItems()
        allItems = pQt.getTopItems(self.twVariables)
        if selItems:
            if side == 'down':
                selItems.reverse()
            movedItems = []
            for item in selItems:
                ind = self.twVariables.indexOfTopLevelItem(item)
                itemDict = self.getItemDict(item)
                check = False
                if side == 'up':
                    if ind > 0:
                        self.twVariables.takeTopLevelItem(ind)
                        newItem = self.on_addVar(ind - 1)
                        check = True
                elif side == 'down':
                    if ind < (len(allItems) - 1):
                        self.twVariables.takeTopLevelItem(ind)
                        newItem = self.on_addVar(ind + 1)
                        check = True
                if check:
                    movedItems.append(newItem)
                    self.setItem(newItem, **itemDict)
                    self.on_varEnable(newItem)
            for moved in movedItems:
                moved.setSelected(True)

    def on_varEnable(self, item):
        """ Enable or disable variable when QCheckBox is clicked
            @param item: (object) : QTreeWidgetItem"""
        state = item.wdgEnabled.isChecked()
        item.wdgLabel.setEnabled(state)
        item.wdgType.setEnabled(state)
        item.wdgValue.setEnabled(state)
        item.wdgComment.setEnabled(state)

    def reindexVar(self):
        """ Reindex variable items """
        for n, item in enumerate(pQt.getTopItems(self.twVariables)):
            item.setText(0, "%s" % (n + 1))

    def getItemDict(self, item):
        """ Get given treeItem dict
            @param item: (object) : QTreeWidgetItem
            @return: (dict) : Given item params """
        newDict = {}
        itemDict = item.__dict__
        newDict['enabled'] = itemDict['wdgEnabled'].isChecked()
        newDict['label'] = str(itemDict['wdgLabel'].text())
        newDict['type'] = str(itemDict['wdgType'].currentText())
        newDict['value'] = str(itemDict['wdgValue'].text())
        newDict['comment'] = str(itemDict['wdgComment'].text())
        return newDict

    @staticmethod
    def setItem(item, **kwargs):
        """ Set item with given params
            @param item: (object) : QTreeWidgetItem
            @param kwargs: (dict) : Item params """
        item.wdgEnabled.setChecked(kwargs['enabled'])
        item.wdgLabel.setText(kwargs['label'])
        item.wdgType.setCurrentIndex(item.wdgType.findText(kwargs['type']))
        item.wdgValue.setText(kwargs['value'])
        item.wdgComment.setText(kwargs['comment'])

    def new_varItem(self):
        """ Create new variable item
            @return: (objrct) : QTreeWidgetItem """
        newInd = (len(pQt.getTopItems(self.twVariables)) + 1)
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, str(newInd))
        newItem.wdgEnabled = self.new_varEnabledWidget()
        newItem.wdgLabel = self.new_varTextWidget()
        newItem.wdgType = self.new_varTypeWidget()
        newItem.wdgValue = self.new_varTextWidget()
        newItem.wdgComment = self.new_varTextWidget()
        return newItem

    def new_varEnabledWidget(self):
        """ Create new varEnable checkBox
            @return: (objrct) : QCheckBox """
        newWidget = QtGui.QCheckBox()
        newWidget.setChecked(True)
        return newWidget

    @staticmethod
    def new_varTypeWidget():
        """ Create new varType comboBox
            @return: (objrct) : QComboBox """
        newWidget = QtGui.QComboBox()
        newWidget.addItems(['=', '+', 'num'])
        return newWidget

    @staticmethod
    def new_varTextWidget():
        """ Create new varText lineEdit
            @return: (objrct) : QLineEdit """
        newWidget = QtGui.QLineEdit()
        return newWidget

    def resetVariables(self):
        """ Reset variables """
        self.twVariables.clear()


class GraphZone(QtGui.QTreeWidget):
    """ Class used by the grapherUi for graph tree edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.columns = 10
        super(GraphZone, self).__init__()
        self._setupUi()
        self._setupMainUi()
        self.popUpMenu()

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

    def _setupMainUi(self):
        self.mainUi.miNewGraphNode.triggered.connect(self.on_newGraphNode)
        self.mainUi.miNewGraphNode.setShortcut("N")

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

    def rf_graph(self):
        """ Refresh graph tree """
        self.resetGraph()
        for node in self.grapher.graphTree['_order']:
            nodeDict = self.grapher.graphTree[node]
            _parent = self.getItemFromNodeName(nodeDict['nodeParent'])
            newItem, newWidget = self.new_graphItem(_parent=_parent)
            if _parent is None:
                self.addTopLevelItem(newItem)
                self.setItemWidget(newItem, 0, newWidget)
                newItem._widgetInd = 0
            else:
                _parent.addChild(newItem)
                ind = (_parent._widgetInd + 1)
                self.setItemWidget(newItem, ind, newWidget)
                newItem._widgetInd = ind
        self.rf_graphColumns()

    def dropEvent(self, QDropEvent):
        srcItems = self.selectedItems()
        dstItem = self.itemAt(QDropEvent.pos())
        kbMod = QDropEvent.keyboardModifiers()
        if kbMod == QtCore.Qt.ControlModifier:
            print 'copy'
        elif kbMod == QtCore.Qt.ShiftModifier:
            print 'clone'
        elif kbMod == QtCore.Qt.AltModifier:
            print 'instance'
        super(GraphZone, self).dropEvent(QDropEvent)
        self.rf_graphColumns()

    def popUpMenu(self):
        """ Create QTreeWidget popup menu """
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popUpMenu)
        self.tbGraph = QtGui.QToolBar()
        self.pMenu = QtGui.QMenu(self.mainUi)
        self.miNewGraphNode = self.tbGraph.addAction("New Node", self.on_newGraphNode)
        self.miNewGraphNode.setShortcut("N")
        self.pMenu.addAction(self.miNewGraphNode)

    def on_popUpMenu(self, point):
        """ Show popup menu
            @param point: (object) : QPoint """
        self.pMenu.exec_(self.mapToGlobal(point))

    def on_newGraphNode(self):
        """ Create new graphNode item """
        selItems = self.selectedItems()
        #-- Add Top Item --#
        if not selItems:
            newItem, newWidget = self.new_graphItem()
            self.addTopLevelItem(newItem)
            self.setItemWidget(newItem, 0, newWidget)
            newItem._widgetInd = 0
        #-- Add Child Item --#
        else:
            if len(selItems) > 1:
                errorDial = QtGui.QErrorMessage(self.mainUi)
                errorDial.showMessage("!!! Warning: Select only one node !!!")
            else:
                newItem, newWidget = self.new_graphItem(_parent=selItems[0])
                selItems[0].addChild(newItem)
                ind = (selItems[0]._widgetInd + 1)
                self.setItemWidget(newItem, ind, newWidget)
                newItem._widgetInd = ind
        self.rf_graphColumns()

    def new_graphItem(self, _parent=None):
        """ New graphNode item
            @return: (object), (object) : QTreeWidgetItem, QWidget """
        newItem = QtGui.QTreeWidgetItem()
        newWidget = GraphNodeWidget(self, newItem, _parent)
        newWidget.pbNode.setText(self.newNodeName())
        newItem._widget = newWidget
        return newItem, newWidget

    def newNodeName(self):
        allItems = pQt.getAllItems(self)
        if not allItems:
            return 'NewNode_1'
        else:
            names = []
            for item in allItems:
                nodeName = item._widget.__repr__()['nodeName']
                if nodeName.startswith('NewNode_'):
                    names.append(nodeName)
            names.sort()
            return 'NewNode_%s' % (int(names[-1].split('_')[-1]) + 1)

    def getItemFromNodeName(self, nodeName):
        if nodeName is None:
            return None
        else:
            allItems = pQt.getAllItems(self)
            for item in allItems:
                if item._widget.__repr__()['nodeName'] == nodeName:
                    return item

    def resetGraph(self):
        """ Reset graph tree """
        self.clear()


graphNodeClass, graphNodeUiClass = uic.loadUiType(grapher2.uiList['graphNode'])
class GraphNodeWidget(graphNodeClass, graphNodeUiClass, Style):

    def __init__(self, tree, item, _parent):
        self.tree = tree
        self.item = item
        self._parent = _parent
        super(GraphNodeWidget, self).__init__()
        self._setupUi()

    def __repr__(self):
        if self._parent is None:
            _parentItem = None
        else:
            _parentItem = self._parent._widget.__repr__()['nodeName']
        return {'nodeName': str(self.pbNode.text()), 'nodeParent': _parentItem,
                'nodeEnabled': self.cbNode.isChecked()}

    def _setupUi(self):
        self.setupUi(self)
        self.setStyleSheet(self.graphNodeBgc)
        self.pbExpand.clicked.connect(self.on_expandNode)
        self.cbNode.clicked.connect(self.on_enableNode)

    def on_enableNode(self):
        """ Enable or disable graphNode """
        self.pbNode.setEnabled(self.cbNode.isChecked())

    def on_expandNode(self):
        if str(self.pbExpand.text()) == '+':
            self.item.setExpanded(True)
            self.pbExpand.setText('-')
        else:
            self.item.setExpanded(False)
            self.pbExpand.setText('+')