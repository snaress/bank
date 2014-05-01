import os
from PyQt4 import QtGui, uic
from functools import partial
from appli import prodManager
from lib.qt.scripts import dialog
from lib.qt.scripts import procQt as pQt
from appli.prodManager.scripts import uiRefresh as pmRefresh
from appli.prodManager.scripts import template as pmTemplate


newProjectClass, newProjectUiClass = uic.loadUiType(prodManager.uiList['newProject'])
class NewProjectUi(newProjectClass, newProjectUiClass):
    """ New Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow"""

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
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
            result, mess = self.pm.newProject(project, alias)
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


editProjectTreeItemClass, editProjectTreeItemUiClass = uic.loadUiType(prodManager.uiList['newTreeItem'])
class EditProjectTreeItem(editProjectTreeItemClass, editProjectTreeItemUiClass):
    """ Load Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow
        @param itemType: (str) : 'container' or 'node' """

    def __init__(self, mainUi, itemType):
        self.mainUi = mainUi
        self.itemType = itemType
        super(EditProjectTreeItem, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup editProjectTreeItem dialog """
        self.setupUi(self)
        self.bCreate.clicked.connect(self.on_create)
        self.bCancel.clicked.connect(self.close)

    def on_create(self):
        """ Command launch when Qbutton 'Create' is clicked """
        name = str(self.leItemName.text())
        label = str(self.leItemLabel.text())
        if not name == '' and not label == '':
            self.mainUi.uiCmds_menu.newProjectTreeItem(self.itemType, itemName=name, itemLabel=label)
        else:
            mess = "!!! Warning: Both name and label should be edited !!!"
            self.confUi = dialog.ConfirmDialog(mess, btns=['Ok'], cmds=[self.on_dialogAccept])
            self.confUi.exec_()

    def on_dialogAccept(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.confUi.close()


editProjectTreeClass, editProjectTreeUiClass = uic.loadUiType(prodManager.uiList['editProjectTree'])
class EditProjectTreeUi(editProjectTreeClass, editProjectTreeUiClass):
    """ Load Project dialog setup class
        @param mainUi: (object) : ProdManager QMainWindow
        @param mess: (str) : Information text
        @param itemType: (str) : 'container' or 'node' """

    def __init__(self, mainUi, mess, itemType):
        self.mainUi = mainUi
        self.mess = mess
        self.itemType = itemType
        self.defaultTemplate = pmTemplate.DefaultTemplate()
        super(EditProjectTreeUi, self).__init__()
        self._setupUi()
        if self.itemType == 'node':
            self.rf_shotPrefix()

    def _setupUi(self):
        """ Setup Load Project dialog """
        self.setupUi(self)
        self.lMessage.setText(self.mess)
        if self.itemType == 'container':
            self.lShotPrefix.setVisible(False)
            self.leShotPrefix.setVisible(False)
        else:
            self.lShotPrefix.setVisible(True)
            self.leShotPrefix.setVisible(True)
        self.bCreate.clicked.connect(self.on_create)
        self.bCancel.clicked.connect(self.close)

    def on_create(self):
        """ Command launch when Qbutton 'Create' of tree editor is clicked """
        nodeList = self._getNodeList(**self._getListParams)
        check, nodeList = self._checkNodeList(nodeList)
        mess, btns = self._getDialogParams(check)
        self.confirmCreation = dialog.ConfirmDialog('\n'.join(mess), btns=btns,
                               cmds=[partial(self.on_confirmCreation, nodeList, check['success']),
                                     self.on_cancelCreationConfirmation])
        self.confirmCreation.exec_()

    def on_confirmCreation(self, nodeList, valideNodePath):
        """ Command launch when Qbutton 'Create' or 'Skip Existing' of dialog is clicked
            @param nodeList: (dict) :  Node list
            @param valideNodePath: (list) : Valid node path list """
        populate = pmRefresh.PopulateTrees(self.mainUi)
        valideNodePath.sort()
        #-- Add New Item --#
        for nodePath in valideNodePath:
            for node in nodeList:
                if nodePath == nodeList[node]['nodePath']:
                    nodeParent = self._getNodeParent(nodePath)
                    params = self.defaultTemplate.projectTreeNodeAttr(nodeList[node]['nodeType'],
                                                                      nodeList[node]['nodeLabel'],
                                                                      nodeList[node]['nodeName'],
                                                                      nodeList[node]['nodePath'])
                    newItem = populate.newProjectTreeItem(**params)
                    if nodeParent is None:
                        self.mainUi.twProjectTree.addTopLevelItem(newItem)
                    else:
                        parent = self.mainUi.getParentItemFromNodePath(self.mainUi.twProjectTree,
                                                                       nodeList[node]['nodePath'])
                        parent.addChild(newItem)
        #-- Updates --#
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        self.mainUi.uiRf_projectTab.ud_projectTreesItem(selTrees[0])
        self.confirmCreation.close()
        self.close()

    def on_cancelCreationConfirmation(self):
        """ Command launch when Qbutton 'Cancel' of dialog is clicked """
        self.confirmCreation.close()

    def rf_shotPrefix(self):
        """ Refresh shot prefix """
        selItems = self.mainUi.twProjectTree.selectedItems()
        self.leShotPrefix.setText('%s_' % selItems[0].nodeLabel)

    @property
    def _getListParams(self):
        """ Get list params from ui
            @return: (dict) : Ui params """
        return {'start': int(self.sbStart.value()),
                'stop': int(self.sbStop.value()),
                'step': int(self.sbStep.value()),
                'padd': int(self.sbPadding.value()),
                'prefixe': str(self.lePrefixe.text()),
                'suffixe': str(self.leSuffixe.text()),
                'shotPrefix': str(self.leShotPrefix.text())}

    @staticmethod
    def _getNodeList(**kwargs):
        """ Get node list from params
            @param kwargs: List params from ui ---> self._getListParams
            @return: (dict) : Node name and label list """
        nodeList = {}
        for n in range(kwargs['start'], kwargs['stop']+1, kwargs['step']):
            padd = str(n).zfill(kwargs['padd'])
            nodeLabel = '%s%s%s' % (kwargs['prefixe'], padd, kwargs['suffixe'])
            nodeName = '%s%s' % (kwargs['shotPrefix'], nodeLabel)
            nodeList[nodeName] = {}
            nodeList[nodeName]['nodeLabel'] = nodeLabel
            nodeList[nodeName]['nodeName'] = nodeName
        return nodeList

    def _checkNodeList(self, nodeList):
        """ Check if new node already exists
            @param nodeList: (dict) : Node list
            @return: (dict) : Check result """
        allItems = pQt.getAllItems(self.mainUi.twProjectTree)
        selItems = self.mainUi.twProjectTree.selectedItems()
        nodePathList, nodeList = self._getNodePathList(selItems, nodeList)
        check = self._checkNodePathList(nodePathList, allItems)
        return check, nodeList

    def _getNodePathList(self, selItems, nodeList):
        """ Get node path list from selected items
            @param selItems: (list) : Selected QTreeWidgetItem
            @param nodeList: (dict) : Node list
            @return: (list) : Node path list, (dict) :  Node list """
        nodePathList = []
        if selItems:
            for selItem in selItems:
                for node in nodeList.keys():
                    nodePath = '%s/%s' % (selItem.nodePath, nodeList[node]['nodeLabel'])
                    nodeList[node]['nodePath'] = nodePath
                    nodeList[node]['nodeType'] = self._getNodeType
                    nodePathList.append(nodePath)
        else:
            for node in nodeList.keys():
                nodeList[node]['nodePath'] = nodeList[node]['nodeLabel']
                nodeList[node]['nodeType'] = self._getNodeType
                nodePathList.append(nodeList[node]['nodeLabel'])
        return nodePathList, nodeList

    @property
    def _getNodeType(self):
        """ Get nodeType
            @return: (str) : Node type """
        selTrees = self.mainUi.twProjectTrees.selectedItems()
        treeName = selTrees[0].treeName
        if self.itemType == 'container':
            nodeType = '%sCtnr' % treeName
        else:
            nodeType = treeName
        return nodeType

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

    def _getNodeParent(self, nodePath):
        """ Get node params
            @param nodePath: (str) : Given node path
            @return: (str) : NodeLabel, (str) : NodeName, (str) : NodeParent """
        if '/' in nodePath:
            nodeParent = nodePath.split('/')[-2]
        else:
            nodeParent = None
        return nodeParent


shotNodeClass, shotNodeUiClass = uic.loadUiType(prodManager.uiList['shotNode'])
class ShotNodeWidget(shotNodeClass, shotNodeUiClass):
    """ ShotInfo tab tree widget
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi, **kwargs):
        self.mainUi = mainUi
        self.params = kwargs
        self.pm = self.mainUi.pm
        super(ShotNodeWidget, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.lNameVal.setText(self.params['nodeName'])
        self.lTypeVal.setText(self.params['nodeType'])
        self.lPathVal.setText(self.params['nodePath'])
