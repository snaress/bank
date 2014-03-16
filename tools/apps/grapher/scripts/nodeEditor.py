from functools import partial
from tools.apps import grapher
from PyQt4 import uic
from tools.apps.grapher.scripts import gpCmds
from tools.apps.grapher.scripts import gpCore


nodeEditorClass, uiNodeEditorClass = uic.loadUiType(grapher.uiList['nodeEditor'])
class NodeEditorUi(nodeEditorClass, uiNodeEditorClass):

    def __init__(self, mainUi, graphNode):
        """@param mainUi: Grapher ui object (QMainWindow)
            @type mainUi: object
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        self.mainUi = mainUi
        self.node = graphNode
        self.style = gpCore.GrapherStyle()
        self.editor = NodeEditor(self.mainUi, self)
        print "\n##### Launch Node Editor: %s #####" % self.node.nodeName
        super(NodeEditorUi, self).__init__()
        self.setupUi(self)
        self._setupEditor()
        self._initEditor()
        self.editor.ud_editorFromNode(self.node)
        self.editor.rf_lockVisibility()

    def _setupEditor(self):
        """ Setup node editor """
        print "#-- Setup Node Editor --#"
        self.setWindowTitle("Node Editor - %s" % self.node.nodeName)
        self.editor._setupNodeId()
        self.editor._setupNodeNotes()
        self.editor._setupNodeVar()
        self.editor._setupNodeRemote()
        self.editor._setupNodeLoop()
        self.editor._setupNodeScript()
        self.editor._setupNodeTrash()
        self.editor._setupNodeEditBtn()

    def _initEditor(self):
        """ Init node editor """
        print "#-- Init Node Editor --#"
        self.editor._initNodeAttr()
        print "#-- Refresh Node Editor --#"
        self.editor.rf_nodeNotesVisibility()
        self.editor.rf_nodeVarVisibility()
        self.editor.rf_nodeRemoteOptVisibility()
        self.editor.rf_nodeLoopOptVisibility()
        self.editor.rf_nodeTrashVisibility()


class NodeEditor(object):

    def __init__(self, mainUi, wnd):
        """ @param mainUi: Grapher ui object (QMainWindow)
            @type mainUi: object
            @param wnd: Node editor ui object (QWidget)
            @type wnd: object """
        self.mainUi = mainUi
        self.wnd = wnd
        self.graph = self.mainUi.twGraph
        self.style = gpCore.GrapherStyle()
        self.varSection = gpCmds.VarSection()

    #========================================== SETUP =============================================#

    def _setupNodeId(self):
        """ Setup node name, node version, node version title """
        self.wnd.leName.setReadOnly(True)
        self.wnd.cbVersion.currentIndexChanged.connect(self.on_version)
        self.wnd.bNewV.clicked.connect(self.on_newVersion)
        self.wnd.bDelV.clicked.connect(self.on_delVersion)

    def _setupNodeNotes(self):
        """ Setup node notes section """
        self.wnd.cbNodeNotes.clicked.connect(self.rf_nodeNotesVisibility)
        self.wnd.qfNodeNotes.setAutoFillBackground(True)
        self.wnd.qfNodeNotes.setStyleSheet(self.style.defaultFrameBgc)
        self.wnd.teNodeNotes.setVisible(False)
        self.wnd.teNodeNotes.setAutoFillBackground(True)
        self.wnd.teNodeNotes.setStyleSheet(self.style.notesBgc)
        self.wnd.teNodeNotes.append('\n'.join(self.style.defaultNotes))

    def _setupNodeVar(self):
        """ Setup node variable section """
        self.wnd.cbNodeVar.clicked.connect(self.rf_nodeVarVisibility)
        self.wnd.qfNodeVar.setAutoFillBackground(True)
        self.wnd.qfNodeVar.setStyleSheet(self.style.defaultFrameBgc)
        self.wnd.qfNodeVarBtn.setVisible(False)
        self.wnd.twNodeVar.setVisible(False)
        self.wnd.style.varHeaderSize(self.wnd.twNodeVar)
        self.wnd.bNodeVarAdd.clicked.connect(partial(self.on_addVar, self.wnd.twNodeVar))
        self.wnd.bNodeVarDel.clicked.connect(partial(self.on_delVar, self.wnd.twNodeVar))
        self.wnd.bNodeVarUp.clicked.connect(partial(self.on_upVar, self.wnd.twNodeVar))
        self.wnd.bNodeVarDn.clicked.connect(partial(self.on_dnVar, self.wnd.twNodeVar))

    def _setupNodeRemote(self):
        """ Setup node remote section """
        self.wnd.cbRemote.clicked.connect(self.rf_nodeRemoteOptVisibility)
        self.wnd.qfRemote.setVisible(False)
        self.wnd.qfRemote.setAutoFillBackground(True)
        self.wnd.qfRemote.setStyleSheet(self.style.remoteBgc)

    def _setupNodeLoop(self):
        """ Setup node loop section """
        self.wnd.qfNodeLoop.setVisible(False)
        self.wnd.qfNodeLoop.setAutoFillBackground(True)
        self.wnd.qfNodeLoop.setStyleSheet(self.style.loopBgc)
        self.wnd.rbLoopRange.clicked.connect(self.rf_nodeLoopOptVisibility)
        self.wnd.rbLoopList.clicked.connect(self.rf_nodeLoopOptVisibility)
        self.wnd.rbLoopSingle.clicked.connect(self.rf_nodeLoopOptVisibility)

    def _setupNodeScript(self):
        """ Setup node script section """
        self.wnd.qfScript.setVisible(False)
        self.wnd.qfScriptSpacer.setVisible(True)
        self.wnd.qfScriptSpacer.setAutoFillBackground(True)
        self.wnd.qfScriptSpacer.setStyleSheet(self.style.defaultFrameBgc)
        self.style.scriptFont(self.wnd.teScript)

    def _setupNodeTrash(self):
        """ Setup node trash section """
        self.wnd.cbNodeTrash.clicked.connect(self.rf_nodeTrashVisibility)
        self.wnd.qfNodeTrash.setAutoFillBackground(True)
        self.wnd.qfNodeTrash.setStyleSheet(self.style.defaultFrameBgc)
        self.wnd.teNodeTrash.setVisible(False)
        self.wnd.teNodeTrash.setAutoFillBackground(True)
        self.wnd.teNodeNotes.setStyleSheet(self.style.trashBgc)

    def _setupNodeEditBtn(self):
        """ Setup node edit buttons """
        self.wnd.bSaveNode.clicked.connect(self.ud_nodeFromEditor)
        if not self.mainUi == self.wnd:
            self.wnd.bCloseNode.setEnabled(True)
            self.wnd.bCloseNode.clicked.connect(self.wnd.close)
        else:
            self.wnd.bCloseNode.setEnabled(False)

    #=========================================== INIT =============================================#

    def _initNodeAttr(self):
        """ Init node variable attributes """
        self.wnd.twNodeVar.varList = []

    #========================================= REFRESH ============================================#

    def rf_lockVisibility(self):
        """ Refresh lock state visibility """
        if self.mainUi.GP_LOCK:
            self.wnd.teNodeNotes.setReadOnly(True)
            self.wnd.teScript.setReadOnly(True)
            self.wnd.teNodeTrash.setReadOnly(True)
        else:
            self.wnd.teNodeNotes.setReadOnly(False)
            self.wnd.teScript.setReadOnly(False)
            self.wnd.teNodeTrash.setReadOnly(False)

    def rf_nodeNotesVisibility(self):
        """ Refresh node notes section visibility """
        if self.wnd.cbNodeNotes.isChecked():
            self.wnd.teNodeNotes.setVisible(True)
            self.wnd.qfNodeNotes.setMaximumHeight(500)
        else:
            self.wnd.teNodeNotes.setVisible(False)
            self.wnd.qfNodeNotes.setMaximumHeight(20)

    def rf_nodeVarVisibility(self):
        """ Refresh node variable section visibility """
        if self.wnd.cbNodeVar.isChecked():
            self.wnd.twNodeVar.setVisible(True)
            self.wnd.qfNodeVarBtn.setVisible(True)
            self.wnd.qfNodeVar.setMaximumHeight(500)
        else:
            self.wnd.twNodeVar.setVisible(False)
            self.wnd.qfNodeVarBtn.setVisible(False)
            self.wnd.qfNodeVar.setMaximumHeight(20)

    def rf_nodeVarTree(self):
        """ Refresh node variable tree """
        self.wnd.twNodeVar.clear()
        gpCmds.PopulateVarTree(self.wnd.twNodeVar).populate()

    def rf_nodeRemoteVisibility(self, graphNode):
        """ Refresh node remote section visibility
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        if graphNode.nodeType == 'purData':
            self.wnd.qfRemote.setVisible(False)
        else:
            self.wnd.qfRemote.setVisible(True)

    def rf_nodeRemoteOptVisibility(self):
        """ Refresh node remote options section visibility """
        if self.wnd.cbRemote.isChecked():
            self.wnd.qfRemoteOption.setVisible(True)
            self.wnd.qfRemote.setMaximumHeight(80)
        else:
            self.wnd.qfRemoteOption.setVisible(False)
            self.wnd.qfRemote.setMaximumHeight(20)

    def rf_nodeLoopVisibility(self, graphNode):
        """ Refresh node loop section visibility
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        if graphNode.nodeType == 'loop':
            self.wnd.qfNodeLoop.setVisible(True)
        else:
            self.wnd.qfNodeLoop.setVisible(False)

    def rf_nodeLoopOptVisibility(self):
        """ Refresh node loop options section visibility """
        if self.wnd.rbLoopRange.isChecked():
            self.wnd.qfLoopRange.setVisible(True)
            self.wnd.qfLoopList.setVisible(False)
            self.wnd.qfLoopSingle.setVisible(False)
        elif self.wnd.rbLoopList.isChecked():
            self.wnd.qfLoopRange.setVisible(False)
            self.wnd.qfLoopList.setVisible(True)
            self.wnd.qfLoopSingle.setVisible(False)
        elif self.wnd.rbLoopSingle.isChecked():
            self.wnd.qfLoopRange.setVisible(False)
            self.wnd.qfLoopList.setVisible(False)
            self.wnd.qfLoopSingle.setVisible(True)

    def rf_nodeTrashVisibility(self):
        """ Refresh node trash section visibility """
        if self.wnd.cbNodeTrash.isChecked():
            self.wnd.teNodeTrash.setVisible(True)
            self.wnd.qfNodeTrash.setMaximumHeight(500)
        else:
            self.wnd.teNodeTrash.setVisible(False)
            self.wnd.qfNodeTrash.setMaximumHeight(20)

    def rf_nodeScriptVisibility(self, graphNode):
        """ Refresh node script visibility
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        if graphNode.nodeType in ['modul', 'loop']:
            self.wnd.qfScript.setVisible(False)
            self.wnd.qfScriptSpacer.setVisible(True)
        else:
            self.wnd.qfScript.setVisible(True)
            self.wnd.qfScriptSpacer.setVisible(False)
            if graphNode.nodeType == 'cmdData':
                self.wnd.qfNodeCmd.setVisible(True)
            else:
                self.wnd.qfNodeCmd.setVisible(False)

    def clearEditor(self):
        """ Clear node editor """
        self.wnd.leName.clear()
        self.wnd.cbVersion.clear()
        self.wnd.leVersionTitle.clear()
        self.wnd.teNodeNotes.clear()
        self.wnd.twNodeVar.clear()
        self.wnd.cbNodeCmd.clear()
        self.wnd.leNodeCmd.clear()
        self.wnd.teScript.clear()
        self.wnd.teNodeTrash.clear()

    #====================================== VERSION ACTION ========================================#

    def on_version(self):
        """ Command launch when node version has changed """
        graphNode = self.getNodeFromEditor
        if graphNode is not None:
            newV = str(self.wnd.cbVersion.currentText())
            graphNode.nodeVersion = newV
            self.ud_editorFromNode(graphNode)

    def on_newVersion(self):
        """ Create a new node version """
        graphNode = self.getNodeFromEditor
        nodeName = graphNode.nodeName
        curV = graphNode.nodeVersion
        newV = str(int(max(graphNode.nodeVersions))+1).zfill(3)
        nodeParams = self.graph.nodeList[nodeName]
        self.graph.nodeList[nodeName]['nodeVersions'].append(newV)
        self.graph.nodeList[nodeName]['nodeVersion'] = newV
        self.graph.nodeList[nodeName]['nodeVTitle'][newV] = self.style.defaultVersionTitle
        self.graph.nodeList[nodeName]['nodeNotes'][newV] = nodeParams['nodeNotes'][curV]
        self.graph.nodeList[nodeName]['nodeVarList'][newV] = nodeParams['nodeVarList'][curV]
        self.graph.nodeList[nodeName]['nodeCmd'][newV] = nodeParams['nodeCmd'][curV]
        self.graph.nodeList[nodeName]['nodeCmdOpt'][newV] = nodeParams['nodeCmdOpt'][curV]
        self.graph.nodeList[nodeName]['nodeScript'][newV] = nodeParams['nodeScript'][curV]
        self.graph.nodeList[nodeName]['nodeTrash'][newV] = nodeParams['nodeTrash'][curV]
        graphNode.nodeVersion = newV
        self.ud_editorFromNode(graphNode)

    def on_delVersion(self):
        """ Delete current node version """
        if self.wnd.cbVersion.count() > 1:
            graphNode = self.getNodeFromEditor
            nodeName = graphNode.nodeName
            curV = graphNode.nodeVersion
            ind = self.graph.nodeList[nodeName]['nodeVersions'].index(curV)
            self.graph.nodeList[nodeName]['nodeVersions'].pop(ind)
            self.graph.nodeList[nodeName]['nodeVTitle'].pop(curV)
            self.graph.nodeList[nodeName]['nodeNotes'].pop(curV)
            self.graph.nodeList[nodeName]['nodeVarList'].pop(curV)
            self.graph.nodeList[nodeName]['nodeCmd'].pop(curV)
            self.graph.nodeList[nodeName]['nodeCmdOpt'].pop(curV)
            self.graph.nodeList[nodeName]['nodeScript'].pop(curV)
            self.graph.nodeList[nodeName]['nodeTrash'].pop(curV)
            if self.getNextVersion is not None:
                graphNode.nodeVersion = self.getNextVersion
            else:
                graphNode.nodeVersion = self.getPrevVersion
            self.ud_editorFromNode(graphNode)

    @property
    def getNextVersion(self):
        """ Get node next version
            @return: Next version if exists, else None
            @rtype: str """
        curInd = self.wnd.cbVersion.currentIndex()
        vL = self.wnd.cbVersion.count()
        if curInd < vL-1:
            return str(self.wnd.cbVersion.itemText(curInd+1))
        else:
            return None

    @property
    def getPrevVersion(self):
        """ Get node previous version
            @return: Previous version if exists, else None
            @rtype: str """
        curInd = self.wnd.cbVersion.currentIndex()
        if curInd > 0:
            return str(self.wnd.cbVersion.itemText(curInd-1))
        else:
            return None

    #======================================== VAR ACTION ==========================================#

    def on_addVar(self, varTree):
        """ Command launch when Add QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.mainUi.GP_LOCK:
            self.varSection.addVar(varTree)
            self.rf_nodeVarTree()
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_delVar(self, varTree):
        """ Command launch when Del QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.mainUi.GP_LOCK:
            self.varSection.delVar(varTree)
            self.rf_nodeVarTree()
            self.varSection._reindexFromOrder(varTree)
            self.rf_nodeVarTree()
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_upVar(self, varTree):
        """ Command launch when Up QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.mainUi.GP_LOCK:
            inds = self.varSection.upVar(varTree)
            self.rf_nodeVarTree()
            self.varSection._reindexFromOrder(varTree)
            self.rf_nodeVarTree()
            self.varSection._reselect(varTree, inds)
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def on_dnVar(self, varTree):
        """ Command launch when Dn QButton is clicked
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        if not self.mainUi.GP_LOCK:
            inds = self.varSection.dnVar(varTree)
            self.rf_nodeVarTree()
            self.varSection._reselect(varTree, inds)
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    #=========================================== UPDATE ===========================================#

    def ud_editorFromNode(self, graphNode):
        """ Update node editor with selected node param
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        version = graphNode.nodeVersion
        self.clearEditor()
        self._loadNodeId(graphNode, version)
        self._loadNodeNotes(graphNode, version)
        self._loadNodeVar(graphNode, version)
        self._loadNodeRemote(graphNode)
        self._loadNodeLoop(graphNode)
        self._loadNodeScript(graphNode, version)
        self._loadNodeTrash(graphNode, version)

    def _loadNodeId(self, graphNode, v):
        """ Update node editor name, version and version title
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param v: Node version
            @type v: str """
        #-- Node Name --#
        self.wnd.leName.setText(graphNode.nodeName)
        #-- Node Version --#
        self.wnd.cbVersion.currentIndexChanged.disconnect(self.on_version)
        self.wnd.cbVersion.addItems(graphNode.nodeVersions)
        self.wnd.cbVersion.setCurrentIndex(self.wnd.cbVersion.findText(v))
        self.wnd.cbVersion.currentIndexChanged.connect(self.on_version)
        #-- Node Version Title --#
        self.wnd.leVersionTitle.setText(graphNode.nodeVTitle[v])

    def _loadNodeNotes(self, graphNode, v):
        """ Update node editor notes
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param v: Node version
            @type v: str """
        self.wnd.teNodeNotes.append('\n'.join(graphNode.nodeNotes[v]))

    def _loadNodeVar(self, graphNode, v):
        """ Update node editor variables
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param v: Node version
            @type v: str """
        nodeVars = eval(str(self.mainUi.twGraph.nodeList[graphNode.nodeName]['nodeVarList'][v]))
        self.wnd.twNodeVar.varList = nodeVars
        self.rf_nodeVarTree()

    def _loadNodeRemote(self, graphNode):
        """ Update node editor remote
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        self.rf_nodeRemoteVisibility(graphNode)

    def _loadNodeLoop(self, graphNode):
        """ Update node editor loop params
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object """
        self.rf_nodeLoopVisibility(graphNode)
        #-- Loop Mode --#
        if graphNode.nodeLoop['mode'] == 'range':
            self.wnd.rbLoopRange.setChecked(True)
        elif graphNode.nodeLoop['mode'] == 'list':
            self.wnd.rbLoopList.setChecked(True)
        elif graphNode.nodeLoop['mode'] == 'single':
            self.wnd.rbLoopSingle.setChecked(True)
        self.rf_nodeLoopOptVisibility()
        #-- Loop Iterator --#
        self.wnd.leLoopIter.setText(graphNode.nodeLoop['iter'])
        #-- Loop Check File --#
        self.wnd.leLoopTmpFile.setText(graphNode.nodeLoop['tmpFile'])
        #-- Loop Range --#
        self.wnd.leRangeStart.setText(graphNode.nodeLoop['range'][0])
        self.wnd.leRangeStop.setText(graphNode.nodeLoop['range'][1])
        self.wnd.leRangeStep.setText(graphNode.nodeLoop['range'][2])
        #-- Loop List --#
        loopList = graphNode.nodeLoop['list']
        if isinstance(loopList, str):
            self.wnd.leLoopList.setText(loopList)
        elif isinstance(loopList, list):
            self.wnd.leLoopList.setText(str(loopList))
        #-- Loop Single --#
        loopSingle = graphNode.nodeLoop['single']
        if isinstance(loopSingle, str):
            self.wnd.leLoopSingle.setText(loopSingle)
        else:
            self.wnd.leLoopSingle.setText(str(loopSingle))

    def _loadNodeScript(self, graphNode, v):
        """ Update node editor script
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param v: Node version
            @type v: str """
        self.rf_nodeScriptVisibility(graphNode)
        self.wnd.cbNodeCmd.addItems(sorted(graphNode.nodeCmds.keys()))
        self.wnd.cbNodeCmd.setCurrentIndex(self.wnd.cbNodeCmd.findText(graphNode.nodeCmd[v]))
        self.wnd.leNodeCmd.setText(graphNode.nodeCmdOpt[v])
        self.wnd.teScript.append('\n'.join(graphNode.nodeScript[v]))

    def _loadNodeTrash(self, graphNode, v):
        """ Update node editor trash
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param v: Node version
            @type v: str """
        self.wnd.teNodeTrash.append('\n'.join(graphNode.nodeTrash[v]))

    def ud_nodeFromEditor(self):
        """ Update selected node with node editor param """
        print "#-- Save Node --#"
        nodeName = str(self.wnd.leName.text())
        v = str(self.wnd.cbVersion.currentText())
        print "Saving %s (version %s)" % (nodeName, v)
        graphNode = self.getNodeFromEditor
        self._saveCommonParams(nodeName, v, graphNode)
        self._saveSpecificParams(nodeName, v, graphNode)
        print "Params saved in node ---> Ok"

    def _saveCommonParams(self, nodeName, v, graphNode):
        """ Save common node params
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        self._saveNodeVersion(nodeName, v, graphNode)
        self._saveNodeNotes(nodeName, v, graphNode)
        self._saveNodeVar(nodeName, v, graphNode)
        self._saveNodeTrash(nodeName, v, graphNode)

    def _saveSpecificParams(self, nodeName, v, graphNode):
        """ Save specific node params
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        if graphNode.nodeType == 'loop':
            self._saveNodeLoop(nodeName, graphNode)
        if graphNode.nodeType == 'cmdData':
            self._saveNodeCmd(nodeName, v, graphNode)
        if graphNode.nodeType in ['sysData', 'cmdData', 'purData']:
            self._saveNodeScript(nodeName, v, graphNode)

    def _saveNodeVersion(self, nodeName, v, graphNode):
        """ Save node version params
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        self.graph.nodeList[nodeName]['nodeVersion'] = v
        title = str(self.wnd.leVersionTitle.text())
        self.graph.nodeList[nodeName]['nodeVTitle'][v] = title
        graphNode.nodeVTitle[v] = title

    def _saveNodeNotes(self, nodeName, v, graphNode):
        """ Save node notes
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        notes = str(self.wnd.teNodeNotes.toPlainText()).split('\n')
        self.graph.nodeList[nodeName]['nodeNotes'][v] = notes
        graphNode.nodeNotes[v] = notes

    def _saveNodeVar(self, nodeName, v, graphNode):
        """ Save node Variables
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        var = self.wnd.twNodeVar.varList
        self.graph.nodeList[nodeName]['nodeVarList'][v] = var
        graphNode.nodeVarList[v] = var

    def _saveNodeTrash(self, nodeName, v, graphNode):
        """ Save node trash
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        trash = str(self.wnd.teNodeTrash.toPlainText()).split('\n')
        self.graph.nodeList[nodeName]['nodeTrash'][v] = trash
        graphNode.nodeTrash[v] = trash

    def _saveNodeLoop(self, nodeName, graphNode):
        """ Save node loop params
            @param nodeName: Selected graph node
            @type nodeName: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        #-- Loop Mode --#
        if self.wnd.rbLoopRange.isChecked():
            self.graph.nodeList[nodeName]['nodeLoop']['mode'] = 'range'
        elif self.wnd.rbLoopList.isChecked():
            self.graph.nodeList[nodeName]['nodeLoop']['mode'] = 'list'
        elif self.wnd.rbLoopSingle.isChecked():
            self.graph.nodeList[nodeName]['nodeLoop']['mode'] = 'single'
        graphNode.nodeLoop['mode'] = self.graph.nodeList[nodeName]['nodeLoop']['mode']
        #-- Loop Iter --#
        self.graph.nodeList[nodeName]['nodeLoop']['iter'] = str(self.wnd.leLoopIter.text())
        graphNode.nodeLoop['iter'] = self.graph.nodeList[nodeName]['nodeLoop']['iter']
        #-- Loop Check File --#
        self.graph.nodeList[nodeName]['nodeLoop']['tmpFile'] = str(self.wnd.leLoopTmpFile.text())
        graphNode.nodeLoop['tmpFile'] = self.graph.nodeList[nodeName]['nodeLoop']['tmpFile']
        #-- Loop Range --#
        self.graph.nodeList[nodeName]['nodeLoop']['range'] = [str(self.wnd.leRangeStart.text()),
                                                              str(self.wnd.leRangeStop.text()),
                                                              str(self.wnd.leRangeStep.text())]
        graphNode.nodeLoop['range'] = self.graph.nodeList[nodeName]['nodeLoop']['range']
        #-- Loop List --#
        loopList = str(self.wnd.leLoopList.text())
        if loopList.startswith('[') and loopList.endswith(']'):
            tmpList = []
            ll = loopList[+1:-1].split(', ')
            for v in ll:
                if v.isdigit():
                    tmpList.append(int(v))
                else:
                    tmpList.append(eval(v))
            self.graph.nodeList[nodeName]['nodeLoop']['list'] = tmpList
        else:
            self.graph.nodeList[nodeName]['nodeLoop']['list'] = loopList
        graphNode.nodeLoop['list'] = self.graph.nodeList[nodeName]['nodeLoop']['list']
        #-- Loop Single --#
        loopSingle = str(self.wnd.leLoopSingle.text())
        if loopSingle.isdigit():
            self.graph.nodeList[nodeName]['nodeLoop']['single'] = int(loopSingle)
        else:
            self.graph.nodeList[nodeName]['nodeLoop']['single'] = loopSingle
        graphNode.nodeLoop['single'] = self.graph.nodeList[nodeName]['nodeLoop']['single']

    def _saveNodeCmd(self, nodeName, v, graphNode):
        """ Save node cmd
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        #-- Node Cmd --#
        cmd = str(self.wnd.cbNodeCmd.currentText())
        self.graph.nodeList[nodeName]['nodeCmd'][v] = cmd
        graphNode.nodeCmd[v] = cmd
        #-- Node Cmd Options --#
        cmdOpt = str(self.wnd.leNodeCmd.text())
        self.graph.nodeList[nodeName]['nodeCmdOpt'][v] = cmdOpt
        graphNode.nodeCmdOpt[v] = cmdOpt

    def _saveNodeScript(self, nodeName, v, graphNode):
        """ Save node script
            @param nodeName: Selected graph node
            @type nodeName: str
            @param v: Node version
            @type v: str
            @param graphNode: Selected graph Node (QTreeWidgetItem)
            @type graphNode: object """
        script = str(self.wnd.teScript.toPlainText()).split('\n')
        self.graph.nodeList[nodeName]['nodeScript'][v] = script
        graphNode.nodeScript[v] = script

    @property
    def getNodeFromEditor(self):
        """ Get QTreeWidgetItem from node editor nameAttr
            @return: Connected graphNode (QTreeWidgetItem)
            @rtype: object """
        if not str(self.wnd.leName.text()) == '':
            return gpCore.GetGrapher(self.mainUi).getObjFromName(str(self.wnd.leName.text()))
        else:
            return None
