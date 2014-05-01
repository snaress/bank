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


class MainTree(object):
    """ Class used by the ProdManagerUi for mainTrees updates and refresh
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.populate = PopulateTrees(self.mainUi)

    def rf_mainTreeSwitch(self):
        """ Refresh main trees switch """
        for n, tree in enumerate(self.pm.project.projectTrees):
            newWidget = QtGui.QRadioButton()
            newWidget.setText(tree)
            newWidget.treeName = tree
            newWidget.treeLabel = '%sTree' % tree
            if n == 0:
                newWidget.setChecked(True)
                self.mainUi.selectedTree = newWidget.treeLabel
            newWidget.connect(newWidget, QtCore.SIGNAL("clicked()"),
                              partial(self.mainUi.uiCmds_mainTree.on_switchTree, newWidget.treeLabel))
            self.mainUi.hlMainTrees.addWidget(newWidget)

    def rf_mainTree(self):
        """ Refresh main trees QTreeWidget """
        self.mainUi.twProject.clear()
        self.populate.mainTree()


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
        self.mainUi.qfProjectTasks.setVisible(False)
        self.mainUi.twProjectTasks.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.twProjectTasks.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.twProjectTasks.header().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.splitProjectTrees.setVisible(False)
        self.mainUi.twProjectTrees.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.twProjectTrees.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.twProjectAttr.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.mainUi.twProjectAttr.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
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
        #-- Init Project Tasks --~#
        self.mainUi.bProjectTaskAdd.setEnabled(state)
        self.mainUi.bProjectTaskDel.setEnabled(state)
        self.mainUi.bProjectTaskUp.setEnabled(state)
        self.mainUi.bProjectTaskDn.setEnabled(state)
        self.mainUi.twProjectTasks.setEnabled(state)
        #-- Init Project Trees --#
        self.mainUi.bProjectTreesAdd.setEnabled(state)
        self.mainUi.bProjectTreesUp.setEnabled(state)
        self.mainUi.bProjectTreesDn.setEnabled(state)
        self.mainUi.bProjectTreeUp.setEnabled(state)
        self.mainUi.bProjectTreeDn.setEnabled(state)
        self.mainUi.bProjectStepUp.setEnabled(state)
        self.mainUi.bProjectStepDn.setEnabled(state)
        self.mainUi.bProjectAttrUp.setEnabled(state)
        self.mainUi.bProjectAttrDn.setEnabled(state)
        self.mainUi.twProjectAttr.setEnabled(state)

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
        #-- Refresh Project Tasks --#
        self.mainUi.twProjectTasks.clear()
        self.populate.projectTasks()
        #-- Refresh Project Trees --#
        self.mainUi.twProjectTrees.clear()
        self.mainUi.twProjectTree.clear()
        self.mainUi.twProjectStep.clear()
        self.mainUi.twProjectAttr.clear()
        self.populate.projectTrees()

    def rf_projectTree(self):
        """ Refresh projectTree """
        self.mainUi.twProjectTree.clear()
        self.mainUi.twProjectStep.clear()
        self.mainUi.twProjectAttr.clear()
        selTree = self.mainUi.twProjectTrees.selectedItems()
        if selTree:
            self.populate.projectTree()
            self.populate.projectStep()
            self.populate.projectAttr()

    def ud_projectTreesItem(self, treeItem):
        """ Update projectTrees QTreeWidgetItem.treeNodes
            @param treeItem: (object) : QTreeWidgetItem """
        #-- Update TreeSteps --#
        treeSteps = []
        for step in pQt.getTopItems(self.mainUi.twProjectStep):
            treeSteps.append(step.nodeName)
        treeItem.treeSteps = treeSteps
        #-- Update TreeAttr --#
        treeAttrs = []
        for attr in pQt.getTopItems(self.mainUi.twProjectAttr):
            treeAttrs.append({attr.nodeName: attr.attrType})
        treeItem.treeAttrs = treeAttrs
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

    def pop_projectAttrMenu(self):
        """ Create project attributes QTreeWidget popupMenu """
        self.mainUi.tbProjectAttrMenu = QtGui.QToolBar()
        self.mainUi.miNewAttr = self.mainUi.tbProjectAttrMenu.addAction("New Attribute",
                                self.mainUi.uiCmds_menu.on_newProjectAttrItem)
        self.mainUi.miUnselectAttrItem = self.mainUi.tbProjectAttrMenu.addAction("Unselect All",
                                         partial(self.mainUi.unselectAllItems,
                                                 self.mainUi.twProjectAttr))
        self.mainUi.miDelAttrItem =  self.mainUi.tbProjectAttrMenu.addAction("Remove Selection",
                                     self.mainUi.uiCmds_menu.on_delAttrItem)
        self.mainUi.twProjectAttr.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainUi.connect(self.mainUi.twProjectAttr,
                            QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                            self.mainUi.on_popProjectAttrMenu)
        self.mainUi.menuProjectAttr = QtGui.QMenu(self.mainUi)
        self.mainUi.menuProjectAttr.setTearOffEnabled(True)
        self.mainUi.menuProjectAttr.addAction(self.mainUi.miNewAttr)
        self.mainUi.menuProjectAttr.addSeparator()
        self.mainUi.menuProjectAttr.addAction(self.mainUi.miUnselectAttrItem)
        self.mainUi.menuProjectAttr.addAction(self.mainUi.miDelAttrItem)


class ShotInfoTab(object):
    """ Class used by the ProdManagerUi for shotInfoTab updates and refresh
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.populate = PopulateTrees(self.mainUi)

    def initShotInfoTab(self):
        """ Initialize shotInfo tab """
        self.mainUi.lShotNodePath.setText('')

    def rf_shotInfoTab(self):
        """ Refresh shotInfo tab """
        self.mainUi.twShotInfo.clear()
        self.mainUi.twShotInfo.setHeaderLabel(self.mainUi.selectedTree)
        self.populate.shotInfoTree()


