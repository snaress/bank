import sys
from functools import partial
from tools.apps import prodManager
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import procQt as pQt
from tools.apps.prodManager.scripts import uiCmds as pmUiCmds
from tools.apps.prodManager.scripts import prodManager as pm


prodManagerClass, prodManagerUiClass = uic.loadUiType(prodManager.uiList['prodManager'])
class ProdManagerUi(prodManagerClass, prodManagerUiClass):
    """ Class containing all prodManager's Ui actions for creation, loading,
        editing and writing datas in or from tool dataBase """

    def __init__(self):
        print "##### Launching ProdManager Ui #####"
        self.pm = pm.ProdManager()
        self.menuActions = pmUiCmds.MenuActions(self)
        self.uiActions = pmUiCmds.UiActions(self)
        super(ProdManagerUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)
        self._setupMenu()
        self._setupMainWindow()
        self._setupProject()
        self._setupShotInfo()
        self.windowInit()

    def _setupMenu(self):
        """ Setup menu """
        self.miNewProject.triggered.connect(self.menuActions.newProject)
        self.miLoadProject.triggered.connect(self.menuActions.loadProject)
        self.miCloseProject.triggered.connect(self.menuActions.closeProject)
        self.miProjectDict.triggered.connect(self.pm.printDict)
        self.miAssetTree.triggered.connect(partial(self.menuActions.helpTreeObj, 'assetTree'))
        self.miShotTree.triggered.connect(partial(self.menuActions.helpTreeObj, 'shotTree'))
        self.miPreviewAttr.triggered.connect(self.menuActions.helptPreviewAttr)

    def _setupMainWindow(self):
        """ Setup main window """
        self.rbMainAsset.clicked.connect(self.uiActions.rf_mainTree)
        self.rbMainShot.clicked.connect(self.uiActions.rf_mainTree)
        self.twProject.itemClicked.connect(self.uiActions.rf_shotInfoTab)

    def _setupProject(self):
        """ Setup project tab """
        self.bEditProjectTab.clicked.connect(self.uiActions.on_editProjectTab)
        self.bCancelProjectTab.clicked.connect(self.uiActions.on_cancelProjectTab)
        self.bOpenProjectWorkDir.clicked.connect(self.uiActions.on_openProjectWorkDir)
        self.cbProjectTree.clicked.connect(self.uiActions.on_projectTree)
        self.rbProjectAsset.clicked.connect(self.uiActions.rf_projectTree)
        self.rbProjectShot.clicked.connect(self.uiActions.rf_projectTree)
        self.bRfProjectTree.clicked.connect(self.uiActions.on_rfProjectTree)
        self.bProjectTreeUp.clicked.connect(partial(self.uiActions.moveProjectNode, 'up', 'tree'))
        self.bProjectTreeDn.clicked.connect(partial(self.uiActions.moveProjectNode, 'down', 'tree'))
        self.bProjectStepUp.clicked.connect(partial(self.uiActions.moveProjectNode, 'up', 'step'))
        self.bProjectStepDn.clicked.connect(partial(self.uiActions.moveProjectNode, 'down', 'step'))
        self.pop_projectTreeMenu()
        self.pop_projectStepMenu()

    def _setupShotInfo(self):
        """ Setup shot info tab """
        self.bEditShotInfoTab.clicked.connect(self.uiActions.on_editShotInfoTab)
        self.bCancelShotInfoTab.clicked.connect(self.uiActions.on_cancelShotInfoTab)
        self.bOpenAssetWorkDir.clicked.connect(self.uiActions.on_openShotInfoWorkDir)
        self.bOpenShotWorkDir.clicked.connect(self.uiActions.on_openShotInfoWorkDir)

    def windowInit(self):
        """ Main ui inititialize """
        self.uiActions.initMainUi()
        self.uiActions.initProjectTab()
        self.uiActions.initShotInfoTab()

    def windowRefresh(self):
        """ Main ui updates """
        self.uiActions.rf_maiUi()
        self.uiActions.rf_projectTab()

    def loadProject(self, projectName, projectAlias):
        """ Load given project
            @param projectName: (str) : Project Name
            @param projectAlias: (str) : Project Alias """
        self.pm.loadProject(projectName, projectAlias)
        self.windowRefresh()

    def pop_projectTreeMenu(self):
        """ Create project tree QTreeWidget popupMenu """
        self.tbProjectTreeMenu = QtGui.QToolBar()
        self.miNewAssetFld = self.tbProjectTreeMenu.addAction("New Asset Folder",
                             partial(self.menuActions.on_newProjectTreeItem, 'assetFld'))
        self.miNewShotFld = self.tbProjectTreeMenu.addAction("New Shot Folder",
                            partial(self.menuActions.on_newProjectTreeItem, 'shotFld'))
        self.miNewShotFlds = self.tbProjectTreeMenu.addAction("New Shot Folder List",
                             partial(self.menuActions.on_newProjectTreeItems, 'shotFld'))
        self.miNewAsset = self.tbProjectTreeMenu.addAction("New Asset",
                          partial(self.menuActions.on_newProjectTreeItem, 'asset'))
        self.miNewShot = self.tbProjectTreeMenu.addAction("New Shot",
                         partial(self.menuActions.on_newProjectTreeItem, 'shot'))
        self.miNewShots = self.tbProjectTreeMenu.addAction("New Shot List",
                          partial(self.menuActions.on_newProjectTreeItems, 'shot'))
        self.miDeleteNode = self.tbProjectTreeMenu.addAction("Delete Selected Nodes",
                            partial(self.menuActions.on_deleteProjectNode, 'tree'))
        self.twProjectTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.twProjectTree,
                     QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popProjectTreeMenu)
        self.menuProjectTree = QtGui.QMenu(self)
        self.menuProjectTree.setTearOffEnabled(True)
        self.menuProjectTree.addAction(self.miNewAssetFld)
        self.menuProjectTree.addAction(self.miNewShotFld)
        self.menuProjectTree.addAction(self.miNewShotFlds)
        self.menuProjectTree.addSeparator()
        self.menuProjectTree.addAction(self.miNewAsset)
        self.menuProjectTree.addAction(self.miNewShot)
        self.menuProjectTree.addAction(self.miNewShots)
        self.menuProjectTree.addSeparator()
        self.menuProjectTree.addAction(self.miDeleteNode)

    def on_popProjectTreeMenu(self, point):
        """ Create project tree popupMenu launcher """
        if self.bEditProjectTab.isChecked():
            checkState = self.rbProjectAsset.isChecked()
            self.miNewAssetFld.setEnabled(checkState)
            self.miNewAsset.setEnabled(checkState)
            self.miNewShotFld.setEnabled(not checkState)
            self.miNewShotFlds.setEnabled(not checkState)
            self.miNewShot.setEnabled(not checkState)
            self.miNewShots.setEnabled(not checkState)
            self.menuProjectTree.exec_(self.twProjectTree.mapToGlobal(point))

    def pop_projectStepMenu(self):
        """ Create project step QTreeWidget popupMenu """
        self.tbProjectStepMenu = QtGui.QToolBar()
        self.miNewAssetStep = self.tbProjectStepMenu.addAction("New Asset Step",
                              partial(self.menuActions.on_newProjectStepItem, 'step'))
        self.miNewAssetSubstep = self.tbProjectStepMenu.addAction("New Asset Substep",
                                 partial(self.menuActions.on_newProjectStepItem, 'substep'))
        self.miNewShotStep = self.tbProjectStepMenu.addAction("New Shot Step",
                             partial(self.menuActions.on_newProjectStepItem, 'step'))
        self.miNewShotSubstep = self.tbProjectStepMenu.addAction("New Shot Substep",
                                partial(self.menuActions.on_newProjectStepItem, 'substep'))
        self.miDeleteStep =  self.tbProjectStepMenu.addAction("Delete Selected Nodes",
                             partial(self.menuActions.on_deleteProjectNode, 'step'))
        self.twProjectStep.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.twProjectStep,
                     QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popProjectStepMenu)
        self.menuProjectStep = QtGui.QMenu(self)
        self.menuProjectStep.setTearOffEnabled(True)
        self.menuProjectStep.addAction(self.miNewAssetStep)
        self.menuProjectStep.addAction(self.miNewAssetSubstep)
        self.menuProjectStep.addSeparator()
        self.menuProjectStep.addAction(self.miNewShotStep)
        self.menuProjectStep.addAction(self.miNewShotSubstep)
        self.menuProjectStep.addSeparator()
        self.menuProjectStep.addAction(self.miDeleteStep)

    def on_popProjectStepMenu(self, point):
        """ Create project tree popupMenu launcher """
        if self.bEditProjectTab.isChecked():
            checkState = self.rbProjectAsset.isChecked()
            self.miNewAssetStep.setEnabled(checkState)
            self.miNewAssetSubstep.setEnabled(checkState)
            self.miNewShotStep.setEnabled(not checkState)
            self.miNewShotSubstep.setEnabled(not checkState)
            self.menuProjectStep.exec_(self.twProjectStep.mapToGlobal(point))

    @property
    def _getPreviewAttr(self):
        """ Get preview QLabel attributes
            @return: (dict) : Preview image attributes """
        previewDict = self.lPreview.__dict__
        for k in previewDict.keys():
            if not k.startswith('ima'):
                previewDict.pop(k)
        previewDict['imaWidgetWidth'] = self.lPreview.maximumWidth()
        previewDict['imaWidgetHeight'] = self.lPreview.maximumHeight()
        return previewDict

    def getTreeItemFromNodePath(self, twTree, nodePath):
        """ Get project tree QTreeWidgetItem with given nodePath
            @param twTree: (object) : QTreeWidget
            @param nodePath: (str) : Node path
            @return: (object) : QTreeWidgetItem """
        allItems = pQt.getAllItems(twTree)
        for item in allItems:
            if item.nodePath == nodePath:
                return item

    def getParentTreeItemFromNodePath(self, twTree, nodePath):
        """ Get project tree QTreeWidgetItem with given nodePath
            @param twTree: (object) : QTreeWidget
            @param nodePath: (str) : Node path
            @return: (object) : Parent QTreeWidgetItem """
        if not nodePath.split('/') > 1:
            return None
        else:
            path = '/'.join(nodePath.split('/')[:-1])
            allItems = pQt.getAllItems(twTree)
            for item in allItems:
                if item.nodePath == path:
                    return item

    def getTreeObjFromTreeWidgetType(self, treeWidgetType):
        """ Get QTreeWidget from given widget type
            @param treeWidgetType: (str) : 'tree' or 'step'
            @return: (object) : QTreeWidget """
        if treeWidgetType == 'tree':
            twTree = self.twProjectTree
        else:
            twTree = self.twProjectStep
        return twTree


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ProdManagerUi()
    window.loadProject('asterix', 'ddd')
    window.show()
    sys.exit(app.exec_())
