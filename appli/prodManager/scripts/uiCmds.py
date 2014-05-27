import os
from PyQt4 import QtGui
from appli import prodManager
from functools import partial
from lib.qt.scripts import dialog
from lib.qt.scripts import procQt as pQt
from appli.prodManager.scripts import core as pmCore
from appli.prodManager.scripts import uiWindow as pmWindow
from appli.prodManager.scripts import uiRefresh as pmRefresh
from appli.prodManager.scripts import template as pmTemplate


class MenuCmds(object):
    """ Class used by the ProdManagerUi for menu actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.defaultTemplate = pmTemplate.DefaultTemplate
        self.populate = pmRefresh.PopulateTrees(self.mainUi)

    #========================================= MENU MAIN =========================================#

    def newProject(self):
        """ Launch new project dialog """
        self.newProjectUi = pmWindow.NewProjectUi(self.mainUi)
        self.newProjectUi.exec_()

    def loadProject(self):
        """ Launch load project dialog """
        self.loadProjectUi = pmWindow.LoadProjectUi(self.mainUi)
        self.loadProjectUi.exec_()

    def printProdManagerParams(self):
        """ Print project attributes """
        self.pm.printProjectParams()

    def printProjectParams(self):
        """ Print project attributes """
        self.pm.project.printParams()

    #================================== POPUP MENU PROJECT TREE ==================================#

    def init_newProjectTreeItem(self, itemType):
        """ Initialize QTreeWidgetItem creation
            @param itemType: (str) : 'container' or 'node'
            @return: (bool) : Creation check state, (str) : Warning message """
        selTree = self.mainUi.twProjectTrees.selectedItems()
        selNode = self.mainUi.twProjectTree.selectedItems()
        create = True
        warn = ""
        if not selTree:
            warn = "!!! Warning: Select a tree to add new items !!!"
            create = False
        else:
            if itemType == 'node' and not selNode:
                warn = "!!! Warning: Select container to add new node !!!"
                create = False
            elif itemType == 'node' and selNode and selNode[0].nodeType in self.pm.project.projectTrees:
                warn = "!!! Warning: New node can only be child of container !!!"
                create = False
        return create, warn

    def on_newProjectTreeItem(self, itemType):
        """ Command launch when miNewContainer is clicked
            @param itemType: (str) : 'container' or 'node' """
        selNode = self.mainUi.twProjectTree.selectedItems()
        create, warn = self.init_newProjectTreeItem(itemType)
        if not create:
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(warn)
        else:
            mess = self._getTreeDialMessage(itemType)
            if selNode:
                mess.append("New item's parent: %s" % selNode[0].nodePath)
            else:
                mess.append("New item's parent: world")
            if itemType == 'node':
                self.pdNewProjectTree = pmWindow.EditProjectTreeItem(self.mainUi, itemType)
            else:
                self.pdNewProjectTree = dialog.PromptDialog('\n'.join(mess),
                                                            partial(self.newProjectTreeItem, itemType),
                                                            self.newProjectTreeCancel)
            self.pdNewProjectTree.show()

    def on_newProjectTreeItems(self, itemType):
        """ Command launch when miNewContainer is clicked
            @param itemType: (str) : 'container' or 'node' """
        selNode = self.mainUi.twProjectTree.selectedItems()
        create, warn = self.init_newProjectTreeItem(itemType)
        if not create:
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(warn)
        else:
            mess = self._getTreeDialMessage(itemType)
            if selNode:
                mess.append("New items parent: %s" % selNode[0].nodePath)
            else:
                mess.append("New items parent: world")
            self.editProjectTreeUi = pmWindow.EditProjectTreeUi(self.mainUi, '\n'.join(mess), itemType)
            self.editProjectTreeUi.exec_()

    @staticmethod
    def _getTreeDialMessage(itemType):
        """ Get dialog message
            @param itemType: (str) : 'container' or 'node'
            @return: (list) : Message """
        mess = []
        if itemType == 'container':
            mess = ["Enter new container name,", "Don't use special caracter or space."]
        elif itemType == 'node':
            mess = ["Enter new node name,", "Don't use special caracter or space."]
        return mess

    def newProjectTreeItem(self, itemType, itemName=None, itemLabel=None):
        """ Command launch when 'Ok' of confirmDialog is clicked
            @param itemType: (str) : 'container' or 'node'
            @param itemName: (str) : New node name
            @param itemLabel: (str) : New node label """
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        selItems = self.mainUi.twProjectTree.selectedItems()
        if selTrees:
            treeName = selTrees[0].treeName
            if not itemType == 'node':
                nodeName = str(self.pdNewProjectTree.leUserValue.text())
                nodeLabel = nodeName
                nodeType = '%sCtnr' % treeName
            else:
                nodeName = itemName
                nodeLabel = itemLabel
                nodeType = treeName
            checkNewNode, nodePath = self._getProjectTreePath(nodeName, nodeLabel)
            if checkNewNode:
                params = self.defaultTemplate.projectTreeNodeAttr(nodeType, nodeLabel,
                                                                  nodeName, nodePath)
                newItem = self.populate.newProjectTreeItem(**params)
                if selItems:
                    selItems[0].addChild(newItem)
                else:
                    self.mainUi.twProjectTree.addTopLevelItem(newItem)
                self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])
            else:
                warn = "!!! Warning !!!\n%s\nalready exists" % nodePath
                errorDial = QtGui.QErrorMessage(self.mainUi)
                errorDial.showMessage(warn)

    def _getProjectTreePath(self, nodeName, nodeLabel):
        """ Get parent item params
            @param nodeName: (str) : New item name
            @return: (bool) : NewName valide, (str) : node path """
        selItems = self.mainUi.twProjectTree.selectedItems()
        if selItems:
            nodePath = '%s/%s' % (selItems[0].nodePath, nodeLabel)
        else:
            nodePath = nodeLabel
        allItems = pQt.getAllItems(self.mainUi.twProjectTree)
        check = True
        for item in allItems:
            if item.nodePath == nodePath:
                check = False
                print "!!! Warning: Node path already exists: %s !!!" % nodePath
            if item.nodeName == nodeName:
                check = False
                print "!!! Warning: Node name already exists: %s !!!" % nodeName
        return check, nodePath

    def newProjectTreeCancel(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.pdNewProjectTree.close()

    def on_delProjectItem(self):
        """ Remove selected items from project tree QTreeWidget """
        self.mainUi.delSelItems(self.mainUi.twProjectTree)
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])

    #================================== POPUP MENU PROJECT STEP ==================================#

    def init_newProjectStepItem(self):
        """ Initialize QTreeWidgetItem creation
            @return: (bool) : Creation check state, (str) : Warning message """
        selTree = self.mainUi.twProjectTrees.selectedItems()
        create = True
        warn = ""
        if not selTree:
            warn = "!!! Warning: Select a tree to add new steps !!!"
            create = False
        return create, warn

    def on_newProjectStepItem(self):
        """ Command launch when miNewStep is clicked """
        create, warn = self.init_newProjectStepItem()
        if not create:
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(warn)
        else:
            mess = ["Enter new step name,", "Don't use special caracter or space."]
            self.pdNewProjectStep = dialog.PromptDialog('\n'.join(mess), self.newProjectStepItem,
                                                        self.newProjectStepCancel)
            self.pdNewProjectStep.show()

    def newProjectStepItem(self):
        """ Command launch when miNewStep is clicked """
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        stepName = str(self.pdNewProjectStep.leUserValue.text())
        if selTrees:
            checkNewStep = self._checkNewStepItem(stepName)
            if checkNewStep:
                newItem = self.populate.newProjectStepItem(stepName)
                self.mainUi.twProjectStep.addTopLevelItem(newItem)
                self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])
            else:
                self.pdNewProjectStep.close()
                warn = "!!! Warning !!!\n%s\nalready exists" % stepName
                errorDial = QtGui.QErrorMessage(self.mainUi)
                errorDial.showMessage(warn)

    def _checkNewStepItem(self, stepName):
        """ Check new step name validity
            @param stepName: (str) : New step name
            @return: (bool) : True if valid, False if not """
        allItems = pQt.getAllItems(self.mainUi.twProjectStep)
        for item in allItems:
            if item.nodeName == stepName:
                return False
        return True

    def newProjectStepCancel(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.pdNewProjectStep.close()

    def on_delStepItem(self):
        """ Remove selected items from project step QTreeWidget """
        self.mainUi.delSelItems(self.mainUi.twProjectStep)
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])

    #================================== POPUP MENU PROJECT ATTR ==================================#

    def init_newProjectAttrItem(self):
        """ Initialize QTreeWidgetItem creation
            @return: (bool) : Creation check state, (str) : Warning message """
        selTree = self.mainUi.twProjectTrees.selectedItems()
        create = True
        warn = ""
        if not selTree:
            warn = "!!! Warning: Select a tree to add new steps !!!"
            create = False
        return create, warn

    def on_newProjectAttrItem(self):
        """ Command launch when miNewAttr is clicked """
        create, warn = self.init_newProjectAttrItem()
        if not create:
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(warn)
        else:
            mess = ["Enter new attribute name,", "Don't use special caracter or space."]
            self.pdNewProjectAttr = dialog.PromptDialog('\n'.join(mess), self.newProjectAttrItem,
                                                        self.newProjectAttrCancel)
            self.pdNewProjectAttr.show()

    def newProjectAttrItem(self):
        """ Command launch when miNewAttr is clicked """
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        attrName = str(self.pdNewProjectAttr.leUserValue.text())
        if selTrees:
            checkNewAttr = self._checkNewAttrItem(attrName)
            if checkNewAttr:
                newItem, newChoice = self.populate.newProjectAttrItem(attrName, 'string')
                self.mainUi.twProjectAttr.addTopLevelItem(newItem)
                self.mainUi.twProjectAttr.setItemWidget(newItem, 1, newChoice)
                self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])
            else:
                self.pdNewProjectAttr.close()
                warn = "!!! Warning !!!\n%s\nalready exists" % attrName
                errorDial = QtGui.QErrorMessage(self.mainUi)
                errorDial.showMessage(warn)

    def _checkNewAttrItem(self, attrName):
        """ Check new atribute name validity
            @param attrName: (str) : New attribute name
            @return: (bool) : True if valid, False if not """
        allItems = pQt.getAllItems(self.mainUi.twProjectAttr)
        for item in allItems:
            if item.nodeName == attrName:
                return False
        return True

    def newProjectAttrCancel(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.pdNewProjectAttr.close()

    def on_delAttrItem(self):
        """ Remove selected items from project attributes QTreeWidget """
        selAttrs = self.mainUi.twProjectAttr.selectedItems()
        if selAttrs:
            attrs = [x.keys()[0] for x in self.defaultTemplate.projectTreeAttrs()]
            if not selAttrs[0].nodeName in attrs:
                self.mainUi.delSelItems(self.mainUi.twProjectAttr)
                selTrees = self.mainUi.twProjectTrees.selectedItems()
                self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])
            else:
                warn = "WARNING: Removing 'workDir' or 'prevIma attribute is not allowed..."
                errorDial = QtGui.QErrorMessage(self.mainUi)
                errorDial.showMessage(warn)

    #==================================== POPUP MENU LT SHOTS ====================================#

    def on_newLtShotTab(self):
        """ Command launch when miNewTab is clicked """
        newLayout = QtGui.QGridLayout()
        newLayout.setContentsMargins(0, 0, 0, 0)
        newWidget = QtGui.QWidget()
        newWidget.setLayout(newLayout)
        newTree = QtGui.QTreeWidget()
        newTree.setColumnCount(int(self.mainUi.sbLtColumns.value()))
        newTree.setHeaderHidden(True)
        newTree.setIndentation(0)
        newTree.setSelectionMode(QtGui.QTreeWidget.NoSelection)
        newLayout.addWidget(newTree)
        self.mainUi.tabLtShots.addTab(newWidget, 'New_Tab')
        self.mainUi.tabLtShots.setCurrentIndex(self.mainUi.tabLtShots.count() - 1)

    def on_delLtShotTab(self):
        """ Command launch when miDelTab is clicked """
        selInd = self.mainUi.tabLtShots.currentIndex()
        if not selInd == 0:
            self.mainUi.tabLtShots.setCurrentIndex(selInd - 1)
            self.mainUi.tabLtShots.removeTab(selInd)
        else:
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage("WARNING: The first tab is undeletable...")


class PreviewImage(object):
    """ Class used by the ProdManagerUi for previewImage actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.template = pmTemplate.DefaultTemplate

    def on_image(self):
        """ Open previewImage in external player """
        print "Launching image: %s" % self.mainUi.lPreview.imaAbsPath
        os.system('start %s %s' % (self.template.imageLauncher(),
                                   os.path.normcase(self.mainUi.lPreview.imaAbsPath)))

    def on_sequence(self):
        """ Open sequence in external player """
        seqInfo = pmCore.getSequenceInfo(self.mainUi.bPreviewSequence.absPath)
        if seqInfo is not None:
            seqName = "%s.%s.%s" % (seqInfo['fileName'].split('.')[0], '@' * seqInfo['padding'],
                                    seqInfo['fileName'].split('.')[2])
            seq = os.path.normpath(os.path.join(seqInfo['filePath'], seqName))
            print '-' * 100
            print "Launching sequence: %s" % os.path.normpath(os.path.join(seqInfo['filePath'],
                                                                           seqInfo['label']))
            for k, v in sorted(seqInfo.iteritems()):
                if not k == 'label':
                    print k, ' = ', v
            os.system('start %s -n %s %s %s %s' % (self.template.sequenceLauncher(),
                                                   seqInfo['first'], seqInfo['last'],
                                                   seqInfo['step'], seq))

    def on_movie(self):
        """ Open movie in external player """
        print "Launching movie: %s" % self.mainUi.bPreviewMovie.absPath
        os.system('start %s %s' % (self.template.movieLauncher(),
                                   os.path.normcase(self.mainUi.bPreviewMovie.absPath)))

    def on_xplorer(self):
        """ Open explorer with stored path """
        os.system('start %s' % (self.mainUi.bPreviewXterm.absPath))

    def on_xterm(self):
        """ Open xterm with stored path """
        os.system('start %s /K "cd /d %s"' % (self.template.xtermLauncher(),
                                              self.mainUi.bPreviewXterm.absPath))


