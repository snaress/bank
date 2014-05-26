import os
import time
import shutil
from functools import partial
from appli import prodManager
from lib.qt.scripts import dialog
from PyQt4 import QtGui, QtCore, uic
from lib.qt.scripts import textEditor
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import procFile as pFile
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
        self.defaultTemplate = pmTemplate.DefaultTemplate
        super(ShotNodeWidget, self).__init__()
        self._setupUi()
        self.rf_prevIma()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.lNameVal.setText(self.params['nodeName'])
        self.lTypeVal.setText(self.params['nodeType'])
        self.lPathVal.setText(self.params['nodePath'])

    def rf_prevIma(self):
        """ Refresh widget prevIma """
        ima = self.getPrevIma()
        if ima is not None:
            maxWidth, maxHeight = self.defaultTemplate.shotInfoPreviewMaxSize()
            self.prevIma = QtGui.QPixmap(ima)
            self.lPreview.setPixmap(self.prevIma)
            self.prevIma.scaled(maxWidth, maxHeight, QtCore.Qt.IgnoreAspectRatio)
            self.mainUi.resizePixmap(maxWidth, maxHeight, self.prevIma, self.lPreview)

    def getPrevIma(self):
        """ Get shotInfo prevIma absolut path
            @return: (str) : shotInfo prevIma absolut path """
        node = self.pm.getNodeFromNodePath(self.params['nodeType'], self.params['nodePath'])
        ima  = prodManager.imaList['prodManager.png']
        if node is not None:
            preview = os.path.join(node.dataPath, 'prevIma.png')
            if not 'prevIma' in node.params:
                if os.path.exists(preview):
                    ima = preview
            else:
                if not node.params['prevIma'] in ['', ' ']:
                    if os.path.exists(preview):
                        ima = preview
        return ima

    def ud_prevIma(self):
        """ Update shot preview imageFile """
        node = self.pm.getNodeFromNodePath(self.params['nodeType'], self.params['nodePath'])
        if node is not None:
            if hasattr(node, 'params'):
                if 'prevIma' in node.params:
                    if not node.params['prevIma'] in ['', ' ']:
                        preview = os.path.join(node.dataPath, 'prevIma.png')
                        maxWidth, maxHeight = self.defaultTemplate.previewMaxSize()
                        self.tmpIma = QtGui.QPixmap(node.params['prevIma'])
                        self.tmpIma.scaled(maxWidth, maxHeight, QtCore.Qt.IgnoreAspectRatio)
                        img = self.tmpIma.toImage().scaled(maxWidth, maxHeight,
                                                           QtCore.Qt.KeepAspectRatio)
                        try:
                            img.save(preview, 'png')
                            print "Saving preview image: %s" % preview
                        except:
                            print "ERROR: Can't save preview image: %s" % preview

    def saveIma(self):
        """ Save preview image """
        node = self.pm.getNodeFromNodePath(self.params['nodeType'], self.params['nodePath'])
        preview = os.path.join(node.dataPath, 'prevIma.png')
        maxWidth, maxHeight = self.defaultTemplate.previewMaxSize()
        img = self.prevIma.toImage().scaled(maxWidth, maxHeight, QtCore.Qt.KeepAspectRatio)
        try:
            img.save(preview, 'png', 100)
            print "Saving preview image: %s" % preview
        except:
            print "ERROR: Can't save preview image: %s" % preview


