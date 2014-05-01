import os
from lib.system.scripts import procFile as pFile


class DefaultTemplate(object):
    """ Class containing all prodManager defaut attributes and params """

    @staticmethod
    def previewMaxSize():
        """ Give preview image default max size
            @return: (int) : maxWidth, (int) : maxHeight """
        return 300, 150

    @staticmethod
    def projectTreeNodeAttr(nodeType, nodeLabel, nodeName, nodePath):
        """ Get default project tree node attributes
            @param nodeType: (str) : 'container' or 'node'
            @param nodeLabel: (str) : Display node name
            @param nodeName: (str) : Id node name
            @param nodePath: (str) : Node tree path
            @return: (dict) : QTreeWidgetItem attributes """
        return {'nodeType': nodeType, 'nodeLabel': nodeLabel,
                'nodeName': nodeName, 'nodePath': nodePath}

    @staticmethod
    def projectTreeAttrs():
        """ Get Default project tree attributes
            @return: (list) : Default attributes """
        return [{'workDir': 'string'}, {'imaDir': 'string'}]


class ProjectTemplate(object):
    """ Class used to managed project params
        @param pm: (object) : prodManager instance """

    def __init__(self, pm):
        self.pm = pm
        self._projectPath = None
        self._projectFile = None

    def addProjectParams(self, **kwargs):
        """ Add given attributes and value to the class
            @param kwargs: Attributes and value params """
        for k, v in kwargs.iteritems():
            if not k.startswith('_'):
                setattr(self, k, v)

    def addTree(self, treeName, new=False):
        """ Add Tree to project
            @param treeName: (str) : New tree name (ex: 'asset', 'shot')
            @param new: (bool) : New tree from ui
            @return: (object) : New tree object """
        if '.' in treeName or 'tree' in treeName:
            print "Warning: Tree name not valid !!!"
            return None
        else:
            trees = getattr(self, 'projectTrees')
            if new:
                if treeName in trees:
                    print "Warning: Tree name already exists (%s) !!!" % treeName
                    return None
                else:
                    trees.append(treeName)
            print "Adding new tree: %sTree ..." % treeName
            setattr(self, 'projectTrees', trees)
            newTree = TreeTemplate(self.pm, treeName)
            setattr(self.pm, '%sTree' % treeName, newTree)
            if new:
                newTree.treeAttrs = [{'workDir': 'string'}]
            return newTree

    def writeProjectFile(self):
        """ Write project file """
        if not os.path.exists(self._projectFile):
            print "!!! Error: Project file absolut path doesn't exists !!!"
        else:
            txt = []
            for k in self.getParams.keys():
                if k.startswith('project'):
                    if isinstance(getattr(self, k), str):
                        txt.append("%s = %r" % (k, getattr(self, k)))
                    else:
                        txt.append("%s = %s" % (k, getattr(self, k)))
            try:
                pFile.writeFile(self._projectFile, '\n'.join(txt))
                print "Writing project file: %s--%s" % (getattr(self, 'projectName'),
                                                        getattr(self, 'projectAlias'))
            except:
                print "!!! Error: Can't write project file !!!"

    @property
    def getParams(self):
        """ Get project params and value
            @return: (dict) : Project params and value """
        params = {}
        for k, v in  self.__dict__.iteritems():
            params[k] = v
        return params

    @property
    def getTrees(self):
        """ Get project tree list
            @return: (list) : Project trees """
        params = self.getParams
        return params['projectTrees']

    def printParams(self):
        """ Print project params """
        print '#' * 100
        print "#----- PROJECT PARAMS -----#"
        for k, v in  self.getParams.iteritems():
            print k, '=', v
        print '#' * 100

    def printTasks(self):
        """ Print project tasks """
        print '#' * 100
        print "#----- PROJECT TASKS -----#"
        tasksDict = getattr(self, 'projectTasks')
        for td in tasksDict:
            print td['taskName']
        print '#' * 100


