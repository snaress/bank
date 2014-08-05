import os
from appli import grapher
from functools import partial
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import procFile as pFile
from lib.qt.scripts import textEditor, scriptEditor


class Comment(textEditor.TextEditor):
    """ Class used by the grapherUi for text edition
        @param parent: (object) : QWidget parent """

    def __init__(self, parent):
        self.parent = parent
        self.stored = None
        super(Comment, self).__init__()
        self._setupWidget()
        self.rf_widgetVis()

    def __repr2__(self):
        return {'commentHtml': str(self.teText.toHtml()),
                'commentTxt': str(self.teText.toPlainText())}

    def __str__(self):
        return self.__repr2__()['commentTxt']

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
        super(Comment, self).on_clearText()
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
        elif str(self.parent.objectName()) == 'nodeEditor':
            self.rf_widgetVis(state=False)

    def resetComment(self):
        """ Reset Grapher comment """
        self.teText.clear()


class ScriptEditor(scriptEditor.ScriptEditor):

    def __init__(self, parent):
        self.parent = parent
        super(ScriptEditor, self).__init__()

    def __repr2__(self):
        return str(self._widget.toPlainText())

    def __str__(self):
        return self.__repr2__()


varEditorClass, varEditorUiClass = uic.loadUiType(grapher.uiList['varEditor'])
class VarEditor(varEditorClass, varEditorUiClass):
    """ Class used by the grapherUi for variable edition
        @param mainUi: (object) : QMainWindow
        @param parent: (object) : QWidget parent """

    def __init__(self, mainUi, parent):
        self.mainUi = mainUi
        self._parent = parent
        self.grapher = self.mainUi.grapher
        super(VarEditor, self).__init__()
        self._setupUi()

    def __repr2__(self):
        items = pQt.getTopItems(self.twVariables)
        varDict = {}
        for n, item in enumerate(items):
            varDict['var%s' % (n + 1)] = self.getItemDict(item)
        return varDict

    def __str__(self):
        text = ["#-- Variables --#"]
        for var in sorted(self.__repr2__().keys()):
            text.append("%s = %s" % (var, self.__repr2__()[var]))
        return '\n'.join(text)

    def _setupUi(self):
        self.setupUi(self)
        #-- Var Tree --#
        self.twVariables = VarTree(self)
        self.glVarEditor.addWidget(self.twVariables)
        #-- Actions --#
        self.bAddVar.clicked.connect(partial(self.on_addVar, index=None))
        self.bDelVar.clicked.connect(self.on_delVar)
        self.bPushVar.clicked.connect(self.on_pushVar)
        self.bPullVar.clicked.connect(self.on_pullVar)

    def rf_variables(self, **kwargs):
        """ Refresh variables values
            @param kwargs: (dict) : Variables dict """
        self.resetTree()
        for var in sorted(kwargs.keys()):
            newItem = self.on_addVar()
            self.setItem(newItem, **kwargs[var])
            self.on_varEnable(newItem)

    def on_addVar(self, index=None):
        """ Add new variable
            @param index: (int) : Index for item insertion
            @return: (object) : QTreeWidgetItem """
        newItem = self.twVariables.new_varItem()
        if index is None:
            self.twVariables.addTopLevelItem(newItem)
        else:
            self.twVariables.insertTopLevelItem(index, newItem)
        self.twVariables.setItemWidget(newItem, 1, newItem.wdgEnabled)
        self.twVariables.setItemWidget(newItem, 2, newItem.wdgLabel)
        self.twVariables.setItemWidget(newItem, 3, newItem.wdgType)
        self.twVariables.setItemWidget(newItem, 4, newItem.wdgValue)
        self.twVariables.setItemWidget(newItem, 5, newItem.wdgComment)
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

    def on_pushVar(self):
        """ Push selected items into buffer """
        if not os.path.exists(grapher.binPath):
            mess = "!!! ERROR: rndBin path not found, check __init__.py !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            tmpPath = os.path.join(self.grapher.userBinPath, 'tmp')
            pFile.mkPathFolders(grapher.binPath, tmpPath)
            tmpFile = os.path.join(tmpPath, 'varBuffer.py')
            selItems = self.twVariables.selectedItems()
            txt = []
            for n, selVar in enumerate(selItems):
                txt.append("selVar_%s = %s" % ((n + 1), self.getItemDict(selVar)))
            try:
                pFile.writeFile(tmpFile, '\n'.join(txt))
                print "[grapherUI] : Variables successfully pushed in user buffer."
            except:
                mess = "!!! ERROR: Can not store variables in buffer !!!"
                self.mainUi._defaultErrorDialog(mess, self.mainUi)

    def on_pullVar(self):
        """ Pull items from buffer """
        if not os.path.exists(grapher.binPath):
            mess = "!!! ERROR: rndBin path not found, check user pref !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            tmpPath = os.path.join(self.grapher.userBinPath, 'tmp')
            tmpFile = os.path.join(tmpPath, 'varBuffer.py')
            varDict = pFile.readPyFile(tmpFile)
            for var in sorted(varDict.keys()):
                if var.startswith('selVar_'):
                    newItem = self.on_addVar()
                    self.setItem(newItem, **varDict[var])

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

    def resetTree(self):
        """ Reset variable tree """
        self.twVariables.clear()


