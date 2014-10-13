import os
from appli import prodManager
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from appli.prodManager import pmCore
from lib.system import procFile as pFile
from appli.prodManager.ui import wgtPreviewUI, wgtMainTreeUI


class Preview(QtGui.QWidget, wgtPreviewUI.Ui_preview):
    """ Preview and launcher ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self._ima = None
        self.pIma = None
        self.pSeq = None
        self.pMov = None
        self.pXplor = None
        self.pXterm = None
        self.pGraph = None
        super(Preview, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup preview Widget """
        self.log.debug("#-- Setup Preview --#")
        self.setupUi(self)
        self.qIma = None
        self.bImage.clicked.connect(self.on_image)
        self.bMovie.clicked.connect(self.on_movie)
        self.bExplorer.clicked.connect(self.on_explorer)
        self.bXterm.clicked.connect(self.on_xTerm)
        self.rf_preview()

    def rf_preview(self):
        """ Refresh preview image """
        self.storeImaFile()
        self.qIma = QtGui.QPixmap(self._ima)
        self.lPreview.setPixmap(self.qIma)
        self.resizePreview()
        self.rf_btnsVisibility()

    def rf_btnsVisibility(self):
        """ Refresh Preview buttons visibility """
        self._setBtnVis(self.pIma, self.bImage)
        self._setBtnVis(self.pSeq, self.bSequence)
        self._setBtnVis(self.pMov, self.bMovie)
        self._setBtnVis(self.pXplor, self.bExplorer)
        self._setBtnVis(self.pXterm, self.bXterm)
        self._setBtnVis(self.pGraph, self.bGrapher)

    def on_image(self):
        path = os.path.normcase(self.pIma)
        os.system('fcheck "%s"' % path)

    def on_movie(self):
        """ Command launched when 'Movie' QPushButton is clicked """
        path = os.path.normcase(self.pMov)
        os.system('"%s"' % path)

    def on_explorer(self):
        """ Command launched when 'Explorer' QPushButton is clicked """
        path = os.path.normpath(self.pXplor)
        os.system('explorer "%s"' % path)

    def on_xTerm(self):
        """ Command launched when 'Xterm' QPushButton is clicked """
        path = os.path.normpath(self.pXterm)
        os.system('start "Toto" /d "%s"' % path)

    def ud_previewIcone(self, imaFile, iconeFile):
        """ Update preview icone file
            @param imaFile: (str) : Image absolut path
            @param iconeFile: (str) : Icone absolut path """
        root = os.path.join(self.pm._prodPath, self.pm._prodId)
        if imaFile == '' or imaFile == ' ':
            self._ima = None
            self.rf_preview()
            self.removePreviewIcone(iconeFile)
        else:
            self._ima = imaFile
            self.rf_preview()
            img = self.resizeImage()
            if pmCore.Manager.checkDataPath(root, os.path.dirname(iconeFile)):
                try:
                    img.save(iconeFile, 'png', 100)
                    self._ima = iconeFile
                    self.rf_preview()
                    self.log.info("Saving preview icone: %s ..." % pFile.conformPath(iconeFile))
                except:
                    self.log.error("Can't save preview icone: %s !!!" % pFile.conformPath(iconeFile))

    def storeImaFile(self):
        """ Store image file """
        if self._ima is None or self._ima == '' or self._ima == ' ':
            self._ima = os.path.join(prodManager.libPath, 'ima', 'prodManager_300x300.png')

    def resizePreview(self):
        """ Resize previw icone QLabel """
        ratio = float(self.qIma.width()) / float(self.qIma.height())
        if self.qIma.width() > self.qIma.height():
            width = 300
            height = int(float(width) / ratio)
        else:
            height = 170
            width = int(float(height) / ratio)
        if 'prodManager' in os.path.basename(self._ima):
            width = 300
            height = 170
        self.lPreview.setMinimumSize(width, height)
        self.lPreview.setMaximumSize(width, height)

    def resizeImage(self):
        """ Resize image to icone size
            @return: (object) : QPixmap """
        ratio = float(self.qIma.width()) / float(self.qIma.height())
        if self.qIma.width() > self.qIma.height():
            maxWidth = 300
            maxHeight = int(300 / ratio)
        else:
            maxWidth = int(300 / ratio)
            maxHeight = 300
        img = self.qIma.toImage().scaled(maxWidth, maxHeight, QtCore.Qt.KeepAspectRatio)
        return img

    def removePreviewIcone(self, iconeFile):
        """ Remove preview icone file
            @param iconeFile: (str) : Icone absolut path """
        if os.path.exists(iconeFile):
            try:
                os.remove(iconeFile)
                self.log.info("Remove preview icone: %s" % pFile.conformPath(iconeFile))
            except:
                self.log.error("Can't remove preview icone: %s !!!" % pFile.conformPath(iconeFile))

    def _setBtnVis(self, path, btn):
        """ Set given QPushButton visibility
            @param path: (str) : Absolut path
            @param btn: (object) : QPushButton """
        if path is None or path == '' or path == ' ':
            btn.setEnabled(False)
        else:
            if os.path.exists(path):
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)


