import os
from appli import factory
from lib.system import procFile as pFile
try:
    import maya.cmds as mc
    __inMaya__ = True
except:
    __inMaya__ = False


class Factory(object):
    """ Factory main class
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="Factory-ui", level=logLvl)
        self.path = factory.factoryPath
        self.libPath = factory.libPath
        self.nConvert = factory.nConvert
        self.texture = Tree('texture', parent=self)
        self.shader = Tree('shader', parent=self)
        self.stockShot = Tree('stockShot', parent=self)

    def parseTree(self, tree):
        """ Parse given tree
            @param tree: (object) : Tree object """
        self.log.info("Parsing %s ..." % tree.treeName)
        tree.tree = []
        cats = os.listdir(tree.path) or []
        #-- Parse Category --#
        for cat in cats:
            catPath = pFile.conformPath(os.path.join(tree.path, cat))
            if not cat.startswith('_') and not cat.startswith('.') and os.path.isdir(catPath):
                newCat = TreeNode('category', cat, catPath, tree=tree)
                tree.tree.append(newCat)
                #-- Parse Sub Category --#
                subCats = os.listdir(catPath) or []
                for subCat in subCats:
                    subCatPath = pFile.conformPath(os.path.join(catPath, subCat))
                    if (not subCat.startswith('_') and not subCat.startswith('.')
                        and os.path.isdir(subCatPath)):
                        newSubCat = TreeNode('subCategory', subCat, subCatPath, tree=tree,
                                             parent=newCat)
                        newCat._children.append(newSubCat)
                        #-- Parse Files --#
                        files = os.listdir(subCatPath) or []
                        for f in files:
                            filePath = pFile.conformPath(os.path.join(subCatPath, f))
                            if (not f.startswith('_') and not f.startswith('.')
                                and os.path.isfile(filePath)):
                                newFile = TreeNode('file', f.split('.')[0], filePath, tree=tree,
                                                   parent=newSubCat)
                                newSubCat._children.append(newFile)
        self.log.info("\t Parsing done.")

    def ud_thumbnailImages(self, imaFile, imaType):
        """ Create or update thumbnail or preview image
            @param imaFile: (str) : Original image absolute path
            @param imaType: (str) : 'icon' or 'preview' """
        srcFile = os.path.normpath(imaFile)
        thumbPath = pFile.conformPath(os.path.join(os.path.dirname(imaFile), '_%s' % imaType))
        if not os.path.exists(thumbPath):
            os.mkdir(thumbPath)
            self.log.info("Create path %s" % thumbPath)
        thumbFile = os.path.splitext(os.path.basename(imaFile))[0]
        thumbAbsPath = os.path.normpath(os.path.join(thumbPath, '%s.png' % thumbFile))
        if imaType == 'icon':
            iconSize = 100
        elif imaType == 'preview':
            iconSize = 250
        else:
            iconSize = 80
        os.system("%s -out png -ratio -resize %s %s -overwrite -o %s %s" % (self.nConvert, iconSize,
                                                                            iconSize, thumbAbsPath,
                                                                            srcFile))

    def ud_thumbnailDatas(self, imaFile, treeName):
        """ Create or update thumbnail data
            @param imaFile: (str) : Original image absolute path
            @param treeName: (str) : Tree object name """
        node = self.getNode(treeName, imaFile)
        dataPath = pFile.conformPath(os.path.dirname(node.dataFile))
        if not os.path.exists(dataPath):
            os.mkdir(dataPath)
            self.log.info("Create path %s" % dataPath)
        dataDict = node.getFileInfo()
        if dataDict is not None:
            dataTxt = []
            for k, v in dataDict.iteritems():
                if isinstance(v, str):
                    dataTxt.append("%s = %r" % (k, v))
                else:
                    dataTxt.append("%s = %s" % (k, v))
            try:
                pFile.writeFile(node.dataFile, '\n'.join(dataTxt))
                self.log.info("Create thumbnail datas successfully: %s" % node.nodeName)
            except:
                self.log.error("Can not create thumbnail datas for %s" % node.nodeName)
        else:
            self.log.warning("Can not access fileData, skip %s" % node.nodeName)

    def getNode(self, treeName, nodePath):
        """ Get node from given treeName and nodePath
            @param treeName: (str) : Tree object name
            @param nodePath: (str) : Node path
            @return: (object) : Node object """
        tree = getattr(self, treeName)
        node = tree.getNode(nodePath=nodePath)
        return node


class Tree(object):
    """ Factory tree object
        @param treeName : (str) : Tree name
        @param parent : (object) : Parent class """

    def __init__(self, treeName, parent=None):
        self._parent = parent
        self.treeName = treeName
        self._parent.log.info("#-- %s --#" % self.treeName)
        self.path = os.path.join(self._parent.path, self.treeName)
        self.tree = []
        self._parent.parseTree(self)

    def getAllNodes(self):
        """ Get all treeNodes
            @return: (list) : Tree nodes list """
        allNodes = []
        for node in self.tree:
            allNodes.extend(self.getAllChildren(node))
        return allNodes

    def getAllChildren(self, node, depth=-1):
        """ get all children from given node
            @param node: (object) : Tree node
            @param depth: (int) : recursion depth
            @return: (list) : Tree nodes list """
        nodes = []
        def recurse(currentNode, depth):
            nodes.append(currentNode)
            if depth != 0:
                for n in range(len(currentNode._children)):
                    recurse(currentNode._children[n], depth-1)
        recurse(node, depth)
        return nodes

    def getNode(self, nodePath=None):
        """ Get node from given nodePath
            @param nodePath: (str) : Node path
            @return: (object) : Node object """
        if nodePath is not None:
            for node in self.getAllNodes():
                if node.nodePath == nodePath:
                    return node


class TreeNode(object):
    """ Factory tree node
        @param nodeType : (str) : 'category', 'subCategory' or 'file'
        @param nodeName : (str) : Node name
        @param nodePath : (str) : Node path
        @param tree : (object) : Parent tree object
        @param parent : (object) : Parent treeNode object """

    def __init__(self, nodeType, nodeName, nodePath, tree=None, parent=None):
        self._tree = tree
        self._parent = parent
        self._children = []
        self.nodeType = nodeType
        self.nodeName = nodeName
        self.nodePath = nodePath

    @property
    def sequencePath(self):
        """ Get sequence path
            @return: (str) : Sequence absolute path """
        path = os.path.join(os.path.dirname(self.nodePath), 'seq', self.nodeName)
        return pFile.conformPath(path)

    @property
    def movieFile(self):
        """ Get movie file
            @return: (str) : Movie file absolute path """
        path = os.path.join(os.path.dirname(self.nodePath), 'mov')
        return pFile.conformPath(os.path.join(path, "%s.mov" % self.nodeName))

    @property
    def dataFile(self):
        """ get data file
            @return: (str) : Data file absolute path """
        path = os.path.join(os.path.dirname(self.nodePath), '_data')
        return pFile.conformPath(os.path.join(path, "%s.py" % self.nodeName))

    @property
    def datas(self):
        """ Get datas
            @return: (dict) : File datas """
        if os.path.exists(self.dataFile):
            return pFile.readPyFile(self.dataFile)

    @property
    def datasString(self):
        """ Convert datas dict into readable string
            @return: (str) : Datas string """
        txt = []
        infoOrder = ['path', 'name', 'width', 'height', 'ratio', 'channel', 'depth',
                     'duration', 'speed']
        if self.datas is not None:
            for ima in self.datas['_order']:
                txt.append("#-- %s --#" % ima)
                for info in infoOrder:
                    if isinstance(self.datas[ima][info], str):
                        txt.append("%s = %r" % (info, self.datas[ima][info]))
                    else:
                        txt.append("%s = %s" % (info, self.datas[ima][info]))
        return '\n'.join(txt)

    def hasSequence(self):
        """ Check if node has sequence folder
            @return: (bool) : True if exists """
        if os.path.exists(self.sequencePath):
            return True
        else:
            return False

    def hasMovie(self):
        """ Check if node has movie file
            @return: (bool) : True if exists """
        if os.path.exists(self.movieFile):
            return True
        else:
            return False

    def getFileInfo(self):
        """ Get file info
            @return: (str) : File info """
        if self.hasSequence():
            path = self.sequencePath
        else:
            path = self.nodePath
        try:
            info = pFile.Image().getInfo(path)
            return info
        except:
            return None