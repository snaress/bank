import sys
from appli import prodManager
from functools import partial
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import procQt as pQt
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
        self.twProjectTrees.clicked.connect(self.uiRf_projectTab.rf_projectTree)
        self.bProjectTreeUp.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                    self.twProjectTree, 'up', rf=True))
        self.bProjectTreeDn.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                    self.twProjectTree, 'down', rf=True))
        self.bProjectStepUp.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                    self.twProjectStep, 'up', rf=True))
        self.bProjectStepDn.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                    self.twProjectStep, 'down', rf=True))
        self.bProjectAttrUp.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                    self.twProjectAttr, 'up', rf=True))
        self.bProjectAttrDn.clicked.connect(partial(self.uiCmds_projectTab.on_moveTreeItem,
                                                    self.twProjectAttr, 'down', rf=True))
        self.uiRf_projectTab.pop_projectTreeMenu()
        self.uiRf_projectTab.pop_projectStepMenu()
        self.uiRf_projectTab.pop_projectAttrMenu()

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

    def on_popProjectTreeMenu(self, point):
        """ Create project tree popupMenu launcher """
        if self.bEditProjectTab.isChecked():
            if self.twProjectTrees.selectedItems():
                self.menuProjectTree.exec_(self.twProjectTree.mapToGlobal(point))

    def on_popProjectStepMenu(self, point):
        """ Create project step popupMenu launcher """
        if self.bEditProjectTab.isChecked():
            if self.twProjectTrees.selectedItems():
                self.menuProjectStep.exec_(self.twProjectStep.mapToGlobal(point))

    def on_popProjectAttrMenu(self, point):
        """ Create project attributes popupMenu launcher """
        if self.bEditProjectTab.isChecked():
            if self.twProjectTrees.selectedItems():
                self.menuProjectAttr.exec_(self.twProjectAttr.mapToGlobal(point))

    @staticmethod
    def unselectAllItems(twTree):
        """ Unselect all items of given QTreeWidget
            @param twTree: (object) : QTreeWidget """
        selItems = twTree.selectedItems()
        if selItems:
            for item in selItems:
                item.setSelected(False)

    @staticmethod
    def delSelItems(twTree):
        """ Remove selected items from given QTreeWidget
            @param twTree: (object) : QTreeWidget """
        selItems = twTree.selectedItems()
        for item in selItems:
            if item.parent() is None:
                ind = twTree.indexOfTopLevelItem(item)
                twTree.takeTopLevelItem(ind)
            else:
                ind = item.parent().indexOfChild(item)
                item.parent().takeChild(ind)

    @staticmethod
    def treeToDict(twTree):
        """ Convert QTreeWidget to dict list
            @param twTree: (object) : QTreeWidget
            @return: (list) : Tree dict list """
        nodeList = []
        items = pQt.getAllItems(twTree)
        for item in items:
            nodeDict = {}
            for k, v in item.__dict__.iteritems():
                nodeDict[k] = v
            nodeList.append(nodeDict)
        return nodeList

    @staticmethod
    def getParentItemFromNodePath(twTree, nodePath):
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



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ProdManagerUi()
    window.loadProject('asterix', 'ddd')
    window.show()
    sys.exit(app.exec_())
