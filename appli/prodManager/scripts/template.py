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
            @return: (str) : Result """
        if '.' in treeName or 'tree' in treeName:
            print "Warning: Tree name not valid !!!"
            return 'error code 1'
        else:
            trees = getattr(self, 'projectTrees')
            if new:
                if treeName in trees:
                    print "Warning: Tree name already exists (%s) !!!" % treeName
                    return 'error code 2'
                else:
                    trees.append(treeName)
            print "Adding new tree: %sTree ..." % treeName
            setattr(self, 'projectTrees', trees)
            setattr(self.pm, '%sTree' % treeName, TreeTemplate(self.pm, treeName))
            return treeName

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
        self.treeOrder = []
        self._treeName = treeName
        self._treeLabel = '%sTree' % self._treeName
        self._treeFile = os.path.join(self.pm.project._projectPath, 'data', '%s.py' % self._treeLabel)

    def writeTree(self):
        """ Write tree object to file """
        treeOrder = []
        for node in self.treeOrder:
            treeDict = {}
            for k, v in node.getParams.iteritems():
                if k.startswith('node'):
                    treeDict[k] = v
            treeOrder.append(treeDict)
        treeTxt = ["treeOrder = %s" % treeOrder]
        try:
            pFile.writeFile(self._treeFile, '\n'.join(treeTxt))
            print "Writing %s file" % self._treeLabel
        except:
            print "!!! Error: Can't write %s file !!!" % self._treeLabel