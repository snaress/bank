import os
from functools import partial
from PyQt4 import QtGui, uic, QtCore
from lib.qt.scripts import dialog
from tools.apps import prodManager
from lib.qt.scripts import procQt as pQt
from tools.apps.prodManager.scripts import template as pmTemplate


newProjectClass, newProjectUiClass = uic.loadUiType(prodManager.uiList['newProject'])
class NewProjectUi(newProjectClass, newProjectUiClass):
    """ New Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow"""

    def __init__(self, mainUi):
        self.mainUi = mainUi
        super(NewProjectUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup New Project dialog """
        self.setupUi(self)
        self.bCreate.clicked.connect(self.on_create)
        self.bCancel.clicked.connect(self.close)

    def on_create(self):
        """ Command launch when Qbutton 'Create' is clicked """
        project = str(self.leProject.text())
        alias = str(self.leAlias.text())
        if not project == '' and not alias == '':
            result, mess = self.mainUi.pm.newProject(project, alias)
            if result == '%s--%s' % (project, alias):
                self.mainUi.windowRefresh()
                self.close()
            else:
                self.confUi = dialog.ConfirmDialog('\n'.join(mess), btns=['Ok'], cmds=[self.on_dialogAccept])
                self.confUi.exec_()
        else:
            mess = ["#-- Warning --#",
                    "Project Name or Project Alias can't be empty !!!"]
            self.confUi = dialog.ConfirmDialog('\n'.join(mess), btns=['Ok'], cmds=[self.on_dialogAccept])
            self.confUi.exec_()

    def on_dialogAccept(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.confUi.close()


loadProjectClass, loadProjectUiClass = uic.loadUiType(prodManager.uiList['loadProject'])
class LoadProjectUi(loadProjectClass, loadProjectUiClass):
    """ Load Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        super(LoadProjectUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Load Project dialog """
        self.setupUi(self)
        self.bLoadProject.clicked.connect(self.on_load)
        self.bCancel.clicked.connect(self.close)
        self._populate()

    def _populate(self):
        """ Populate projects QTreeWidget """
        rootDir = os.path.join(prodManager.binPath, 'project')
        fldList = os.listdir(rootDir) or []
        for fld in fldList:
            projectPath = os.path.join(rootDir, fld)
            if os.path.isdir(projectPath) and not fld.startswith('.') and not fld.startswith('_'):
                newItem = QtGui.QTreeWidgetItem()
                newItem.setText(0, fld)
                newItem.projectName = fld.split('--')[0]
                newItem.projectAlias = fld.split('--')[1]
                newItem.projectAbsPath = projectPath
                self.twProjects.addTopLevelItem(newItem)

    def on_load(self):
        """  Command launch when bLoadProject is clicked """
        selItems = self.twProjects.selectedItems()
        if selItems:
            self.mainUi.loadProject(selItems[0].projectName, selItems[0].projectAlias)
            self.close()


editProjectTreeClass, editProjectTreeUiClass = uic.loadUiType(prodManager.uiList['editProjectTree'])
class EditProjectTreeUi(editProjectTreeClass, editProjectTreeUiClass):
    """ Load Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow
        @param mess: (str) : Information text
        @param itemType: (str) : 'shotFld' or 'shot' """

    def __init__(self, mainUi, mess, itemType):
        self.mainUi = mainUi
        self.mess = mess
        self.itemType = itemType
        self.defaultTemplate = pmTemplate.DefaultTemplate()
        super(EditProjectTreeUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Load Project dialog """
        self.setupUi(self)
        self.lMessage.setText(self.mess)
        self.bCreate.clicked.connect(self.on_create)
        self.bCancel.clicked.connect(self.close)

    def on_create(self):
        """ Command launch when Qbutton 'Create' of tree editor is clicked """
        nodeList = self._getNodeList(**self._getListParams)
        check = self._checkNodeList(nodeList)
        mess, btns = self._getDialogParams(check)
        self.confirmCreation = dialog.ConfirmDialog('\n'.join(mess), btns=btns,
                               cmds=[partial(self.on_confirmCreation, check['success']),
                                     self.on_cancelCreationConfirmation])
        self.confirmCreation.exec_()

    def on_confirmCreation(self, valideNodePath):
        """ Command launch when Qbutton 'Create' or 'Skip Existing' of dialog is clicked
            @param valideNodePath: (list) : Valid node path list """
        populate = PopulateProjectTrees(self.mainUi)
        for nodePath in valideNodePath:
            nodeLabel, nodeName, nodeParent = self._getNodeParams(nodePath)
            params = self.defaultTemplate.projectTreeNodeAttr(self.itemType, nodeLabel, nodeName, nodePath)
            newItem = populate.newTreeItem(**params)
            if nodeParent is None:
                self.mainUi.twProjectTree.addTopLevelItem(newItem)
            else:
                parent = self.mainUi.getParentTreeItemFromNodePath(self.mainUi.twProjectTree, nodePath)
                parent.addChild(newItem)
        self.confirmCreation.close()
        self.close()

    def on_cancelCreationConfirmation(self):
        """ Command launch when Qbutton 'Cancel' of dialog is clicked """
        self.confirmCreation.close()

    def _getDialogParams(self, check):
        """ Get dialog message and buttons list
            @param check: (dict) : Check node list result
            @return: (list) : Message, (list) : Buttons list """
        if self.itemType == 'shot':
            mess = ["########## Shot List Creation ##########"," "]
        else:
            mess = ["########## Shot Folder List Creation ##########"," "]
        btns = ['Create', 'Cancel']
        if check['fail']:
            mess.append("#-- Existing nodes --#")
            for node in check['fail']:
                mess.append(node)
            btns = ['Skip Existing', 'Cancel']
        return mess, btns

    @property
    def _getListParams(self):
        """ Get list params from ui
            @return: (dict) : Ui params """
        return {'start': int(self.sbStart.value()),
                'stop': int(self.sbStop.value()),
                'step': int(self.sbStep.value()),
                'padd': int(self.sbPadding.value()),
                'prefixe': str(self.lePrefixe.text()),
                'suffixe': str(self.leSuffixe.text())}

    @staticmethod
    def _getNodeList(**kwargs):
        """ Get node list from params
            @param kwargs: List params from ui ---> self._getListParams
            @return: (list) : Node list """
        nodeList = []
        for n in range(kwargs['start'], kwargs['stop']+1, kwargs['step']):
            padd = str(n).zfill(kwargs['padd'])
            nodeList.append('%s%s%s' % (kwargs['prefixe'], padd, kwargs['suffixe']))
        return nodeList

    def _checkNodeList(self, nodeList):
        """ Check if new node already exists
            @param nodeList: (list) : Node list
            @return: (dict) : Check result """
        allItems = pQt.getAllItems(self.mainUi.twProjectTree)
        selItems = self.mainUi.twProjectTree.selectedItems()
        nodePathList = self._getNodePathList(selItems, nodeList)
        check = self._checkNodePathList(nodePathList, allItems)
        return check

    @staticmethod
    def _getNodePathList(selItems, nodeList):
        """ Get node path list from selected items
            @param selItems: (list) : Selected QTreeWidgetItem
            @param nodeList: (list) : Node list
            @return: (list) : Node path list """
        nodePathList = []
        if selItems:
            for selItem in selItems:
                for node in nodeList:
                    nodePathList.append('%s/%s' % (selItem.nodePath, node))
        else:
            for node in nodeList:
                nodePathList.append(node)
        return nodePathList

    @staticmethod
    def _checkNodePathList(nodePathList, allItems):
        """ Check if node path list is valid
            @param nodePathList: (list) : Node path list
            @param allItems: (list) : QTreeWidgetItem list
            @return: (dict) : Check results """
        check = {'success': [], 'fail': []}
        for node in nodePathList:
            state = True
            for item in allItems:
                if item.nodePath == node:
                    state = False
                    if not item.nodePath in check['fail']:
                        check['fail'].append(item.nodePath)
            if state:
                check['success'].append(node)
        return check

    def _getNodeParams(self, nodePath):
        """ Get node params
            @param nodePath: (str) : Given node path
            @return: (str) : NodeLabel, (str) : NodeName, (str) : NodeParent """
        if '/' in nodePath:
            nodeLabel = nodePath.split('/')[-1]
            nodeParent = nodePath.split('/')[-2]
        else:
            nodeLabel = nodePath
            nodeParent = None
        if self.itemType == 'shot':
            nodeName = '%s_%s' % (nodeParent, nodeLabel)
        else:
            nodeName = nodeLabel
        return nodeLabel, nodeName, nodeParent


lineTestWidgetClass, lineTestWidgetUiClass = uic.loadUiType(prodManager.uiList['lineTestWidget'])
class LineTestWidget(lineTestWidgetClass, lineTestWidgetUiClass):

    def __init__(self):
        super(LineTestWidget, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup main widget """
        self.setupUi(self)
        self.leLtTitle.setStyleSheet("background: Tomato")
        self.dtLtDate.setStyleSheet("background: Tomato")


class PopulateProjectTrees(object):
    """ Populate Project tab trees QTreeWidget
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.defaultTemplate = pmTemplate.DefaultTemplate()

    def populateTree(self, treeType, twTree):
        """ Populate project asset and shot tree
            @param treeType: (str) : 'assetTree' or 'shotTree'
            @param twTree: (object) : QTreeWidget to populate """
        treeObj = getattr(self.pm, '%sObj' % treeType)
        for node in treeObj.treeOrder:
            newItem = self.newTreeItem(**node.getParams)
            parentItem = self.mainUi.getParentTreeItemFromNodePath(twTree, newItem.nodePath)
            if parentItem is None:
                twTree.addTopLevelItem(newItem)
            else:
                parentItem.addChild(newItem)

    def populateStep(self, treeType):
        """ Populate project asset and shot steps
            @param treeType: (str) : 'assetTree' or 'shotTree' """
        if treeType == 'assetTree':
            stepDict = self.pm.projectAssetSteps
        else:
            stepDict = self.pm.projectShotSteps
        for step in stepDict['stepOrder']:
            params = self.defaultTemplate.projectStepNodeAttr('step', step, None)
            newStep = self.newStepItem(**params)
            self.mainUi.twProjectStep.addTopLevelItem(newStep)
            for subStep in stepDict[step]:
                subParams = self.defaultTemplate.projectStepNodeAttr('substep', subStep, step)
                newSubStep = self.newStepItem(**subParams)
                newStep.addChild(newSubStep)

    def populateMain(self, treeType):
        """ Populate main ui tree
            @param treeType: (str) : 'assetTree' or 'shotTree' """
        treeObj = getattr(self.pm, '%sObj' % treeType)
        for node in treeObj.treeOrder:
            newItem = self.newMainItem(**node.getParams)
            parentItem = self.mainUi.getParentTreeItemFromNodePath(self.mainUi.twProject, newItem.nodePath)
            if parentItem is None:
                self.mainUi.twProject.addTopLevelItem(newItem)
            else:
                parentItem.addChild(newItem)

    @staticmethod
    def newTreeItem(**kwargs):
        """ Create new project tree QTreeWidgetItem
            @param kwargs: (dict) : New node params
                                    template.DefaultTemplete().projectTreeNodeAttr(**kwargs)
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        if kwargs['nodeType'] in ['assetFld', 'shotFld']:
            newItem.setText(0, kwargs['nodeLabel'].upper())
        else:
             newItem.setText(0, kwargs['nodeLabel'])
        for k in kwargs.keys():
            setattr(newItem, k, kwargs[k])
        return newItem

    @staticmethod
    def newStepItem(**kwargs):
        """ Create new project step QTreeWidgetItem
            @param kwargs: New node params
                           template.DefaultTemplete().projectTreeNodeAttr(**kwargs)
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, kwargs['stepLabel'])
        for k in kwargs.keys():
            setattr(newItem, k, kwargs[k])
        if kwargs['stepParent'] is None:
            newItem.stepPath = kwargs['stepLabel']
        else:
            newItem.stepPath = '%s/%s' % (kwargs['stepParent'], kwargs['stepLabel'])
        return newItem

    def newMainItem(self, **kwargs):
        """ Create new main tree QTreeWidgetItem
            @param kwargs: New node params
                           template.DefaultTemplete().projectTreeNodeAttr(**kwargs)
            @return: (object) : New QTreeWidgetItem """
        newItem = self.newTreeItem(**kwargs)
        if kwargs['nodeType'] in ['shot', 'asset']:
            dataPath = os.path.join(self.pm._projectPath, 'tree', kwargs['nodeType'])
            for fld in kwargs['nodePath'].split('/'):
                dataPath = os.path.join(dataPath, fld)
            dataFile = os.path.join(dataPath, '%s.py' % kwargs['nodeName'])
            newItem._dataPath = dataPath
            newItem._dataFile = dataFile
            newItem._dataLtPath = os.path.join(dataPath, 'lt')
            newItem._dataLtFile = os.path.join(newItem._dataLtPath, "lt--%s.py" % newItem.nodeName)
            if os.path.exists(dataFile):
                for k, v in self.pm.readFile(dataFile).iteritems():
                    if k.startswith('asset') or k.startswith('shot'):
                        setattr(newItem, k, v)
        return newItem


class PopulateLineTestTrees(object):
    """ Populate LineTest tab Trees QTreeWidget
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm

    def populateSteps(self, treeType):
        """ Populate linetest steps tree
            @param treeType: (str) : 'assetTree' or 'shotTree' """
        if treeType == 'assetTree':
            steps = self.pm.projectAssetSteps['stepOrder']
        else:
            steps = self.pm.projectShotSteps['stepOrder']
        for step in steps:
            newItem = self.newStepItem(step)
            self.mainUi.twLtSteps.addTopLevelItem(newItem)

    def populateLineTest(self, item, step):
        """ Populate linetest steps tree """
        if os.path.exists(item._dataLtFile):
            fileParams = self.pm.readFile(item._dataLtFile)
            ltList = fileParams['lt_%s' % step.stepName]
            for lt in ltList:
                newItem, newWidget = self.newLineTestItem(**lt)
                self.mainUi.twLineTest.insertTopLevelItems(0, [newItem])
                self.mainUi.twLineTest.setItemWidget(newItem, 0, newWidget)

    @staticmethod
    def newStepItem(step):
        """ Create new lineTest step QTreeWidgetItem
            @param step: (str) : Step Name
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, step)
        newItem.stepName = step
        return newItem

    @staticmethod
    def newLineTestItem(**kwargs):
        """ Create new lineTest item QTreeWidgetItem
            @param kwargs: (dict) : LineTest params
                                    template.DefaultTemplete().lineTestAttr(**kwargs)
            @return: (object): New QTreeWidgetItem, (object) : New QWidget """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setBackground(0, QtGui.QBrush(QtGui.QColor("Tomato")))
        newLt = LineTestWidget()
        newLt.leLtTitle.setText(kwargs['ltTitle'])
        newLt.lLtUserValue.setText(kwargs['ltUser'])
        newDate = QtCore.QDate(int(kwargs['ltDate'].split('/')[0]),
                               int(kwargs['ltDate'].split('/')[1]),
                               int(kwargs['ltDate'].split('/')[2]))
        newTime = QtCore.QTime(int(kwargs['ltTime'].split(':')[0]),
                               int(kwargs['ltTime'].split(':')[1]),
                               int(kwargs['ltTime'].split(':')[2]))
        newLt.dtLtDate.setDateTime(QtCore.QDateTime(newDate, newTime))
        return newItem, newLt