class MainTree(object):
    """ Class used by the ProdManagerUi for main tree actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm

    def on_switchTree(self, treeLabel):
        """ Switch main tree
            @param treeLabel: (str) : Tree label """
        self.mainUi.selectedTree = treeLabel
        self.mainUi.uiRf_mainTrees.rf_mainTree()
        selTab = self.mainUi.tabProdManager.tabText(self.mainUi.tabProdManager.currentIndex())
        if selTab == 'Linetest':
            self.mainUi.uiRf_linetestTab.rf_stepSwitch()
        self.on_treeItem()

    def on_treeItem(self):
        """ Refresh selected tab params """
        selTab = self.mainUi.tabProdManager.tabText(self.mainUi.tabProdManager.currentIndex())
        selItems = self.mainUi.twProject.selectedItems()
        if selItems:
            self.mainUi.uiRf_previewImage.rf_xterm()
            self.mainUi.uiRf_previewImage.rf_xplorer()
        if selTab == 'Shot Info':
            self.mainUi.uiRf_shotInfoTab.rf_shotInfoTree()
            self.mainUi.uiRf_shotInfoTab.rf_shotParamsTree()
            self.mainUi.uiRf_shotInfoTab.rf_shotComment()
        elif selTab == 'Linetest':
            if selItems:
                if not 'Ctnr' in selItems[0].nodeType:
                    self.mainUi.uiRf_linetestTab.rf_lineTestTabVis(state=True)
                    self.mainUi.uiRf_linetestTab.rf_ltTree()
                else:
                    self.mainUi.uiRf_linetestTab.rf_lineTestTabVis(state=False)
                    self.mainUi.twLinetest.clear()
            else:
                self.mainUi.uiRf_linetestTab.rf_lineTestTabVis(state=False)
                self.mainUi.twLinetest.clear()
            self.mainUi.uiCmds_linetestTab.on_linetest()
            self.mainUi.uiRf_linetestTab.rf_ltShots()

    def on_tabItem(self):
        self.on_treeItem()
        selTab = self.mainUi.tabProdManager.tabText(self.mainUi.tabProdManager.currentIndex())
        self.mainUi.twLinetest.clear()
        self.mainUi.uiCmds_linetestTab.on_linetest()
        if selTab == 'Linetest':
            self.mainUi.uiRf_linetestTab.rf_stepSwitch()


class ProjectTab(object):
    """ Class used by the ProdManagerUi for project tab actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.populate = pmRefresh.PopulateTrees(self.mainUi)

    def on_editProjectTab(self):
        """ Command launch when bEditProjectTab is clicked """
        checkState = self.mainUi.bEditProjectTab.isChecked()
        if checkState:
            self.mainUi.bEditProjectTab.setText("Save")
        else:
            self.mainUi.bEditProjectTab.setText("Edit")
            self.ud_projectTabParams()
            self.pm.project.writeProjectFile()
            for tree in self.pm.project.projectTrees:
                treeObj = getattr(self.pm, '%sTree' % tree)
                treeObj.writeTreeToFile()
            self.mainUi.uiRf_mainTrees.rf_mainTreeSwitch()
        self.mainUi.uiRf_projectTab.rf_projectTabVis(state=checkState)

    def on_cancelProjectTab(self):
        """ Command launch when bCancelProjectTab is clicked """
        self.mainUi.bEditProjectTab.setText("Edit")
        self.mainUi.bEditProjectTab.setChecked(False)
        self.mainUi.uiRf_projectTab.rf_projectTab()
        self.mainUi.uiRf_projectTab.rf_projectTabVis()

    def on_openProjectWorkDir(self):
        """ Command launch when bOpenProjectWorkDir is clicked """
        if self.pm.project.projectWorkDir == '':
            root = prodManager.rootDisk
        else:
            root = self.pm.projectWorkDir
        self.fdProjectWorkDir = dialog.fileDialog(fdRoot=root, fdCmd=self.ud_projectWorkDir)
        self.fdProjectWorkDir.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        self.fdProjectWorkDir.exec_()

    def ud_projectWorkDir(self):
        """ Update Work dir with selected path from dialog """
        selPath = self.fdProjectWorkDir.selectedFiles()
        if selPath:
            self.mainUi.leProjectWorkDir.setText(str(selPath[0]))

    def on_projectTasks(self):
        """ Command launch when cbProjectTasks is clicked """
        self.mainUi.qfProjectTasks.setVisible(self.mainUi.cbProjectTasks.isChecked())

    def on_addTask(self):
        """ Command launch when bProjectTaskAdd is clicked """
        mess = ["New Task: Don't use special caracter"]
        self.pdAddTask = dialog.PromptDialog('\n'.join(mess), self.addTaskAccept, self.addTaskCancel)
        self.pdAddTask.exec_()

    def addTaskAccept(self):
        """ Command launch when the promptDialog bOk is clicked """
        taskName = str(self.pdAddTask.leUserValue.text())
        if not taskName in self.mainUi.getTaskList:
            self.pdAddTask.close()
            newTask, newCol, newStat = self.populate.newProjectTaskItem(taskName)
            self.mainUi.twProjectTasks.addTopLevelItem(newTask)
            self.mainUi.twProjectTasks.setItemWidget(newTask, 1, newCol)
            self.mainUi.twProjectTasks.setItemWidget(newTask, 2, newStat)
        else:
            self.pdAddTask.close()
            warn = "Warning: Task name already exists (%s) !!!" % taskName
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(warn)

    def addTaskCancel(self):
        """ Command launch when the promptDialog bCancel is clicked """
        self.pdAddTask.close()

    def on_delTask(self):
        """ Remove selected items from project tasks QTreeWidget """
        selTasks = self.mainUi.twProjectTasks.selectedItems()
        if selTasks:
            self.mainUi.delSelItems(self.mainUi.twProjectTasks)

    def on_taskColor(self, item):
        """ Command launch when bColorChoice of projectTasks QTreeWidgetItem is clicked
            @param item: (object) : Project task QTreeWidgetItem """
        if self.mainUi.bEditProjectTab.isChecked():
            # noinspection PyArgumentList
            color = QtGui.QColorDialog.getColor()
            if color.isValid():
                rgba = color.getRgb()
                item.colWidget.setStyleSheet("background:rgb(%s, %s, %s)" % (rgba[0], rgba[1], rgba[2]))
                item.taskColor = (rgba[0], rgba[1], rgba[2])

    def on_taskStat(self, item):
        """ Command launch when cbStat of projectTasks QTreeWidgetItem is clicked
            @param item: (object) : Project task QTreeWidgetItem """
        if self.mainUi.bEditProjectTab.isChecked():
            item.taskStat = item.statWidget.isChecked()

    def on_projectTrees(self):
        """ Command launch when cbProjectTree is clicked """
        self.mainUi.splitProjectTrees.setVisible(self.mainUi.cbProjectTrees.isChecked())

    def on_addTree(self):
        """ Command launch when bProjectTreesAdd is clicked """
        mess = ["New Tree: Don't use special caracter or 'tree' word", "Ex: 'asset', 'shot'"]
        self.pdAddTree = dialog.PromptDialog('\n'.join(mess), self.addTreeAccept, self.addTreeCancel)
        self.pdAddTree.exec_()

    def addTreeAccept(self):
        """ Command launch when the promptDialog bOk is clicked """
        treeName = str(self.pdAddTree.leUserValue.text())
        mess = None
        if not '.' in treeName and not 'tree' in treeName:
            if not treeName in self.pm.project.projectTrees:
                self.pdAddTree.close()
                newItem = self.populate.newProjectTreesItem(treeName)
                self.mainUi.twProjectTrees.addTopLevelItem(newItem)
            else:
                mess = "Warning: Tree name already exists (%s) !!!" % treeName
        else:
            mess = "Warning: Tree name not valid !!!"
        if mess is not None:
            self.pdAddTree.close()
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(mess)

    def addTreeCancel(self):
        """ Command launch when the promptDialog bCancel is clicked """
        self.pdAddTree.close()

    def on_moveTreeItem(self, twTree, side, rf=False):
        """ Move selected item from given QTreeWidget
            @param twTree: (object) : QTreeWidget contening item to move
            @param side: (str) : 'up' or 'down'
            @param rf: (bool) : Refresh projectTrees params """
        selItems = twTree.selectedItems()
        if selItems:
            item = selItems[0]
            #-- Move QTreeWidgetItem --#
            if item.parent() is None:
                movedItem = self._moveTopItem(twTree, item, side)
            else:
                movedItem = self._moveChildItem(item, side)
            if rf:
                selTree = self.mainUi.twProjectTrees.selectedItems()
                if selTree:
                    self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTree[0])
            #-- Reselect QTreeWidgetItem --#
            if movedItem is not None:
                twTree.setCurrentItem(movedItem)

    @staticmethod
    def _moveTopItem(twTree, item, side):
        """ Move top level item
            @param twTree: (object) : QTreeWidget contening item to move
            @param item: (object) : QTreeWidgetItem to move
            @param side: (str) : 'up' or 'down'
            @return: (object) : Moved QTreeWidgetItem """
        movedItem = None
        ind = twTree.indexOfTopLevelItem(item)
        if side == 'up':
            if ind > 0:
                movedItem = twTree.takeTopLevelItem(ind)
                twTree.insertTopLevelItem(ind-1, movedItem)
        elif side == 'down':
            N = twTree.topLevelItemCount()
            if ind < N-1:
                movedItem = twTree.takeTopLevelItem(ind)
                twTree.insertTopLevelItem(ind+1, movedItem)
        return movedItem

    @staticmethod
    def _moveChildItem(item, side):
        """ Move child item
            @param item: (object) : QTreeWidgetItem
            @param side: (str) : 'up' or 'down'
            @return: (object) : Moved QTreeWidgetItem """
        movedItem = None
        parent = item.parent()
        ind = parent.indexOfChild(item)
        if side == 'up':
            if ind > 0:
                movedItem = parent.takeChild(ind)
                parent.insertChild(ind-1, movedItem)
        elif side == 'down':
            N = parent.childCount()
            if ind < N-1:
                movedItem = parent.takeChild(ind)
                parent.insertChild(ind+1, movedItem)
        return movedItem

    def on_attrType(self):
        """ Change selected attribute type """
        if self.mainUi.bEditProjectTab.isChecked():
            if self.mainUi.twProjectTrees.selectedItems():
                tree = self.mainUi.twProjectTrees.selectedItems()[0]
                allItems = pQt.getAllItems(self.mainUi.twProjectAttr)
                for item in allItems:
                    item.attrType = str(item.widget.currentText())
                self.mainUi.uiRf_projectTab.ud_projectTreesItem(tree)

    def ud_projectTabParams(self):
        """ Update ProdManager instance """
        self.pm.project.projectStart = str(self.mainUi.deProjectStart.text())
        self.pm.project.projectEnd = str(self.mainUi.deProjectEnd.text())
        self.pm.project.projectWorkDir = str(self.mainUi.leProjectWorkDir.text())
        self.pm.project.projectTasks = self.mainUi.getTaskParams
        for item in pQt.getAllItems(self.mainUi.twProjectTrees):
            if not hasattr(self.pm, '%sTree' % item.treeName):
                self.pm.project.addTree(item.treeName, new=True)
            treeObj = getattr(self.pm, '%sTree' % item.treeName)
            treeObj.buildTreeFromUi(item.treeSteps, item.treeAttrs, item.treeNodes)


