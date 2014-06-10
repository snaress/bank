from PyQt4 import QtGui, QtCore, uic
from lib import qt


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


class ClickHandler(object):

    def __init__(self, time, singleClickCmd=None, doubleClickCmd=None):
        """ Activate double click for QPushButton
            @param time: (int) : Time in milliSec
            @param singleClickCmd: (object) : Command launch when single click is detected
            @param doubleClickCmd: (object) : Command launch when double click is detected """
        self.singleCmd = singleClickCmd
        self.doubleCmd = doubleClickCmd
        self.timer = QtCore.QTimer()
        self.timer.setInterval(time)
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


confirmDialogClass, confirmDialogUiClass = uic.loadUiType(qt.uiList['confirmDialog'])
class ConfirmDialog(confirmDialogClass, confirmDialogUiClass):
    """ Confirm dialog popup
        @param mess: (str) : Dialog texte
        @param btns: (list) : Buttons list (4 max)
        @param cmds: (list) Commands list(4 max) """

    def __init__(self, mess, btns=[], cmds=[]):
        #-- Init --#
        btns.reverse()
        cmds.reverse()
        super(ConfirmDialog, self).__init__()
        self.setupUi(self)
        #-- Get Kwargs --#
        self.mess = mess
        self.btns = btns
        self.cmds = cmds
        self.max = [self.bButton1, self.bButton2, self.bButton3, self.bButton4]
        #-- Message --#
        self.lMessage.setText(self.mess)
        #-- Button Visibility --#
        hide = (len(self.max))-(len(self.btns))
        for n in range(hide):
            self.max[n].setVisible(False)
        #-- Button Text and Action--#
        for n, btn in enumerate(self.btns):
            ind = (len(self.max))-n
            self.max[ind-1].setText(btn)
            self.max[ind-1].clicked.connect(self.cmds[n])


promptDialogClass, promptDialogUiClass = uic.loadUiType(qt.uiList['promptDialog'])
class PromptDialog(promptDialogClass, promptDialogUiClass):

    def __init__(self, mess, cmdsAccept, cmdsCancel):
        """ @param mess: (str) : Dialog texte
            @param cmdsAccept: (object) : Accept Command
            @param cmdsCancel: (object) : Cancel Command """
        #-- Init --#
        super(PromptDialog, self).__init__()
        self.setupUi(self)
        #-- Get Kwargs --#
        self.mess = mess
        self.accept = cmdsAccept
        self.cancel = cmdsCancel
        #-- Message --#
        self.lMessage.setText(self.mess)
        #-- Button Action--#
        self.bAccept.clicked.connect(self.accept)
        self.bCancel.clicked.connect(self.cancel)


commentDialogClass, commentDialogUiClass = uic.loadUiType(qt.uiList['commentDialog'])
class CommentDialog(commentDialogClass, commentDialogUiClass):

    def __init__(self, mess, cmdsAccept, cmdsCancel):
        """ @param mess: (str) : Dialog texte
            @param cmdsAccept: (object) : Accept Command
            @param cmdsCancel: (object) : Cancel Command """
        #-- Init --#
        super(CommentDialog, self).__init__()
        self.setupUi(self)
        #-- Get Kwargs --#
        self.mess = mess
        self.accept = cmdsAccept
        self.cancel = cmdsCancel
        #-- Message --#
        self.lMessage.setText(self.mess)
        #-- Button Action--#
        self.bAccept.clicked.connect(self.accept)
        self.bCancel.clicked.connect(self.cancel)
