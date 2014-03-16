import os
import sys
from lib.qt.scripts import dialog
from functools import partial
from tools.apps import grapher
from PyQt4 import QtGui, QtCore, uic
from lib.system.scripts import procFile as pFile
from tools.apps.grapher.scripts import gpCmds
from tools.apps.grapher.scripts import gpCore
from tools.apps.grapher.scripts import nodeEditor


mainClass, uiClass = uic.loadUiType(grapher.uiList['grapher'])
class MainWindow(mainClass, uiClass):
    print "##### Launch Grapher #####"

    def __init__(self):
        self.style = gpCore.GrapherStyle()
        self.varSection = gpCmds.VarSection()
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.menuSection = self.ud_menuCmds
        self.editor = self.ud_nodeEditor
        self._setupGrapher()
        self._initGrapher()
        self.setGeometry(self.style.defaultWndGeometry)

    #========================================== SETUP =============================================#

    def _setupGrapher(self):
        """ Setup grapher ui """
        print "#-- Setup Grapher --#"
        self._setupMenuFile()
        self._setupMenuGraph()
        self._setupMenuExec()
        self._setupMenuPref()
        self._setupMenuHelp()
        self._setupGlobalNotes()
        self._setupGlobalVar()
        self._setupGraphZone()
        self._setupNodeEditor()

    def _setupMenuFile(self):
        """ Setup menu 'File' """
        self.miNewGraph.triggered.connect(partial(self.mi_newGraph, clearLock=True))
        self.miNewGraph.setShortcut("Ctrl+N")
        self.miLoadGraph.triggered.connect(self.mi_loadGraph)
        self.miLoadGraph.setShortcut("Ctrl+O")
        self.miSaveGraph.triggered.connect(self.mi_saveGraph)
        self.miSaveGraph.setShortcut("Ctrl+S")
        self.miSaveGraphAs.triggered.connect(self.mi_saveGraphAs)
        self.miSaveGraphAs.setShortcut("Shift+S")
        self.miQuit.triggered.connect(self.mi_quitGrapher)
        self.miQuit.setShortcut("Ctrl+Shift+W")

    def _setupMenuGraph(self):
        """ Setup menu 'Graph' """
        #-- New Node --#
        self.mibModul.triggered.connect(partial(self.on_newNode, 'modul'))
        self.mibModul.setShortcut("1")
        self.mibSysData.triggered.connect(partial(self.on_newNode, 'sysData'))
        self.mibSysData.setShortcut("2")
        self.mibCmdData.triggered.connect(partial(self.on_newNode, 'cmdData'))
        self.mibCmdData.setShortcut("3")
        self.mibPurData.triggered.connect(partial(self.on_newNode, 'purData'))
        self.mibPurData.setShortcut("4")
        self.mibLoop.triggered.connect(partial(self.on_newNode, 'loop'))
        self.mibLoop.setShortcut("5")
        #-- Rename Node --#
        self.mibRename.triggered.connect(self.on_rename)
        self.mibRename.setShortcut("F2")
        #-- Delete Node --#
        self.mibDelSelNode.triggered.connect(self.on_delSelNodes)
        self.mibDelSelNode.setShortcut("Del")
        #-- Edit Node --#
        self.mibEditInside.triggered.connect(self._singleClick)
        self.mibEditInside.setShortcut("Ctrl+Return")
        self.mibEditOutside.triggered.connect(self._doubleClick)
        self.mibEditOutside.setShortcut("Shift+Return")
        #-- Expand Node --#
        self.mibExpandAll.triggered.connect(self.menuSection.expandAll)
        self.mibExpandAll.setShortcut("Shift+F3")
        self.mibExpandBranch.triggered.connect(self.menuSection.expandBranch)
        self.mibExpandBranch.setShortcut("F3")
        self.mibExpandActif.triggered.connect(self.menuSection.expandActif)
        self.mibExpandActif.setShortcut("Ctrl+F3")
        self.mibExpandInactif.triggered.connect(self.menuSection.expandInactif)
        self.mibExpandInactif.setShortcut("Ctrl+Shift+F3")
        #-- Collapse Node --#
        self.mibCollapseAll.triggered.connect(self.menuSection.collapseAll)
        self.mibCollapseAll.setShortcut("Shift+F4")
        self.mibCollapseBranch.triggered.connect(self.menuSection.collapseBranch)
        self.mibCollapseBranch.setShortcut("F4")
        self.mibCollapseActif.triggered.connect(self.menuSection.collapseActif)
        self.mibCollapseActif.setShortcut("Ctrl+F4")
        self.mibCollapseInactif.triggered.connect(self.menuSection.collapseInactif)
        self.mibCollapseInactif.setShortcut("Ctrl+Shift+F4")
        #-- Copy Paste Node --#
        self.mibCopyNode.triggered.connect(partial(self.menuSection.storeNodeToBuffer, 'copy', 'node'))
        self.mibCopyNode.setShortcut("Ctrl+C")
        self.mibCopyBranch.triggered.connect(partial(self.menuSection.storeNodeToBuffer, 'copy', 'branch'))
        self.mibCopyBranch.setShortcut("Shift+C")
        self.mibCutBranch.triggered.connect(partial(self.menuSection.storeNodeToBuffer, 'move', 'branch'))
        self.mibCutBranch.setShortcut("Ctrl+X")
        self.mibPaste.triggered.connect(self.menuSection.pasteBufferToNode)
        self.mibPaste.setShortcut("Ctrl+V")
        #-- Move Node --#
        self.mibMoveUp.triggered.connect(partial(self.menuSection.moveNode, 'up'))
        self.mibMoveUp.setShortcut("Ctrl+Up")
        self.mibMoveDn.triggered.connect(partial(self.menuSection.moveNode, 'down'))
        self.mibMoveDn.setShortcut("Ctrl+Down")

    def _setupMenuExec(self):
        """ Setup menu 'Exec' """
        self.miExecGraph.triggered.connect(self.mi_execGraph)
        self.miExecGraph.setShortcut("Alt+E")
        self.miXterm.triggered.connect(self.mi_Xterm)
        self.miXterm.setShortcut("Alt+X")
        self.miXplorer.triggered.connect(self.mi_Xplorer)
        self.miXplorer.setShortcut("Alt+C")

    def _setupMenuPref(self):
        """ Setup menu 'Pref' """
        self.miNodeEditor.triggered.connect(self.mi_nodeEditor)
        self.miNodeEditor.setShortcut("E")

    def _setupMenuHelp(self):
        """ Setup menu 'Help' """
        self.miGrapherVar.triggered.connect(self.mi_grapherVar)
        self.miGrapherVar.setShortcut("Ctrl+I")
        self.miGraphDict.triggered.connect(self.mi_graphDict)
        self.miGraphDict.setShortcut("Ctrl+Shift+I")

    def _setupGlobalNotes(self):
        """ Setup global notes section """
        self.cbGlobalNotes.clicked.connect(self.rf_globalNotesVisibility)
        self.qfGlobalNotes.setAutoFillBackground(True)
        self.qfGlobalNotes.setStyleSheet(self.style.defaultFrameBgc)
        self.teGlobalNotes.setVisible(False)
        self.teGlobalNotes.setAutoFillBackground(True)
        self.teGlobalNotes.setStyleSheet(self.style.notesBgc)
        self.teGlobalNotes.append('\n'.join(self.style.defaultNotes))

    def _setupGlobalVar(self):
        """ Setup global variable section """
        self.cbGlobalVar.clicked.connect(self.rf_globalVarVisibility)
        self.qfGlobalVar.setAutoFillBackground(True)
        self.qfGlobalVar.setStyleSheet(self.style.defaultFrameBgc)
        self.qfGlobalVarBtn.setVisible(False)
        self.twGlobalVar.setVisible(False)
        self.style.varHeaderSize(self.twGlobalVar)
        self.bGlobalVarAdd.clicked.connect(partial(self.on_addVar, self.twGlobalVar))
        self.bGlobalVarDel.clicked.connect(partial(self.on_delVar, self.twGlobalVar))
        self.bGlobalVarUp.clicked.connect(partial(self.on_upVar, self.twGlobalVar))
        self.bGlobalVarDn.clicked.connect(partial(self.on_dnVar, self.twGlobalVar))

    def _setupGraphZone(self):
        """ Setup graph tree section """
        self.twGraph.currentItemChanged.connect(self.editor.clearEditor)
        self.twGraph.setColumnCount(self.style.graphZoneColumns)
        self.twGraph.setAutoFillBackground(True)
        self.twGraph.setStyleSheet(self.style.graphZoneBgc)
        self.style.graphHeaderSize(self.twGraph)

    def _setupNodeEditor(self):
        """ Setup node editor section """
        print "#-- Setup Node Editor --#"
        self.qfNodeEditor.setVisible(False)
        self.editor._setupNodeId()
        self.editor._setupNodeNotes()
        self.editor._setupNodeVar()
        self.editor._setupNodeRemote()
        self.editor._setupNodeLoop()
        self.editor._setupNodeScript()
        self.editor._setupNodeTrash()
        self.editor._setupNodeEditBtn()

    #=========================================== INIT =============================================#

    def _initGrapher(self):
        """ Init grapher ui """
        print "#-- Init Grapher --#"
        gpCore.createLibFld()
        self._initInternalAttr()
        self._initGlobalVarAttr()
        self._initGraphZoneAttr()
        self._initNodeEditor()
        print "#-- Refresh Grapher --#"
        self.rf_globalNotesVisibility()
        self.rf_globalVarVisibility()

    def _initInternalAttr(self, init=True, gpFile=None):
        """ Init grapher attributes
            @keyword init: Mode init
            @type init: bool
            @keyword gpFile: Graph file absolut path
            @type gpFile: str """
        if init:
            self.GP_NAME = None
            self.GP_FILENAME = None
            self.GP_DIRPATH = None
            self.GP_ABSPATH = None
            self.GP_LOCK = False
            self.GP_LOCKFILE = None
            if not hasattr(self, 'GP_recentFiles'):
                self.GP_recentFiles = []
        else:
            self.GP_FILENAME = os.path.basename(gpFile)
            self.GP_NAME = self.GP_FILENAME.split('.')[0]
            self.GP_DIRPATH = os.path.dirname(gpFile)
            self.GP_ABSPATH = gpFile

    def _initGlobalVarAttr(self):
        """ Init global variable attributes """
        self.twGlobalVar.varList = []

    def _initGraphZoneAttr(self):
        """ Init graph zone attributes """
        self.twGraph.rootList = []
        self.twGraph.nodeList = {}

    def _initNodeEditor(self):
        """ Init node editor """
        print "#-- Init Node Editor --#"
        self.editor._initNodeAttr()
        print "#-- Refresh Node Editor --#"
        self.editor.rf_nodeNotesVisibility()
        self.editor.rf_nodeVarVisibility()
        self.editor.rf_nodeRemoteOptVisibility()
        self.editor.rf_nodeLoopOptVisibility()
        self.editor.rf_nodeTrashVisibility()

    #========================================== REFRESH ===========================================#

    def rf_lockVisibility(self):
        """ Refresh lock state visibility """
        if self.GP_LOCK:
            self.qfGlobalNotes.setStyleSheet(self.style.lockFrameBgc)
            self.teGlobalNotes.setReadOnly(True)
            self.qfGlobalVar.setStyleSheet(self.style.lockFrameBgc)
        else:
            self.qfGlobalNotes.setStyleSheet(self.style.defaultFrameBgc)
            self.teGlobalNotes.setReadOnly(False)
            self.qfGlobalVar.setStyleSheet(self.style.defaultFrameBgc)

    def rf_globalNotesVisibility(self):
        """ Refresh global notes section visibility """
        if self.cbGlobalNotes.isChecked():
            self.teGlobalNotes.setVisible(True)
            self.qfGlobalNotes.setMaximumHeight(500)
        else:
            self.teGlobalNotes.setVisible(False)
            self.qfGlobalNotes.setMaximumHeight(20)

    def rf_globalVarVisibility(self):
        """ Refresh global variable section visibility """
        if self.cbGlobalVar.isChecked():
            self.twGlobalVar.setVisible(True)
            self.qfGlobalVarBtn.setVisible(True)
            self.qfGlobalVar.setMaximumHeight(500)
        else:
            self.twGlobalVar.setVisible(False)
            self.qfGlobalVarBtn.setVisible(False)
            self.qfGlobalVar.setMaximumHeight(20)

    def rf_globalVarTree(self):
        """ Refresh global variable tree """
        self.twGlobalVar.clear()
        gpCmds.PopulateVarTree(self.twGlobalVar).populate()

    def rf_graphTree(self):
        """ Refresh graph tree """
        self.twGraph.clear()
        gpCmds.PopulateGraphTree(self).populate()

    def clearMainUi(self):
        """ Clear Grapher QMainWindow """
        self._initInternalAttr()
        self.teGlobalNotes.clear()
        self.teGlobalNotes.append('\n'.join(self.style.defaultNotes))
        self._initGlobalVarAttr()
        self.twGlobalVar.clear()
        self._initGraphZoneAttr()
        self.twGraph.clear()

    #========================================= MENU FILE ==========================================#

    def mi_newGraph(self, clearLock=True):
        """ Command launch when miNewGraph is clicked
            @keyword clearLock: Force clear lock file
            @type clearLock: bool """
        mess = "Save befor opening new graph ?"
        btnL = ["Save", "Don't Save", "Cancel"]
        cmdL = [partial(self._newGraphDialogBtn1, clearLock),
                partial(self._newGraphDialogBtn2, clearLock),
                self._newGraphDialogBtn3]
        self.cdNewGraph = dialog.ConfirmDialog(mess, btns=btnL, cmds=cmdL)
        self.cdNewGraph.exec_()

    def _newGraphDialogBtn1(self, clearLock):
        """ Command launch when 'Save' of confirmDialog is clicked
            @param clearLock: Force clear lock file
            @type clearLock: bool """
        if self.GP_FILENAME is not None:
            if clearLock:
                gpCore.removeLockFile(self.GP_LOCKFILE)
            if self.mi_saveGraph():
                self.clearMainUi()
                self.cdNewGraph.close()
                self.rf_lockVisibility()
        else:
            print ''.join(["#-- GRAPHER: Internal var GP_FILENAME not set.",
                           " Graph must exists in bdd for autoSave --#"])

    def _newGraphDialogBtn2(self, clearLock):
        """ Command launch when 'Don't Save' of confirmDialog is clicked
            @param clearLock: Force clear lock file
            @type clearLock: bool """
        if clearLock:
            gpCore.removeLockFile(self.GP_LOCKFILE)
        self.clearMainUi()
        self.cdNewGraph.close()
        self.rf_lockVisibility()

    def _newGraphDialogBtn3(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.cdNewGraph.close()

    def mi_loadGraph(self):
        """ Command launch when a graph file is about to be loaded """
        print "\n##### Load Graph #####"
        if self.GP_DIRPATH is None:
            rootPath = grapher.defaultPath
        else:
            rootPath = self.GP_DIRPATH
        self.fdLoadGraph = dialog.fileDialog(fdMode='open', fdRoot=rootPath,
                                             fdRoots=self.GP_recentFiles,
                                             fdFilters=['gp_*.py'], fdCmd=self._loadGraph)
        self.fdLoadGraph.show()

    def _loadGraph(self):
        """ Command launch when a graph file is about to be loaded """
        selFile = self.fdLoadGraph.selectedFiles()
        graphFile = str(selFile[0].replace('/', os.sep))
        #-- Verif Lock File --#
        lockFile = graphFile.replace('.py', '.lock.txt')
        if os.path.exists(lockFile):
            lockInfo = pFile.readFile(lockFile)
            mess = ["!!! WARNING: Graph Locked !!!",
                    "User: %s" % lockInfo[0].split(' = ')[1].replace('\n', ''),
                    "Station: %s" % lockInfo[1].split(' = ')[1].replace('\n', ''),
                    "Date: %s" % (lockInfo[2].split(' = ')[1].split('__')[0].replace('_', '/')),
                    "Time: %s" % (lockInfo[2].split(' = ')[1].split('__')[1].replace('_', ':'))]
            btnL = ["Read Only", "Break Lock", "Cancel"]
            cmdL = [partial(self._newLockDialogBtn1, graphFile),
                    partial(self._newLockDialogBtn2, graphFile),
                    self._newLockDialogBtn3]
            self.cdNewGraph = dialog.ConfirmDialog('\n'.join(mess), btns=btnL, cmds=cmdL)
            self.cdNewGraph.exec_()
        #-- Load Graph --#
        else:
            self.fdLoadGraph.close()
            gpCore.removeLockFile(self.GP_LOCKFILE)
            gpCore.createLockFile(lockFile)
            self.mi_newGraph(clearLock=False)
            self.GP_LOCK = False
            self.GP_LOCKFILE = lockFile
            self.menuSection.loadGraph(graphFile)
            self.rf_lockVisibility()

    def _newLockDialogBtn1(self, graphFile):
        """ Command launch when 'Read Only' of confirmDialog is clicked
            @param graphFile: Graph File absolut path
            @type graphFile: str """
        self.cdNewGraph.close()
        self.fdLoadGraph.close()
        lockFile = graphFile.replace('.py', '.lock.txt')
        gpCore.removeLockFile(self.GP_LOCKFILE)
        self.mi_newGraph(clearLock=False)
        self.GP_LOCK = True
        self.GP_LOCKFILE = lockFile
        self.menuSection.loadGraph(graphFile)
        self.rf_lockVisibility()

    def _newLockDialogBtn2(self, graphFile):
        """ Command launch when 'Break Lock' of confirmDialog is clicked
            @param graphFile: Graph File absolut path
            @type graphFile: str """
        self.cdNewGraph.close()
        self.fdLoadGraph.close()
        lockFile = graphFile.replace('.py', '.lock.txt')
        gpCore.removeLockFile(self.GP_LOCKFILE)
        gpCore.createLockFile(lockFile)
        self.mi_newGraph(clearLock=False)
        self.GP_LOCK = False
        self.GP_LOCKFILE = lockFile
        self.menuSection.loadGraph(graphFile)
        self.rf_lockVisibility()

    def _newLockDialogBtn3(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.cdNewGraph.close()

    def mi_saveGraph(self):
        """ Command launch when miSaveGraph is clicked """
        print "\n##### Save Graph #####"
        if self.GP_DIRPATH is None:
            self.mi_saveGraphAs()
            return True
        else:
            if self.GP_LOCK:
                print "!!! WARNING: Can't save in a lock file !!!"
                return False
            else:
                self.menuSection.saveGraph()
                return True

    def mi_saveGraphAs(self):
        """ Command launch when miSaveGraphAs is clicked """
        print "\n##### Save Graph As #####"
        if self.GP_DIRPATH is None:
            rootPath = grapher.defaultPath
        else:
            rootPath = self.GP_DIRPATH
        self.fdSaveGraphAs = dialog.fileDialog(fdMode='save', fdRoot=rootPath,
                                               fdRoots=self.GP_recentFiles,
                                               fdFilters=['gp_*.py'], fdCmd=self._saveGraphAs)
        self.fdSaveGraphAs.show()

    def _saveGraphAs(self):
        """ Command launch when a graph file is about to be saved """
        selFile = self.fdSaveGraphAs.selectedFiles()
        graphFile = str(selFile[0].replace('/', os.sep))
        lockFile = graphFile.replace('.py', '.lock.txt')
        self.fdSaveGraphAs.close()
        if not os.path.exists(lockFile):
            gpCore.removeLockFile(self.GP_LOCKFILE)
            gpCore.createLockFile(lockFile)
            self.GP_LOCK = False
            self.GP_LOCKFILE = lockFile
            self.menuSection.saveGraphAs(graphFile)
        else:
            print "!!! WARNING: Can't save in a lock file !!!"
        self.rf_lockVisibility()

    def mi_quitGrapher(self):
        """ Command launch when miQuit is clicked """
        mess = "Save befor closing grapher ?"
        btnL = ["Save", "Don't Save", "Cancel"]
        cmdL = [self._quitDialogBtn1,
                self._quitDialogBtn2,
                self._quitDialogBtn3]
        self.cdQuit = dialog.ConfirmDialog(mess, btns=btnL, cmds=cmdL)
        self.cdQuit.exec_()

    def _quitDialogBtn1(self):
        """ Command launch when 'Save' of confirmDialog is clicked """
        self.cdQuit.close()
        if self.mi_saveGraph():
            gpCore.removeLockFile(self.GP_LOCKFILE)
            self.close()

    def _quitDialogBtn2(self):
        """ Command launch when 'Don't Save' of confirmDialog is clicked """
        self.cdQuit.close()
        gpCore.removeLockFile(self.GP_LOCKFILE)
        self.close()

    def _quitDialogBtn3(self):
        """ Command launch when 'Cancel' of confirmDialog is clicked """
        self.cdQuit.close()

    #========================================= MENU GRAPH =========================================#

    def on_newNode(self, nodeType):
        """ Command launch when miNewNode.nodeName QAction is clicked
            @param nodeType: New graphNode type ('modul', 'sysData', 'cmdData', 'purData', 'loop')
            @type nodeType: str """
        if not self.GP_LOCK:
            #-- Store Selection --#
            selItems = self.twGraph.selectedItems()
            selNodes = []
            for item in selItems:
                selNodes.append(item.nodeName)
            #-- Add New Node --#
            self.menuSection.newNode(nodeType)
            self.rf_graphTree()
            self.menuSection._reselectNodes(selNodes)
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_singleClick(self, graphNode):
        """ Command launch when single click is detected on graph node
            @param graphNode: Selected graphNode (QTreeWidgetItem)
            @type graphNode: object """
        self.menuSection._clickedNode(graphNode)
        if self.qfNodeEditor.isVisible():
            self.editor.ud_editorFromNode(graphNode)
            self.editor.rf_lockVisibility()

    def _singleClick(self):
        """ Command launch when single click is detected on graph node via keyboard shortcuts """
        graphNode = self.getSelectedGraphNode
        self.on_singleClick(graphNode)

    def on_doubleClick(self, graphNode):
        """ Command launch when douvle click is detected on graph node
            @param graphNode: Selected graphNode (QTreeWidgetItem)
            @type graphNode: object """
        self.editorUi = nodeEditor.NodeEditorUi(self, graphNode)
        self.editorUi.show()

    def _doubleClick(self):
        """ Command launch when double click is detected on graph node via keyboard shortcuts """
        graphNode = self.getSelectedGraphNode
        self.menuSection._clickedNode(graphNode)
        self.on_doubleClick(graphNode)

    def on_rename(self):
        """ Rename selected node """
        if not self.GP_LOCK:
            graphNode = self.getSelectedGraphNode
            if graphNode is not None:
                mess = "Rename %s" % graphNode.nodeName
                self.pdRename = dialog.PromptDialog(mess, self._renameDialogAccept,
                                                          self._renameDialogCancel)
                self.pdRename.exec_()
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def _renameDialogAccept(self):
        """ Command launch when 'Ok' of promptDialog is clicked """
        newName = str(self.pdRename.leUserValue.text())
        graphNode = self.getSelectedGraphNode
        if self.menuSection._verifNewNodeName(newName):
            print "Rename %s to %s" % (graphNode.nodeName, newName)
            self.menuSection._replaceRootList(graphNode, newName)
            self.menuSection._replaceParentChildren(graphNode, newName)
            self.menuSection._replaceChildrenParent(graphNode, newName)
            self.menuSection._replaceNodeName(graphNode, newName)
            graphNode.buttonObject.setText(newName)
            self.pdRename.close()
            if self.qfNodeEditor.isVisible():
                self._singleClick()
        else:
            mess = ["Rename %s" % graphNode.nodeName,
                    "!!! WARNING: %r already exists !!!" % newName]
            self.pdRename.lMessage.setText('\n'.join(mess))
            self.pdRename.leUserValue.clear()

    def _renameDialogCancel(self):
        """ Command launch when 'Cancel' of promptDialog is clicked """
        self.pdRename.close()

    def on_delSelNodes(self):
        """ Command launch when miDelSelNode QAction is clicked """
        if not self.GP_LOCK:
            self.menuSection.delSelNodes()
            self.rf_graphTree()
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    #========================================= MENU EXEC ==========================================#

    def mi_execGraph(self):
        """ Command launch when miExecGraph is clicked """
        gpCore.ExecGrapher(self).execGraph()

    def mi_Xterm(self):
        """ Command launch when miXterm is clicked """
        gpCore.xTerm(self.GP_DIRPATH)

    def mi_Xplorer(self):
        """ Command launch when miXplorer is clicked """
        gpCore.xPlorer(self.GP_DIRPATH)

    #========================================= MENU PREF ==========================================#

    def mi_nodeEditor(self):
        """ Command launch when miNodeEditor is clicked """
        if self.qfNodeEditor.isVisible():
            self.qfNodeEditor.setVisible(False)
            self.editor.clearEditor()
        else:
            self.qfNodeEditor.setVisible(True)
            selItems = self.twGraph.selectedItems()
            if len(selItems) == 1:
                self._singleClick()

    #========================================= MENU HELP ==========================================#

    def mi_grapherVar(self):
        """ Command launch when miGrapherVar is clicked """
        print self.menuSection.printInternalVar

    def mi_graphDict(self):
        """ Command launch when miGraphDict is clicked """
        print self.menuSection.printGraphDict

    #======================================== VAR ACTION ==========================================#

    def on_addVar(self, varTree):
        """ Command launch when Add QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.GP_LOCK:
            self.varSection.addVar(varTree)
            self.rf_globalVarTree()
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_delVar(self, varTree):
        """ Command launch when Del QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.GP_LOCK:
            self.varSection.delVar(varTree)
            self.rf_globalVarTree()
            self.varSection._reindexFromOrder(varTree)
            self.rf_globalVarTree()
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_upVar(self, varTree):
        """ Command launch when Up QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.GP_LOCK:
            inds = self.varSection.upVar(varTree)
            self.rf_globalVarTree()
            self.varSection._reindexFromOrder(varTree)
            self.rf_globalVarTree()
            self.varSection._reselect(varTree, inds)
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_dnVar(self, varTree):
        """ Command launch when Dn QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.GP_LOCK:
            inds = self.varSection.dnVar(varTree)
            self.rf_globalVarTree()
            self.varSection._reselect(varTree, inds)
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    #=========================================== UPDATE ===========================================#

    @property
    def ud_menuCmds(self):
        """ Update MenuCmds class
            @return: MenuCmds class
            @rtype: object """
        return gpCmds.MenuCmds(self)

    @property
    def ud_nodeEditor(self):
        """ Update NodeEditor class
            @return: NodeEditor class
            @rtype: object """
        return nodeEditor.NodeEditor(self, self)

    @property
    def getSelectedGraphNode(self):
        """ Get selected QTreeWidgetItem from graph
            @return: Selected graphNode (QTreeWidgetItem)
            @rtype: object """
        selItems = self.twGraph.selectedItems()
        if len(selItems) == 1:
            return selItems[0]
        else:
            return None


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    graphToLoad = os.path.join(grapher.defaultPath, 'leVoeu', 'shots', 's001', 'p005', 'gp_s001_p005.py')
    gpCmds.MenuCmds(window).loadGraph(graphToLoad)
    sys.exit(app.exec_())
