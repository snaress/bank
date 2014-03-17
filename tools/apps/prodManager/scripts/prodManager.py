import os
from tools.apps import prodManager
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import procFile as pFile
from tools.apps.prodManager.scripts import core as pmCore


class ProdManager(object):
    """ Class containing all prodManager's commands for creation, loading,
        editing and writing datas in or from tool dataBase """

    def __init__(self):
        self.projectName = None
        self.projectAlias = None
        self.assetTreeFile = None
        self.assetTreeObj = TreeObj()
        self.shotTreeFile = None
        self.shotTreeObj = TreeObj()

    def newProject(self, projectName, projectAlias):
        """ Create new project in dataBase
            @param projectName: (str) : New project name
            @param projectAlias: (str) : New project alias
            @return: (str) : New project creation result, (list) : Result message """
        print "#----- Create New Project -----#"
        result = pmCore.createNewProject(projectName, projectAlias)
        if result == "error code 1":
            mess = ["#!!! Error !!!#", "Project Name or Project Alias not valid !!!",
                    "Don't use special caracter or one in the list behind :", "., -, #, ', \", space"]
        elif result == "error code 2":
            mess = ["#!!! Error !!!#", "Project already exists in dataBase !!!"]
        elif result == "error code 3":
            mess = ["#!!! Error !!!#", "Can't create folder in dataBase !!!"]
        elif result == "error code 4":
            mess = ["#!!! Error !!!#", "Can't create project file in dataBase !!!"]
        else:
            mess = ["#%s#" % ('-'*60),
                    "Project successfully created in dataBase: %s" % result,
                    "#%s#" % ('-'*60)]
        print '\n'.join(mess)
        if result == '%s--%s' % (projectName, projectAlias):
            self.loadProject(projectName, projectAlias)
        return result, mess

    def loadProject(self, projectName, projectAlias):
        """ Load project from dataBase
            @param projectName: (str) : New project name
            @param projectAlias: (str) : New project alias """
        print "#----- Load Project -----#"
        print "Loading '%s--%s' ..." % (projectName, projectAlias)
        self.projectName = projectName
        self.projectAlias = projectAlias
        self._projectPath = self.getProjectPath
        self._projectFile = os.path.join(self._projectPath, '%s--%s.py' % (projectName, projectAlias))
        projectParams = self.readFile(self._projectFile)
        self._addAttrList(**projectParams)
        self.assetTreeFile = os.path.join(self._projectPath, 'data', 'assetTree.py')
        self.shotTreeFile = os.path.join(self._projectPath, 'data', 'shotTree.py')
        self.buildTrees()
        print "'%s--%s' successfully loaded" % (projectName, projectAlias)

    @staticmethod
    def readFile(pyFile):
        """ Read given python file
            @param pyFile: (str) : Python file absolut path
            @return: (dict) : File contents """
        if os.path.exists(pyFile):
            projectParams = {}
            execfile(pyFile, projectParams)
            return projectParams
        else:
            print "!!! Error: Can't read, file doesn't exists !!!"

    def writeProjectFile(self):
        """ Write project file """
        if not hasattr(self, '_projectFile'):
            print "!!! Error: Class object doesn't have '_projectFile' attribute !!!"
        else:
            if not os.path.exists(self._projectFile):
                print "!!! Error: Project file absolut path doesn't exists !!!"
            else:
                txt = []
                for k in self.__dict__.keys():
                    if k.startswith('project'):
                        if isinstance(getattr(self, k), str):
                            txt.append("%s = %r" % (k, getattr(self, k)))
                        else:
                            txt.append("%s = %s" % (k, getattr(self, k)))
                try:
                    pFile.writeFile(self._projectFile, '\n'.join(txt))
                    print "Writing project file: %s--%s" % (self.projectName, self.projectAlias)
                except:
                    print "!!! Error: Can't write project file !!!"

    def buildTreeFromUi(self, mainUi):
        """ Build tree obj from ui
            @param mainUi: (object) : ProdManager QMainWindow """
        items = pQt.getAllItems(mainUi.twProjectTree)
        if mainUi.rbProjectAsset.isChecked():
            self.assetTreeObj = TreeObj()
            tree = self.assetTreeObj
        else:
            self.shotTreeObj = TreeObj()
            tree = self.shotTreeObj
        for item in items:
            tree.addNode(**item.__dict__)

    def buildTrees(self, force=False):
        """ Build asset and shot tree obj from file
            @param force: (bool) : Force building with reset class first """
        print "Build trees (force=%s) ..." % force
        if force:
            self.assetTreeObj = TreeObj()
            self.shotTreeObj = TreeObj()
        self.buildTreeFromFile('assetTree')
        self.buildTreeFromFile('shotTree')

    def buildTreeFromFile(self, treeType, force=False):
        """ Build given tree obj from file
            @param treeType: (str) : 'assetTree' or 'shotTree'
            @param force: (bool) : Force building with reset class first """
        treeFile = getattr(self, '%sFile' % treeType)
        if os.path.exists(treeFile):
            print "\tBuild %s object ..." % treeType
            if force:
                setattr(self, '%sObj' % treeType, TreeObj())
            treeObj = getattr(self, '%sObj' % treeType)
            treeDict = self.readFile(treeFile)
            for node in treeDict['treeOrder']:
                #-- Add _Data Params --#
                if node['nodeType'] in ['asset', 'shot']:
                    dataPath = os.path.join(self._projectPath, 'tree', node['nodeType'])
                    for fld in node['nodePath'].split('/'):
                        dataPath = os.path.join(dataPath, fld)
                    dataFile = os.path.join(dataPath, '%s.py' % node['nodeName'])
                    node['_dataPath'] = dataPath
                    node['_dataFile'] = dataFile
                    #-- Add Node Params --#
                    if os.path.exists(dataFile):
                        nodeParams = self.readFile(dataFile)
                        for k, v in nodeParams.iteritems():
                            if k.startswith('asset') or k.startswith('shot'):
                                node[k] = v
                treeObj.addNode(**node)

    def buildStepFromUi(self, mainUi):
        """ Build step attribute from ui
            @param mainUi: (object) : ProdManager QMainWindow """
        #-- Get Top Level Items --#
        topItems = pQt.getTopItems(mainUi.twProjectStep)
        stepParams = {'stepOrder': []}
        for topItem in topItems:
            stepParams['stepOrder'].append(topItem.stepLabel)
            stepParams[topItem.stepLabel] = []
        #-- Get Tree Nodes --#
        allItems = pQt.getAllItems(mainUi.twProjectStep)
        for item in allItems:
            if item.stepType == 'substep':
                stepParams[item.stepParent].append(item.stepLabel)
        #-- Update Attribute --#
        if mainUi.rbProjectAsset.isChecked():
            self.projectAssetSteps = stepParams
        else:
            self.projectShotSteps = stepParams

    def buildSteps(self):
        """ Build asset and shot step attribute from file """
        print "Build steps ..."
        self.buildStepFromFile('assetTree')
        self.buildStepFromFile('shotTree')

    def buildStepFromFile(self, treeType):
        """ Build step attribute from ui
            @param treeType: (str) : 'assetTree' or 'shotTree' """
        projectParams = self.readFile(self._projectFile)
        print "\tBuild %s steps attributes ..." % treeType
        if treeType == 'assetTree':
            self.projectAssetSteps = projectParams['projectAssetSteps']
        else:
            self.projectShotSteps = projectParams['projectShotSteps']

    def writeTrees(self):
        """ Write asset and shot treeObject file """
        self.writeTree('assetTree')
        self.writeTree('shotTree')

    def writeTree(self, treeType):
        """ Write given treeObject file
            @param treeType: (str) : 'assetTree' or 'shotTree' """
        tree = getattr(self, '%sObj' % treeType)
        treeOrder = []
        for node in tree.treeOrder:
            treeDict = {}
            for k, v in node.getParams.iteritems():
                if k.startswith('node'):
                    treeDict[k] = v
            treeOrder.append(treeDict)
        treeTxt = ["treeOrder = %s" % treeOrder]
        treeFile = getattr(self, '%sFile' % treeType)
        try:
            pFile.writeFile(treeFile, '\n'.join(treeTxt))
            print "Writing %s file" % treeType
        except:
            print "!!! Error: Can't write %s file !!!" % treeType

    @property
    def getProjectPath(self):
        """ Get project path from projectName and ProjectAlias
            @return: (str) : Project path """
        return os.path.join(prodManager.binPath, 'project',
                            '%s--%s' % (self.projectName, self.projectAlias))

    @property
    def getProjects(self):
        """ Get all projects in dataBase
            @return: (list) : Project list """
        rootPath = os.path.join(prodManager.binPath, 'project')
        projects = os.listdir(rootPath) or []
        projectList = []
        for project in projects:
            projectPath = os.path.join(rootPath, project)
            if not project.startswith('.') and not project.startswith('_') and os.path.isdir(projectPath):
                projectList.append(project)
        return projectList

    def printProjects(self):
        """ Print projects in dataBase """
        print "#" * 60
        print "#-- Project List --#"
        for project in self.getProjects:
            print project
        print "#" * 60

    def printDict(self):
        """ Print class object dict """
        print "#" * 60
        print "#-- Project Dict --#"
        for k in sorted(self.__dict__.keys()):
            if not k.startswith('__'):
                if isinstance(getattr(self, k), str):
                    print "%s = %r" % (k, getattr(self, k))
                else:
                    print "%s = %s" % (k, getattr(self, k))
        print "#" * 60

    def _addAttrList(self, **kwargs):
        """ Add given attributes and value to the class
            @param kwargs: Attributes and value params """
        for k, v in kwargs.iteritems():
            if not k.startswith('_'):
                setattr(self, k, v)

    def _reset(self):
        """ Reset class """
        print "#----- Reset Class -----#"
        #-- Reset Attr --#
        for attr in ['projectName', 'projectAlias', 'assetTreeFile', 'shotTreeFile']:
            setattr(self, attr, None)
        self.assetTreeObj = TreeObj()
        self.shotTreeObj = TreeObj()
        #-- Remove Attr --#
        for attr in ['projectStart', 'projectEnd', 'projectWorkDir', '_projectPath',
                     '_projectFile', 'projectAssetSteps', 'projectShotSteps']:
            delattr(self, attr)