class VarTree(QtGui.QTreeWidget):
    """ Overrided QTreeWidget used by varEditor
        @param parent: (object) : QWidget parent """

    def __init__(self, parent):
        self.treeParent = parent
        super(VarTree, self).__init__()
        self._setupTree()

    def _setupTree(self):
        #-- Columns --#
        self.setColumnCount(6)
        self.setHeaderLabels(['Ind', 'On', 'Label', 'Type', 'Value', 'Comment'])
        self.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.header().setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        #-- Items --#
        self.setIndentation(0)
        self.setItemsExpandable(False)
        self.setSelectionMode(QtGui.QTreeWidget.ExtendedSelection)
        #-- Drag & Drop --#
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.LinkAction)

    def dropEvent(self, QDropEvent):
        """ Overrides QTreeWidget dorp event
            @param QDropEvent: (object) : QtGui.QDropEvent """
        srcItems = self.selectedItems()
        dstInd = (self.indexAt(QDropEvent.pos()).row() + 1)
        kbMod = QDropEvent.keyboardModifiers()
        #-- Create New Items --#
        for n, srcItem in enumerate(srcItems):
            itemDict = self.treeParent.getItemDict(srcItem)
            newItem = self.treeParent.on_addVar(index=(dstInd + n))
            self.treeParent.setItem(newItem, **itemDict)
        #-- Remove Items --#
        if not kbMod == QtCore.Qt.ControlModifier:
            for srcItem in srcItems:
                self.takeTopLevelItem(self.indexOfTopLevelItem(srcItem))
        self.treeParent.reindexVar()

    def new_varItem(self):
        """ Create new variable item
            @return: (objrct) : QTreeWidgetItem """
        newInd = (len(pQt.getTopItems(self)) + 1)
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, str(newInd))
        newItem._treeParent = self
        newItem._wdgtParent = self.treeParent
        newItem.wdgEnabled = self.new_varEnabledWidget()
        newItem.wdgLabel = self.new_varTextWidget()
        newItem.wdgType = self.new_varTypeWidget()
        newItem.wdgValue = self.new_varTextWidget()
        newItem.wdgComment = self.new_varTextWidget()
        return newItem

    @staticmethod
    def new_varEnabledWidget():
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