class PopulateTrees(object):
    """ Populate prodManager trees QTreeWidget
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.defaultTemplate = pmTemplate.DefaultTemplate

    def projectTasks(self):
        """ Populate projectTasks QTreeWidget """
        for taskDict in self.pm.project.projectTasks:
            taskName = taskDict.keys()[0]
            taskColor = taskDict[taskName]['color']
            taskStat = taskDict[taskName]['stat']
            newTask, newColor, newStat = self.newProjectTaskItem(taskName, taskColor=taskColor,
                                                                           taskStat=taskStat)
            self.mainUi.twProjectTasks.addTopLevelItem(newTask)
            self.mainUi.twProjectTasks.setItemWidget(newTask, 1, newColor)
            self.mainUi.twProjectTasks.setItemWidget(newTask, 2, newStat)

    def projectTrees(self):
        """ Populate projectTrees QTreeWidget """
        trees = []
        for tree in self.pm.project.projectTrees:
            treeObj = getattr(self.pm, '%sTree' % tree)
            newTree = self.newProjectTreesItem(tree, treeSteps=treeObj.treeSteps,
                                                     treeAttrs=treeObj.treeAttrs,
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

    def projectAttr(self):
        """ Populate projectAttr QTreeWidget """
        selTree = self.mainUi.twProjectTrees.selectedItems()
        for attrDict in selTree[0].treeAttrs:
            attrName = attrDict.keys()[0]
            newItem, newChoice = self.newProjectAttrItem(attrName, attrDict[attrName])
            self.mainUi.twProjectAttr.addTopLevelItem(newItem)
            self.mainUi.twProjectAttr.setItemWidget(newItem, 1, newChoice)

    def mainTree(self):
        """ Populate main tree QTreeWidget """
        if self.mainUi.selectedTree is not None:
            treeObj = getattr(self.pm, self.mainUi.selectedTree)
            for nodeDict in treeObj.treeNodes:
                parent = self.mainUi.getParentItemFromNodePath(self.mainUi.twProject,
                                                               nodeDict['nodePath'])
                newItem = self.newMainTreeItem(**nodeDict)
                if parent is None:
                    self.mainUi.twProject.addTopLevelItem(newItem)
                else:
                    parent.addChild(newItem)

    def shotInfoTree(self):
        """ Populate shotInfo tree QTreeWidget """
        selItems = self.mainUi.twProject.selectedItems()
        if selItems:
            selItem = selItems[0]
            allItems = pQt.getAllItems(self.mainUi.twProject)
            self.mainUi.lShotNodePath.setText(selItem.nodePath)
            for item in allItems:
                if not 'Ctnr' in item.nodeType and item.nodePath.startswith(selItem.nodePath):
                    newItem = self.newShotInfoItem(**item.__dict__)
                    newWidget = self.mainUi.pmWindow.ShotNodeWidget(self.mainUi, **item.__dict__)
                    newItem.widget = newWidget
                    self.mainUi.twShotInfo.addTopLevelItem(newItem)
                    self.mainUi.twShotInfo.setItemWidget(newItem, 0, newWidget)

    def newProjectTaskItem(self, taskName, taskColor=None, taskStat=None):
        """ Create new project task QTreeWidgetItem
            @param taskName: (str) : Task Name
            @param taskColor: (tuple) : Rgb color
            @param taskStat: (bool) : Task count in stats
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, taskName)
        newItem.nodeName = taskName
        newColor = self.newProjectTaskColor(newItem, taskColor)
        newStat = self.newProjectTaskStat(newItem, taskStat)
        newItem.colWidget = newColor
        newItem.statWidget = newStat
        return newItem, newColor, newStat

    def newProjectTaskColor(self, newItem, taskColor):
        """ New task color QPushButton
            @param newItem: (object) : New parent QTreeWidgetItem
            @param taskColor: (tuple) : Rgb color
            @return: (object) : New task color QPushButton """
        newColor = QtGui.QPushButton()
        newColor.setText('')
        newColor.setMaximumWidth(40)
        newColor.connect(newColor, QtCore.SIGNAL("clicked()"),
                         partial(self.mainUi.uiCmds_projectTab.on_taskColor, newItem))
        if taskColor is None:
            newItem.taskColor = (200, 200, 200)
        else:
            newItem.taskColor = taskColor
            newColor.setStyleSheet("background:rgb(%s, %s, %s)" % (taskColor[0],
                                                                   taskColor[1],
                                                                   taskColor[2]))
        return newColor

    def newProjectTaskStat(self, newItem, taskStat):
        """ New task stat QCheckBox
            @param newItem: (object) : New parent QTreeWidgetItem
            @param taskStat: (bool) : Task count in stats
            @return: (object) : New task stat QCheckBox """
        newStat = QtGui.QCheckBox()
        newStat.setText('')
        newStat.connect(newStat, QtCore.SIGNAL("clicked()"),
                        partial(self.mainUi.uiCmds_projectTab.on_taskStat, newItem))
        if taskStat is None:
            newItem.taskStat = True
            newStat.setChecked(True)
        else:
            newItem.taskStat = taskStat
            newStat.setChecked(taskStat)
        return newStat

    def newProjectTreesItem(self, treeName, treeSteps=None, treeAttrs=None, treeNodes=None):
        """ Create new project tree QTreeWidgetItem
            @param treeName: (str) : New tree name (ex: 'asset', 'shot')
            @param treeSteps: (list) : List of tree steps
            @param treeAttrs: (list) : List of tree attributes
            @param treeNodes: (list) : List of nodes dict
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, treeName)
        newItem.setText(1, '%sTree' % treeName)
        newItem.treeName = treeName
        newItem.treeLabel = '%sTree' % treeName
        #-- Tree Steps --#
        if treeSteps is None:
            newItem.treeSteps = []
        else:
            newItem.treeSteps = treeSteps
        #-- Tree Attributes --#
        if treeAttrs is None:
            newItem.treeAttrs = self.defaultTemplate.projectTreeAttrs()
        else:
            newItem.treeAttrs = treeAttrs
        #-- Tree Nodes --#
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

    @staticmethod
    def newProjectStepItem(stepName):
        """ Create new project step QTreeWidgetItem
            @param stepName: (str) : Item Name
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, stepName)
        newItem.nodeType = 'step'
        newItem.nodeName = stepName
        return newItem

    def newProjectAttrItem(self, attrName, attrType):
        """ Create new project attribute QTreeWidgetItem
            @param attrName: (str) : Item Name
            @param attrType: (str) : 'string' or 'float' or 'int' or 'bool' or 'comment'
            @return: (object) : New QTreeWidgetItem """
        #-- Item --#
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, attrName)
        newItem.nodeType = 'attr'
        newItem.nodeName = attrName
        newItem.attrType = attrType
        #-- Type --#
        newChoice = QtGui.QComboBox()
        newChoice.addItems(['string', 'int', 'float', 'bool', 'comment'])
        newChoice.setCurrentIndex(newChoice.findText(attrType))
        newChoice.connect(newChoice, QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                          self.mainUi.uiCmds_projectTab.on_attrType)
        #-- Result --#
        newItem.widget = newChoice
        return newItem, newChoice

    def newMainTreeItem(self, **kwargs):
        """ Create new main tree QTreeWidgetItem
            @param kwargs: (dict) : Item default params
            @return: (object) : New QTreeWidgetItem """
        newItem = self.newProjectTreeItem(**kwargs)
        if not 'Ctnr' in kwargs['nodeType']:
            dataPath = os.path.join(self.pm.project._projectPath, 'tree', kwargs['nodeType'])
            for fld in kwargs['nodePath'].split('/'):
                newItem.dataPath = os.path.join(dataPath, fld)
            newItem.dataFile = os.path.join(newItem.dataPath, '%s.py' % kwargs['nodeName'])
        return newItem

    def newShotInfoItem(self, **kwargs):
        """ Create new shotInfo tree QTreeWidgetItem
            @param kwargs: (dict) : Item default params
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        #-- Data Info --#
        if not 'Ctnr' in kwargs['nodeType']:
            dataPath = os.path.join(self.pm.project._projectPath, 'tree', kwargs['nodeType'])
            for fld in kwargs['nodePath'].split('/'):
                newItem.dataPath = os.path.join(dataPath, fld)
            newItem.dataFile = os.path.join(newItem.dataPath, '%s.py' % kwargs['nodeName'])
        #-- Default Node Attr --#
        for k, v in kwargs.iteritems():
            if k.startswith('node'):
                setattr(newItem, k, v)
        return newItem