class TreeTemplate(object):
    """ Class used to managed project trees
        @param pm: (object) : prodManager instance
        @param treeName: (str) : New tree name """

    def __init__(self, pm, treeName):
        self.pm = pm
        self.treeSteps = []
        self.treeAttrs = []
        self.treeNodes = []
        self.treeOrder = []
        self._treeName = treeName
        self._treeLabel = '%sTree' % self._treeName
        self._treeFile = os.path.join(self.pm.project._projectPath, 'data', '%s.py' % self._treeLabel)

    def addNode(self, updateTreeNodes=True, **kwargs):
        """ Add new node to tree
            @param updateTreeNodes: (bool) : Update param 'treeNodes'
            @param kwargs: (dict) : New node params
                           @keyword nodeType: (str) : '$treeName' or '$treeNameCtnr'
                           @keyword nodeLabel: (str) : Display node name
                           @keyword nodeName: (str) : Id node name
                           @keyword nodePath: (str) : Node tree path
            @return: (object) : New node object if success, (bool) : False if fail """
        if self._checkNewNode(kwargs['nodePath'], kwargs['nodeName']):
            newNode = TreeNode(self, **kwargs)
            self.treeOrder.append(newNode)
            if updateTreeNodes:
                self.treeNodes.append(kwargs)
            return newNode
        else:
            return False

    def addStep(self, stepName):
        """ Append new step to tree
            @param stepName: (str) : Step name
            @return: (str) : New step if success, (bool) : False if fail """
        if self._checkNewStep(stepName):
            self.treeSteps.append(stepName)
            return stepName
        else:
            return False

    def insertStep(self, index, stepName):
        """ Insert new step in tree at given index position
            @param index: (int) : Position in the list
            @param stepName: (str) : Step name
            @return: (str) : New step if success, (bool) : False if fail """
        if self._checkNewStep(stepName):
            try:
                self.treeSteps.insert(index, stepName)
                return stepName
            except:
                print "!!! Warning: Can't insert step in list !!!"
                return False
        else:
            return False

    def addAttr(self, attrName):
        """ Append new attribute to tree
            @param attrName: (str) : Attribute name
            @return: (str) : New attribute if success, (bool) : False if fail """
        if self._checkNewAttr(attrName):
            self.treeAttrs.append(attrName)
            return attrName
        else:
            return False

    def insertAttr(self, index, attrName):
        """ Insert new step in tree at given index position
            @param index: (int) : Position in the list
            @param attrName: (str) : Attribute name
            @return: (str) : New attribute if success, (bool) : False if fail """
        if self._checkNewAttr(attrName):
            try:
                self.treeAttrs.insert(index, attrName)
                return attrName
            except:
                print "!!! Warning: Can't insert step in list !!!"
                return False
        else:
            return False

    def buildTreeFromFile(self):
        """ Build tree from given file """
        self.treeSteps = []
        self.treeAttrs = []
        self.treeNodes = []
        self.treeOrder = []
        if os.path.exists(self._treeFile):
            print "Building %s ..." % self._treeLabel
            tree = pFile.readPyFile(self._treeFile)
            self.treeSteps = tree['treeSteps']
            self.treeAttrs = tree['treeAttrs']
            for node in tree['treeNodes']:
                self.addNode(**node)

    def buildTreeFromUi(self, treeSteps, treeAttrs, treeNodes):
        """ Build tree obj from ui
            @param treeSteps: (list) : Tree step list
            @param treeAttrs: (list) : Tree attributes list
            @param treeNodes: (list) : Node dict list """
        self.treeSteps = treeSteps
        self.treeAttrs = treeAttrs
        self.treeNodes = treeNodes
        self.treeOrder = []
        for nodeDict in self.treeNodes:
            self.addNode(updateTreeNodes=False, **nodeDict)

    def writeTreeToFile(self):
        """ Write tree object to file """
        treeTxt = ["treeSteps = %s" % self.treeSteps,
                   "treeAttrs = %s" % self.treeAttrs,
                   "treeNodes = %s" % self.treeNodes]
        try:
            pFile.writeFile(self._treeFile, '\n'.join(treeTxt))
            print "Writing %s file" % self._treeLabel
        except:
            print "!!! Error: Can't write %s file !!!" % self._treeLabel

    @property
    def getParams(self):
        """ Get tree params and value
            @return: (dict) : Tree params and value """
        params = {}
        for k, v in  self.__dict__.iteritems():
            params[k] = v
        return params

    @property
    def getSteps(self):
        """ Get tree step list
            @return: (list) : Tree steps """
        params = self.getParams
        return params['treeSteps']

    @property
    def getAttrs(self):
        """ Get tree attributes list
            @return: (list) : Tree steps """
        params = self.getParams
        return params['treeAttrs']

    def printParams(self):
        """ Print tree params """
        print '#' * 100
        print "#----- %s TREE PARAMS -----#" % self._treeName.upper()
        for k, v in  self.getParams.iteritems():
            print k, '=', v
        print '#' * 100

    def printSteps(self):
        """ Print tree steps """
        print '#' * 100
        print "#----- %s TREE STEPS -----#" % self._treeName.upper()
        for step in self.getSteps:
            print step
        print '#' * 100

    def printAttrs(self):
        """ Print tree attributes """
        print '#' * 100
        print "#----- %s TREE ATTRIBUTES -----#" % self._treeName.upper()
        for attr in self.getAttrs:
            print attr
        print '#' * 100

    def _checkNewNode(self, nodePath, nodeName):
        """ Check if new node already exists
            @param nodePath: (str) : Node path
            @param nodeName: (str) : Node name
            @return: (bool) : Check state """
        for node in self.treeOrder:
            if node.nodePath == nodePath:
                print "!!! Warning: %s already exists !!!" % nodePath
                return False
            elif node.nodeName == nodeName:
                print "!!! Warning: %s already exists !!!" % nodeName
                return False
        return True

    def _checkNewStep(self, stepName):
        """ Check if new step already exists
            @param stepName: (str) : Step name
            @return: (bool) : Check state """
        for step in self.treeSteps:
            if step == stepName:
                print "!!! Warning: %s already exists !!!" % stepName
                return False
        return True

    def _checkNewAttr(self, attrName):
        """ Check if new attribute already exists
            @param attrName: (str) : Attribute name
            @return: (bool) : Check state """
        for attr in self.treeAttrs:
            if attr == attrName:
                print "!!! Warning: %s already exists !!!" % attrName
                return False
        return True


class TreeNode(object):
    """ Tree node object class
        @param tree: (object) : Parent tree template
        @param kwargs: (dict) : Default node params """

    def __init__(self, tree, **kwargs):
        self.tree = tree
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @property
    def getParams(self):
        """ Get tree node params and value
            @return: (dict) : Tree node params and value """
        params = {}
        for k, v in  self.__dict__.iteritems():
            params[k] = v
        return params

    def printParams(self):
        """ Print tree params """
        print '#' * 100
        print "#----- %s TREE NODE PARAMS -----#" % getattr(self, 'nodeName')
        for k, v in  self.getParams.iteritems():
            print k, '=', v
        print '#' * 100
