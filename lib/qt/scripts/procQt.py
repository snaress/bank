from lib import qt
from PyQt4 import QtGui, uic


def getAllItems(twTree):
    """ Get all QTreeWidgetItem of given QTreeWidget
        @param twTree: (object) : QTreeWidget object
        @return: (list) : All QTreeWidgetItem list """
    items = []
    allItems = QtGui.QTreeWidgetItemIterator(twTree, QtGui.QTreeWidgetItemIterator.All) or None
    if allItems is not None:
        while allItems.value():
            item = allItems.value()
            items.append(item)
            allItems += 1
    return items

def getTopItems(twTree):
    """ Get all topLevelItems of given QTreeWidget
        @param twTree: (object) : QTreeWidget object
        @return: (list) : All topLevelItem list """
    items = []
    nTop = twTree.topLevelItemCount()
    for n in range(nTop):
        items.append(twTree.topLevelItem(n))
    return items

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
        @param cmds: (list) : Commands list """

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
