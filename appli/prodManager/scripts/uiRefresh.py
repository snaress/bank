import os
from functools import partial
from PyQt4 import QtGui, QtCore
from lib.qt.scripts import procQt as pQt
from appli.prodManager.scripts import template as pmTemplate


class PreviewImage(object):
    """ Class used by the ProdManagerUi for previewImage updates and refresh
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.defaultTemplate = pmTemplate.DefaultTemplate

    def rf_previewIma(self, ima):
        """ Refresh preview image with given image
            @param ima: (str) : Preview image absolut path """
        self.mainUi.previewIma = QtGui.QPixmap(ima)
        self.mainUi.lPreview.setPixmap(self.mainUi.previewIma)
        self.rf_previewSize()
        self.rf_previewAttr(ima)

    def rf_previewSize(self):
        """ Refresh preview size """
        maxWidth, maxHeight = self.defaultTemplate.previewMaxSize()
        imaWidth = self.mainUi.previewIma.width()
        imaHeight = self.mainUi.previewIma.height()
        maxRatio = float(maxWidth)/float(maxHeight)
        imaRatio = float(imaWidth)/float(imaHeight)
        if imaRatio < maxRatio:
            newWidth = int(maxHeight*imaRatio)
            self.mainUi.lPreview.setMinimumSize(QtCore.QSize(newWidth, maxHeight))
            self.mainUi.lPreview.setMaximumSize(QtCore.QSize(newWidth, maxHeight))
        elif imaRatio == maxRatio:
            self.mainUi.lPreview.setMinimumSize(QtCore.QSize(maxWidth, maxHeight))
            self.mainUi.lPreview.setMaximumSize(QtCore.QSize(maxWidth, maxHeight))
        elif imaRatio > maxRatio:
            newHeight = int(maxWidth/imaRatio)
            self.mainUi.lPreview.setMinimumSize(QtCore.QSize(maxWidth, newHeight))
            self.mainUi.lPreview.setMaximumSize(QtCore.QSize(maxWidth, newHeight))

    def rf_previewAttr(self, ima):
        """ Refresh preview attribute with given image
            @param ima: (str) : Preview image absolut path """
        self.mainUi.lPreview.imaAbsPath = ima
        self.mainUi.lPreview.imaFileName = os.path.basename(ima)
        self.mainUi.lPreview.imaDirPath = os.path.dirname(ima)
        self.mainUi.lPreview.imaWidth = self.mainUi.previewIma.width()
        self.mainUi.lPreview.imaHeight = self.mainUi.previewIma.height()


class ProjectTab(object):
    """ Class used by the ProdManagerUi for projectTab updates and refresh
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.populate = PopulateTrees(self.mainUi)

    def initProjectTab(self):
        """ Initialize project tab """
        self.mainUi.qfProject.setVisible(False)
        self.mainUi.lProject.setText('')
        self.mainUi.deProjectStart.setDisplayFormat("yyyy/MM/dd")
        self.mainUi.deProjectEnd.setDisplayFormat("yyyy/MM/dd")
        self.mainUi.splitProjectTrees.setVisible(False)
        self.mainUi.twProjectTrees.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.twProjectTrees.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.rf_projectTabVis()

    def rf_projectTabVis(self, state=False):
        """ Refresh project tab ui visibility
            @param state: (bool) : Visibility state """
        #-- Init Project Label --#
        self.mainUi.bCancelProjectTab.setVisible(state)
        #-- Init Project Date --#
        self.mainUi.deProjectStart.setEnabled(state)
        self.mainUi.deProjectStart.setCalendarPopup(state)
        self.mainUi.deProjectEnd.setEnabled(state)
        self.mainUi.deProjectEnd.setCalendarPopup(state)
        #-- Init Project Work Directory --#
        self.mainUi.leProjectWorkDir.setEnabled(state)
        self.mainUi.bOpenProjectWorkDir.setEnabled(state)
        #-- Init Project Trees --#
        self.mainUi.bProjectTreesAdd.setEnabled(state)
        self.mainUi.bProjectTreesUp.setEnabled(state)
        self.mainUi.bProjectTreesDn.setEnabled(state)
        self.mainUi.bProjectTreeUp.setEnabled(state)
        self.mainUi.bProjectTreeDn.setEnabled(state)
        self.mainUi.bProjectStepUp.setEnabled(state)
        self.mainUi.bProjectStepDn.setEnabled(state)

    def rf_projectTab(self):
        """ Refresh project tab """
        self.mainUi.setWindowTitle("ProdManager: %s--%s" % (self.pm.project.projectName,
                                                            self.pm.project.projectAlias))
        #-- Refresh Project Label --#
        self.mainUi.qfProject.setVisible(True)
        self.mainUi.lProject.setText('%s (%s)' % (self.pm.project.projectName,
                                                  self.pm.project.projectAlias))
        #-- Refresh Project Date --#
        self.mainUi.deProjectStart.setDate(QtCore.QDate(int(self.pm.project.projectStart.split('/')[0]),
                                                        int(self.pm.project.projectStart.split('/')[1]),
                                                        int(self.pm.project.projectStart.split('/')[2])))
        self.mainUi.deProjectEnd.setDate(QtCore.QDate(int(self.pm.project.projectEnd.split('/')[0]),
                                                      int(self.pm.project.projectEnd.split('/')[1]),
                                                      int(self.pm.project.projectEnd.split('/')[2])))
        #-- Refresh Project Work Directory --#
        self.mainUi.leProjectWorkDir.setText(self.pm.project.projectWorkDir)
        #-- Refresh Project Trees --#
        self.mainUi.twProjectTrees.clear()
        self.mainUi.twProjectTree.clear()
        self.mainUi.twProjectStep.clear()
        self.populate.projectTrees()

    def rf_projectTree(self):
        """ Refresh projectTree """
        self.mainUi.twProjectTree.clear()
        self.mainUi.twProjectStep.clear()
        selTree = self.mainUi.twProjectTrees.selectedItems()
        if selTree:
            self.populate.projectTree()
            self.populate.projectStep()

    def ud_projectTreesItem(self, treeItem):
        """ Update projectTrees QTreeWidgetItem.treeNodes
            @param treeItem: (object) : QTreeWidgetItem """
        #-- Update TreeSteps --#
        treeSteps = []
        for step in pQt.getTopItems(self.mainUi.twProjectStep):
            treeSteps.append(step.nodeName)
        treeItem.treeSteps = treeSteps
        #-- Update TreeNodes --#
        treeDict = self.mainUi.treeToDict(self.mainUi.twProjectTree)
        treeItem.treeNodes = treeDict

    def pop_projectTreeMenu(self):
        """ Create project tree QTreeWidget popupMenu """
        self.mainUi.tbProjectTreeMenu = QtGui.QToolBar()
        self.mainUi.miNewContainer = self.mainUi.tbProjectTreeMenu.addAction("New Container",
                                     partial(self.mainUi.uiCmds_menu.on_newProjectTreeItem,
                                             'container'))
        self.mainUi.miNewNode = self.mainUi.tbProjectTreeMenu.addAction("New Node",
                                partial(self.mainUi.uiCmds_menu.on_newProjectTreeItem, 'node'))
        self.mainUi.miNewContainers = self.mainUi.tbProjectTreeMenu.addAction("New Container List",
                                      partial(self.mainUi.uiCmds_menu.on_newProjectTreeItems,
                                              'container'))
        self.mainUi.miNewNodes = self.mainUi.tbProjectTreeMenu.addAction("New Node List",
                                 partial(self.mainUi.uiCmds_menu.on_newProjectTreeItems, 'node'))
        self.mainUi.miUnselectTreeItem = self.mainUi.tbProjectTreeMenu.addAction("Unselect All",
                                         partial(self.mainUi.unselectAllItems,
                                                 self.mainUi.twProjectTree))
        self.mainUi.miDelTreeItem = self.mainUi.tbProjectTreeMenu.addAction("Remove Selection",
                                    self.mainUi.uiCmds_menu.on_delProjectItem)
        self.mainUi.twProjectTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainUi.connect(self.mainUi.twProjectTree,
                            QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                            self.mainUi.on_popProjectTreeMenu)
        self.mainUi.menuProjectTree = QtGui.QMenu(self.mainUi)
        self.mainUi.menuProjectTree.setTearOffEnabled(True)
        self.mainUi.menuProjectTree.addAction(self.mainUi.miNewContainer)
        self.mainUi.menuProjectTree.addAction(self.mainUi.miNewContainers)
        self.mainUi.menuProjectTree.addSeparator()
        self.mainUi.menuProjectTree.addAction(self.mainUi.miNewNode)
        self.mainUi.menuProjectTree.addAction(self.mainUi.miNewNodes)
        self.mainUi.menuProjectTree.addSeparator()
        self.mainUi.menuProjectTree.addAction(self.mainUi.miUnselectTreeItem)
        self.mainUi.menuProjectTree.addAction(self.mainUi.miDelTreeItem)

    def pop_projectStepMenu(self):
        """ Create project step QTreeWidget popupMenu """
        self.mainUi.tbProjectStepMenu = QtGui.QToolBar()
        self.mainUi.miNewStep = self.mainUi.tbProjectStepMenu.addAction("New Step",
                                self.mainUi.uiCmds_menu.on_newProjectStepItem)
        self.mainUi.miUnselectStepItem = self.mainUi.tbProjectStepMenu.addAction("Unselect All",
                                         partial(self.mainUi.unselectAllItems,
                                                 self.mainUi.twProjectStep))
        self.mainUi.miDelStepItem =  self.mainUi.tbProjectStepMenu.addAction("Remove Selection",
                                     self.mainUi.uiCmds_menu.on_delStepItem)
        self.mainUi.twProjectStep.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainUi.connect(self.mainUi.twProjectStep,
                            QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                            self.mainUi.on_popProjectStepMenu)
        self.mainUi.menuProjectStep = QtGui.QMenu(self.mainUi)
        self.mainUi.menuProjectStep.setTearOffEnabled(True)
        self.mainUi.menuProjectStep.addAction(self.mainUi.miNewStep)
        self.mainUi.menuProjectStep.addSeparator()
        self.mainUi.menuProjectStep.addAction(self.mainUi.miUnselectStepItem)
        self.mainUi.menuProjectStep.addAction(self.mainUi.miDelStepItem)


