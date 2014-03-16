import os
from functools import partial
from tools.apps import grapher
from PyQt4 import QtGui, QtCore
from lib.qt.scripts import dialog
from tools.apps.grapher.scripts import gpCore
from lib.system.scripts import procFile as pFile


class MenuCmds(object):

    def __init__(self, mainUi):
        """ @param mainUi: Grapher ui object (QMainWindow)
            @type mainUi: object """
        self.mainUi = mainUi
        self.graphTree = self.mainUi.twGraph
        self.env = gpCore.GrapherEnv()
        self.style = gpCore.GrapherStyle()

    #========================================= MENU FILE ==========================================#

    def _addToRecentFile(self, gpFile):
        """ Add Loaded or saved graph file to recent files
            @param gpFile: Graph file absolut path
            @type gpFile: str """
        label = os.path.dirname(gpFile)
        if not label in self.mainUi.GP_recentFiles:
            qPath = QtCore.QUrl.fromLocalFile(label)
            self.mainUi.GP_recentFiles.insert(0, qPath)

    def loadGraph(self, graphFile):
        """ Command launch when miLoadGraph is clicked
            @param graphFile: Graph File absolut path
            @type graphFile: str """
        graphDict = gpCore.Grapher(**{}).readGraph(graphFile)
        self.mainUi._initInternalAttr(init=False, gpFile=graphFile)
        #-- Load Global Notes --#
        self.mainUi.teGlobalNotes.clear()
        self.mainUi.teGlobalNotes.append('\n'.join(graphDict['gp_globalNotes']))
        #-- Load Global Var --#
        self.mainUi.twGlobalVar.varList = graphDict['gp_globalVar']
        self.mainUi.rf_globalVarTree()
        self.mainUi.twGraph.rootList = graphDict['gp_graphRootList']
        self.mainUi.twGraph.nodeList = graphDict['gp_graphNodeList']
        self.mainUi.rf_graphTree()
        self._addToRecentFile(graphFile)
        self.mainUi.setWindowTitle("Grapher - %s" % os.path.basename(graphFile))

    def saveGraph(self):
        """ Command launch when miSaveGraph is clicked """
        graphFile = self.mainUi.GP_ABSPATH
        graphDict = gpCore.GetGrapher(self.mainUi).uiToDict
        gpCore.Grapher(**graphDict).writeGraph(graphFile)
        self.mainUi._initInternalAttr(init=False, gpFile=graphFile)
        self._addToRecentFile(graphFile)

    def saveGraphAs(self, selFile):
        """ Command launch when miSaveGraphAs is clicked
            @param selFile: Graph File absolut path
            @type selFile: str """
        filePath = os.sep.join(selFile.split(os.sep)[0:-1])
        fileName = selFile.split(os.sep)[-1]
        if not fileName.startswith('gp_'):
            fileName = "gp_%s" % fileName
        if not fileName.endswith('.py'):
            fileName = "%s.py" % fileName
        graphFile = os.path.join(filePath, fileName)
        graphDict = gpCore.GetGrapher(self.mainUi).uiToDict
        gpCore.Grapher(**graphDict).writeGraph(graphFile)
        self.mainUi._initInternalAttr(init=False, gpFile=graphFile)
        self._addToRecentFile(graphFile)
        self.mainUi.setWindowTitle("Grapher - %s" % os.path.basename(graphFile))

    #======================================== MENU GRAPH ==========================================#

    def newNode(self, nodeType):
        """ Create new graph node
            @param nodeType: New graphNode type ('modul', 'sysData', 'cmdData', 'purData', 'loop')
            @type nodeType: str """
        selNodes = self.graphTree.selectedItems()
        if selNodes:
            for node in selNodes:
                nodeName = self.getNewNodeName(nodeType)
                nodePath = "%s/%s" % (node.nodePath, nodeName)
                self.graphTree.nodeList[nodeName] = self.getNewNodeDict(node.nodeName, nodeName,
                                                                        nodePath, nodeType,
                                                                        node.nodeIndex+1)
                node.nodeChildren.append(nodeName)
                node.nodeExpanded = True
                self.graphTree.nodeList[node.nodeName]['nodeExpanded'] = True
        else:
            nodeName = self.getNewNodeName(nodeType)
            nodePath = "/%s" % nodeName
            self.graphTree.rootList.append(nodeName)
            self.graphTree.nodeList[nodeName] = self.getNewNodeDict(None, nodeName, nodePath,
                                                                    nodeType, 0)

    def delSelNodes(self):
        """ Remove selected graphNodes """
        delList = self.getAllChildren
        #-- Delete nodes from tree graph --#
        for node in delList:
            if node in self.graphTree.rootList:
                self.graphTree.rootList.remove(node)
            if node in self.graphTree.nodeList:
                del self.graphTree.nodeList[node]
        #-- Update children list --#
        rmList = []
        for item in self.graphTree.nodeList:
            children = self.graphTree.nodeList[item]['nodeChildren']
            for child in children:
                if child in delList:
                    rmList.append("%s___%s" % (item, child))
        for c in rmList:
            self.graphTree.nodeList[c.split('___')[0]]['nodeChildren'].remove(c.split('___')[1])

    def expandAll(self):
        """ Expand all graph node """
        allItems = gpCore.getAllItems(self.graphTree)
        for item in allItems:
            if item.nodeChildren:
                self._expandItem(item)
        self.graphTree.expandAll()

    def expandBranch(self):
        """ Expand selected branch """
        for item in self.getBranch:
            if item.nodeChildren:
                self._expandItem(item)

    def expandActif(self):
        """ Expand actif graph node """
        allItems = gpCore.getAllItems(self.graphTree)
        for item in allItems:
            if item.nodeChildren:
                if item.nodeActive:
                    self._expandItem(item)

    def expandInactif(self):
        """ Expand inactif graph node """
        allItems = gpCore.getAllItems(self.graphTree)
        for item in allItems:
            if item.nodeChildren:
                if not item.nodeActive:
                    self._expandItem(item)

    def collapseAll(self):
        """ Collapse all graph node """
        allItems = gpCore.getAllItems(self.graphTree)
        for item in allItems:
            if item.nodeChildren:
                self._collapseItem(item)
        self.graphTree.collapseAll()

    def collapseBranch(self):
        """ Collapse selected branch """
        for item in self.getBranch:
            if item.nodeChildren:
                self._collapseItem(item)

    def collapseActif(self):
        """ Collapse actif graph node """
        allItems = gpCore.getAllItems(self.graphTree)
        for item in allItems:
            if item.nodeChildren:
                if item.nodeActive:
                    self._collapseItem(item)

    def collapseInactif(self):
        """ Collapse inactif graph node """
        allItems = gpCore.getAllItems(self.graphTree)
        for item in allItems:
            if item.nodeChildren:
                if not item.nodeActive:
                    self._collapseItem(item)

    def storeNodeToBuffer(self, mode, cpType):
        """ Store selected graph node to buffer
            @param mode: Buffer mode ('copy' or 'move')
            @type mode: str
            @param cpType: Buffer type ('node' or 'branch')
            @type cpType: str """
        selItems = self.graphTree.selectedItems()
        if selItems:
            nodeList = {}
            rootList = []
            if cpType == 'node':
                for item in selItems:
                    nodeList[item.nodeName] = self.graphTree.nodeList[item.nodeName]
            elif cpType == 'branch':
                for item in selItems:
                    rootList.append(item.nodeName)
                allChild = self.getAllChildren
                for node in allChild:
                    nodeList[node] = self.graphTree.nodeList[node]
            txt = ["gp_mode = %r" % mode, "gp_cpType = %r" % cpType,
                   "gp_rootList = %s" % rootList, "gp_nodeList = %s" % nodeList]
            cpBuffer = os.path.join(grapher.libPath, 'users', grapher.user, 'tmp', 'cpBuffer.py')
            pFile.writeFile(cpBuffer, '\n'.join(txt), add=False)

    def pasteBufferToNode(self):
        """ Paste buffer to seleted graph node """
        if not self.mainUi.GP_LOCK:
            selItems = self.graphTree.selectedItems()
            maxInd = self.style.graphZoneColumns/3
            if selItems:
                cpBuffer = os.path.join(grapher.libPath, 'users', grapher.user, 'tmp', 'cpBuffer.py')
                buffer = {}
                execfile(cpBuffer, buffer)
                #-- Cut Nodes --#
                if buffer['gp_mode'] == 'move':
                    self._cutNodes(buffer)
                self.mainUi.rf_graphTree()
                for item in selItems:
                    #-- Copy Nodes --#
                    if buffer['gp_cpType'] == 'node':
                        self._copyNodes(buffer, maxInd, item)
                        self.mainUi.rf_graphTree()
                    #-- Copy Branch --#
                    elif buffer['gp_cpType'] == 'branch':
                        self._copyTopBanch(buffer, item)
                        self._copyChildBranch(buffer, maxInd)
        else:
            print "!!! WARNING: Can not edit a read only graph !!!"

    def moveNode(self, side):
        """ Move selected nodes up or down
            @param side: Move direction ('up' or 'down')
            @type side: str """
        selItems = self.graphTree.selectedItems()
        if len(selItems) == 1:
            selNodes = []
            for n, node in enumerate(selItems):
                selNodes.append(node.nodeName)
                parent = node.nodeParent
                curInd = self.graphTree.nodeList[parent]['nodeChildren'].index(node.nodeName)
                if side == 'up':
                    if curInd > (0 + n):
                        newInd = curInd - 1
                        self.graphTree.nodeList[parent]['nodeChildren'].pop(curInd)
                        self.graphTree.nodeList[parent]['nodeChildren'].insert(newInd, node.nodeName)
                elif side == 'down':
                    if curInd <= (len(selItems) - n):
                        newInd = curInd + 1
                        self.graphTree.nodeList[parent]['nodeChildren'].pop(curInd)
                        self.graphTree.nodeList[parent]['nodeChildren'].insert(newInd, node.nodeName)
            self.mainUi.rf_graphTree()
            self._reselectNodes(selNodes)

    def _expandItem(self, item):
        """ Expand given QTreeWidgetItem
            @param item: QTreeWidgetItem to expand
            @type item: object """
        item.setExpanded(True)
        item.nodeExpanded = True
        item.expandObject.setText("-")
        self.graphTree.nodeList[item.nodeName]['nodeExpanded'] = True

    def _collapseItem(self, item):
        """ Collapse given QTreeWidgetItem
            @param item: QTreeWidgetItem to expand
            @type item: object """
        if item.nodeChildren:
            item.setExpanded(False)
            item.nodeExpanded = False
            item.expandObject.setText("+")
            self.graphTree.nodeList[item.nodeName]['nodeExpanded'] = False

    def _reselectNodes(self, selNodes):
        """ Reselect last graph node selection
            @param selNodes: Selected graph node list
            @type selNodes: list """
        allItems = QtGui.QTreeWidgetItemIterator(self.graphTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None:
            while allItems.value():
                item = allItems.value()
                if item.nodeName in selNodes:
                    item.setSelected(True)
                allItems += 1

    def _clickedNode(self, node):
        """ Command launch when a graph node is selected
            @param node: Tree node item (QTreeWidgetItem)
            @type node: object """
        allItems = QtGui.QTreeWidgetItemIterator(self.graphTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None :
            while allItems.value():
                item = allItems.value()
                if item.nodeName == node.nodeName:
                    item.setSelected(True)
                else:
                    item.setSelected(False)
                allItems += 1

    def _cutNodes(self, buffer):
        """ Cut nodes in buffer list
            @param buffer: Copy / Paste buffer
            @type buffer: dict """
        for node in buffer['gp_nodeList']:
            parent = self.graphTree.nodeList[node]['nodeParent']
            ind = self.graphTree.nodeList[parent]['nodeChildren'].index(node)
            self.graphTree.nodeList[parent]['nodeChildren'].pop(ind)
        for node in buffer['gp_nodeList']:
            self.graphTree.nodeList.pop(node)

    def _copyNodes(self, buffer, maxInd, item):
        """ Copy nodes in buffer list
            @param buffer: Copy / Paste buffer
            @type buffer: dict
            @param maxInd: Max index
            @type maxInd: int
            @param item: Parent QTreeWidgetItem
            @type item: object """
        for n in range(maxInd):
            for node in buffer['gp_nodeList']:
                if buffer['gp_nodeList'][node]['nodeIndex'] == n:
                    pasteDict = self.getNewCpNodeDict(buffer, item, node)
                    self.graphTree.nodeList[pasteDict['nodeName']] = pasteDict
                    self.graphTree.nodeList[item.nodeName]['nodeChildren'].append(pasteDict['nodeName'])
                    self.graphTree.nodeList[item.nodeName]['nodeExpanded'] = True

    def _copyTopBanch(self, buffer, item):
        """ Copy branch top nodes in buffer list
            @param buffer: Copy / Paste buffer
            @type buffer: dict
            @param item: Parent QTreeWidgetItem
            @type item: object """
        for node in buffer['gp_rootList']:
            pasteDict = self.getNewCpNodeDict(buffer, item, node)
            self.graphTree.nodeList[pasteDict['nodeName']] = pasteDict
            self.graphTree.nodeList[item.nodeName]['nodeChildren'].append(pasteDict['nodeName'])
            self.graphTree.nodeList[item.nodeName]['nodeExpanded'] = True
            for child in buffer['gp_nodeList'][node]['nodeChildren']:
                buffer['gp_nodeList'][child]['nodeParent'] = pasteDict['nodeName']
            self.mainUi.rf_graphTree()

    def _copyChildBranch(self, buffer, maxInd):
        """ Copy branch child nodes in buffer list
            @param buffer: Copy / Paste buffer
            @type buffer: dict
            @param maxInd: Max index
            @type maxInd: int """
        for n in range(maxInd):
            for node in buffer['gp_nodeList']:
                if not node in buffer['gp_rootList'] and buffer['gp_nodeList'][node]['nodeIndex'] == n:
                    item = gpCore.GetGrapher(self.mainUi).getObjFromName(buffer['gp_nodeList'][node]['nodeParent'])
                    pasteDict = self.getNewCpNodeDict(buffer, item, node)
                    self.graphTree.nodeList[pasteDict['nodeName']] = pasteDict
                    self.graphTree.nodeList[item.nodeName]['nodeChildren'].append(pasteDict['nodeName'])
                    self.graphTree.nodeList[item.nodeName]['nodeExpanded'] = True
                    for child in buffer['gp_nodeList'][node]['nodeChildren']:
                        buffer['gp_nodeList'][child]['nodeParent'] = pasteDict['nodeName']
                    self.mainUi.rf_graphTree()

    def getNewNodeName(self, nodeType):
        """ Get new graph node name
            @param nodeType: Graph node type ('modul', 'sysData', 'cmdData', 'purData', 'loop')
            @type nodeType: str
            @return: New graph node name
            @rtype: str """
        index = 0
        for node in self.graphTree.nodeList:
            if node.startswith('new_%s_' % nodeType):
                ind = int(node.split('_')[-1])
                if ind > index:
                    index = ind
        return "new_%s_%s" % (nodeType, str(index+1))

    def getNewCpNodeName(self, nodeName):
        """ Get new graph node buffer name
            @param nodeName: Graph node name
            @type nodeType: str
            @return: New graph node name
            @rtype: str """
        if not '_' in nodeName:
            return "%s_1" % nodeName
        else:
            if not nodeName.split('_')[-1].isdigit():
                return "%s_1" % nodeName
            else:
                baseName = '_'.join(nodeName.split('_')[:-1])
                inds = []
                for tmpItem in self.graphTree.nodeList:
                    if self.graphTree.nodeList[tmpItem]['nodeName'].startswith('%s_' % baseName):
                        if tmpItem.split('_')[-1].isdigit():
                            inds.append(tmpItem.split('_')[-1])
                if not inds:
                    return nodeName
                else:
                    return "%s_%s" % ('_'.join(nodeName.split('_')[:-1]), int(max(inds))+1)

    def getNewNodeDict(self, parent, nodeName, nodePath, nodeType, nodeIndex):
        """ Init new graph node dict
            @param parent: Parent node name
            @type parent: str
            @param nodeName: New node name
            @type nodeName: str
            @param nodePath: New node graph path
            @type nodePath: str
            @param nodeType: New node type
            @type nodeType: str
            @param nodeIndex: New node index
            @type nodeIndex: int
            @return: New node dict
            @rtype: dict """
        nodeDict = {'nodeParent': parent, 'nodeChildren': [], 'nodePath': nodePath,
                    'nodeIndex': nodeIndex, 'nodeActive': True, 'nodeName': nodeName,
                    'nodeType': nodeType, 'nodeExpanded': False,
                    'nodeVersions': ['001'], 'nodeVersion': '001',
                    'nodeVTitle' : {'001': self.style.defaultVersionTitle},
                    'nodeNotes': {'001': self.style.defaultNotes}, 'nodeVarList': {'001': []},
                    'nodeRemote': {'wait': True, 'delay': 2, 'machines': []},
                    'nodeLoop': {'mode': 'range', 'iter': 'i', 'tmpFile': 'tmpCheck',
                                 'range': ['1', '100', '1'], 'list': '', 'single': 1},
                    'nodeCmds': self.env.grapherEnv, 'nodeCmd': {'001': 'mayaBatch'},
                    'nodeCmdOpt': {'001': ''}, 'nodeScript': {'001': []},
                    'nodeTrash': {'001': self.style.defaultTrash}}
        return nodeDict

    def getNewCpNodeDict(self, buffer, item, node, nodeType=None):
        """ Edit buffer graph dict
            @param buffer: Buffer cp node list
            @type buffer: list
            @param item: Selected QTreeWidgetItem graph node
            @type item: object
            @param node: Buffer node nade
            @type node: str
            @keyword nodeType: Item branch type ('None', 'top', 'child')
            @type nodeType: str
            @return: Edited paste dict
            @rtype: dict """
        pasteDict = {}
        for k, v in buffer['gp_nodeList'][node].iteritems():
            if k.startswith('node'):
                if k == 'nodeParent':
                    if nodeType is None or nodeType == 'top':
                        v = item.nodeName
                elif k == 'nodeChildren':
                    v = []
                elif k == 'nodePath':
                    v = '%s/%s' % (item.nodePath, self.getNewCpNodeName(node))
                elif k == 'nodeIndex':
                    v = int(item.nodeIndex) + 1
                elif k == 'nodeName':
                    v = self.getNewCpNodeName(node)
                pasteDict[k] = v
        return pasteDict

    def _verifNewNodeName(self, newNodeName):
        """ Check new node name validity
            @param newNodeName: New node name
            @type newNodeName: str
            @return: Verif state
            @rtype: bool """
        allItems = QtGui.QTreeWidgetItemIterator(self.graphTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None:
            while allItems.value():
                item = allItems.value()
                if item.nodeName == newNodeName:
                    return False
                allItems += 1
        return True

    def _replaceRootList(self, graphNode, newNodeName):
        """ Replace root list name
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param newNodeName: New node name
            @type newNodeName: str """
        if graphNode.nodeName in self.graphTree.rootList:
            ind = self.graphTree.rootList.index(graphNode.nodeName)
            self.graphTree.rootList.pop(ind)
            self.graphTree.rootList.insert(ind, newNodeName)

    def _replaceParentChildren(self, graphNode, newNodeName):
        """ Replace children list of parent node
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param newNodeName: New node name
            @type newNodeName: str """
        getGrapher = gpCore.GetGrapher(self.mainUi)
        if graphNode.nodeParent is not None:
            parent = graphNode.nodeParent
            ind = self.graphTree.nodeList[parent]['nodeChildren'].index(graphNode.nodeName)
            self.graphTree.nodeList[parent]['nodeChildren'].pop(ind)
            self.graphTree.nodeList[parent]['nodeChildren'].insert(ind, newNodeName)
            parentNode = getGrapher.getObjFromName(parent)
            parentNode.nodeChildren = self.graphTree.nodeList[parent]['nodeChildren']

    def _replaceChildrenParent(self, graphNode, newNodeName):
        """ Replace parent of node children list
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param newNodeName: New node name
            @type newNodeName: str """
        getGrapher = gpCore.GetGrapher(self.mainUi)
        for child in graphNode.nodeChildren:
            self.graphTree.nodeList[child]['nodeParent'] = newNodeName
            childNode = getGrapher.getObjFromName(child)
            childNode.nodeParent = newNodeName
        for child in self.getAllChildren:
            childPath = self.graphTree.nodeList[child]['nodePath']
            self.graphTree.nodeList[child]['nodePath'] = childPath.replace(graphNode.nodeName,
                                                                           newNodeName)
            childNode = getGrapher.getObjFromName(child)
            childNode.nodePath = childPath.replace(graphNode.nodeName, newNodeName)

    def _replaceNodeName(self, graphNode, newNodeName):
        """ Replace parent of node children list
            @param graphNode: Selected treeNode (QTreeWidgetItem)
            @type graphNode: object
            @param newNodeName: New node name
            @type newNodeName: str """
        self.graphTree.nodeList[newNodeName] = self.graphTree.nodeList.pop(graphNode.nodeName)
        self.graphTree.nodeList[newNodeName]['nodeName'] = newNodeName
        path = graphNode.nodePath
        self.graphTree.nodeList[newNodeName]['nodePath'] = path.replace(graphNode.nodeName, newNodeName)
        graphNode.nodePath = path.replace(graphNode.nodeName, newNodeName)
        graphNode.nodeName = newNodeName

    #========================================= MENU HELP ==========================================#

    @property
    def printInternalVar(self):
        """ Print grapher internal variables
            @return: Grapher internal var
            @rtype: str """
        txtHelp = ["// ", "// ##### HELP: GRAPHER INTERNAL VAR #####",
                   "// Graph Name: GP_NAME = %s" % self.mainUi.GP_NAME,
                   "// Graph File: GP_FILENAME = %s" % self.mainUi.GP_FILENAME,
                   "// Graph Dir: GP_DIRPATH = %s" % self.mainUi.GP_DIRPATH,
                   "// Graph Path: GP_ABSPATH = %s" % self.mainUi.GP_ABSPATH,
                   "// Graph Lock: GP_LOCK = %s" % self.mainUi.GP_LOCK,
                   "// Graph Lock File: GP_LOCKFILE = %s" % self.mainUi.GP_LOCKFILE,
                   "// ", "// ##### HELP: GRAPHER ENV #####"]
        env = self.env.grapherEnv
        for k, v in env.iteritems():
            txtHelp.append("// Graph %r env: %s" % (k, v))
        return "\n".join(txtHelp)

    @property
    def printGraphDict(self):
        """ Print grapher contents
            @return: Grapher text convertion
            @rtype: str """
        graphDict = gpCore.GetGrapher(self.mainUi).uiToDict
        txtHelp = ["// ", "// ##### HELP: GRAPHER DICT #####",
                   "// #-- Global Notes --#"]
        for line in graphDict['gp_globalNotes']:
            txtHelp.append("// %s" % line)
        txtHelp.append("// #-- Global Variables --#")
        for gpVar in graphDict['gp_globalVar']:
            txtHelp.append("// %s" % str(gpVar))
        txtHelp.append("// #-- Graph Zone --#")
        txtHelp.append("// Root List: %s" % graphDict['gp_graphRootList'])
        txtHelp.append("// Node List:")
        if graphDict['gp_graphNodeList']:
            for k, v in sorted(graphDict['gp_graphNodeList'].items()):
                key = "// %s: {" % k
                txtHelp.append(key)
                space = "%s" % (" "*(len(key)-1))
                for nk, nv in sorted(graphDict['gp_graphNodeList'][k].items()):
                    txtHelp.append("%s %s: %s" % (space, nk, nv))
                txtHelp.append("%s}" % space)
        return "\n".join(txtHelp)

    #=========================================== EXTRA ============================================#

    @property
    def getAllChildren(self):
        """ Store all children of selected node
            @return: Graph node list
            @rtype: list """
        selItems = self.graphTree.selectedItems()
        gpPaths = []
        childList = []
        #-- Store selected items to delete --#
        for item in selItems:
            gpPaths.append(item.nodePath)
            childList.append(item.nodeName)
        allItems = QtGui.QTreeWidgetItemIterator(self.graphTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        #-- Store all descendent of selected items --#
        if allItems is not None:
            while allItems.value():
                item = allItems.value()
                for path in gpPaths:
                    if item.nodePath.startswith('%s/' % path):
                        childList.append(item.nodeName)
                allItems += 1
        return childList

    @property
    def getBranch(self):
        """ Get QTreeWidgetItem child
            @return: Graph node QTreeWidgetItem list
            @rtype: list """
        selItems = self.graphTree.selectedItems()
        gpPaths = []
        childList = []
        #-- Store selected items to delete --#
        for item in selItems:
            gpPaths.append(item.nodePath)
            childList.append(item)
        allItems = QtGui.QTreeWidgetItemIterator(self.graphTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        #-- Store all descendent of selected items --#
        if allItems is not None:
            while allItems.value():
                item = allItems.value()
                for path in gpPaths:
                    if item.nodePath.startswith('%s/' % path):
                        childList.append(item)
                allItems += 1
        return childList


class VarSection(object):

    @staticmethod
    def addVar(varTree):
        """ Add variable to specified variable section
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        ind = len(varTree.varList)
        var = {'index': ind, 'active': True, 'type': 0,
               'label': '',  'value': '', 'comment': ''}
        varTree.varList.append(var)

    @staticmethod
    def delVar(varTree):
        """ Delete seleted variables from specified variable section
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        selInd = []
        for item in varTree.selectedItems():
            ind = item.varIndex
            selInd.append(ind)
        selInd.sort(reverse=True)
        for ind in selInd:
            for var in varTree.varList:
                if var['index'] == ind:
                    varTree.varList.pop(ind)

    @staticmethod
    def upVar(varTree):
        """ Move up selected variables from specified variable section
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object
            @return: QTreeWidgetItem index list
            @rtype: list """
        newInds = []
        for n, item in enumerate(varTree.selectedItems()):
            ind = item.varIndex
            for var in varTree.varList:
                if var['index'] == ind:
                    selVar = var
                    newInd = ind-1
                    if newInd >= n:
                        varTree.varList.pop(ind)
                        varTree.varList.insert(newInd, selVar)
                        newInds.append(newInd)
        return newInds

    @staticmethod
    def dnVar(varTree):
        """ Move down selected variables from specified variable section
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object
            @return: QTreeWidgetItem index list
            @rtype: list """
        selInd = []
        for item in varTree.selectedItems():
            ind = item.varIndex
            selInd.append(ind)
        newInds = []
        for n, item in enumerate(varTree.selectedItems()):
            for ind in selInd:
                for var in varTree.varList:
                    if var['index'] == ind:
                        selVar = var
                        newInd = ind+1
                        if newInd < varTree.topLevelItemCount():
                            varTree.varList[newInd]['index'] = ind
                            varTree.varList[ind]['index'] = newInd
                            varTree.varList.pop(ind)
                            varTree.varList.insert(newInd, selVar)
                            newInds.append(newInd)
        return newInds

    @staticmethod
    def _reindexFromOrder(varTree):
        """ Reindex QTreeWidgetItem from tree order
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object """
        for n in range(varTree.topLevelItemCount()):
            varTree.varList[n]['index'] = n
            item = varTree.topLevelItem(n)
            item.varIndex = n

    @staticmethod
    def _reselect(varTree, newInds):
        """ Reselect Last selected items
            @param varTree: Variable tree object (QTreeWidget)
            @type varTree: object
            @param newInds: List of moved index
            @type newInds: list """
        for n in range(varTree.topLevelItemCount()):
            if varTree.varList[n]['index'] in newInds:
                varTree.topLevelItem(n).setSelected(True)


class PopulateVarTree(object):

    def __init__(self, twTree):
        """ @param twTree: Variable tree zone (QTreeWidget)
            @type twTree: object """
        self.twTree = twTree

    def populate(self):
        """ Add item to QTreeWidget """
        for var in self.twTree.varList:
            newItem = self.newTreeNode(var)
            newActive = self.newCheckBox(var, newItem)
            newLabel = self.newLineEdit(var, 'label', newItem)
            newType = self.newComboBox(var, newItem)
            newValue = self.newLineEdit(var, 'value', newItem)
            newComment = self.newLineEdit(var, 'comment', newItem)
            self.twTree.addTopLevelItem(newItem)
            self.twTree.setItemWidget(newItem, 1, newActive)
            self.twTree.setItemWidget(newItem, 2, newLabel)
            self.twTree.setItemWidget(newItem, 3, newType)
            self.twTree.setItemWidget(newItem, 4, newValue)
            self.twTree.setItemWidget(newItem, 5, newComment)
            newItem.varActive = newActive
            newItem.varLabel = newLabel
            newItem.varType = newType
            newItem.varValue = newValue
            newItem.varComment = newComment

    @staticmethod
    def newTreeNode(var):
        """ Add QTreeWidgetItem
            @param var: Variable params
            @type var: dict
            @return: New QtreeWidgetItem (QTreeWidgetItem)
            @rtype: object """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, str(var['index']))
        newItem.varIndex = var['index']
        return newItem

    def newCheckBox(self, var, parent):
        """ Add QChecBox to new QTreeWidgetItem
            @param var: Variable params
            @type var: dict
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QCheckBox (QCheckBox)
            @rtype: object """
        newActive = QtGui.QCheckBox()
        newActive.setChecked(var['active'])
        newActive.varParent = parent
        newActive.clicked.connect(partial(self.on_active, newActive))
        return newActive

    def newLineEdit(self, var, zone, parent):
        """ Add QLineEdit to new QTreeWidgetItem
            @param var: Variable params
            @type var: dict
            @param zone: 'label' or 'value' or 'comment'
            @type zone: str
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QLineEdit (QLineEdit)
            @rtype: object """
        newText = QtGui.QLineEdit()
        newText.setText(var[zone])
        newText.varParent = parent
        newText.varZone = zone
        newText.editingFinished.connect(partial(self.on_lineEdit, newText, zone))
        return newText

    def newComboBox(self, var, parent):
        """ Add QComboBox to new QTreeWidgetItem
            @param var: (dict) : Variable params
            @type var: dict
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QComboBox (QComboBox)
            @rtype: object """
        newChoice = QtGui.QComboBox()
        newChoice.addItems([' = ', ' + '])
        newChoice.setCurrentIndex(var['type'])
        newChoice.varParent = parent
        newChoice.currentIndexChanged.connect(partial(self.on_type, newChoice))
        return newChoice

    def on_active(self, checkBox):
        """ Command launch when QCheckBox of selected QTreeWidgetItem is clicked
            @param checkBox: Current edited checkBox (QCheckBox)
            @type checkBox: object """
        checkBox.varParent.varLabel.setEnabled(checkBox.isChecked())
        checkBox.varParent.varType.setEnabled(checkBox.isChecked())
        checkBox.varParent.varValue.setEnabled(checkBox.isChecked())
        checkBox.varParent.varComment.setEnabled(checkBox.isChecked())
        for var in self.twTree.varList:
            if var['index'] == checkBox.varParent.varIndex:
                var['active'] = checkBox.isChecked()

    def on_lineEdit(self, lineEdit, zone):
        """ Command launch when QLineEdit of selected QTreeWidgetItem has changed
            @param lineEdit: Current edited line (QLineEdit)
            @type lineEdit: object
            @param zone: 'label' or 'value' or 'comment'
            @type zone: str """
        for var in self.twTree.varList:
            if var['index'] == lineEdit.varParent.varIndex:
                var[zone] = str(lineEdit.text())

    def on_type(self, comboBox):
        """ Command launch when QComboBox of selected QTreeWidgetItem is clicked
            @param comboBox: Current edited comboBox(QComboBox)
            @type comboBox: object """
        for var in self.twTree.varList:
            if var['index'] == comboBox.varParent.varIndex:
                var['type'] = comboBox.currentIndex()


class PopulateGraphTree(object):

    def __init__(self, mainUi):
        """ @param mainUi: Grapher ui object (QMainWindow)
            @type mainUi: object """
        self.mainUi = mainUi
        self.twTree = self.mainUi.twGraph
        self.style = gpCore.GrapherStyle()

    def populate(self):
        """ Add item to QTreeWidget """
        self.populateRoot()
        self.populateChildren()

    def populateRoot(self):
        """ Add top level items """
        for root in self.twTree.rootList:
            newItem = QtGui.QTreeWidgetItem()
            for k, v in self.twTree.nodeList[root].iteritems():
                if k.startswith('node'):
                    setattr(newItem, k, v)
            self.twTree.addTopLevelItem(newItem)
            self.addWidget(newItem, 'top')
            newItem.setExpanded(newItem.nodeExpanded)

    def populateChildren(self):
        """ Add child items """
        maxInd = self.style.graphZoneColumns/3
        for n in range(maxInd):
            for node in self.twTree.nodeList:
                if self.twTree.nodeList[node]['nodeIndex'] == n:
                    for child in self.twTree.nodeList[node]['nodeChildren']:
                        newItem = QtGui.QTreeWidgetItem()
                        for k, v in self.twTree.nodeList[child].iteritems():
                            if k.startswith('node'):
                                setattr(newItem, k, v)
                        treeNode = gpCore.GetGrapher(self.mainUi).getObjFromName(node)
                        treeNode.addChild(newItem)
                        newItem = self.addWidget(newItem, 'child')
                        newItem.setExpanded(newItem.nodeExpanded)

    def addWidget(self, newItem, itemType):
        """ Add widget to new QTreeWidgetItem
            @param newItem: New graph node object (QTreeWidgetItem)
            @type newItem: object
            @param itemType: New graph node type('top' or 'child')
            @type itemType: str
            @return: New graph node object (QTreeWidgetItem)
            @rtype: object """
        newActive = self.newCheckBox(newItem)
        newButton = self.newButton(newItem)
        if itemType == 'top':
            self.twTree.setItemWidget(newItem, 0, newActive)
            self.twTree.setItemWidget(newItem, 1, newButton)
        elif itemType == 'child':
            self.twTree.setItemWidget(newItem, newItem.nodeIndex*3, newActive)
            self.twTree.setItemWidget(newItem, (newItem.nodeIndex*3)+1, newButton)
        newItem.activeObject = newActive
        newItem.buttonObject = newButton
        if newItem.nodeChildren:
            newExpand = self.newExpandBtn(newItem)
            if itemType == 'top':
                self.twTree.setItemWidget(newItem, 2, newExpand)
            elif itemType == 'child':
                self.twTree.setItemWidget(newItem, (newItem.nodeIndex*3)+2, newExpand)
            newItem.expandObject = newExpand
        return newItem

    def newCheckBox(self, parent):
        """ Add QChecBox to new QTreeWidgetItem
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QCheckBox (QCheckBox)
            @rtype: object """
        newActive = QtGui.QCheckBox()
        newActive.setChecked(parent.nodeActive)
        newActive.parent = parent
        newActive.clicked.connect(partial(self.on_cbNode, parent))
        newActive.setAutoFillBackground(True)
        newActive.setStyleSheet(self.style.graphNodeBgc(parent.nodeType))
        return newActive

    def newButton(self, parent):
        """ Add QPushButton to new QTreeWidgetItem
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QPushButton (QPushButton)
            @rtype: object """
        newButton = QtGui.QPushButton()
        newButton.setText(parent.nodeName)
        newButton.parent = parent
        cmd1 = partial(self.mainUi.on_singleClick, parent)
        cmd2 = partial(self.mainUi.on_doubleClick, parent)
        click_handler = dialog.ClickHandler(150, singleClickCmd=cmd1, doubleClickCmd=cmd2)
        newButton.clicked.connect(click_handler)
        newButton.setAutoFillBackground(True)
        newButton.setStyleSheet(self.style.graphNodeBgc(parent.nodeType))
        return newButton

    def newExpandBtn(self, parent):
        """ Add expand QPushButton to new QTreeWidgetItem
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QPushButton (QPushButton)
            @rtype: object """
        newBbtn = QtGui.QPushButton()
        if parent.isExpanded:
            newBbtn.setText("-")
        else:
            newBbtn.setText("+")
        parent.setExpanded(parent.nodeExpanded)
        newBbtn.parent = parent
        newBbtn.clicked.connect(partial(self.on_expandNode, parent))
        newBbtn.setAutoFillBackground(True)
        newBbtn.setStyleSheet(self.style.graphNodeBgc(parent.nodeType))
        return newBbtn

    def on_cbNode(self, node):
        """ Command launch when a graph node QCheckBox is clicked
            @param node: Tree node item (QTreeWidgetItem)
            @type node: object """
        allItems = QtGui.QTreeWidgetItemIterator(self.twTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None :
            while allItems.value():
                item = allItems.value()
                if item.nodeName == node.nodeName:
                    state = node.activeObject.isChecked()
                    node.nodeActive = state
                    self.twTree.nodeList[node.nodeName]['nodeActive'] = state
                allItems += 1

    def on_expandNode(self, node):
        """ Expand or collapse QTreeWidgetItem
            @param node: Tree node item (QTreeWidgetItem)
            @type node: object """
        current = node.nodeExpanded
        allItems = QtGui.QTreeWidgetItemIterator(self.twTree,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None :
            while allItems.value():
                item = allItems.value()
                if item.nodeName == node.nodeName:
                    if current:
                        node.nodeExpanded = False
                        self.twTree.nodeList[node.nodeName]['nodeExpanded'] = False
                        item.setExpanded(False)
                        item.expandObject.setText("+")
                    else:
                        node.nodeExpanded = True
                        self.twTree.nodeList[node.nodeName]['nodeExpanded'] = True
                        item.setExpanded(True)
                        item.expandObject.setText("-")
                allItems += 1
