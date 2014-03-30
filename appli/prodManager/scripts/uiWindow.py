import os
from appli import prodManager
from lib.qt.scripts import dialog
from PyQt4 import QtGui, uic


newProjectClass, newProjectUiClass = uic.loadUiType(prodManager.uiList['newProject'])
class NewProjectUi(newProjectClass, newProjectUiClass):
    """ New Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow"""

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        super(NewProjectUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup New Project dialog """
        self.setupUi(self)
        self.bCreate.clicked.connect(self.on_create)
        self.bCancel.clicked.connect(self.close)

    def on_create(self):
        """ Command launch when Qbutton 'Create' is clicked """
        project = str(self.leProject.text())
        alias = str(self.leAlias.text())
        if not project == '' and not alias == '':
            result, mess = self.pm.newProject(project, alias)
            if result == '%s--%s' % (project, alias):
                self.mainUi.windowRefresh()
                self.close()
            else:
                self.confUi = dialog.ConfirmDialog('\n'.join(mess), btns=['Ok'], cmds=[self.on_dialogAccept])
                self.confUi.exec_()
        else:
            mess = ["#-- Warning --#",
                    "Project Name or Project Alias can't be empty !!!"]
            self.confUi = dialog.ConfirmDialog('\n'.join(mess), btns=['Ok'], cmds=[self.on_dialogAccept])
            self.confUi.exec_()

    def on_dialogAccept(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.confUi.close()


loadProjectClass, loadProjectUiClass = uic.loadUiType(prodManager.uiList['loadProject'])
class LoadProjectUi(loadProjectClass, loadProjectUiClass):
    """ Load Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        super(LoadProjectUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Load Project dialog """
        self.setupUi(self)
        self.bLoadProject.clicked.connect(self.on_load)
        self.bCancel.clicked.connect(self.close)
        self._populate()

    def _populate(self):
        """ Populate projects QTreeWidget """
        rootDir = os.path.join(prodManager.binPath, 'project')
        fldList = os.listdir(rootDir) or []
        for fld in fldList:
            projectPath = os.path.join(rootDir, fld)
            if os.path.isdir(projectPath) and not fld.startswith('.') and not fld.startswith('_'):
                newItem = QtGui.QTreeWidgetItem()
                newItem.setText(0, fld)
                newItem.projectName = fld.split('--')[0]
                newItem.projectAlias = fld.split('--')[1]
                newItem.projectAbsPath = projectPath
                self.twProjects.addTopLevelItem(newItem)

    def on_load(self):
        """  Command launch when bLoadProject is clicked """
        selItems = self.twProjects.selectedItems()
        if selItems:
            self.mainUi.loadProject(selItems[0].projectName, selItems[0].projectAlias)
            self.close()