class PopulateTrees(object):
    """ Populate prodManager trees QTreeWidget
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm

    def projectTrees(self):
        """ Populate projectTrees QTreeWidget """
        trees = []
        for tree in self.pm.project.projectTrees:
            treeObj = getattr(self.pm, '%sTree' % tree)
            newTree = self.newProjectTreesItem(tree, treeSteps=treeObj.treeSteps,
                                               treeNodes=treeObj.treeNodes)
            trees.append(newTree)
        self.mainUi.twProjectTrees.addTopLevelItems(trees)

    def projectTree(self):
        """ Populate projectTree QTreeWidget """
        selTree = self.mainUi.twProjectTrees.selectedItems()
        for nodeDict in selTree[0].treeNodes:
            parent = self.mainUi.getParentItemFromNodePath(self.mainUi.twProjectTree,
                                                           nodeDict['nodePath'])
            newItem = self.newProjectTreeItem(**nodeDict)
            if parent is None:
                self.mainUi.twProjectTree.addTopLevelItem(newItem)
            else:
                parent.addChild(newItem)

    def projectStep(self):
        """ Populate projectStep QTreeWidget """
        selTree = self.mainUi.twProjectTrees.selectedItems()
        for step in selTree[0].treeSteps:
            newItem = self.newProjectStepItem(step)
            self.mainUi.twProjectStep.addTopLevelItem(newItem)

    @staticmethod
    def newProjectTreesItem(treeName, treeSteps=None, treeNodes=None):
        """ Create new project tree QTreeWidgetItem
            @param treeName: (str) : New tree name (ex: 'asset', 'shot')
            @param treeSteps: (list) : List of tree steps
            @param treeNodes: (list) : List of nodes dict
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, treeName)
        newItem.setText(1, '%sTree' % treeName)
        newItem.treeName = treeName
        newItem.treeLabel = '%sTree' % treeName
        if treeSteps is None:
            newItem.treeSteps = []
        else:
            newItem.treeSteps = treeSteps
        if treeNodes is None:
            newItem.treeNodes = []
        else:
            newItem.treeNodes = treeNodes
        return newItem

    def newProjectTreeItem(self, **kwargs):
        """ Create new project tree QTreeWidgetItem
            @param kwargs: (dict) : Item default params
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        if kwargs['nodeType'] in self.pm.project.projectTrees:
            newItem.setText(0, kwargs['nodeLabel'])
            newItem.setTextColor(0, QtGui.QColor(50, 100, 255))
        else:
            newItem.setText(0, kwargs['nodeLabel'].upper())
        for k, v in kwargs.iteritems():
            if k.startswith('node'):
                setattr(newItem, k, v)
        return newItem

    def newProjectStepItem(self, stepName):
        """ Create new project step QTreeWidgetItem
            @param stepName: (str) : Item Name
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, stepName)
        newItem.nodeType = 'step'
        newItem.nodeName = stepName
        return newItem