class TreeObj(object):
    """ Tree object class """

    def __init__(self):
        self.treeOrder = []

    def addNode(self, **kwargs):
        """ Add new node to tree
            @param kwargs: New node params
            @return: (bool) : Check state """
        if self._checkNewNode(kwargs['nodePath']):
            self.treeOrder.append(TreeNode(**kwargs))
            return True
        else:
            return False

    def getNodeByName(self, nodeName):
        """ Get params of given node
            @param nodeName: (str) : Asset name (ex: 'asterix') or shot name (ex: 's001_p001')
            @return: (object) : Tree Node object """
        for node in self.treeOrder:
            if node.nodeName == nodeName:
                return node

    def getNodeParams(self, nodeName):
        """ Get params of given node
            @param nodeName: (str) : Asset name (ex: 'asterix') or shot name (ex: 's001_p001')
            @return: (dict) : Node params """
        node = self.getNodeByName(nodeName)
        if node is not None:
            return node.getParams

    def printTree(self):
        """ Print given tree object """
        print "#" * 60
        print "#-- Tree Object --#"
        for node in self.treeOrder:
            Ntab = len(node.nodePath.split('/')) - 1
            print '-' * 100
            print "%s%s" % ('\t'*Ntab, node.nodePath)
            for k, v in node.getParams.iteritems():
                print "%s%s = %s" % ('\t'*(Ntab+1), k, v)
        print "#" * 60

    def _checkNewNode(self, nodePath):
        """ Check if new node already exists
            @param nodePath: (str) : Node path
            @return: (bool) : Check state """
        for node in self.treeOrder:
            if node.nodePath == nodePath:
                print "!!! Warning: %s already exists !!!" % nodePath
                return False
        return True


