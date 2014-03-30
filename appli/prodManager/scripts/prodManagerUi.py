import sys
from appli import prodManager
from functools import partial
from PyQt4 import QtGui, QtCore, uic
from appli.prodManager.scripts import prodManager as pm
from appli.prodManager.scripts import uiCmds as pmUiCmds
from appli.prodManager.scripts import uiRefresh as pmRefresh


prodManagerClass, prodManagerUiClass = uic.loadUiType(prodManager.uiList['prodManager'])
class ProdManagerUi(prodManagerClass, prodManagerUiClass):
    """ Class containing all prodManager's Ui actions for creation, loading,
        editing and writing datas in or from tool dataBase """

    def __init__(self):
        print "##### Launching ProdManager Ui #####"
        self.pm = pm.ProdManager()
        self.uiRf_previewImage = pmRefresh.PreviewImage(self)
        self.uiRf_projectTab = pmRefresh.ProjectTab(self)
        self.uiCmds_menu = pmUiCmds.MenuCmds(self)
        self.uiCmds_projectTab = pmUiCmds.ProjectTab(self)
        super(ProdManagerUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)
        self._setupMenu()
        self._setupProject()
        self.windowInit()

    def _setupMenu(self):
        """ Setup menu """
        self.miNewProject.triggered.connect(self.uiCmds_menu.newProject)
        self.miLoadProject.triggered.connect(self.uiCmds_menu.loadProject)
        self.miProdManagerParams.triggered.connect(self.uiCmds_menu.printProdManagerParams)
        self.miProjectParams.triggered.connect(self.uiCmds_menu.printProjectParams)

    def _setupProject(self):
        """ Setup project tab """
        self.bEditProjectTab.clicked.connect(self.uiCmds_projectTab.on_editProjectTab)
        self.bCancelProjectTab.clicked.connect(self.uiCmds_projectTab.on_cancelProjectTab)
        self.bOpenProjectWorkDir.clicked.connect(self.uiCmds_projectTab.on_openProjectWorkDir)
        self.cbProjectTrees.clicked.connect(self.uiCmds_projectTab.on_projectTrees)
        self.bProjectTreesAdd.clicked.connect(self.uiCmds_projectTab.on_addTree)
        self.bProjectTreesUp.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                     self.twProjectTrees, 'up'))
        self.bProjectTreesDn.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                     self.twProjectTrees, 'down'))

    def windowInit(self):
        """ Main ui inititialize """
        self.setGeometry(QtCore.QRect(100, 50, 1200, 800))
        self.setWindowTitle("ProdManager: Untitled")
        self.uiRf_previewImage.rf_previewIma(prodManager.imaList['prodManager.png'])
        self.uiRf_projectTab.initProjectTab()

    def windowRefresh(self):
        """ Main ui updates """
        self.uiRf_projectTab.rf_projectTab()

    def loadProject(self, projectName, projectAlias):
        """ Load given project
            @param projectName: (str) : Project Name
            @param projectAlias: (str) : Project Alias """
        self.pm.loadProject(projectName, projectAlias)
        self.windowRefresh()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ProdManagerUi()
    window.loadProject('asterix', 'ddd')
    window.show()
    sys.exit(app.exec_())
