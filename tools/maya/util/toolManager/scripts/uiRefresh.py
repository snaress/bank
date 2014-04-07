import os
from PyQt4 import QtGui, uic
from functools import partial
from tools.maya.util import toolManager
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import  procFile as pFile


class PopulateTree(object):
    """ Populate toolManager tree QTreeWidget
        @param mainUi: (object) : ToolManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi

    def toolsTree(self):
        """ Populate tools tree QTreeWidget """
        if not os.path.exists(self.mainUi.rootPath):
            print "!!! Error: RootPath doesn't exist (%s) !!!" % self.mainUi.rootPath
        else:
            #-- Populate Tools Type --#
            toolTypes = os.listdir(self.mainUi.rootPath) or []
            for toolType in toolTypes:
                typePath = os.path.join(self.mainUi.rootPath, toolType)
                if os.path.isdir(typePath) and not toolType.startswith('.'):
                    newType = self.newTreeItem('container', toolType, typePath)
                    newCtnr = self.containerItem(toolType)
                    newType.buttonWidget = newCtnr
                    newCtnr.clicked.connect(partial(self.on_container, newType))
                    self.mainUi.twTools.addTopLevelItem(newType)
                    self.mainUi.twTools.setItemWidget(newType, 0, newCtnr)
                    #-- Populate Tools --#
                    toolNames = os.listdir(typePath) or []
                    for toolName in toolNames:
                        toolPath = os.path.join(typePath, toolName)
                        launchFile = os.path.join(toolPath, '__tmLauncher__.py')
                        if (os.path.isdir(toolPath) and not toolName.startswith('.') and
                            os.path.exists(launchFile)):
                            newTool = self.newTreeItem('tool', toolName, toolPath)
                            toolTask, toolComm = self._getWidgetParams(launchFile)
                            toolWidget = ToolWidget(self.mainUi, toolName, toolTask, toolComm)
                            newType.addChild(newTool)
                            self.mainUi.twTools.setItemWidget(newTool, 0, toolWidget)

    def _getWidgetParams(self, launchFile):
        toolTask = 'WIP'
        toolComm = "No comments !!!"
        lines = pFile.readFile(launchFile)
        for line in lines:
            if line.startswith('toolTask'):
                toolTask = line.split(' = ')[-1].split('"')[1]
            if line.startswith('toolComment'):
                toolComm = line.split(' = ')[-1].split('"')[1]
        return toolTask, toolComm

    def newTreeItem(self, nodeType, nodeName, nodePath):
        """ Create new tools tree QTreeWidgetItem
            @param nodeType: (str) : 'container' or 'tool'
            @param nodeName: (str) : New node name
            @param nodePath: (str) : New node path
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.nodeTree = self.mainUi.twTools
        newItem.nodeType = nodeType
        newItem.nodeName = nodeName
        newItem.nodePath = nodePath
        return newItem

    @staticmethod
    def containerItem(nodeName):
        """ New item widget
            @param nodeName: (str) : New node name
            @return: (object) : New item widget """
        newCtnr = QtGui.QPushButton()
        newCtnr.setText(nodeName.upper())
        newFont = QtGui.QFont()
        newFont.setBold(True)
        newCtnr.setFont(newFont)
        newCtnr.setCheckable(True)
        return newCtnr

    def on_container(self, topLevelItem):
        """ Command launch when container item button is clicked
            @param topLevelItem: (object) : Top level QTreeWidgetItem """
        allItems = pQt.getTopItems(self.mainUi.twTools)
        for item in allItems:
            if not item.nodeName == topLevelItem.nodeName:
                item.setExpanded(False)
                item.buttonWidget.setChecked(False)
        topLevelItem.setExpanded(topLevelItem.buttonWidget.isChecked())


toolWidgetClass, toolWidgetUiClass = uic.loadUiType(toolManager.uiList['toolWidget'])
class ToolWidget(toolWidgetClass, toolWidgetUiClass):
    """ Tool QTreeWidgetItem widget
        @param mainUi: (object) : ToolManager QMainWindow
        @param toolName: (str) : Tool name
        @param toolTask: (str) : Tool task
        @param toolComment: (str) : One line comment """

    def __init__(self, mainUi, toolName, toolTask, toolComment):
        self.mainUi = mainUi
        self.toolName = toolName
        self.toolTask = toolTask
        self.toolComment = toolComment
        super(ToolWidget, self).__init__()
        self._setupUi()
        self.initTaskColor()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.lToolName.setText(self.toolName)
        self.lToolTask.setText(self.toolTask)
        self.lToolComment.setText(self.toolComment)

    def initTaskColor(self):
        """ Task color init """
        taskColor = QtGui.QColor(125, 125, 125)
        taskColorWip  = QtGui.QColor(255, 0, 0)
        taskColorDev  = QtGui.QColor(255, 200, 0)
        taskColorProd  = QtGui.QColor(0, 255, 0)
        if self.toolTask == 'WIP':
            color = taskColorWip
        elif self.toolTask == 'DEV':
            color = taskColorDev
        elif self.toolTask == 'PROD':
            color = taskColorProd
        else:
            color = taskColor
        values = "{r}, {g}, {b}, {a}".format(r = color.red(), g = color.green(),
                                             b = color.blue(), a = 255)
        self.lToolTask.setStyleSheet("QLabel { color: rgba("+values+"); }")