class ProjectTree(QtGui.QWidget, wgtMainTreeUI.Ui_mainTree):
    """ Project settings ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        super(ProjectTree, self).__init__()
        self._setupUi()
        self._refresh()

    def _setupUi(self):
        """ Setup projectTree Widget """
        self.log.debug("#-- Setup Tree Project --#")
        self.setupUi(self)
        self.twTree = Tree(self)
        self.vlTree.insertWidget(-1, self.twTree)
        self.rbTreeMode.clicked.connect(self.twTree.rf_tree)
        self.rbStepMode.clicked.connect(self.twTree.rf_tree)
        self.rbAsset.clicked.connect(self.on_rbTree)
        self.rbShot.clicked.connect(self.on_rbTree)

    def _refresh(self):
        """ Refresh projectTree widget """
        self.log.debug("#-- Refresh Tree Project --#")
        self.twTree.rf_tree()

    def on_rbTree(self):
        """ Command launched when 'rbTree' is clicked """
        self.twTree.rf_tree()
        if self.mainUi.getSelTab() == 'OverView':
            self.mainUi.wgOverView._refresh()

    def getSelMode(self):
        """ Get selected display mode
            @return: (str) : Selected tree display mode """
        if self.rbTreeMode.isChecked():
            return 'treeMode'
        elif self.rbStepMode.isChecked():
            return 'stepMode'

    def getSelTree(self):
        """ Get selected tree
            @return: (str) : Selected tree name """
        if self.rbAsset.isChecked():
            return 'asset'
        elif self.rbShot.isChecked():
            return 'shot'

    def _newRadioButton(self, treeName):
        """ Create new QRadioButton
            @param treeName: (str) : Button label
            @return: (object) : QRadioButton """
        newButton = QtGui.QRadioButton()
        newButton.setText(treeName)
        newButton.clicked.connect(self.twTree.rf_tree)
        return newButton


class Tree(QtGui.QTreeWidget):
    """ QTreeWidget used by ProjectTree
        @param parent: (object) : Parent QWidget """

    def __init__(self, parent):
        self._parent = parent
        self.mainUi = self._parent.mainUi
        self.pm = self._parent.pm
        self.log = self._parent.log
        super(Tree, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup projectTree QTreeWidget """
        self.log.debug("\t Setup mainTree widget ...")
        self.header().setVisible(False)
        self.itemClicked.connect(self.on_treeNode)

    def rf_tree(self):
        """ Refresh mainTree """
        self.clear()
        if self._parent.getSelTree() is not None:
            selTree = self._parent.getSelTree()
            treeDict = self.pm.prodTrees[selTree]
            if self._parent.getSelMode() == 'treeMode':
                self.log.debug("\t Refreshing main tree (Tree Mode) ...")
                self.rf_treeMode(selTree, treeDict)
            elif self._parent.getSelMode() == 'stepMode':
                self.log.debug("\t Refreshing main tree (Step Mode) ...")
                self.rf_stepMode(selTree, treeDict)

    def rf_treeMode(self, selTree, treeDict):
        """ Refresh main tree with treeMode listing
            @param treeDict: (dict) : Tree dict """
        for node in treeDict['tree']['_order']:
            newItem = TreeNode(**treeDict['tree'][node])
            if len(node.split('/')) == 1:
                self.addTopLevelItem(newItem)
            else:
                parent = self._getItemFromTreePath('/'.join(node.split('/')[:-1]))
                parent.addChild(newItem)
            if getattr(newItem, 'nodeType') == 'shotNode':
                newItem._itemPath = node
                newItem._dataPath = os.path.join(self.pm._treePath, selTree)
                for fld in node.split('/'):
                    newItem._dataPath = os.path.join(newItem._dataPath, fld)
                newItem._dataPath = pFile.conformPath(newItem._dataPath)
                newItem._dataFile = "%s.py" % newItem._dataPath
                for step in treeDict['steps']:
                    newStep = TreeNode(nodeType='step', nodeLabel=step, nodeName=step)
                    newStep._tree = selTree
                    newStep._step = step
                    newStep._dataPath = newItem._dataPath
                    newStep._ltPath = pFile.conformPath(os.path.join(newStep._dataPath, 'lt', step))
                    newStep._dataFile = newItem._dataFile
                    newItem.addChild(newStep)

    def rf_stepMode(self, selTree, treeDict):
        """ Refresh main tree with stepMode listing
            @param treeDict: (dict) : Tree dict """
        for step in treeDict['steps']:
            newStep = TreeNode(nodeType='step', nodeLabel=step, nodeName=step)
            self.addTopLevelItem(newStep)
            for node in treeDict['tree']['_order']:
                newItem = TreeNode(**treeDict['tree'][node])
                if len(node.split('/')) == 1:
                    newStep.addChild(newItem)
                else:
                    rootPath = "%s/%s" % (step, '/'.join(node.split('/')[:-1]))
                    parent = self._getItemFromTreePath(rootPath)
                    parent.addChild(newItem)
                if getattr(newItem, 'nodeType') == 'shotNode':
                    newItem._tree = selTree
                    newItem._step = step
                    newItem._itemPath = node
                    newItem._dataPath = os.path.join(self.pm._treePath, selTree)
                    for fld in node.split('/'):
                        newItem._dataPath = os.path.join(newItem._dataPath, fld)
                    newItem._dataPath = pFile.conformPath(newItem._dataPath)
                    newItem._ltPath = pFile.conformPath(os.path.join(newItem._dataPath, 'lt', step))
                    newItem._dataFile = "%s.py" % newItem._dataPath

    def on_treeNode(self):
        """ Command launch when shotNode is clicked """
        if self.mainUi.getSelTab() == 'Shots':
            self.mainUi.wgShots._refresh()
        elif self.mainUi.getSelTab() == 'LineTest':
            self.mainUi.wgLineTest._refresh()
        elif self.mainUi.getSelTab() == 'OverView':
            self.mainUi.wgOverView._refresh()

    def addTopLevelItem(self, QTreeWidgetItem):
        super(Tree, self).addTopLevelItem(QTreeWidgetItem)

    def addTopLevelItems(self, list_of_QTreeWidgetItem):
        super(Tree, self).addTopLevelItems(list_of_QTreeWidgetItem)

    def insertTopLevelItem(self, p_int, QTreeWidgetItem):
        super(Tree, self).insertTopLevelItem(p_int, QTreeWidgetItem)

    def insertTopLevelItems(self, p_int, list_of_QTreeWidgetItem):
        super(Tree, self).insertTopLevelItems(p_int, list_of_QTreeWidgetItem)

    @staticmethod
    def _getItemTreePath(item):
        """ Get given QTreeWidgetItem tree path
            @param item: (object) : QTreeWidgetItem
            @return: (str) : Item tree path """
        if item.parent() is None:
            root = item.nodeLabel
        else:
            root = ""
            parents = pQt.getAllParent(item)
            parents.reverse()
            for n, p in enumerate(parents[:-1]):
                if n == 0:
                    root = p.nodeLabel
                else:
                    root = "%s/%s" % (root, p.nodeLabel)
            root = "%s/%s" % (root, item.nodeLabel)
        return root

    def _getItemFromTreePath(self, treePath):
        """ Get item from given tree path
            @param treePath: (str) : Tree path
            @return: (object) : QTreeWidgetItem """
        for item in pQt.getAllItems(self):
            if self._getItemTreePath(item) == treePath:
                return item


class TreeNode(QtGui.QTreeWidgetItem):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        super(TreeNode, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup treeNode QTreeWidgetItem """
        self.setText(0, getattr(self, 'nodeLabel'))
        if hasattr(self, 'nodeType'):
            if getattr(self, 'nodeType') == 'shotNode':
                self.setTextColor(0, QtGui.QColor(125, 255, 255))

    def addChild(self, QTreeWidgetItem):
        super(TreeNode, self).addChild(QTreeWidgetItem)

    def addChildren(self, list_of_QTreeWidgetItem):
        super(TreeNode, self).addChildren(list_of_QTreeWidgetItem)

    def insertChild(self, p_int, QTreeWidgetItem):
        super(TreeNode, self).insertChild(p_int, QTreeWidgetItem)

    def insertChildren(self, p_int, list_of_QTreeWidgetItem):
        super(TreeNode, self).insertChildren(p_int, list_of_QTreeWidgetItem)
