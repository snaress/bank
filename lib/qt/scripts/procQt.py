from lib import qt
from PyQt4 import QtGui, uic


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


confirmDialogClass, confirmDialogUiClass = uic.loadUiType(qt.uiList['confirmDialog2'])
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


promptDialogClass, promptDialogUiClass = uic.loadUiType(qt.uiList['promptDialog2'])
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