class ShotInfoTab(object):
    """ Class used by the ProdManagerUi for shotInfo tab actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm

    def on_shotInfoItem(self):
        """ Refresh selected item params """
        self.mainUi.uiRf_shotInfoTab.rf_shotParamsTree()
        self.mainUi.uiRf_shotInfoTab.rf_shotComment()

    def on_editShotParams(self):
        """ Command launch when bEditShotParams is clicked """
        if self.checkComment():
            checkState = self.mainUi.bEditShotParams.isChecked()
            if checkState:
                self.mainUi.bEditShotParams.setText("Save")
            else:
                self.mainUi.bEditShotParams.setText("Edit")
                self.ud_shotParams()
            self.mainUi.uiRf_shotInfoTab.rf_shotParamsVis(state=checkState)
            self.mainUi.twProject.setEnabled(not checkState)
            self.mainUi.twShotInfo.setEnabled(not checkState)
        else:
            self.mainUi.bEditShotParams.setChecked(True)

    def checkComment(self):
        """ Check shot comment validity
            @return: (bool) : True if valid, False if not """
        try:
            str(self.mainUi.shotTextEditor.teText.toHtml())
            return True
        except:
            warn = "!!! ERROR: Comment not valid !!!\nDon't use special caracters."
            errorDial = QtGui.QErrorMessage(self.mainUi)
            errorDial.showMessage(warn)
            return False

    def on_cancelShotParams(self):
        """ Command launch when bCancelShotParams is clicked """
        self.mainUi.bEditShotParams.setText("Edit")
        self.mainUi.bEditShotParams.setChecked(False)
        self.mainUi.uiRf_shotInfoTab.rf_shotParamsVis()
        self.mainUi.uiRf_shotInfoTab.rf_shotParamsTree()
        self.mainUi.uiRf_shotInfoTab.rf_shotComment()
        self.mainUi.twProject.setEnabled(True)
        self.mainUi.twShotInfo.setEnabled(True)

    def ud_shotParams(self):
        """ Update ProdManager instance """
        items = self.mainUi.twShotInfo.selectedItems()
        if items:
            node = self.pm.getNodeFromNodePath(items[0].nodeType, items[0].nodePath)
            if node is not None:
                node.ud_paramsFromUi(self.mainUi)
                node.writeNodeToFile()
                if 'prevIma' in node.params and not node.params['prevIma'] in ['', ' ']:
                    src = node.params['prevIma']
                    dst = os.path.join(node.dataPath, 'prevIma.png')
                    if not os.path.exists(dst):
                        items[0].widget.ud_prevIma()
                    else:
                        if os.path.getmtime(src) > os.path.getmtime(dst):
                            items[0].widget.ud_prevIma()
                        else:
                            print "%s preview image is up to date" % items[0].nodeName
                items[0].widget.rf_prevIma()


class LinetestTab(object):
    """ Class used by the ProdManagerUi for Linetest tab actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.populate = pmRefresh.PopulateTrees(self.mainUi)

    def on_stepSwitch(self):
        """ Update linetest tree with given step """
        selShot = self.mainUi.twProject.selectedItems()
        if not selShot:
            self.mainUi.twLinetest.clear()
        else:
            if 'Ctnr' in selShot[0].nodeType:
                self.mainUi.twLinetest.clear()
            else:
                self.mainUi.uiRf_linetestTab.rf_ltTree()
                self.on_linetest()

    def on_newLt(self):
        """ Add new linetest """
        step = str(self.mainUi.cbLtStep.currentText())
        selShot = self.mainUi.twProject.selectedItems()
        if selShot:
            if not 'Ctnr' in selShot[0].nodeType:
                node = self.pm.getNodeFromNodePath(selShot[0].nodeType, selShot[0].nodePath)
                if step is not None and not step in ['', ' ']:
                    ltFile = node.newLt(step)
                    if ltFile is not None:
                        self.mainUi.uiRf_linetestTab.rf_ltTree()

    def on_delLt(self):
        """ Delete selected linetest """
        selLt = self.mainUi.twLinetest.selectedItems()
        if selLt:
            if os.path.exists(selLt[0]._ltAbsPath):
                warn = ["!!! WARNING !!!",
                        "Delete linetest %s ?" % selLt[0]._ltFile.split('.')[0],
                        "LT User: %s" % selLt[0].widget.params['ltUser'],
                        "LT Title: %s" % selLt[0].widget.params['ltTitle'],
                        "LT Date: %s %s" % (selLt[0].widget.params['ltDate'].replace('_', '/'),
                                            selLt[0].widget.params['ltTime'].replace('_', ':'))]
                self.warnDial0 = dialog.ConfirmDialog('\n'.join(warn), btns=['Ok', 'Cancel'],
                                                      cmds=[self.on_dialAccept0, self.on_dialCancel0])
                self.warnDial0.exec_()

    def on_dialAccept0(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        selLt = self.mainUi.twLinetest.selectedItems()
        try:
            os.remove(selLt[0]._ltAbsPath)
            check = True
            print "Deleting linetest: %s ..." % selLt[0]._ltFile
        except:
            check = False
            print "!!! ERROR : Cannot delete linetest: %s !!!" % selLt[0]._ltFile
        if check:
            self.mainUi.uiRf_linetestTab.rf_ltTree()
            self.warnDial0.close()

    def on_dialCancel0(self):
        """ Command launch when Qbutton 'Cancel' of dialog is clicked """
        self.warnDial0.close()

    def on_linetest(self):
        """ Refresh preview image, sequence and movie info """
        selLt = self.mainUi.twLinetest.selectedItems()
        if selLt:
            if hasattr(selLt[0], '_ltLink'):
                params = selLt[0].widget.params
            else:
                params = selLt[0].parent().widget.params
            #-- Preview Image --#
            if not params['ltIma'] == '' and not params['ltIma'] == ' ':
                self.mainUi.bPreviewImage.setEnabled(True)
                self.mainUi.uiRf_previewImage.rf_previewIma(params['ltIma'])
            else:
                self.mainUi.bPreviewImage.setEnabled(False)
                self.mainUi.uiRf_previewImage.rf_previewIma(prodManager.imaList['prodManager.png'])
            #-- LT Sequence --#
            if not params['ltSeq'] == '' and not params['ltSeq'] == ' ':
                self.mainUi.bPreviewSequence.setEnabled(True)
                self.mainUi.bPreviewSequence.absPath = params['ltSeq']
            else:
                self.mainUi.bPreviewSequence.setEnabled(False)
                self.mainUi.bPreviewSequence.absPath = None
            #-- LT Movie --#
            if not params['ltMov'] == '' and not params['ltMov'] == ' ':
                self.mainUi.bPreviewMovie.setEnabled(True)
                self.mainUi.bPreviewMovie.absPath = params['ltMov']
            else:
                self.mainUi.bPreviewMovie.setEnabled(False)
                self.mainUi.bPreviewMovie.absPath = None
        else:
            self.mainUi.bPreviewImage.setEnabled(False)
            self.mainUi.uiRf_previewImage.rf_previewIma(prodManager.imaList['prodManager.png'])
            self.mainUi.bPreviewSequence.setEnabled(False)
            self.mainUi.bPreviewSequence.absPath = None
            self.mainUi.bPreviewMovie.setEnabled(False)
            self.mainUi.bPreviewMovie.absPath = None
