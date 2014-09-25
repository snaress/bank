from appli import prodManager
from functools import partial
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from appli.prodManager.ui import tabProjectUI, wgtProdTreeUI, dialShotNodeUI


class ProjectTab(QtGui.QWidget, tabProjectUI.Ui_projectTab):
    """ Project settings ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(ProjectTab, self).__init__()
        self._setupUi()
        self._refresh()

    def _setupUi(self):
        """ Setup project tabWidget """
        self.setupUi(self)
        self.log.info("#-- Setup Tab Project --#")
        self.bEditProd.clicked.connect(self.on_editProjectTab)
        self.bCancelEdit.clicked.connect(self.on_cancelProjectTab)
        self.bOpenWorkDir.clicked.connect(self.on_openWorkDir)
        self.wgTrees = ProdTrees(self.mainUi, self)
        self.hlParams.insertWidget(1, self.wgTrees)
        self.wgTask = ProdTask(self.mainUi, self)
        self.hlParams.insertWidget(3, self.wgTask)
        self.wgTree = ProdTree(self.mainUi, self)
        self.vlProdTree.insertWidget(0, self.wgTree)
        self.wgStep = ProdStep(self.mainUi, self)
        self.vlProdStep.insertWidget(0, self.wgStep)
        self.wgAttr = ProdAttributes(self.mainUi, self)
        self.vlProdAttr.insertWidget(0, self.wgAttr)

    def _refresh(self):
        """ Init project tabWidget """
        self.log.info("#-- Refresh Tab Project --#")
        self.rf_title()
        self.rf_date()
        self.rf_workDir()
        self.wgTrees._refresh()
        self.wgTask._refresh()
        self.rf_tabVis()

    def _update(self):
        """ Update pmObject with tabWidget values """
        self.pm.prodStartDate = str(self.deStart.text())
        self.pm.prodStopDate = str(self.deEnd.text())
        self.pm.prodWorkDir = str(self.leWorkDir.text())
        self.pm.prodTrees = self.wgTrees.__getDict__()
        self.pm.prodTasks = self.wgTask.__getDict__()

    def rf_tabVis(self, state=False):
        """ Refresh project tab ui visibility
            @param state: (bool) : Visibility state """
        self.log.info("#-- Refresh Tab Project Visibility --#")
        #-- Init Project Label --#
        self.bCancelEdit.setVisible(state)
        #-- Init Project Date --#
        self.deStart.setReadOnly(not state)
        self.deStart.setCalendarPopup(state)
        self.deEnd.setReadOnly(not state)
        self.deEnd.setCalendarPopup(state)
        #-- Init Project Work Directory --#
        self.leWorkDir.setReadOnly(not state)
        self.bOpenWorkDir.setEnabled(state)
        #-- Init Project Widgets --#
        self.wgTrees.rf_widgetVisibility(state=state)
        self.wgTask.rf_widgetVisibility(state=state)
        self.wgTree.rf_widgetVisibility(state=state)
        self.wgStep.rf_widgetVisibility(state=state)
        self.wgAttr.rf_widgetVisibility(state=state)

    def rf_title(self):
        """ Refresh project title """
        self.log.debug("Refreshing prod title ...")
        self.lProd.setText("%s (%s)" % (self.pm.prodName, self.pm.prodAlias))
        self.log.debug("\t %s (%s)" % (self.pm.prodName, self.pm.prodAlias))

    def rf_date(self):
        """ Refresh project date """
        self.log.debug("Refreshing prod date ...")
        self.deStart.setDate(QtCore.QDate(int(self.pm.prodStartDate.split('/')[0]),
                                          int(self.pm.prodStartDate.split('/')[1]),
                                          int(self.pm.prodStartDate.split('/')[2])))
        self.deEnd.setDate(QtCore.QDate(int(self.pm.prodStopDate.split('/')[0]),
                                        int(self.pm.prodStopDate.split('/')[1]),
                                        int(self.pm.prodStopDate.split('/')[2])))
        self.log.debug("\t Project Start: %s; Project End: %s" % (self.pm.prodStartDate,
                                                                  self.pm.prodStopDate))

    def rf_workDir(self):
        """ Refresh project workDir """
        self.log.debug("Refreshing prod work directory ...")
        self.leWorkDir.setText(self.pm.prodWorkDir)
        self.log.debug("\t Project Work Directory: %s" % self.pm.prodWorkDir)

    def on_editProjectTab(self):
        """ Command launch when bEditProjectTab is clicked """
        checkState = self.bEditProd.isChecked()
        if checkState:
            self.bEditProd.setText("Save")
            self.setStyleSheet(self.mainUi.applyStyle(styleName='redGrey'))
        else:
            self.bEditProd.setText("Edit")
            self._update()
            self.pm.writeProject()
            self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.rf_tabVis(state=checkState)

    def on_cancelProjectTab(self):
        """ Command launch when bCancelProjectTab is clicked """
        self.bEditProd.setText("Edit")
        self.bEditProd.setChecked(False)
        self._refresh()
        self.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))

    def on_openWorkDir(self):
        """ Command launch when bOpenWorkDir is clicked """
        root = self.pm.prodWorkDir
        if self.pm.prodWorkDir == '':
            root = prodManager.rootDisk
        self.fdWorkDir = pQt.fileDialog(fdRoot=root, fdCmd=self.ud_workDir)
        self.fdWorkDir.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        self.fdWorkDir.exec_()

    def ud_workDir(self):
        """ Update Work dir with selected path from dialog """
        selPath = self.fdWorkDir.selectedFiles()
        if selPath:
            self.leWorkDir.setText(str(selPath[0]))


class DefaultProdTree(QtGui.QWidget, wgtProdTreeUI.Ui_prodTree):
    """ Default tree widget used in tabProject """

    def __init__(self):
        super(DefaultProdTree, self).__init__()
        self.setupUi(self)

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.bAddItem.setEnabled(state)
        self.bDelItem.setEnabled(state)
        self.bItemUp.setEnabled(state)
        self.bItemDn.setEnabled(state)

    def on_delItem(self):
        """ Command launch when 'Del Item' QPushButton is clicked """
        pQt.delSelItems(self.twTree)

    def on_moveItem(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        selItems = self.twTree.selectedItems() or []
        items = []
        movedItems = []
        for item in selItems:
            items.append(str(item.text(0)))
            movedItems.append(pQt.moveSelItems(self.twTree, item, side))
        for item in pQt.getTopItems(self.twTree):
            if str(item.text(0)) in items:
                item.setSelected(True)
            else:
                item.setSelected(False)
        return movedItems


class ProdTask(DefaultProdTree):
    """ Project task widget
        @param mainUi: (object) : QMainWindow
        @param parent: (object) : Parent QWidget """

    def __init__(self, mainUi, parent):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self._parent = parent
        super(ProdTask, self).__init__()
        self._setupUi()

    def __getDict__(self):
        """ Get prodTask params writtable dict
            @return: (dict) : ProdTask params """
        taskDict = {'_order': []}
        for item in pQt.getTopItems(self.twTree):
            taskDict['_order'].append(item.taskName)
            taskDict[item.taskName] = {'color': item.taskColor, 'stat': item._wgStat.isChecked()}
        return taskDict

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("\t Setup prodTask widget ...")
        self.bAddItem.setText("Add Task")
        self.bAddItem.clicked.connect(self.on_addTask)
        self.bDelItem.setText("Del Task")
        self.bDelItem.clicked.connect(self.on_delItem)
        self.bItemUp.clicked.connect(partial(self.on_moveItem, 'up'))
        self.bItemDn.clicked.connect(partial(self.on_moveItem, 'down'))
        self.twTree.setColumnCount(3)
        self.twTree.setHeaderLabels(['Task', 'Color', 'Stat'])
        self.twTree.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.twTree.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.twTree.header().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

    def _refresh(self):
        """ Refresh tasks QTreeWidget """
        self.log.debug("Refreshing prodTask widget ...")
        self.twTree.clear()
        for task in self.pm.prodTasks['_order']:
            self._addTask(taskName=task, taskColor=self.pm.prodTasks[task]['color'],
                          taskStat=self.pm.prodTasks[task]['stat'])

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("\t Refreshing prodTask visibility ...")
        super(ProdTask, self).rf_widgetVisibility(state=state)
        for item in pQt.getTopItems(self.twTree):
            item._wgColor.setEnabled(state)
            item._wgStat.setEnabled(state)

    def on_addTask(self):
        """ Command launch when 'Add Task' QPushButton is clicked """
        self.log.debug("#-- New Task --#")
        self.addTaskDialog = pQt.PromptDialog("New Task", partial(self._addTask, taskName=None,
                                                                  taskColor=None, taskStat=None))
        self.addTaskDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.addTaskDialog.exec_()

    def on_delItem(self):
        """ Command launch when 'Del Task' QPushButton is clicked """
        self.log.debug("#-- Delete Task --#")
        super(ProdTask, self).on_delItem()

    def on_moveItem(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        self.log.debug("#-- Move Task --#")
        treeDict = self.__getDict__()
        movedItems = super(ProdTask, self).on_moveItem(side=side)
        for item in movedItems:
            if item is not None:
                self.log.debug("\t Move %s %r" % (side, item.taskName))
                item._wgColor = self._newTaskColor(item, item.taskColor)
                # noinspection PyTypeChecker
                item._wgStat = self._newTaskStat(treeDict[item.taskName]['stat'])
                self.twTree.setItemWidget(item, 1, item._wgColor)
                self.twTree.setItemWidget(item, 2, item._wgStat)

    def on_taskColor(self, item):
        """ Command launch when 'colorChoice' QPushButton is clicked
            @param item: (object) : Task QTreeWidgetItem """
        if self._parent.bEditProd.isChecked():
            self.log.debug("#-- Edit Task Color --#")
            # noinspection PyArgumentList
            color = QtGui.QColorDialog.getColor()
            if color.isValid():
                rgba = color.getRgb()
                item._wgColor.setStyleSheet("background:rgb(%s, %s, %s)" % (rgba[0], rgba[1], rgba[2]))
                item.taskColor = (rgba[0], rgba[1], rgba[2])
                self.log.debug("\t %s color = %s" % (item.taskName, (rgba[0], rgba[1], rgba[2])))

    def getTaskList(self):
        """ Get task list from widget
            @return: (list) : Task list """
        return self.__getDict__()['_order']

    def _addTask(self, taskName=None, taskColor=None, taskStat=None):
        """ Add new task to QTreeWidget
            @param taskName: (str) : Task Name
            @param taskColor: (tuple) : Rgb color
            @param taskStat: (bool) : Task count in stats """
        fromDialog = False
        if taskName is None:
            fromDialog = True
            taskName = self.addTaskDialog.result()['result_1']
        if not taskName in self.getTaskList():
            self.log.debug("\t Adding task %r ..." % taskName)
            if fromDialog:
                self.addTaskDialog.close()
            newItem = self._newTaskItem(taskName, taskColor=taskColor, taskStat=taskStat)
            self.twTree.addTopLevelItem(newItem)
            self.twTree.setItemWidget(newItem, 1, newItem._wgColor)
            self.twTree.setItemWidget(newItem, 2, newItem._wgStat)
        else:
            pQt.errorDialog("Task %r already exists !!!" % taskName, self.addTaskDialog)

    def _newTaskItem(self, taskName, taskColor=None, taskStat=None):
        """ Create new task QTreeWidgetItem
            @param taskName: (str) : Task Name
            @param taskColor: (tuple) : Rgb color
            @param taskStat: (bool) : Task count in stats
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, taskName)
        newItem.taskName = taskName
        newItem._wgColor = self._newTaskColor(newItem, taskColor)
        newItem._wgStat = self._newTaskStat(taskStat)
        return newItem

    def _newTaskColor(self, item, taskColor, dialog=True):
        """ New task color QPushButton
            @param item: (object) : QTreeWidgetItem
            @param taskColor: (tuple) : Rgb color
            @param dialog: (bool) : Color dialog picker enable or not
            @return: (object) : New task color QPushButton """
        newColor = QtGui.QPushButton()
        newColor.setText('')
        newColor.setMaximumWidth(40)
        if dialog:
            newColor.connect(newColor, QtCore.SIGNAL("clicked()"), partial(self.on_taskColor, item))
        if taskColor is None:
            item.taskColor = (200, 200, 200)
        else:
            item.taskColor = taskColor
            newColor.setStyleSheet("background:rgb(%s, %s, %s)" % (taskColor[0], taskColor[1], taskColor[2]))
        return newColor

    @staticmethod
    def _newTaskStat(taskStat):
        """ New task stat QCheckBox
            @param taskStat: (bool) : Task count in stats
            @return: (object) : New task stat QCheckBox """
        newStat = QtGui.QCheckBox()
        newStat.setText('')
        if taskStat is None:
            newStat.setChecked(True)
        else:
            newStat.setChecked(taskStat)
        return newStat