class TreeNode(object):
    """ Tree node object class
        @param kwargs: Node params """

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @property
    def getParams(self):
        """ Get node params
            @return: (dict) : Node params """
        params = {}
        starts = ['node', '_data', 'asset', 'shot']
        for k, v in self.__dict__.iteritems():
            check = False
            for s in starts:
                if k.startswith(s):
                    check = True
            if check:
                params[k] = v
        return params

    def getAttr(self, key):
        """ Get given attribute value
            @param key: (str) : Attribute name
            @return: Value of given attribute """
        return getattr(self, key)

    def writeNode(self):
        """ Write node params file in data base """
        if getattr(self, 'nodeType') in ['asset', 'shot']:
            dataFile = getattr(self, '_dataFile')
            check = True
            if not os.path.exists(dataFile):
                check = pmCore.createDataPath(dataFile)
            if check:
                dataTxt = []
                for k, v in self.getParams.iteritems():
                    if k.startswith('asset') or k.startswith('shot'):
                        if isinstance(k, str):
                            dataTxt.append("%s = %r" % (k, v))
                        else:
                            dataTxt.append("%s = %s" % (k, v))
                try:
                    pFile.writeFile(dataFile, '\n'.join(dataTxt))
                    print "Writing %s node" % getattr(self, 'nodeName')
                except:
                    print "!!! Error: Can't write %s node !!!" % getattr(self, 'nodeName')
        else:
            print "!!! Error: Nothing to write from containers !!!"
