from lib import qt
from PyQt4 import QtGui, QtCore, uic


#============================================ Action =============================================#

class ClickHandler(object):
    """ Single and double click options
        @param dcTimer: (int) : Double click timer (in mili seconds)
        @param singleClickCmd: (object) : Single click command
        @param doubleClickCmd: (object) : Double click command """

    # noinspection PyUnresolvedReferences
    def __init__(self, dcTimer=200, singleClickCmd=None, doubleClickCmd=None):
        """ Activate double click for QPushButton
            @param dcTimer: (int) : Time in milliSec
            @param singleClickCmd: (object) : Command launch when single click is detected
            @param doubleClickCmd: (object) : Command launch when double click is detected """
        self.singleCmd = singleClickCmd
        self.doubleCmd = doubleClickCmd
        self.timer = QtCore.QTimer()
        self.timer.setInterval(dcTimer)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_count = 0

    def timeout(self):
        if self.click_count == 1:
            if self.singleCmd is not None:
                self.singleCmd()
        elif self.click_count > 1:
            if self.doubleCmd is not None:
                self.doubleCmd()
        self.click_count = 0

    def __call__(self):
        self.click_count += 1
        if not self.timer.isActive():
            self.timer.start()

#========================================== QTreeWidget ==========================================#

def getAllItems(QTreeWidget):
    """ Get all QTreeWidgetItem of given QTreeWidget
        @param QTreeWidget: (object) : QTreeWidget object
        @return: (list) : All QTreeWidgetItem list """
    items = []
    allItems = QtGui.QTreeWidgetItemIterator(QTreeWidget, QtGui.QTreeWidgetItemIterator.All) or None
    if allItems is not None:
        while allItems.value():
            item = allItems.value()
            items.append(item)
            allItems += 1
    return items

def getTopItems(QTreeWidget):
    """ Get all topLevelItems of given QTreeWidget
        @param QTreeWidget: (object) : QTreeWidget object
        @return: (list) : All topLevelItem list """
    items = []
    nTop = QTreeWidget.topLevelItemCount()
    for n in range(nTop):
        items.append(QTreeWidget.topLevelItem(n))
    return items

def getAllChildren(QTreeWidgetItem, depth=-1):
    """ Get all children of given QTreeWidgetItem
        @param QTreeWidgetItem: (object) : Recusion start QTreeWidgetItem
        @param depth: (int) : Number of recursion (-1 = infinite)
        @return: (list) : QTreeWigdetItem list """
    items = []

    def recurse(currentItem, depth):
        items.append(currentItem)
        if depth != 0:
            for n in range(currentItem.childCount()):
                recurse(currentItem.child(n), depth-1)

    recurse(QTreeWidgetItem, depth)
    return items

def getAllParent(QTreeWidgetItem, depth=-1):
    """ Get all parent of given QTreeWidgetItem
        @param QTreeWidgetItem: (object) : Recusion start QTreeWidgetItem
        @param depth: (int) : Number of recursion (-1 = infinite)
        @return: (list) : QTreeWigdetItem list """
    items = []

    def recurse(currentItem, depth):
        items.append(currentItem)
        if depth != 0:
            if currentItem.parent() is not None:
                recurse(currentItem.parent(), depth-1)

    recurse(QTreeWidgetItem, depth)
    return items

def rf_selTreeItemTextColor(twTree, columns=None, color1=None, color2=None, rgb1=None, rgb2=None):
    """ Refresh selected QTreeWidgetItems font color
        @param twTree: (object) : QTreeWidget
        @param columns: (int or list) : Columns number
        @param color1: (str) : Color key when item is selected
        @param color2: (str) : Color key when item is not selected
        @param rgb1: (tuple) : Rgb color when item is selected
        @param rgb2: (tuple) : Rgb color when item is not selected """
    #-- Get columns --#
    columnList = []
    if columns is None:
        for n in range(twTree.columnCount()):
            columnList.append(n)
    elif isinstance(columns, int):
        columnList = [columns]
    elif isinstance(columns, list):
        columnList = columns
    #-- Edit TextColor --#
    allItems = getAllItems(twTree)
    for item in allItems:
        for n in columnList:
            if item.isSelected():
                item.setTextColor(n, UiStyle().qtColor(color=color1, rgb=rgb1))
            else:
                item.setTextColor(n, UiStyle().qtColor(color=color2, rgb=rgb2))

