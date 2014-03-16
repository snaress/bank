import os
from functools import partial
from PyQt4 import QtGui, QtCore
from lib.qt.scripts import dialog
from tools.apps import prodManager
from lib.qt.scripts import procQt as pQt
from tools.apps.prodManager.scripts import sats as pmSats
from tools.apps.prodManager.scripts import template as pmTemplate


class MenuActions(object):
    """ Class used by the ProdManagerUi for menu actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.defaulTemplate = pmTemplate.DefaultTemplate()

    #========================================== PROJECT ==========================================#

    def newProject(self):
        """ Launch new project dialog """
        self.newProjectUi = pmSats.NewProjectUi(self.mainUi)
        self.newProjectUi.exec_()

    def loadProject(self):
        """ Launch load project dialog """
        self.loadProjectUi = pmSats.LoadProjectUi(self.mainUi)
        self.loadProjectUi.exec_()

    def closeProject(self):
        """ Close project """
        print "Close project: %s (%s)" % (self.pm.projectName, self.pm.projectAlias)
        self.pm._reset()
        self.mainUi.windowInit()

    #======================================= PROJECT TAB =========================================#

    def on_deleteProjectNode(self, treeWidgetType):
        """ Delete given tree node
            @param treeWidgetType: (str) : 'tree' or 'step' """
        twTree = self.mainUi.getTreeObjFromTreeWidgetType(treeWidgetType)
        selItems = twTree.selectedItems()
        for item in selItems:
            if item.parent() is None:
                ind = twTree.indexOfTopLevelItem(item)
                twTree.takeTopLevelItem(ind)
            else:
                ind = item.parent().indexOfChild(item)
                item.parent().takeChild(ind)

    #========== Project Tree ==========#

    def on_newProjectTreeItem(self, itemType):
        """ Command launch when project QTreeWidget popupMenu node creation action is clicked
            @param itemType: (str) : 'assetFld' or 'asset' or 'shotFld' or 'shot' """
        selItems = self.mainUi.twProjectTree.selectedItems()
        if not selItems and itemType in ['asset', 'shot']:
            warn = "!!! Warning: Select folder to parent new nodes !!!"
            self.warnDial0 = dialog.ConfirmDialog(warn, btns=['Ok'], cmds=[self.on_dialAccept0])
            self.warnDial0.exec_()
        else:
            mess = self._getDialMessage(itemType)
            if selItems:
                mess.append("New node's parent: %s" % selItems[0].nodePath)
            else:
                mess.append("New node's parent: world")
            self.newProjectTreeDial = dialog.PromptDialog('\n'.join(mess),
                                      partial(self.newProjectTreeItem, itemType),
                                      self.newProjectTreeCancel)
            self.newProjectTreeDial.show()

    def _getDialMessage(self, itemType):
        """ Get dialog message
            @param itemType: (str) : 'assetFld' or 'asset' or 'shotFld' or 'shot'
            @return: (list) : Message """
        mess = []
        if itemType == 'assetFld':
            mess = ["Enter new asset folder name,", "Don't use special caracter or space."]
        elif itemType == 'asset':
            mess = ["Enter new asset name,", "Don't use special caracter or space."]
        elif itemType == 'shotFld':
            mess = ["Enter new shot folder name,", "Don't use special caracter or space."]
        elif itemType == 'shot':
            mess = ["Enter new shot name,", "Don't use special caracter or space."]
        return mess

    def on_dialAccept0(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.warnDial0.close()

    def newProjectTreeItem(self, itemType):
        """ Command launch when 'Ok' of confirmDialog is clicked
            @param itemType: (str) : 'assetFld' or 'asset' or 'shotFld' or 'shot' """
        newNode = str(self.newProjectTreeDial.leUserValue.text())
        selItems = self.mainUi.twProjectTree.selectedItems()
        checkNewNode, newNodePath = self._getProjectTreePath(selItems, newNode)
        populateTrees = pmSats.PopulateProjectTrees(self.mainUi)
        if checkNewNode:
            if itemType == 'shot':
                nodeName = '%s_%s' % (selItems[0].nodeLabel, newNode)
            else:
                nodeName = newNode
            params = self.defaulTemplate.projectTreeNodeAttr(itemType, newNode, nodeName, newNodePath)
            newItem = populateTrees.newTreeItem(**params)
            if selItems:
                selItems[0].addChild(newItem)
            else:
                self.mainUi.twProjectTree.addTopLevelItem(newItem)
            self.newProjectTreeDial.close()
        else:
            warn = "!!! Warning !!!\n%s\nalready exists" % newNodePath
            self.warnDial1 = dialog.ConfirmDialog(warn, btns=['Ok'], cmds=[self.on_dialAccept1])
            self.warnDial1.exec_()

    def _getProjectTreePath(self, selItems, newNode):
        """ Get parent item params
            @param selItems: (list) : Selected QTreeWidgetItem
            @param newNode: (str) : New item name
            @return: (bool) : NewName valide, (str) : node path """
        if selItems:
            nodePath = '%s/%s' % (selItems[0].nodePath, newNode)
        else:
            nodePath = newNode
        allItems = pQt.getAllItems(self.mainUi.twProjectTree)
        check = True
        for item in allItems:
            if item.nodePath == nodePath:
                check = False
        return check, nodePath

    def on_dialAccept1(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.warnDial1.close()

    def newProjectTreeCancel(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.newProjectTreeDial.close()

    def on_newProjectTreeItems(self, itemType):
        """ Command launch when project QTreeWidget popupMenu node creation action list is clicked
            @param itemType: (str) : 'shotFld' or 'shot' """
        mess = []
        if itemType == 'shotFld':
            mess = ["Enter new shot folder prefixe and suffixe,", "Don't use special caracter or space."]
        elif itemType == 'shot':
            mess = ["Enter new shot prefixe and suffixe,", "Don't use special caracter or space."]
        selItems = self.mainUi.twProjectTree.selectedItems()
        if not selItems and itemType == 'shot':
            warn = "!!! Warning: Select a shot folder to parent new nodes !!!"
            self.warnDial2 = dialog.ConfirmDialog(warn, btns=['Ok'], cmds=[self.on_dialAccept2])
            self.warnDial2.exec_()
        else:
            if selItems:
                mess.append("New node's parent: %s" % selItems[0].nodePath)
            else:
                mess.append("New node's parent: world")
            self.editProjectTreeUi = pmSats.EditProjectTreeUi(self.mainUi, '\n'.join(mess), itemType)
            self.editProjectTreeUi.exec_()

    def on_dialAccept2(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.warnDial2.close()

    #========== Project Step ==========#

    def on_newProjectStepItem(self, stepType):
        """ Command launch when project QTreeWidget popupMenu step creation action is clicked
            @param stepType: (str) : 'step' or 'substep' """
        mess = []
        if stepType == 'step':
            mess = ["Enter new step name,", "Don't use special caracter or space."]
        elif stepType == 'substep':
            mess = ["Enter new substep name,", "Don't use special caracter or space."]
        selItems = self.mainUi.twProjectStep.selectedItems()
        if not selItems and stepType == 'substep':
            warn = "!!! Warning: Select a step item to parent new substep !!!"
            self.warnDial3 = dialog.ConfirmDialog(warn, btns=['Ok'], cmds=[self.on_dialAccept3])
            self.warnDial3.exec_()
        else:
            if stepType == 'substep':
                mess.append("New substep's parent: %s" % selItems[0].stepLabel)
            else:
                mess.append("New substep's parent: world")
            self.newProjectStepDial = dialog.PromptDialog('\n'.join(mess),
                                      partial(self.newProjectStepItem, stepType),
                                      self.newProjectStepDialCancel)
            self.newProjectStepDial.show()

    def on_dialAccept3(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.warnDial3.close()

    def newProjectStepItem(self, stepType):
        """ Command launch when 'Ok' of promptDialog is clicked
            @param stepType: (str) : 'step' or 'substep' """
        newStepNode = str(self.newProjectStepDial.leUserValue.text())
        check, parentNode, stepPath = self._checkNewStep(newStepNode, stepType)
        populateProjectTrees = pmSats.PopulateProjectTrees(self.mainUi)
        if check:
            if parentNode is None:
                params = self.defaulTemplate.projectStepNodeAttr(stepType, newStepNode, None)
                newItem = populateProjectTrees.newStepItem(**params)
                self.mainUi.twProjectStep.addTopLevelItem(newItem)
            else:
                params = self.defaulTemplate.projectStepNodeAttr(stepType, newStepNode, parentNode.stepLabel)
                newItem = populateProjectTrees.newStepItem(**params)
                parentNode.addChild(newItem)
            self.newProjectStepDial.close()
        else:
            warn = "!!! Error: Step or substep already exists (%s) !!!" % stepPath
            self.warnDial4 = dialog.ConfirmDialog(warn, btns=['Ok'], cmds=[self.on_dialAccept4])
            self.warnDial4.exec_()

    def _checkNewStep(self, newStepNode, stepType):
        """ Check if new step name is valid
            @param newStepNode: (str) : New step name
            @param stepType: (str) : 'step' or 'substep'
            @return: (bool) : Check, (object) : parentNode, (str) : stepPath """
        if stepType == 'step':
            parentNode = None
            stepPath = newStepNode
        else:
            selItems = self.mainUi.twProjectStep.selectedItems()
            parentNode = selItems[0]
            stepPath = '%s/%s' % (parentNode.stepLabel, newStepNode)
        allItems = pQt.getAllItems(self.mainUi.twProjectStep)
        for item in allItems:
            if item.stepPath == stepPath:
                return False, parentNode, stepPath
        return True, parentNode, stepPath

    def on_dialAccept4(self):
        """ Command launch when Qbutton 'Ok' of dialog is clicked """
        self.warnDial4.close()

    def newProjectStepDialCancel(self):
        """ Command launch when 'Cancel' of promptDialog is clicked """
        self.newProjectStepDial.close()

    #=========================================== HELP ============================================#

    def helpTreeObj(self, treeType):
        """ Print given tree objext
            @param treeType: (str) : 'assetTree' or 'shotTree' """
        if treeType == 'assetTree':
            self.pm.assetTreeObj.printTree()
        else:
            self.pm.shotTreeObj.printTree()

    def helptPreviewAttr(self):
        """ Print preview QLabel attributes """
        previewDict = self.mainUi._getPreviewAttr
        print "#" * 60
        print "#-- Preview Image Attributes --#"
        for k, v in previewDict.iteritems():
            print "%s = %s" % (k, v)
        print "#" * 60


class UiActions(object):
    """ Class used by the ProdManagerUi for updates and actions
        @param mainUi: (object) : ProdManager QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.defaultTemplate = pmTemplate.DefaultTemplate()

    #========================================== MAIN UI ==========================================#

    def initMainUi(self):
        """ Initialize main ui """
        self.mainUi.setGeometry(QtCore.QRect(100, 50, 1200, 800))
        self.mainUi.setWindowTitle("ProdManager: Untitled")
        self.rf_previewIma(prodManager.imaList['prodManager.png'])
        self.rf_mainTree()
        self.mainUi.tabProdManager.setCurrentIndex(0)

    def rf_maiUi(self):
        """ Refresh mainUi global widgets """
        self.rf_mainTree()

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

    def rf_mainTree(self):
        """ Refresh main ui tree from classObject """
        self.mainUi.twProject.clear()
        populate = pmSats.PopulateProjectTrees(self.mainUi)
        if self.mainUi.rbMainAsset.isChecked():
            populate.populateMain('assetTree')
        else:
            populate.populateMain('shotTree')

    #======================================== PROJECT TAB ========================================#

    def initProjectTab(self):
        """ Initialize project tab """
        self.mainUi.qfProject.setVisible(False)
        self.mainUi.lProject.setText('')
        self.mainUi.deProjectStart.setDisplayFormat("yyyy/MM/dd")
        self.mainUi.deProjectEnd.setDisplayFormat("yyyy/MM/dd")
        self.mainUi.qfProjectTree.setVisible(False)
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
        #-- Init Project Tree --#
        self.mainUi.bProjectTreeUp.setEnabled(state)
        self.mainUi.bProjectTreeDn.setEnabled(state)
        self.mainUi.bProjectStepUp.setEnabled(state)
        self.mainUi.bProjectStepDn.setEnabled(state)

    def rf_projectTab(self):
        """ Refresh project tab """
        self.mainUi.setWindowTitle("ProdManager: %s--%s" % (self.pm.projectName, self.pm.projectAlias))
        #-- Refresh Project Label --#
        self.mainUi.qfProject.setVisible(True)
        self.mainUi.lProject.setText('%s (%s)' % (self.pm.projectName, self.pm.projectAlias))
        #-- Refresh Project Date --#
        self.mainUi.deProjectStart.setDate(QtCore.QDate(int(self.pm.projectStart.split('/')[0]),
                                                        int(self.pm.projectStart.split('/')[1]),
                                                        int(self.pm.projectStart.split('/')[2])))
        self.mainUi.deProjectEnd.setDate(QtCore.QDate(int(self.pm.projectEnd.split('/')[0]),
                                                      int(self.pm.projectEnd.split('/')[1]),
                                                      int(self.pm.projectEnd.split('/')[2])))
        #-- Refresh Project Work Directory --#
        self.mainUi.leProjectWorkDir.setText(self.pm.projectWorkDir)

    def on_editProjectTab(self):
        """ Command launch when bEditProjectTab is clicked """
        checkState = self.mainUi.bEditProjectTab.isChecked()
        if checkState:
            self.mainUi.bEditProjectTab.setText("Save")
        else:
            self.mainUi.bEditProjectTab.setText("Edit")
            self.ud_projectTabParams()
            if self.mainUi.cbProjectTree.isChecked():
                self.pm.buildTreeFromUi(self.mainUi)
                self.pm.buildStepFromUi(self.mainUi)
                if self.mainUi.rbProjectAsset.isChecked():
                    self.pm.writeTree('assetTree')
                else:
                    self.pm.writeTree('shotTree')
            self.pm.writeProjectFile()
            self.rf_mainTree()
        self.rf_projectTabVis(state=checkState)

    def on_cancelProjectTab(self):
        """ Command launch when bCancelProjectTab is clicked """
        self.mainUi.bEditProjectTab.setText("Edit")
        self.mainUi.bEditProjectTab.setChecked(False)
        self.rf_projectTab()
        self.rf_projectTabVis()

    def ud_projectTabParams(self):
        """ Update ProdManager instance """
        self.pm.projectStart = str(self.mainUi.deProjectStart.text())
        self.pm.projectEnd = str(self.mainUi.deProjectEnd.text())
        self.pm.projectWorkDir = str(self.mainUi.leProjectWorkDir.text())

    def on_openProjectWorkDir(self):
        """ Command launch when bOpenProjectWorkDir is clicked """
        if self.pm.projectWorkDir == '':
            root = os.path.join('F:', os.sep)
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

    def on_projectTree(self):
        """ Command launch when cbProjectTree is clicked """
        if self.mainUi.cbProjectTree.isChecked():
            self.mainUi.qfProjectTree.setVisible(True)
            self.rf_projectTree()
        else:
            self.mainUi.qfProjectTree.setVisible(False)

    def rf_projectTree(self):
        """ Refresh project tree from classObject """
        self.mainUi.twProjectTree.clear()
        self.mainUi.twProjectStep.clear()
        populate = pmSats.PopulateProjectTrees(self.mainUi)
        if self.mainUi.rbProjectAsset.isChecked():
            populate.populateTree('assetTree', self.mainUi.twProjectTree)
            populate.populateStep('assetTree')
        else:
            populate.populateTree('shotTree', self.mainUi.twProjectTree)
            populate.populateStep('shotTree')

    def on_rfProjectTree(self):
        """ Refresh prodManager class and ui class """
        self.pm.buildTrees(force=True)
        self.pm.buildSteps()
        self.rf_projectTree()

    def moveProjectNode(self, direction, treeWidgetType):
        """ Move Project tree or Project step node
            @param direction: (str) : 'up' or 'down'
            @param treeWidgetType: (str) : 'tree' or 'step' """
        twTree = self.mainUi.getTreeObjFromTreeWidgetType(treeWidgetType)
        selItems = twTree.selectedItems()
        if selItems:
            item = selItems[0]
            #-- Move QTreeWidgetItem --#
            if item.parent() is None:
                movedItem = self._moveTopItem(treeWidgetType, item, direction)
            else:
                movedItem = self._moveChildItem(item, direction)
            #-- Reselect QTreeWidgetItem --#
            if movedItem is not None:
                twTree.setCurrentItem(movedItem)

    def _moveTopItem(self, treeWidgetType, item, direction):
        """ Move top level item
            @param treeWidgetType: (str) : 'tree' or 'step'
            @param item: (object) :  QTreeWidgetItem
            @param direction: (str) : 'up' or 'down'
            @return: (object) : Moved QTreeWidgetItem """
        twTree = self.mainUi.getTreeObjFromTreeWidgetType(treeWidgetType)
        movedItem = None
        ind = twTree.indexOfTopLevelItem(item)
        if direction == 'up':
            if ind > 0:
                movedItem = twTree.takeTopLevelItem(ind)
                twTree.insertTopLevelItem(ind-1, movedItem)
        elif direction == 'down':
            N = twTree.topLevelItemCount()
            if ind < N-1:
                movedItem = twTree.takeTopLevelItem(ind)
                twTree.insertTopLevelItem(ind+1, movedItem)
        return movedItem

    @staticmethod
    def _moveChildItem(item, direction):
        """ Move child item
            @param item: (object) : QTreeWidgetItem
            @param direction: (str) : 'up' or 'down'
            @return: (object) : Moved QTreeWidgetItem """
        movedItem = None
        parent = item.parent()
        ind = parent.indexOfChild(item)
        if direction == 'up':
            if ind > 0:
                movedItem = parent.takeChild(ind)
                parent.insertChild(ind-1, movedItem)
        elif direction == 'down':
            N = parent.childCount()
            if ind < N-1:
                movedItem = parent.takeChild(ind)
                parent.insertChild(ind+1, movedItem)
        return movedItem

    #========================================= SHOT INFO =========================================#

    def initShotInfoTab(self):
        """ Initialize Shot Info tab """
        self.mainUi.lShotNodeLabel.setText('')
        self.mainUi.qfShotType.setVisible(False)
        self.mainUi.qfAssetType.setVisible(False)
        self.rf_shotInfoTabVis()

    def rf_shotInfoTabVis(self, state=False):
        """ Refresh shot info tab ui visibility
            @param state: (bool) : Visibility state """
        #-- Init Project Label --#
        self.mainUi.bCancelShotInfoTab.setVisible(state)
        #-- Init Shot Info --#
        self.mainUi.leShotWorkDir.setEnabled(state)
        self.mainUi.bOpenShotWorkDir.setEnabled(state)
        self.mainUi.sbShotIn.setEnabled(state)
        self.mainUi.sbShotOut.setEnabled(state)
        self.mainUi.sbShotFrames.setEnabled(False)
        self.mainUi.sbShotHandleIn.setEnabled(state)
        self.mainUi.sbShotHandleOut.setEnabled(state)
        self.mainUi.sbShotFocal.setEnabled(state)

    def rf_shotInfoTab(self):
        """ Refresh Shot Info tab from classObject """
        selItems = self.mainUi.twProject.selectedItems()
        if not selItems:
            self.initShotInfoTab()
        else:
            item = selItems[0]
            checkState = self.mainUi.rbMainAsset.isChecked()
            self.mainUi.qfAssetType.setVisible(checkState)
            self.mainUi.qfShotType.setVisible(not checkState)
            if not item.nodeType in ['asset', 'shot']:
                self.initShotInfoTab()
            else:
                self.mainUi.lShotNodeLabel.setText(item.nodeName)
                if checkState:
                    self.rf_defaultAssetParams(item)
                else:
                    self.rf_defaultShotParams(item)

    def rf_defaultAssetParams(self, item):
        """ Refresh default asset attributes
            @param item: (object) : Selected main QTreeWidgetItem """
        self.mainUi.lAssetNodeTypeVal.setText(item.nodeType)
        self.mainUi.lAssetNameVal.setText(item.nodeName)
        self.mainUi.lAssetTypeVal.setText('/'.join(item.nodePath.split('/')[:-1]))

    def rf_defaultShotParams(self, item):
        """ Refresh default shot attributes
            @param item: (object) : Selected main QTreeWidgetItem """
        self.mainUi.lShotNodeTypeVal.setText(item.nodeType)
        self.mainUi.lShotSeqVal.setText(item.nodePath.split('/')[-2])
        self.mainUi.lShotShotVal.setText(item.nodeLabel)
        self.mainUi.lShotNameVal.setText(item.nodeName)

    def on_editShotInfoTab(self):
        """ Command launch when bEditShotInfoTab is clicked """
        checkState = self.mainUi.bEditShotInfoTab.isChecked()
        if checkState:
            self.mainUi.bEditShotInfoTab.setText("Save")
        else:
            self.mainUi.bEditShotInfoTab.setText("Edit")
            selItems = self.mainUi.twProject.selectedItems()
            if selItems:
                if self.mainUi.rbMainAsset.isChecked():
                    self.pm.assetTreeObj.writeNode(selItems[0].nodeName)
                else:
                    self.pm.shotTreeObj.writeNode(selItems[0].nodeName)
        self.rf_shotInfoTabVis(state=checkState)

    def on_cancelShotInfoTab(self):
        """ Command launch when bCancelShotInfoTab is clicked """
        selItems = self.mainUi.twProject.selectedItems()
        if selItems:
            self.mainUi.bEditShotInfoTab.setText("Edit")
            self.mainUi.bEditShotInfoTab.setChecked(False)
        self.rf_shotInfoTabVis()

# def _getShotNodeParams(self, item):
#     """ Get node params from given QTreeWidgetItem
#         @param item: (object) : Selected Main QTreeWidgetItem
#         @return: (dict) : Node params """
#     if not os.path.exists(item._dataFile):
#         nodeParams = self.defaultTemplate.shotNodeAttr('', 0, 0, 0, 0, 0)
#     else:
#         nodeParams = self.pm.readFile(item._dataFile)
#     return nodeParams