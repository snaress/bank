import os
from PyQt4 import QtGui
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.prodManager.ui import tabOverViewUI


class OverViewTab(QtGui.QWidget, tabOverViewUI.Ui_overViewTab):

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(OverViewTab, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup overView tabWidget """
        self.setupUi(self)
        self.log.debug("#-- Setup Tab OverView --#")

    def _refresh(self):
        """ Refresh overView tabWidget """
        self.log.debug("#-- Refresh Tab OverView --#")
        self.twTree.clear()
        prodData = pFile.readPyFile(self.pm._prodFile)
        treeDict = prodData['prodTrees'][self.mainUi.getSelTree()]
        self.rf_columns(treeDict)
        for path in treeDict['tree']['_order']:
            newItem = self._newItem(path, treeDict['steps'], prodData['prodTasks'],
                                    treeDict['tree'][path])
            if len(path.split('/')) == 1:
                self.twTree.addTopLevelItem(newItem)
            else:
                parentPath = '/'.join(path.split('/')[:-1])
                parent = self.getItemFromPath(parentPath)
                parent.addChild(newItem)
            for n, step in enumerate(newItem.widgets):
                self.twTree.setItemWidget(newItem, n+1, newItem.widgets[n])

    def rf_columns(self, treeDict):
        """ Refresh columns with stepNames
            @param treeDict: (dict) : Tree datas """
        stepLabels = treeDict['steps']
        stepLabels.insert(0, ' ')
        self.twTree.setHeaderLabels(stepLabels)
        self.twTree.setColumnCount(len(stepLabels))
        for n in range(len(stepLabels)):
            self.twTree.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)

    def getItemFromPath(self, path):
        """ Get item from given tree path
            @param path: (str) : Tree path
            @return: (object) : QTreeWidgetItem """
        for item in pQt.getAllItems(self.twTree):
            if item.itemPath == path:
                return item

    def _newItem(self, itemPath, steps, taskDict, nodeDict):
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, nodeDict['nodeLabel'])
        newItem.itemPath = itemPath
        newItem.widgets = []
        if nodeDict['nodeType'] == 'shotNode':
            path = os.path.join(self.pm._prodPath, self.pm._prodId, 'tree',
                                self.mainUi.getSelTree())
            for p in itemPath.split('/'):
                path = os.path.join(path, p)
            newItem.nodePath = pFile.conformPath(path)
            for step in steps:
                print step
                newWidget = QtGui.QPushButton()
                newItem.taskFile = pFile.conformPath(os.path.join(path, 'lt', step, 'ltTask.py'))
                if not os.path.exists(newItem.taskFile):
                    newWidget.setText("ToDo")
                    taskColor = taskDict['ToDo']['color']
                else:
                    taskData = pFile.readPyFile(newItem.taskFile)
                    print taskData
                    newWidget.setText(taskData['task'])
                    taskColor = taskDict[taskData['task']]
                newWidget.setStyleSheet("background-color:rgb(%s, %s, %s)" % (taskColor[0],
                                                                              taskColor[1],
                                                                              taskColor[2]))
                newItem.widgets.append(newWidget)
        return newItem