libEditorClass, libEditorUiClass = uic.loadUiType(grapher.uiList['libEditor'])
class LibEditor(libEditorClass, libEditorUiClass):
    """ Class used by the grapher libEditor Ui for lib edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        super(LibEditor, self).__init__()
        self._setupUi()
        self.rf_libTree()
        self.rf_libPath()
        self.rf_libTab()

    def _setupUi(self):
        self.setupUi(self)
        self.rbStudio.clicked.connect(self.on_libRoot)
        self.rbProd.clicked.connect(self.on_libRoot)
        self.rbUsers.clicked.connect(self.on_libRoot)
        self.rbScript.clicked.connect(self.on_libType)
        self.rbNode.clicked.connect(self.on_libType)
        self.rbBranch.clicked.connect(self.on_libType)
        self.twLibTree.clicked.connect(self.on_libTree)
        self.wgScript = ScriptEditor(self)
        self.vlScript.insertWidget(-1, self.wgScript)
        self.pbSave.clicked.connect(self.on_save)

    def rf_libTree(self):
        """ Refresh lib tree """
        self.twLibTree.clear()
        rootPath, libFld = self.libRootPath
        if libFld == 'prod':
            prods = os.listdir(rootPath) or []
            for prod in prods:
                prodPath = os.path.join(rootPath, prod)
                if os.path.isdir(prodPath):
                    newProdItem = self.newLibItem(prod, prodPath, 'fld')
                    self._addCategory(prodPath, newProdItem)
        else:
            self._addCategory(rootPath)

    def rf_libPath(self):
        """ Refresh lib path label """
        selItems = self.twLibTree.selectedItems()
        if not selItems:
            path, fld = self.libRootPath
            self.lLibPathVal.setText(path)
        else:
            if selItems[0].itemType == 'fld':
                if not hasattr(selItems[0], 'isRoot'):
                    self.lLibPathVal.setText(selItems[0].path)
                else:
                    self.lLibPathVal.setText(os.path.join(selItems[0].path, self.getItemType))
            else:
                self.lLibPathVal.setText(os.path.join(selItems[0].path.split(os.sep))[:-1])

    def rf_libFileName(self):
        """ Refresh lib fileName lineEdit """
        self.leFileName.clear()
        selItems = self.twLibTree.selectedItems()
        if selItems:
            if selItems[0].itemType == 'file':
                fileName = selItems[0].path.split(os.sep)[-1].replace('.py', '')
                self.leFileName.setText(fileName)

    def rf_libTab(self):
        """ Refresh lib edit tab """
        if self.rbScript.isChecked():
            self.flScript.setVisible(True)
            self.flSaveSpacer.setVisible(False)
        else:
            self.flScript.setVisible(False)
            self.flSaveSpacer.setVisible(True)

    def _addCategory(self, rootPath, _parent=None):
        """ Add lib subFolders and files
            @param rootPath: (str) : Lib root path
            @param _parent: (object) : Parent QTreeWidgetItem """
        cats = os.listdir(rootPath) or []
        for cat in cats:
            libPath = None
            catPath = os.path.join(rootPath, cat)
            newCatItem = self.newLibItem(cat, catPath, 'fld', _parent=_parent)
            newCatItem.isRoot = True
            if self.rbScript.isChecked():
                libPath = os.path.join(catPath, 'script')
            elif self.rbNode.isChecked():
                libPath = os.path.join(catPath, 'node')
            elif self.rbBranch.isChecked():
                libPath = os.path.join(catPath, 'branch')
            files = os.listdir(libPath) or []
            for f in files:
                filePath = os.path.join(libPath, f)
                if os.path.isfile(filePath):
                    self.newLibItem(f, filePath, 'file', _parent=newCatItem)

    def newLibItem(self, label, libPath, itemType, _parent=None):
        """ Create new QTreeWidgetItem
            @param label: (str) : Item label
            @param libPath: (str) : Item lib path
            @param itemType: (str) : 'fld' or 'file'
            @param _parent: (object) : Parent QtreeWidgetItem
            @return: (object) : Parent QtreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, label)
        if itemType == 'file':
            newItem.setTextColor(0, QtGui.QColor(0, 0, 255))
        newItem.name = label
        newItem.path = libPath
        newItem.itemType = itemType
        if _parent is None:
            self.twLibTree.addTopLevelItem(newItem)
        else:
            _parent.addChild(newItem)
        return newItem

    def on_libRoot(self):
        """ Command launch when rbLibRoot is clicked """
        self.rf_libTree()
        self.rf_libPath()
        self.rf_libFileName()

    def on_libType(self):
        """ Command launch when rbLibType is clicked """
        self.rf_libPath()
        self.rf_libFileName()
        self.rf_libTab()

    def on_libTree(self):
        """ Command launch when itemTree QTreeWidgetItem is clicked """
        self.rf_libPath()
        self.rf_libFileName()
        self.rf_libTab()

    def on_save(self):
        """ Command launch when QPushButton 'save' is clicked """
        checkFN = True
        filePath = str(self.lLibPathVal.text())
        fileName = str(self.leFileName.text())
        #-- Check FileName --#
        exclude = [' ', '/', '\\', '.']
        if fileName == '' or fileName == ' ' or fileName.startswith('_'):
            mess = "!!! ERROR: FileName can not be empty !!!"
            self.mainUi._defaultErrorDialog(mess, self)
        else:
            for iter in exclude:
                if iter in fileName:
                    checkFN = False
            if not checkFN:
                mess = "!!! ERROR: FileName is not valid !!!"
                self.mainUi._defaultErrorDialog(mess, self)
            else:
                #-- Check FilePath --#
                if not (filePath.endswith('script') or not filePath.endswith('node')
                        or not filePath.endswith('branch')):
                    mess = "!!! ERROR: FilePath is not valid !!!"
                    self.mainUi._defaultErrorDialog(mess, self)
                else:
                    absPath = os.path.join(filePath, "%s.py" % fileName)
                    if os.path.exists(absPath):
                        print 'exists'

    @property
    def libRootPath(self):
        """ Get lib root path
            @return: (str), (str) : Lib root path, Lib folder """
        path = grapher.binPath
        libFld = None
        #-- Lib Root --#
        if self.rbStudio.isChecked():
            libFld = 'studio'
            path = os.path.join(path, libFld)
        elif self.rbProd.isChecked():
            libFld = 'prod'
            path = os.path.join(path, libFld)
        elif self.rbUsers.isChecked():
            libFld = 'users'
            path = os.path.join(path, libFld, grapher.user[0], grapher.user, 'lib')
        return path, libFld

    @property
    def getItemType(self):
        if self.rbScript.isChecked():
            return 'script'
        elif self.rbNode.isChecked():
            return 'node'
        elif self.rbBranch.isChecked():
            return 'branch'