#=========================================== QComboBox ===========================================#

def getComboBoxItems(QComboBox):
    """ Get all given conboBox items
        @param QComboBox: (object) : QComboBox
        @return: (list) : Items text list """
    items = []
    for n in range(QComboBox.count()):
        items.append(str(QComboBox.itemText(n)))
    return items

#============================================ QDialog ============================================#

def fileDialog(fdMode='open', fdFileMode='AnyFile', fdRoot=None, fdRoots=None,
               fdFilters=None, fdCmd=None):
    """ FileDialog popup
        @param fdMode: (str) : setAcceptMode 'open' or 'save'
        @param fdFileMode: (str) : setFileMode 'AnyFile', 'ExistingFile', 'Directory', 'DirectoryOnly'
        @param fdRoot: (str) : Start root path
        @param fdRoots: (list) : List of recent files (list[str(QUrl)])
        @param fdFilters: (list) : List of extensions
        @param fdCmd: (object) : Command for accepted execution
        @return: (object) : QFileDiaolog widget object """
    fd = QtGui.QFileDialog()
    #-- FileDialog AcceptedMode --#
    if fdMode == 'open':
        fd.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
    elif fdMode == 'save':
        fd.setAcceptMode(QtGui.QFileDialog.AcceptSave)
    #-- FileDialog FileMode --#
    if fdFileMode == 'AnyFile':
        fd.setFileMode(QtGui.QFileDialog.AnyFile)
    elif fdFileMode == 'ExistingFile':
        fd.setFileMode(QtGui.QFileDialog.ExistingFile)
    elif fdFileMode == 'Directory':
        fd.setFileMode(QtGui.QFileDialog.Directory)
    elif fdFileMode == 'DirectoryOnly':
        fd.setFileMode(QtGui.QFileDialog.DirectoryOnly)
    #-- FileDialog Params --#
    if fdRoot is not None:
        fd.setDirectory(fdRoot)
    if fdRoots is not None:
        fd.setSidebarUrls(fdRoots)
    if fdFilters is not None:
        fd.setFilters(fdFilters)
    if fdCmd is not None:
        fd.accepted.connect(fdCmd)
    return fd

def errorDialog(message, parent):
    """ Launch default error dialog
        @param message: (str or list): Message to print
        @param parent: (object) : Parent ui """
    errorDial = QtGui.QErrorMessage(parent)
    if isinstance(message, list):
        errorDial.showMessage('\n'.join(message))
    else:
        errorDial.showMessage(message)


confirmDialogClass, confirmDialogUiClass = uic.loadUiType(qt.uiList['confirmDialog'])
class ConfirmDialog(confirmDialogClass, confirmDialogUiClass):
    """ Confirm dialog popup
        @param message: (str) : Dialog texte
        @param buttons: (list) : Buttons list
        @param btnCmds: (list) : Commands list
        @param cancelBtn: (bool) : Add cacnel button """

    def __init__(self, message, buttons, btnCmds, cancelBtn=True):
        if not len(buttons) == len(btnCmds):
            raise KeyError, "!!! Error: Buttons list and cmds lists should have same length !!!"
        else:
            self.mess = message
            buttons.reverse()
            self.btns = buttons
            btnCmds.reverse()
            self.btnCmds = btnCmds
            self.cancelBtn = cancelBtn
            super(ConfirmDialog, self).__init__()
            self.setupUi(self)
            self.initDialog()

    def initDialog(self):
        """ Init dialog window """
        self.lMessage.setText(self.mess)
        if self.cancelBtn:
            newButton = self.newButton('Cancel', self.close)
            self.hlButtons.insertWidget(1, newButton)
        for n, btn in enumerate(self.btns):
            newButton = self.newButton(btn, self.btnCmds[n])
            self.hlButtons.insertWidget(1, newButton)

    def newButton(self, label, btnCmd):
        """ Create new button
            @param label: (str) : Button label
            @param btnCmd: (object) : Button command
            @return: (object) : New QPushButton """
        newButton = QtGui.QPushButton()
        newButton.setText(label)
        newButton.clicked.connect(btnCmd)
        return newButton