class ProdTrees(DefaultProdTree):
    """ Project trees widget
        @param mainUi: (object) : QMainWindow
        @param parent: (object) : Parent QWidget """

    def __init__(self, mainUi, parent):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self._parent = parent
        super(ProdTrees, self).__init__()
        self._setupUi()

    def __getDict__(self):
        """ Get prodTask params writtable dict
            @return: (dict) : ProdTask params """
        treeDict = {'_order': []}
        for item in pQt.getTopItems(self.twTree):
            treeDict['_order'].append(item.treeName)
            treeDict[item.treeName] = item.treeDict
        return treeDict

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup widget """
        self.log.debug("\t Setup prodTrees widget ...")
        self.bAddItem.setText("Add Tree")
        self.bAddItem.clicked.connect(self.on_addTree)
        self.bDelItem.setText("Del Tree")
        self.bDelItem.clicked.connect(self.on_delItem)
        self.bItemUp.clicked.connect(partial(self.on_moveItem, 'up'))
        self.bItemDn.clicked.connect(partial(self.on_moveItem, 'down'))
        self.twTree.setColumnCount(1)
        self.twTree.setHeaderLabels(["Project Trees"])
        self.twTree.header().setStretchLastSection(True)
        self.twTree.itemClicked.connect(self.on_treeItem)

    def _refresh(self):
        """ Refresh trees QTreeWidget """
        self.log.debug("Refreshing prodTrees widget ...")
        self.twTree.clear()
        for tree in self.pm.prodTrees['_order']:
            self._addTree(treeName=tree, treeDict=self.pm.prodTrees[tree])

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("\t Refreshing prodTrees visibility ...")
        super(ProdTrees, self).rf_widgetVisibility(state=state)

    def on_addTree(self):
        """ Command launch when 'Add Tree' QPushButton is clicked """
        self.log.debug("#-- New Tree --#")
        mess = "New Tree: Enter tree name (ex: assets or shots)"
        self.addTreeDialog = pQt.PromptDialog(mess, partial(self._addTree, treeName=None,
                                                                           treeDict=None))
        self.addTreeDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.addTreeDialog.exec_()

    def on_delItem(self):
        """ Command launch when 'Del Tree' QPushButton is clicked """
        self.log.debug("#-- Delete Tree --#")
        super(ProdTrees, self).on_delItem()

    def on_moveItem(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        self.log.debug("#-- Move Tree --#")
        movedItems = super(ProdTrees, self).on_moveItem(side=side)
        for item in movedItems:
            self.log.debug("\t Move %r %s" % (str(item.text(0)), side))

    def on_treeItem(self):
        """ refresh selected tree params """
        self._parent.wgStep._refresh()
        self._parent.wgAttr._refresh()
        self._parent.wgAttr.rf_widgetVisibility(self._parent.bEditProd.isChecked())

    def getTreeList(self):
        """ Get tree list from widget
            @return: (list) : Tree list """
        return self.__getDict__()['_order']

    def _addTree(self, treeName=None, treeDict=None):
        """ Add new tree to QTreeWidget
            @param treeName: (str) : Tree Name """
        fromDialog = False
        if treeName is None:
            fromDialog = True
            treeName = self.addTreeDialog.result()['result_1']
        if not treeName in self.getTreeList():
            self.log.debug("\t Adding tree %r ..." % treeName)
            if fromDialog:
                self.addTreeDialog.close()
            if treeDict is None:
                treeDict = {'tree': {'_order': []}, 'steps': [], 'attr': {'_order': []}}
            newItem = self._newTreeItem(treeName, treeDict)
            self.twTree.addTopLevelItem(newItem)
        else:
            pQt.errorDialog("Tree %r already exists !!!" % treeName, self.addTreeDialog)

    @staticmethod
    def _newTreeItem(treeName, treeDict):
        """ Create new tree QTreeWidgetItem
            @param treeName: (str) : Tree Name
            @param treeDict: (str) : Tree dict
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, treeName)
        newItem.treeName = treeName
        newItem.treeDict = treeDict
        return newItem


