from appli import grapher
from PyQt4 import QtGui, uic
from functools import partial
from lib.qt.scripts import textEditor
from lib.qt.scripts import procQt as pQt
from appli.grapher.scripts import refresh


nodeEditorClass, nodeEditorUiClass = uic.loadUiType(grapher.uiList['nodeEditor'])
class NodeEditor(nodeEditorClass, nodeEditorUiClass):
    """ Class used for graph nodes editing """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.rf_shared = refresh.SharedWidget(self.mainUi, self)
        super(NodeEditor, self).__init__()
        self._setupUi()
        self.initUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupMain()

    def _setupMain(self):
        #-- Comment Zone --#
        self.wgComment = TextEditor(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(self.rf_shared.rf_commentVis)
        #-- Variables Zone --#
        self.wgVariables = VarEditor(self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(self.rf_shared.rf_variablesVis)
        #-- Trash Zone --#
        self.cbTrash.clicked.connect(self.rf_trashVis)

    def initUi(self):
        """ Initialize ui """
        self.rf_shared.rf_commentVis()
        self.rf_shared.rf_variablesVis()
        self.rf_trashVis()

    def rf_trashVis(self):
        """ Refresh nodeEditor trash visibility """
        widgets = [self.teTrash]
        self.mainUi.rf_zoneVisibility(self.cbTrash, widgets, self.flTrash)

    def resetUi(self):
        """ Reset NodeEditor ui """
        self.wgComment.resetComment()
        self.wgVariables.resetVariables()


class TextEditor(textEditor.TextEditor):
    """ Class used by the grapherUi for text editing
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


varEditorClass, varEditorUiClass = uic.loadUiType(grapher.uiList['varEditor'])
class VarEditor(varEditorClass, varEditorUiClass):

    def __init__(self, parent):
        self.parent = parent
        super(VarEditor, self).__init__()
        self._setupUi()

    def __repr__(self):
        items = pQt.getTopItems(self.twVariables)
        varDict = {}
        for n, item in enumerate(items):
            varDict['var%s' % (n+1)] = self.getItemDict(item)
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

    def on_addVar(self, index=None):
        """ Add new variable
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
                        newItem = self.on_addVar(ind-1)
                        check = True
                elif side == 'down':
                    if ind < (len(allItems) - 1):
                        self.twVariables.takeTopLevelItem(ind)
                        newItem = self.on_addVar(ind+1)
                        check = True
                if check:
                    movedItems.append(newItem)
                    self.setItem(newItem, **itemDict)
            for moved in movedItems:
                moved.setSelected(True)

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
        newDict['type'] = ''
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


class Style(object):
    """ Class used for grapher style settings """

    @property
    def lockColor(self):
        return "background-color:Tomato;"

    @property
    def graphBgc(self):
        return "background-color:Black;"