promptDialogClass, promptDialogUiClass = uic.loadUiType(qt.uiList['promptDialog'])
class PromptDialog(promptDialogClass, promptDialogUiClass):
    """ Prompt dialog popup
        @param message: (str) : Dialog texte
        @param acceptCmd: (object) : Accept command
        @param cancelCmd: (object) : Cancel command
        @param Nlines: (int) : Prompt line count """

    def __init__(self, message, acceptCmd, cancelCmd=None, Nlines=1):
        self.message = message
        self.acceptCmd = acceptCmd
        self.cancelCmd = cancelCmd
        self.Nlines = Nlines
        super(PromptDialog, self).__init__()
        self.setupUi(self)
        self.initDialog()

    def initDialog(self):
        """ Init dialog window """
        self.lMessage.setText(self.message)
        for n in range(self.Nlines):
            newWidget = QtGui.QLineEdit()
            newItem = QtGui.QTreeWidgetItem()
            newItem._widget = newWidget
            self.twPrompt.addTopLevelItem(newItem)
            self.twPrompt.setItemWidget(newItem, 0, newWidget)
        self.bAccept.clicked.connect(self.acceptCmd)
        if self.cancelCmd is None:
            self.bCancel.clicked.connect(self.close)
        else:
            self.bCancel.clicked.connect(self.cancelCmd)

    def result(self):
        """ Get QLineEdit value
            @return: (dict) : Prompt result """
        results = {}
        allItems = getTopItems(self.twPrompt)
        for n, item in enumerate(allItems):
            results['result_%s' % (n+1)] = str(item._widget.text())
        return results

#============================================ QStyle =============================================#

class UiStyle(object):

    _blackColor = (0, 0, 0)
    _darkGreyColor = (62, 62, 62)
    _darkGreyColor2 = (75, 75, 75)
    _darkGreyColor3 = (85, 85, 85)
    _lightGreyColor = (192, 192, 192)
    _whiteColor = (255, 255, 255)

    def __init__(self):
        pass

    def darkGreyWidget(self):
        return "background-color: rgb%s; color: rgb%s" % (str(self._darkGreyColor),
                                                          str(self._lightGreyColor))

    def darkGreyHeader(self):
        return "QHeaderView::section {background-color: rgb%s; color: rgb%s}" % (str(self._darkGreyColor2),
                                                                                 str(self._lightGreyColor))

    def darkGreyTabs(self):
        return "QTabBar::tab {background-color: rgb%s; color: rgb%s}; "  % (str(self._darkGreyColor2),
                                                                            str(self._lightGreyColor))

    def qtColor(self, color=None, rgb=None):
        """ Return QColor object. If rgb is not None, color key will not be evaluated
            @param color: (str) : Background color ('black', 'darkGrey', 'grey', 'lightGrey', white)
            @param rgb: (tuple) : Background color (int, int, int)
            @return: (object) : QColor """
        if rgb is None:
            colors = ['black', 'darkGrey', 'grey', 'lightGrey', 'white']
            if color in colors:
                col = getattr(self, '_%sColor' % color)
                return QtGui.QColor(col[0], col[1], col[2])
            else:
                raise KeyError, "Unknown color: %s. Should be in %s" % (color, colors)
        else:
            return QtGui.QColor(rgb[0], rgb[1], rgb[2])
