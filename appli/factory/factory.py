import os
from appli import factory
from lib.system import procFile as pFile


class Factory(object):
    """ Factory main class
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="Factory", level=logLvl)
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
    def seqPath(self):
        return os.path.join(self.nodePath, 'seq')

    @property
    def movPath(self):
        return os.path.join(self.nodePath, 'mov')

    @property
    def hasSeq(self):
        if os.path.exists(self.seqPath):
            return True
        else:
            return False

    @property
    def hasMov(self):
        if os.path.exists(self.movPath):
            return True
        else:
            return False
