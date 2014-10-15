import os, sys
from functools import partial
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.userManager import userManager
from appli.userManager.ui import userManagerUI, userEditorUI


class UserManagerUi(QtGui.QMainWindow, userManagerUI.Ui_userManager, pQt.Style):
    """ UserManagerUi MainWindow
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="UM-ui", level=logLvl)
        self.log.info("#-- Launching UserManager --#")
        self.um = userManager.UserManager(logLvl=logLvl)
        self.um.parse()
        super(UserManagerUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        self.log.debug("#-- Setup UserManager Ui --#")
        self.setupUi(self)
        self.setStyleSheet(self.applyStyle(styleName='darkOrange'))
        self.bNewUser.clicked.connect(self.on_newUser)
        self.bEditUser.clicked.connect(self.on_editUser)
        self.bDelUser.clicked.connect(self.on_delUser)
        self.twTree = UserTree(self)

    def on_newUser(self):
        """ Command launched when 'New User' QPushButton is clicked """
        self.editor = UserEditor(self)
        self.editor.exec_()

    def on_editUser(self):
        """ Command launched when 'Edit User' QPushButton is clicked """
        selItems = self.twTree.selectedItems()
        if selItems:
            self.editor = UserEditor(self, userNode=selItems[0].userNode)
            self.editor.exec_()

    def on_delUser(self):
        """ Command launched when 'Del User' QPushButton is clicked """
        selItems = self.twTree.selectedItems()
        if selItems:
            node = selItems[0].userNode
            mess = "Delete User: %s %s -- %r ?" % (node.name, node.firstName, node.alias)
            self.confDial = pQt.ConfirmDialog(mess, ['Delete'], [partial(self.delUser, node)])
            self.confDial.exec_()

    def delUser(self, userNode):
        """ Delete selected user
            @param userNode: (object) : User node """
        result, log = userNode.remove()
        if not result:
            pQt.errorDialog(log, self.confDial)
        else:
            self.um.parse()
            self.twTree._refresh()
            self.confDial.close()


class UserTree(QtGui.QTreeWidget):
    """ UserManager tree
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        super(UserTree, self).__init__()
        self.mainUi = mainUi
        self.um = self.mainUi.um
        self.log = self.mainUi.log
        self._setupWidget()
        self.mainUi.glUserManager.addWidget(self)
        self._refresh()

    def _setupWidget(self):
        self.log.debug("#-- Setup UserTree Widget --#")
        self.setColumnCount(len(self.um.userAttrs))
        self.setHeaderLabels(self.um.userAttrs)
        self.header().setStretchLastSection(False)
        alignment = QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter
        self.setSortingEnabled(True)
        self.header().setSortIndicatorShown(True)
        self.header().setSortIndicator(2, QtCore.Qt.AscendingOrder)
        for n in range(len(self.um.userAttrs)):
            self.headerItem().setTextAlignment(n, alignment)
            self.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)

    def _refresh(self):
        self.clear()
        userItems = []
        for user in self.um.users:
            newUserItem = UserItem(self.mainUi, user)
            userItems.append(newUserItem)
        self.addTopLevelItems(userItems)


class UserItem(QtGui.QTreeWidgetItem):
    """ UserManager treeItem
        @param mainUi: (object) : QMainWindow
        @param userNode: (object) : UserManager.users node """

    def __init__(self, mainUi, userNode):
        self.mainUi = mainUi
        self.um = self.mainUi.um
        self.userNode = userNode
        super(UserItem, self).__init__()
        self._refresh()

    def _refresh(self):
        userDict = self.userNode.__getDict__
        for n, attr in enumerate(self.um.userAttrs):
            if not attr in ['photo', 'logo']:
                self.setText(n, userDict[attr])
                self.setTextAlignment(n, 4)


class UserEditor(QtGui.QDialog, userEditorUI.Ui_userEditor, pQt.Style):
    """ UserManager treeItem editor
        @param mainUi: (object) : QMainWindow
        @param userNode: (object) : UserManager.users node """

    def __init__(self, mainUi, userNode=None):
        self.mainUi = mainUi
        self.um = self.mainUi.um
        self.log = self.mainUi.log
        self.usersPath = os.path.join(self.um.binPath, 'users')
        self.userNode = userNode
        super(UserEditor, self).__init__()
        self._setupUi()
        self._refresh()

    @property
    def __getDict__(self):
        return {'name': str(self.leName.text()),
                'firstName': str(self.leFirstName.text()),
                'alias': str(self.leAlias.text()),
                'photo': str(self.lePhoto.text()),
                'logo': str(self.leLogo.text()),
                'userGrp': str(self.cbUserGrp.currentText()),
                'status': str(self.cbStatus.currentText())}

    def _setupUi(self):
        self.setupUi(self)
        self.setStyleSheet(self.applyStyle(styleName='darkOrange'))
        self.bOpenPhoto.clicked.connect(partial(self.on_open, self.lePhoto))
        self.bOpenLogo.clicked.connect(partial(self.on_open, self.leLogo))
        self.cbUserGrp.addItems(self.um.userGroups)
        self.cbUserGrp.setCurrentIndex(self.cbUserGrp.findText("grp"))
        self.cbStatus.addItems(self.um.userStatus)
        self.cbStatus.setCurrentIndex(self.cbStatus.findText("active"))
        self.bSave.clicked.connect(self.on_save)
        self.bCancel.clicked.connect(self.close)

    def _refresh(self):
        if self.userNode is not None:
            self.leName.setText(self.userNode.name)
            self.leFirstName.setText(self.userNode.firstName)
            self.leAlias.setText(self.userNode.alias)
            self.lePhoto.setText(self.userNode.photo)
            self.leLogo.setText(self.userNode.logo)
            self.cbUserGrp.setCurrentIndex(self.cbUserGrp.findText(self.userNode.userGrp))
            self.cbStatus.setCurrentIndex(self.cbStatus.findText(self.userNode.status))
        else:
            self.lePhoto.setEnabled(False)
            self.bOpenPhoto.setEnabled(False)
            self.leLogo.setEnabled(False)
            self.bOpenLogo.setEnabled(False)

    def on_open(self, QLineEdit):
        """ Command launched when 'Open' QPushButton is clicked
            @param QLineEdit: (object) : QLineEdit """
        if os.path.exists(self.userNode._userPath):
            self.fdPath = pQt.fileDialog(fdRoot=self.userNode._userPath,
                                         fdCmd=partial(self.ud_imaPath, QLineEdit))
            self.fdPath.setFileMode(QtGui.QFileDialog.AnyFile)
            self.fdPath.exec_()

    def on_save(self):
        """ Command launched whan 'Save' QPushButton is clicked """
        if self.userNode is None:
            result, log = self.um.newUser(**self.__getDict__)
        else:
            self.userNode.updateData(**self.__getDict__)
            result, log = self.userNode.writeData()
        if not result:
            pQt.errorDialog(log, self)
        else:
            self.userNode.updateIcone('photo')
            self.mainUi.twTree._refresh()
            self.close()

    def ud_imaPath(self, QLineEdit):
        """ Update given image path widget
            @param QLineEdit: (object) : QLineEdit """
        selPath = self.fdPath.selectedFiles()
        if selPath:
            QLineEdit.setText(str(selPath[0]))


def launch(logLvl='info'):
    """ UserManager launcher
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """
    app = QtGui.QApplication(sys.argv)
    window = UserManagerUi(logLvl=logLvl)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()