class ProdStep(DefaultProdTree):
    """ Project step widget
        @param mainUi: (object) : QMainWindow
        @param parent: (object) : Parent QWidget """

    def __init__(self, mainUi, parent):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self._parent = parent
        super(ProdStep, self).__init__()
        self._setupUi()

    def __getDict__(self):
        """ Get prodStep params writtable list
            @return: (list) : ProdStep params """
        steps = []
        for item in pQt.getTopItems(self.twTree):
            steps.append(item.stepName)
        return steps

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("\t Setup prodStep widget ...")
        self.bAddItem.setText("Add Step")
        self.bAddItem.clicked.connect(self.on_addStep)
        self.bDelItem.setText("Del Step")
        self.bDelItem.clicked.connect(self.on_delItem)
        self.bItemUp.clicked.connect(partial(self.on_moveItem, 'up'))
        self.bItemDn.clicked.connect(partial(self.on_moveItem, 'down'))
        self.twTree.setColumnCount(1)
        self.twTree.setHeaderLabels(["Tree Steps"])
        self.twTree.header().setStretchLastSection(True)

    def _refresh(self):
        """ Refresh trees QTreeWidget """
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        self.log.debug("Refreshing prodStep widget ...")
        self.twTree.clear()
        if selTreeItems:
            for step in selTreeItems[0].treeDict['steps']:
                self._addStep(stepName=step)

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("\t Refreshing prodStep visibility ...")
        super(ProdStep, self).rf_widgetVisibility(state=state)

    def on_addStep(self):
        """ Command launch when 'Add Step' QPushButton is clicked """
        self.log.debug("#-- New Step --#")
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        if selTreeItems:
            mess = "New Step: Enter step name"
            self.addStepDialog = pQt.PromptDialog(mess, partial(self._addStep, stepName=None))
            self.addStepDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
            self.addStepDialog.exec_()
        else:
            pQt.errorDialog("Select a tree before adding steps", self._parent)

    def on_delItem(self):
        """ Command launch when 'Del Tree' QPushButton is clicked """
        self.log.debug("#-- Delete Tree --#")
        super(ProdStep, self).on_delItem()
        self.storeParams()

    def on_moveItem(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        self.log.debug("#-- Move Tree --#")
        movedItems = super(ProdStep, self).on_moveItem(side=side)
        for item in movedItems:
            if item is not None:
                self.log.debug("\t Move %r %s" % (str(item.text(0)), side))
        self.storeParams()

    def storeParams(self):
        """ Store step params """
        self.log.debug("#-- Store Step Params --#")
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        if selTreeItems:
            treeItem = selTreeItems[0]
            treeItem.treeDict['steps'] = self.__getDict__()

    def _addStep(self, stepName=None):
        """ Add new step to QTreeWidget
            @param stepName: (str) : Step Name """
        fromDialog = False
        if stepName is None:
            fromDialog = True
            stepName = self.addStepDialog.result()['result_1']
        if not stepName in self.__getDict__():
            self.log.debug("\t Adding step %r ..." % stepName)
            newItem = self._newStepItem(stepName)
            self.twTree.addTopLevelItem(newItem)
            if fromDialog:
                self.addStepDialog.close()
                self.storeParams()
        else:
            pQt.errorDialog("Step %r already exists !!!" % stepName, self.addStepDialog)

    @staticmethod
    def _newStepItem(stepName):
        """ Create new step QTreeWidgetItem
            @param stepName: (str) : Step Name
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, stepName)
        newItem.stepName = stepName
        return newItem


class ProdAttributes(DefaultProdTree):
    """ Project attributes widget
        @param mainUi: (object) : QMainWindow
        @param parent: (object) : Parent QWidget """

    def __init__(self, mainUi, parent):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self._parent = parent
        super(ProdAttributes, self).__init__()
        self._setupUi()

    def __getDict__(self):
        """ Get prodAttr params writtable dict
            @return: (dict) : ProdAttr params """
        attrDict = {'_order': []}
        for item in pQt.getTopItems(self.twTree):
            attrDict['_order'].append(item.attrName)
            attrDict[item.attrName] = str(item._wgType.currentText())
        return attrDict

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("\t Setup prodAttr widget ...")
        self.bAddItem.setText("Add Attr")
        self.bAddItem.clicked.connect(self.on_addAttr)
        self.bDelItem.setText("Del Attr")
        self.bDelItem.clicked.connect(self.on_delItem)
        self.bItemUp.clicked.connect(partial(self.on_moveItem, 'up'))
        self.bItemDn.clicked.connect(partial(self.on_moveItem, 'down'))
        self.twTree.setColumnCount(2)
        self.twTree.setHeaderLabels(['Label', 'Type'])
        self.twTree.header().setStretchLastSection(True)
        self.twTree.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

    def _refresh(self):
        """ Refresh attributes QTreeWidget """
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        self.log.debug("Refreshing prodTrees widget ...")
        self.twTree.clear()
        if selTreeItems:
            for attr in selTreeItems[0].treeDict['attr']['_order']:
                self._addAttr(attrName=attr, attrType=selTreeItems[0].treeDict['attr'][attr])

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("\t Refreshing prodAttr visibility ...")
        super(ProdAttributes, self).rf_widgetVisibility(state=state)
        for item in pQt.getTopItems(self.twTree):
            item._wgType.setEnabled(state)

    def on_addAttr(self):
        """ Command launch when 'Add Attr' QPushButton is clicked """
        self.log.debug("#-- New Attribute --#")
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        if selTreeItems:
            mess = "New Attribute: Enter label"
            self.addAttrDialog = pQt.PromptDialog(mess, partial(self._addAttr, attrName=None))
            self.addAttrDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
            self.addAttrDialog.exec_()
        else:
            pQt.errorDialog("Select a tree before adding steps", self._parent)

    def on_delItem(self):
        """ Command launch when 'Del Tree' QPushButton is clicked """
        self.log.debug("#-- Delete Attribute --#")
        super(ProdAttributes, self).on_delItem()
        self.storeParams()

    def on_moveItem(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        self.log.debug("#-- Move Attr --#")
        treeDict = self.__getDict__()
        movedItems = super(ProdAttributes, self).on_moveItem(side=side)
        for item in movedItems:
            if item is not None:
                self.log.debug("\t Move %s %r" % (side, item.attrName))
                item._wgType = self._newAttrType(treeDict[item.attrName])
                self.twTree.setItemWidget(item, 1, item._wgType)
        self.storeParams()

    def storeParams(self):
        """ Store attribute params """
        self.log.debug("#-- Store Attr Params --#")
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        if selTreeItems:
            treeItem = selTreeItems[0]
            treeItem.treeDict['attr'] = self.__getDict__()

    def _addAttr(self, attrName=None, attrType=None):
        """ Add new attribute to QTreeWidget
            @param attrName: (str) : Attribute Label
            @param attrType: (str) : Attribute type ('str', 'int' or 'float') """
        fromDialog = False
        if attrName is None:
            fromDialog = True
            attrName = self.addAttrDialog.result()['result_1']
            attrType = 'str'
        if not attrName in self.__getDict__()['_order']:
            self.log.debug("\t Adding attribute %r: %s ..." % (attrName, attrType))
            newItem = self._newAttrItem(attrName, attrType)
            self.twTree.addTopLevelItem(newItem)
            self.twTree.setItemWidget(newItem, 1, newItem._wgType)
            if fromDialog:
                self.addAttrDialog.close()
                self.storeParams()
        else:
            pQt.errorDialog("Attribute %r already exists !!!" % attrName, self.addAttrDialog)

    def _newAttrItem(self, attrName, attrType):
        """ Create new attribute QTreeWidgetItem
            @param attrName: (str) : Attribute Name
            @param attrType: (str) : Attribute type ('str', 'int' or 'float')
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, attrName)
        newItem.attrName = attrName
        newItem._wgType = self._newAttrType(attrType)
        return newItem

    # noinspection PyUnresolvedReferences
    def _newAttrType(self, attrType):
        """ Create new attribute type QComboBox
            @param attrType: (str) : Attribute type ('str', 'int' or 'float')
            @return: (object) : New QComboBox """
        newType = QtGui.QComboBox()
        newType.addItems(['str', 'int', 'float'])
        newType.setCurrentIndex(newType.findText(attrType))
        newType.currentIndexChanged.connect(self.storeParams)
        return newType