shotParamFileClass, shotParamFileUiClass = uic.loadUiType(prodManager.uiList['shotParamFile'])
class ShotParamFileWidget(shotParamFileClass, shotParamFileUiClass):
    """ ShotParamFile tree widget
        @param mainUi: (object) : ProdManager QMainWindow
        @param paramType: (str) : Param type ('file', 'dir', 'string', 'int', 'float', 'bool')
        @param value: (str) : Param value """

    def __init__(self, mainUi, paramType, value):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.paramType = paramType
        self.value = value
        super(ShotParamFileWidget, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.paramVal.setText(self.value)
        self.paramVal.setReadOnly(True)
        self.bOpen.setVisible(False)
        self.bOpen.clicked.connect(self.on_fileDialog)

    def on_fileDialog(self):
        """ Command launch when QPushButton 'open' is clicked """
        root = self._getRootDir
        self.fdDir = dialog.fileDialog(fdRoot=root, fdCmd=self.ud_paramVal)
        if self.paramType == 'dir':
            self.fdDir.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        elif self.paramType == 'file':
            self.fdDir.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdDir.exec_()

    @property
    def _getRootDir(self):
        """ Get selected shot fileDialog rootDir
            @return: (str) : FileDialog rootDir """
        if str(self.paramVal.text()) == '':
            if self._getWorkDir is None:
                if self.pm.project.projectWorkDir == '':
                    return prodManager.rootDisk
                else:
                    return self.pm.project.projectWorkDir
            else:
                return self._getWorkDir
        else:
            return str(self.paramVal.text())

    @property
    def _getWorkDir(self):
        """ Get selected shot work directory
            @return: (str) : Work directory """
        allItems = pQt.getTopItems(self.mainUi.twShotParams)
        for item in allItems:
            if item.paramName == 'workDir':
                workDir = str(item.widget.paramVal.text())
                if workDir in ['', ' ']:
                    return None
                else:
                    return str(item.widget.paramVal.text())
        return None

    def ud_paramVal(self):
        """ Update param value with selected path """
        selPath = self.fdDir.selectedFiles()
        if selPath:
            self.paramVal.setText(str(selPath[0]))


linetestClass, linetestUiClass = uic.loadUiType(prodManager.uiList['ltNode'])
class LineTestWidget(linetestClass, linetestUiClass):
    """ Linetest tree widget
        @param mainUi: (object) : ProdManager QMainWindow
        @param treeItem: (object) : Linetest QTreeWidgetItem
        @param kwargs: (dict) : New linetest params
            @keyword ltTitle: (str) : Linetest title
            @keyword ltUser: (str) : Linetest author
            @keyword ltDate: (str) : Linetest creation date
            @keyword ltTime : (str) : Linetest creation time
            @keyword ltIma : (str) : Linetest preview image
            @keyword ltSeq : (str) : Linetest sequence player
            @keyword ltMov : (str) : Linetest movie
            @keyword ltComments: (list) : Linetest comments (html) """

    def __init__(self, mainUi, treeItem, **kwargs):
        self.mainUi = mainUi
        self.ltItem = treeItem
        self.params = kwargs
        self.populate = pmRefresh.PopulateTrees(self.mainUi)
        super(LineTestWidget, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.leLtTitle.setText(self.params['ltTitle'])
        self.leLtTitle.setReadOnly(True)
        self.lLtUser.setText(self.params['ltUser'])
        self.dtLtDate.setDate(QtCore.QDate(int(self.params['ltDate'].split('_')[0]),
                                           int(self.params['ltDate'].split('_')[1]),
                                           int(self.params['ltDate'].split('_')[2])))
        self.dtLtDate.setReadOnly(True)
        self.dtLtTime.setTime(QtCore.QTime(int(self.params['ltTime'].split('_')[0]),
                                           int(self.params['ltTime'].split('_')[1]),
                                           int(self.params['ltTime'].split('_')[2])))
        self.dtLtTime.setReadOnly(True)
        self.bLtEdit.clicked.connect(self.on_edit)
        self.bLtAddCmt.clicked.connect(self.on_AddComment)

    def on_edit(self):
        """ Command launch when bLtEdit is clicked """
        self.ltEditor = LineTestEditor(self.ltItem, self)
        self.ltEditor.show()

    def on_AddComment(self):
        """ Add comment to linetest """
        cmtDict = {'cmtUser': prodManager.user,
                   'cmtDate': time.strftime("%Y_%m_%d", time.localtime()),
                   'cmtTime': time.strftime("%H_%M_%S", time.localtime()),
                   'cmtText': "", 'cmtHtml': ""}
        self.params['ltComments'].insert(0, cmtDict)
        self.writeLtToFile()
        newItem, newWidget = self.populate.newLtCommentItem(**cmtDict)
        self.ltItem.insertChild(0, newItem)
        self.mainUi.twLinetest.setItemWidget(newItem, 0, newWidget)
        self.ltItem.setExpanded(False)
        self.ltItem.setExpanded(True)

    def rf_comments(self):
        """ Refresh Comments list """
        #-- Clear Comments --#
        for i in range(self.ltItem.childCount(), 0, -1):
            self.ltItem.takeChild(i-1)
        #-- Populate Comments --#
        for cmtDict in self.params['ltComments']:
            newItem, newWidget = self.populate.newLtCommentItem(**cmtDict)
            self.ltItem.addChild(newItem)
            self.mainUi.twLinetest.setItemWidget(newItem, 0, newWidget)

    def writeLtToFile(self):
        """ Write linetest file in the bdd """
        ltText = []
        for k, v in self.params.iteritems():
            if k.startswith('lt'):
                if isinstance(v, str):
                    ltText.extend(["%s = %r" % (k, v)])
                else:
                    ltText.extend(["%s = %s" % (k, v)])
        try:
            pFile.writeFile(self.ltItem._ltAbsPath, '\n'.join(ltText))
            print "Writing linetest file: %s" % self.ltItem._ltFile
        except:
            print "!!! ERROR : Can't write linetest file: %s" % self.ltItem._ltFile


linetestEditorClass, linetestEditorUiClass = uic.loadUiType(prodManager.uiList['ltNodeEditor'])
class LineTestEditor(linetestEditorClass, linetestEditorUiClass):
    """ Linetest tree widget editor
        @param ltItem: (object) : Parent QTreeWidgetItem
        @param ltWidget: (object) : Parent widget """

    def __init__(self, ltItem, ltWidget):
        self.ltItem = ltItem
        self.ltWidget = ltWidget
        self.mainUi = self.ltWidget.mainUi
        super(LineTestEditor, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.leTitle.setText(str(self.ltWidget.leLtTitle.text()))
        self.dtDate.setDate(QtCore.QDate(self._getDate[0], self._getDate[1], self._getDate[2]))
        self.dtTime.setTime(QtCore.QTime(self._getTime[0], self._getTime[1], self._getTime[2]))
        self.leImaPath.setText(self.ltWidget.params['ltIma'])
        self.bImaOpen.clicked.connect(partial(self.on_open, self.leImaPath))
        self.leSeqPath.setText(self.ltWidget.params['ltSeq'])
        self.bSeqOpen.clicked.connect(partial(self.on_open, self.leSeqPath))
        self.leMovPath.setText(self.ltWidget.params['ltMov'])
        self.bMovOpen.clicked.connect(partial(self.on_open, self.leMovPath))
        self.bSave.clicked.connect(self.on_save)
        self.bCancel.clicked.connect(self.close)

    def on_open(self, lineEdit):
        """ Open fileDialog for given path type
            @param lineEdit: (object) : Given QLineEdit """
        if not str(lineEdit.text()) == '':
            rootDir = str(lineEdit.text())
        else:
            rootDir = self._getRootDir
        self.fdPath = dialog.fileDialog(fdRoot=rootDir, fdCmd=partial(self.fd_accept, lineEdit))
        self.fdPath.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdPath.show()

    def fd_accept(self, lineEdit):
        """ Command launch when the fileDialog bAccept is clicked
            @param lineEdit: (object) : Given QLineEdit """
        selPath = self.fdPath.selectedFiles()
        if selPath:
            lineEdit.setText(selPath[0])
            self.fdPath.close()

    def on_save(self):
        """ Command launch when widget bSave is clicked """
        #-- Check Edited --#
        dateTimeChanged = False
        checkNewFile = False
        newLtFile = None
        if not self._getDate == self._setDate or not self._getTime == self._setTime:
            dateTimeChanged = True
            newLtFile = 'lt-%s_%02d_%02d-%02d_%02d_%02d.py' % (self._setDate[0], self._setDate[1],
                                                               self._setDate[2], self._setTime[0],
                                                               self._setTime[1], self._setTime[2])
            if not os.path.exists(os.path.join(self.ltItem._ltPath, newLtFile)):
                checkNewFile = True
        if dateTimeChanged and not checkNewFile:
            print "!!! ERROR : Linetest date and time already exists !!!"
        else:
            #-- Update LtWidget --#
            self.ltWidget.leLtTitle.setText(str(self.leTitle.text()))
            self.ltWidget.params['ltTitle'] = str(self.leTitle.text())
            if dateTimeChanged:
                self.ltWidget.dtLtDate.setDate(QtCore.QDate(self._setDate[0], self._setDate[1],
                                                            self._setDate[2]))
                self.ltWidget.params['ltDate'] = '%s_%02d_%02d' % (self._setDate[0],
                                                                   self._setDate[1],
                                                                   self._setDate[2])
                self.ltWidget.dtLtTime.setTime(QtCore.QTime(self._setTime[0], self._setTime[1],
                                                            self._setTime[2]))
                self.ltWidget.params['ltTime'] = '%02d_%02d_%02d' % (self._setTime[0],
                                                                     self._setTime[1],
                                                                     self._setTime[2])
            self.ltWidget.params['ltIma'] = str(self.leImaPath.text())
            self.ltWidget.params['ltSeq'] = str(self.leSeqPath.text())
            self.ltWidget.params['ltMov'] = str(self.leMovPath.text())
            #-- Update LtFile --#
            self.ltWidget.writeLtToFile()
            if dateTimeChanged:
                print "Rename linetest: %s ---> %s" % (self.ltItem._ltFile, newLtFile)
                shutil.move(self.ltItem._ltAbsPath, os.path.join(self.ltItem._ltPath, newLtFile))
                self.mainUi.uiRf_linetestTab.rf_ltTree()
            self.close()

    @property
    def _getDate(self):
        """ Get linetest widget date
            @return: (list) : Year, Month, Day """
        _date = self.ltWidget.dtLtDate.date()
        return [_date.year(), _date.month(), _date.day()]

    @property
    def _setDate(self):
        """ Set linetest widget date
            @return: (list) : Year, Month, Day """
        _date = self.dtDate.date()
        return [_date.year(), _date.month(), _date.day()]

    @property
    def _getTime(self):
        """ Get linetest widget time
            @return: (list) : Hour, Minute, Second """
        _time =  self.ltWidget.dtLtTime.time()
        return [_time.hour(), _time.minute(), _time.second()]

    @property
    def _setTime(self):
        """ Set linetest widget time
            @return: (list) : Hour, Minute, Second """
        _time =  self.dtTime.time()
        return [_time.hour(), _time.minute(), _time.second()]

    @property
    def _getRootDir(self):
        """ get fileDialog rootDir
            @return: (dtr) : Root directory """
        dataFile = self.ltItem._ltLink.dataFile
        params = pFile.readPyFile(dataFile, filterIn='node')
        if not params['nodeParams']['workDir'] == '':
            return params['nodeParams']['workDir']
        else:
            if hasattr(self.mainUi.pm.project, 'projectWorkDir'):
                return self.mainUi.pm.project.projectWorkDir
            else:
                return prodManager.rootDisk


ltCommentClass, ltCommentUiClass = uic.loadUiType(prodManager.uiList['ltCmtNode'])
class LtCommentWidget(ltCommentClass, ltCommentUiClass):
    """ Linetest comment tree widget
        @param mainUi: (object) : ProdManager QMainWindow
        @param cmtItem: (object) : Parent QTreeWidgetItem
        @param kwargs: (dict) : New linetest comment params
            @keyword cmtUser: (str) : Comment author
            @keyword cmtDate: (str) : Comment creation date
            @keyword cmtTime : (str) : Comment creation time
            @keyword cmtText: (str) : Comment plain text
            @keyword cmtHtml: (str) : Comment html text """

    def __init__(self, mainUi, cmtItem, **kwargs):
        self.mainUi = mainUi
        self.cmtItem = cmtItem
        self.params = kwargs
        super(LtCommentWidget, self).__init__()
        self._setupUi()
        self.rf_textEditSize()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.lCmtUser.setText(self.params['cmtUser'])
        self.dtCmtDate.setDate(QtCore.QDate(int(self.params['cmtDate'].split('_')[0]),
                                            int(self.params['cmtDate'].split('_')[1]),
                                            int(self.params['cmtDate'].split('_')[2])))
        self.dtCmtDate.setReadOnly(True)
        self.dtCmtTime.setTime(QtCore.QTime(int(self.params['cmtTime'].split('_')[0]),
                                            int(self.params['cmtTime'].split('_')[1]),
                                            int(self.params['cmtTime'].split('_')[2])))
        self.dtCmtTime.setReadOnly(True)
        self.teComment.setHtml(self.params['cmtHtml'])
        self.teComment.setReadOnly(True)
        self.bCmtEdit.clicked.connect(self.on_edit)
        self.teComment.setHtml(self.params['cmtHtml'])
        self.teComment.setReadOnly(True)

    def rf_textEditSize(self):
        """ Refresh QTextEdit size """
        if self.params['cmtText'] == '' or self.params['cmtText'] == '\n':
            self.teComment.setMaximumHeight(22)
        else:
            self.teComment.setMaximumHeight(22*len(self.params['cmtText'].split('\n')))

    def on_edit(self):
        """ Command launch when bCmtEdit is clicked """
        self.cmtEditor = LtCmtEditor(self.cmtItem, self)
        self.cmtEditor.show()


ltCmtEditorClass, ltCmtEditorUiClass = uic.loadUiType(prodManager.uiList['ltCmtNodeEditor'])
class LtCmtEditor(ltCmtEditorClass, ltCmtEditorUiClass):
    """ Linetest comment tree widget editor
        @param cmtItem: (object) : Parent QTreeWidgetItem
        @param cmtWidget: (object) : Parent widget """

    def __init__(self, cmtItem, cmtWidget):
        self.cmtItem = cmtItem
        self.cmtWidget = cmtWidget
        self.ltItem = self.cmtItem.parent()
        self.mainUi = self.cmtWidget.mainUi
        super(LtCmtEditor, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.initTextEditor()
        self.dtDate.setDate(QtCore.QDate(self._getDate[0], self._getDate[1], self._getDate[2]))
        self.dtTime.setTime(QtCore.QTime(self._getTime[0], self._getTime[1], self._getTime[2]))
        self.comment.teText.setHtml(str(self.cmtWidget.teComment.toHtml()))
        self.bSave.clicked.connect(self.on_save)
        self.bCancel.clicked.connect(self.close)

    def initTextEditor(self):
        """ Initialized text editor """
        self.comment = textEditor.TextEditorWidget()
        self.comment.bClearText.setEnabled(False)
        self.comment.bLoadFile.setEnabled(False)
        self.comment.bSaveFile.setEnabled(False)
        self.vlComment.addWidget(self.comment)
        self.vlComment.setMargin(1)

    def on_save(self):
        """ Command launch when widget bSave is clicked """
        #-- Check Edited --#
        dateTimeChanged = False
        checkNewCmt = True
        oldIndex = self._getOldIndex
        newIndex = None
        newDate = "%s_%02d_%02d" % (self._setDate[0], self._setDate[1], self._setDate[2])
        newTime = "%02d_%02d_%02d" % (self._setTime[0], self._setTime[1], self._setTime[2])
        if not self._getDate == self._setDate or not self._getTime == self._setTime:
            dateTimeChanged = True
            checkNewCmt, newIndex = self._checkNewCmt(newDate, newTime)
        if dateTimeChanged and not checkNewCmt:
            print "!!! ERROR : Linetest comment date and time already exists !!!"
        else:
            #-- Update CmtWidget --#
            self.cmtWidget.teComment.setText(str(self.comment.teText.toPlainText()))
            self.cmtWidget.teComment.setHtml(str(self.comment.teText.toHtml()))
            self.cmtWidget.params['cmtText'] = str(self.comment.teText.toPlainText())
            self.cmtWidget.params['cmtHtml'] = str(self.comment.teText.toHtml())
            if dateTimeChanged:
                self.cmtWidget.dtCmtDate.setDate(QtCore.QDate(self._setDate[0], self._setDate[1],
                                                              self._setDate[2]))
                self.cmtWidget.params['cmtDate'] = '%s_%02d_%02d' % (self._setDate[0],
                                                                     self._setDate[1],
                                                                     self._setDate[2])
                self.cmtWidget.dtCmtTime.setTime(QtCore.QTime(self._setTime[0], self._setTime[1],
                                                              self._setTime[2]))
                self.cmtWidget.params['cmtTime'] = '%02d_%02d_%02d' % (self._setTime[0],
                                                                       self._setTime[1],
                                                                       self._setTime[2])
            #-- Update LtItem --#
            self.ltItem.widget.params['ltComments'].pop(oldIndex)
            if dateTimeChanged:
                self.ltItem.widget.params['ltComments'].insert(newIndex, self.cmtWidget.params)
            else:
                self.ltItem.widget.params['ltComments'].insert(oldIndex, self.cmtWidget.params)
            #-- Update LtFile --#
            self.ltItem.widget.writeLtToFile()
            if dateTimeChanged:
                self.ltItem.widget.rf_comments()
            self.close()

    def _checkNewCmt(self, newDate, newTime):
        """ Check comment new date validity
            @param newDate: (str) : yyyy_mm_dd
            @param newTime: (dtr) : hh_mm_ss
            @return: (bool), (int) : True if new date is valide, False if not
                                     New comment index in ltCmtParams list """
        cmts = self.ltItem.widget.params['ltComments']
        for cmtDict in cmts:
            if cmtDict['cmtDate'] == newDate and cmtDict['cmtTime'] == newTime:
                return False, None, None
        dates = ['%s_%s' % (newDate, newTime)]
        for cmtDict in cmts:
            fullDate =  '%s_%s' % (cmtDict['cmtDate'], cmtDict['cmtTime'])
            _oldDate, _oldTime = self._getOldDateTime
            if not fullDate == '%s_%s' % (_oldDate, _oldTime):
                dates.append('%s_%s' % (cmtDict['cmtDate'], cmtDict['cmtTime']))
        dateList = sorted(dates, reverse=True)
        newInd = dateList.index('%s_%s' % (newDate, newTime))
        return True, newInd

    @property
    def _getOldDateTime(self):
        """ Get linetest comment current date and time
            @return: (str), (str) : Comment date (yyyy/mm/dd), Comment Time (hh/mm/ss) """
        oldDate = "%s_%02d_%02d" % (self._getDate[0], self._getDate[1], self._getDate[2])
        oldTime = "%02d_%02d_%02d" % (self._getTime[0], self._getTime[1], self._getTime[2])
        return oldDate, oldTime

    @property
    def _getOldIndex(self):
        """ Get linetest comment index in ltItem.params['ltComments']
            @return: (int) : Old index """
        oldDate, oldTime = self._getOldDateTime
        oldInd = None
        for n, cmtDict in enumerate(self.ltItem.widget.params['ltComments']):
            if cmtDict['cmtDate'] == oldDate and cmtDict['cmtTime'] == oldTime:
                oldInd = n
        return oldInd

    @property
    def _getDate(self):
        """ Get linetest widget date
            @return: (list) : Year, Month, Day """
        _date = self.cmtWidget.dtCmtDate.date()
        return [_date.year(), _date.month(), _date.day()]

    @property
    def _setDate(self):
        """ Set linetest widget date
            @return: (list) : Year, Month, Day """
        _date = self.dtDate.date()
        return [_date.year(), _date.month(), _date.day()]

    @property
    def _getTime(self):
        """ Get linetest widget time
            @return: (list) : Hour, Minute, Second """
        _time =  self.cmtWidget.dtCmtTime.time()
        return [_time.hour(), _time.minute(), _time.second()]

    @property
    def _setTime(self):
        """ Set linetest widget time
            @return: (list) : Hour, Minute, Second """
        _time =  self.dtTime.time()
        return [_time.hour(), _time.minute(), _time.second()]


ltShotClass, ltShotUiClass = uic.loadUiType(prodManager.uiList['ltShot'])
class LtShotWidget(ltShotClass, ltShotUiClass):
    """ Linetest shot widget ui class
        @param kwargs: (dict) : Linetest shot params """

    def __init__(self, mainUi, mainTreeItem, tree, **kwargs):
        self.mainUi = mainUi
        self.treeLink = mainTreeItem
        self.tree = tree
        self.params = kwargs
        super(LtShotWidget, self).__init__()
        self._setupUi()
        self.rf_imaPreview()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self.bShotName.setText(self.treeLink.nodeName)
        self.bShotName.clicked.connect(self.on_ltShot)

    def rf_imaPreview(self):
        """ Refresh preview image """
        clns = int(self.mainUi.sbLtColumns.value())
        maxWidth = int(self.tree.width() / clns)
        maxHeight = int(maxWidth / 2)
        self.pmapShot = QtGui.QPixmap(self.imaPreview)
        self.lShot.setPixmap(self.pmapShot)
        self.pmapShot.scaled(maxWidth, maxHeight, QtCore.Qt.IgnoreAspectRatio)
        self.mainUi.resizePixmap(maxWidth, maxHeight, self.pmapShot, self.lShot)
        for c in range(int(self.mainUi.sbLtColumns.value())):
            self.tree.setColumnWidth(c, maxWidth)

    def on_ltShot(self):
        """ Refresh linetest tree """
        selItems = self.mainUi.twProject.selectedItems()
        if selItems:
            selItems[0].setSelected(False)
        self.treeLink.setSelected(True)
        self.mainUi.uiRf_linetestTab.rf_ltTree()

    @property
    def imaPreview(self):
        """ Get image preview
            @return: (str) : ShotNode image preview """
        ima = prodManager.imaList['prodManager.png']
        if 'ltIma' in self.params:
            preview = self.params['ltIma']
            if not preview == '' and not preview == ' ':
                ima = preview
        return ima
