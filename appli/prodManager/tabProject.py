from appli import prodManager
from functools import partial
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from appli.prodManager.ui import tabProjectUI, wgtProdTaskUI, wgtProdStepUI, wgtProdTreeUI


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
        self.log.debug("#-- Setup Tab Project --#")
        self.bEditProd.clicked.connect(self.on_editProjectTab)
        self.bCancelEdit.clicked.connect(self.on_cancelProjectTab)
        self.bOpenWorkDir.clicked.connect(self.on_openWorkDir)
        self.wgTrees = ProdTrees(self.mainUi, self)
        self.hlParams.insertWidget(1, self.wgTrees)
        self.wgTask = ProdTask(self.mainUi, self)
        self.hlParams.insertWidget(3, self.wgTask)

    def _refresh(self):
        """ Init project tabWidget """
        self.log.debug("#-- Refresh Tab Project --#")
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
        self.log.debug("#-- Refresh Tab Project Visibility --#")
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


class ProdTrees(QtGui.QWidget, wgtProdTreeUI.Ui_prodTree):
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
        for item in pQt.getTopItems(self.twTrees):
            treeDict['_order'].append(item.treeName)
            treeDict[item.treeName] = {'steps': [], 'attr': {'_order': []}}
        return treeDict

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("Setup prod trees widget ...")
        self.setupUi(self)
        self.bAddItem.setText("Add Tree")
        self.bAddItem.clicked.connect(self.on_addTree)
        self.bDelItem.setText("Del Tree")
        self.bDelItem.clicked.connect(self.on_delTree)
        self.bItemUp.clicked.connect(partial(self.on_moveTree, 'up'))
        self.bItemDn.clicked.connect(partial(self.on_moveTree, 'down'))
        self.twTrees.setHeaderLabels(["Project Trees"])
        self.twTrees.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

    def _refresh(self):
        """ Refresh trees QTreeWidget """
        self.log.debug("Refreshing prodTrees widget ...")
        self.twTrees.clear()
        for tree in self.pm.prodTrees['_order']:
            self._addTree(treeName=tree)

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("Refreshing prodTree visibility ...")
        self.bAddItem.setEnabled(state)
        self.bDelItem.setEnabled(state)
        self.bItemUp.setEnabled(state)
        self.bItemDn.setEnabled(state)

    def on_addTree(self):
        """ Command launch when 'Add Tree' QPushButton is clicked """
        self.log.debug("#-- New Tree --#")
        mess = "New Tree: Enter tree name (ex: assets or shots)"
        self.addTreeDialog = pQt.PromptDialog(mess, partial(self._addTree, treeName=None))
        self.addTreeDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.addTreeDialog.exec_()

    def on_delTree(self):
        """ Command launch when 'Del Tree' QPushButton is clicked """
        self.log.debug("#-- Delete Tree --#")
        pQt.delSelItems(self.twTrees)

    def on_moveTree(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        self.log.debug("#-- Move Tree --#")
        selItems = self.twTrees.selectedItems() or []
        trees = []
        for item in selItems:
            trees.append(item.treeName)
            movedItem = pQt.moveSelItems(self.twTrees, item, side)
            if movedItem is not None:
                self.log.debug("\t Move %s %r" % (side, item.treeName))
        for item in pQt.getTopItems(self.twTrees):
            if item.treeName in trees:
                item.setSelected(True)
            else:
                item.setSelected(False)

    def getTreeList(self):
        """ Get tree list from widget
            @return: (list) : Tree list """
        return self.__getDict__()['_order']

    def _addTree(self, treeName=None):
        """ Add new tree to QTreeWidget
            @param treeName: (str) : Tree Name """
        if treeName is None:
            newTree = self.addTreeDialog.result()['result_1']
        else:
            newTree = treeName
        if not newTree in self.getTreeList():
            self.log.debug("\t Adding tree %r ..." % newTree)
            if treeName is None:
                self.addTreeDialog.close()
            newItem = self._newTreeItem(newTree)
            self.twTrees.addTopLevelItem(newItem)
        else:
            pQt.errorDialog("Tree %r already exists !!!" % newTree, self.addTreeDialog)

    def _newTreeItem(self, treeName):
        """ Create new tree QTreeWidgetItem
            @param treeName: (str) : Tree Name
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, treeName)
        newItem.treeName = treeName
        return newItem


class ProdTask(QtGui.QWidget, wgtProdTaskUI.Ui_prodTask):
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
        for item in pQt.getTopItems(self.twTasks):
            taskDict['_order'].append(item.taskName)
            taskDict[item.taskName] = {'color': item.taskColor, 'stat': item._wgStat.isChecked()}
        return taskDict

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("Setup prod task widget ...")
        self.setupUi(self)
        self.bAddTask.clicked.connect(self.on_addTask)
        self.bDelTask.clicked.connect(self.on_delTask)
        self.bTaskUp.clicked.connect(partial(self.on_moveTask, 'up'))
        self.bTaskDn.clicked.connect(partial(self.on_moveTask, 'down'))
        self.twTasks.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.twTasks.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.twTasks.header().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

    def _refresh(self):
        """ Refresh tasks QTreeWidget """
        self.log.debug("Refreshing prodTask widget ...")
        self.twTasks.clear()
        for task in self.pm.prodTasks['_order']:
            self._addTask(taskName=task, taskColor=self.pm.prodTasks[task]['color'],
                          taskStat=self.pm.prodTasks[task]['stat'])

    def rf_widgetVisibility(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.log.debug("Refreshing prodTask visibility ...")
        self.bAddTask.setEnabled(state)
        self.bDelTask.setEnabled(state)
        self.bTaskUp.setEnabled(state)
        self.bTaskDn.setEnabled(state)
        for item in pQt.getTopItems(self.twTasks):
            item._wgColor.setEnabled(state)
            item._wgStat.setEnabled(state)

    def on_addTask(self):
        """ Command launch when 'Add Task' QPushButton is clicked """
        self.log.debug("#-- New Task --#")
        self.addTaskDialog = pQt.PromptDialog("New Task", partial(self._addTask, taskName=None,
                                                                  taskColor=None, taskStat=None))
        self.addTaskDialog.setStyleSheet(self.mainUi.applyStyle(styleName=self.mainUi._currentStyle))
        self.addTaskDialog.exec_()

    def on_delTask(self):
        """ Command launch when 'Del Task' QPushButton is clicked """
        self.log.debug("#-- Delete Task --#")
        pQt.delSelItems(self.twTasks)

    def on_moveTask(self, side):
        """ Command launch when 'up' or 'down' QPushButton is clicked
            @param side: (str) : 'up' or 'down' """
        self.log.debug("#-- Move Task --#")
        selItems = self.twTasks.selectedItems() or []
        tasks = []
        for item in selItems:
            tasks.append(item.taskName)
            taskColor = item.taskColor
            taskStat = item._wgStat.isChecked()
            movedItem = pQt.moveSelItems(self.twTasks, item, side)
            if movedItem is not None:
                self.log.debug("\t Move %s %r" % (side, item.taskName))
                movedItem._wgColor = self._newTaskColor(movedItem, taskColor)
                movedItem._wgStat = self._newTaskStat(taskStat)
                self.twTasks.setItemWidget(movedItem, 1, movedItem._wgColor)
                self.twTasks.setItemWidget(movedItem, 2, movedItem._wgStat)
        for item in pQt.getTopItems(self.twTasks):
            if item.taskName in tasks:
                item.setSelected(True)
            else:
                item.setSelected(False)

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
        if taskName is None:
            newTask = self.addTaskDialog.result()['result_1']
        else:
            newTask = taskName
        if not newTask in self.getTaskList():
            self.log.debug("\t Adding task %r ..." % newTask)
            if taskName is None:
                self.addTaskDialog.close()
            newItem = self._newTaskItem(newTask, taskColor=taskColor, taskStat=taskStat)
            self.twTasks.addTopLevelItem(newItem)
            self.twTasks.setItemWidget(newItem, 1, newItem._wgColor)
            self.twTasks.setItemWidget(newItem, 2, newItem._wgStat)
        else:
            pQt.errorDialog("Task %r already exists !!!" % newTask, self.addTaskDialog)

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

    def _newTaskStat(self, taskStat):
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


class ProdStep(QtGui.QWidget, wgtProdStepUI.Ui_stepTree):
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

    def _setupUi(self):
        """ Setup widget """
        self.log.debug("Setup prod step widget ...")
        self.setupUi(self)