class ProdTree(DefaultProdTree):
    """ Project tree widget
        @param mainUi: (object) : QMainWindow
        @param parent: (object) : Parent QWidget """

    def __init__(self, mainUi, parent):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self._parent = parent
        super(ProdTree, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("\t Setup prodTree widget ...")
        self.bAddItem.setText("Add Node")
        self.bAddItem.clicked.connect(self.on_addNode)
        self.bDelItem.setText("Del Node")
        self.bItemUp.setVisible(False)
        self.bItemDn.setVisible(False)
        self.twTree.setColumnCount(1)
        self.twTree.setHeaderLabels(["Project Tree"])
        self.twTree.setSortingEnabled(True)
        self.twTree.header().setStretchLastSection(True)
        self.twTree.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.twTree.setSelectionMode(QtGui.QTreeWidget.ExtendedSelection)

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("\t Refreshing prodTree visibility ...")
        super(ProdTree, self).rf_widgetVisibility(state=state)

    def on_addNode(self):
        """ Command launch when 'Add Node' QPushButton is clicked """
        self.log.debug("#-- New Tree Node --#")
        selTreeItems = self._parent.wgTrees.twTree.selectedItems()
        if selTreeItems:
            self.addNodeDialog = EditProdTree()
            self.addNodeDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
            self.addNodeDialog.exec_()
        else:
            pQt.errorDialog("Select a tree before adding node", self._parent)

    def _addNode(self, nodeType, nodeName=None, parent=None):
        print 'toto'

    def _newItem(self, itemType, itemName):
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, itemName)
        newItem.nodeType = itemType
        newItem.nodeName = itemName
        return newItem


