import os
from lib.system.scripts import procFile as pFile
from appli.prodManager.scripts import core as pmCore


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
    def assetSteps():
        """ Get default asset steps
            @return: (list) : Project asset steps """
        return ['design', 'modeling', 'mapping', 'rigg', 'cloth', 'hair', 'actor']

    @staticmethod
    def shotSteps():
        """ Get default shot steps
            @return: (list) : Project shot steps """
        return ['storyBord', 'animatic', 'anim', 'lighting', 'cloth', 'fx', 'compo']


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

    def printParams(self):
        """ Print project params """
        print '#' * 100
        print "#----- PROJECT PARAMS -----#"
        for k, v in  self.getParams.iteritems():
            print k, '=', v
        print '#' * 100


class TreeTemplate(object):
    """ Class used to managed project trees
        @param pm: (object) : prodManager instance
        @param treeName: (str) : New tree name """

    def __init__(self, pm, treeName):
        self.pm = pm
        self.treeNodes = []
        self.treeOrder = []
        self._treeName = treeName
        self._treeLabel = '%sTree' % self._treeName
        self._treeFile = os.path.join(self.pm.project._projectPath, 'data', '%s.py' % self._treeLabel)

    def buildTreeFromFile(self):
        """ Build tree from given file """
        self.treeNodes = []
        self.treeOrder = []
        if os.path.exists(self._treeFile):
            print "Building %s ..." % self._treeLabel
            tree = pFile.readPyFile(self._treeFile)
            self.treeNodes = tree['treeNodes']
            for node in tree['treeNodes']:
                self.treeOrder.append(TreeNode(self, **node))

    def buildTreeFromUi(self, treeNodes):
        """ Build tree obj from ui
            @param treeNodes: (list) : Node dict list """
        self.treeNodes = treeNodes
        self.treeOrder = []
        for nodeDict in self.treeNodes:
            self.treeOrder.append(TreeNode(self, **nodeDict))

    def writeTreeToFile(self):
        """ Write tree object to file """
        if pmCore.createDataPath(self._treeFile):
            treeTxt = ["treeNodes = %s" % self.treeNodes]
            try:
                pFile.writeFile(self._treeFile, '\n'.join(treeTxt))
                print "Writing %s file" % self._treeLabel
            except:
                print "!!! Error: Can't write %s file !!!" % self._treeLabel


class TreeNode(object):
    """ Tree node object class
        @param tree: (object) : Parent tree template
        @param kwargs: (dict) : Default node params """

    def __init__(self, tree, **kwargs):
        self.tree = tree
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