class EditProdTree(QtGui.QDialog, dialShotNodeUI.Ui_editProdTree):

    def __init__(self):
        super(EditProdTree, self).__init__()
        self._setupUi()
        self.rf_nameCvtnVis()
        self.rf_methodeVis()

    def _setupUi(self):
        """ Setup dialog """
        self.setupUi(self)
        self.rbContainer.clicked.connect(self.rf_nameCvtnVis)
        self.rbShotNode.clicked.connect(self.rf_nameCvtnVis)
        self.rbUnique.clicked.connect(self.rf_methodeVis)
        self.rbMulti.clicked.connect(self.rf_methodeVis)
        self.bCancel.clicked.connect(self.close)

    def rf_nameCvtnVis(self):
        """ Refresh name convention visibility """
        self.lNameCvtn.setVisible(self.rbShotNode.isChecked())
        self.cbNameCvtn.setVisible(self.rbShotNode.isChecked())
        if self.rbShotNode.isChecked():
            self.lMessage.setText("Enter New ShotNode Name")
        else:
            self.lMessage.setText("Enter New Container Name")

    def rf_methodeVis(self):
        """ Refresh methode visibility """
        self.fUnique.setVisible(self.rbUnique.isChecked())
        self.fMulti.setVisible(self.rbMulti.isChecked())
