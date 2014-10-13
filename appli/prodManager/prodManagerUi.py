import os, sys
from functools import partial
from appli import prodManager
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.prodManager import prodManager as pm
from appli.prodManager.ui import prodLoaderUI, prodManagerUI
from appli.prodManager import pmCore, tabProject, tabShots, treeProject, tabLineTest, tabOverView


class ProdLoaderUi(QtGui.QMainWindow, prodLoaderUI.Ui_prodLoader, pmCore.Loader, pQt.Style):
    """ PreLoad ui used by ProdManagerUi
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="PM-launcher", level=logLvl)
        self.log.info("#-- Launching ProdLoader --#")
        self._user = prodManager.user
        self._binPath = prodManager.binPath
        self._prodsPath = os.path.join(prodManager.binPath, 'prod')
        self._rootPath = os.path.join(self._binPath, 'pref')
        self._prefFile = os.path.join(self._rootPath, "%s.py" % self._user)
        super(ProdLoaderUi, self).__init__()
        self.setupUi(self)
        self._setupUi()
        self._initUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup Loader mainUi """
        self.log.info("#-- Setup Loader Ui --#")
        self.setStyleSheet(self.applyStyle(styleName='darkGrey'))
        self.bCreate.clicked.connect(self.on_createNewProd)
        #-- All Prods --#
        for n in range(3):
            self.twAll.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)
        self.twAll.itemDoubleClicked.connect(partial(self.launchProdManager, self.twAll))
        self.bInclude.clicked.connect(self.on_includeToPref)
        #-- User Prods --#
        for n in range(3):
            self.twPref.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)
        self.twPref.itemDoubleClicked.connect(partial(self.launchProdManager, self.twPref))
        self.bRemove.clicked.connect(self.on_removeFromPref)

    def _initUi(self):
        """ Init Loader mainUi """
        self.log.debug("#-- Init Ui --#")
        self.rf_allProds()
        self.rf_prefProds()

    def rf_allProds(self):
        """ Refresh 'All Prods' treeWidget """
        self.log.debug("Refreshing all prods ...")
        self.twAll.clear()
        prods = os.listdir(self._prodsPath) or []
        items = []
        for prod in sorted(prods):
            absPath = os.path.join(self._prodsPath, prod)
            if os.path.isdir(absPath):
                newItem = self._newItem(prod.split('--')[0], prod.split('--')[1])
                items.append(newItem)
        self.twAll.addTopLevelItems(items)
        self.twAll.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)

    def rf_prefProds(self):
        """ Refresh 'User Prods' treeWidget """
        self.log.debug("Refreshing user prods ...")
        self.twPref.clear()
        self._checkPrefPath()
        bookMarks = pFile.readPyFile(self._prefFile)['prodBookMarks']
        items = []
        for prod in sorted(bookMarks):
            newItem = self._newItem(prod.split('--')[0], prod.split('--')[1])
            items.append(newItem)
        self.twPref.addTopLevelItems(items)
        self.twPref.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)

    def on_createNewProd(self):
        """ Command launched when 'Create New Prod' pushButton is clicked """
        self.log.debug("#-- New Prod --#")
        mess = "Create New Prod:\nLine 1: Prod Alias\nLine 2: Prod Name"
        self.newProdDialog = pQt.PromptDialog(mess, self._createNewProd, Nlines=2)
        self.newProdDialog.setStyleSheet(self.applyStyle(styleName='darkGrey'))
        self.newProdDialog.exec_()

    def _createNewProd(self):
        """ Create new prod """
        self.log.debug("Creating New Prod ...")
        prodAlias = self.newProdDialog.result()['result_1']
        prodName = self.newProdDialog.result()['result_2']
        if prodAlias == '' or prodName == '':
            pQt.errorDialog("Prod Alias and Prod Name must be edited !!!", self.newProdDialog)
        else:
            result = self.createNewProd(self._prodsPath, prodAlias, prodName)
            if not isinstance(result, bool):
                self.log.error(result.replace('error__', ''))
                pQt.errorDialog(result.replace('error__', ''), self.newProdDialog)
            else:
                self.log.info("New prod successfully created: %s--%s." % (prodAlias, prodName))
                self.newProdDialog.close()
                self.rf_allProds()

    def on_includeToPref(self):
        """ Include selected prods into user prodBokkMarks """
        prefDict = pFile.readPyFile(self._prefFile)
        selItems = self.twAll.selectedItems() or []
        for item in selItems:
            if not item.prodId in prefDict['prodBookMarks']:
                prefDict['prodBookMarks'].append(item.prodId)
        txt = []
        for k, v in prefDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        pFile.writeFile(self._prefFile, '\n'.join(txt))
        self.log.info("Pref file saved: %s" % self._user)
        self.rf_prefProds()

    def on_removeFromPref(self):
        """ Remove Selected prods from user prodBookMarks """
        prefDict = pFile.readPyFile(self._prefFile)
        selItems = self.twPref.selectedItems() or []
        for item in selItems:
            if item.prodId in prefDict['prodBookMarks']:
                prefDict['prodBookMarks'].pop(prefDict['prodBookMarks'].index(item.prodId))
        txt = []
        for k, v in prefDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        pFile.writeFile(self._prefFile, '\n'.join(txt))
        self.log.info("Pref file saved: %s" % self._user)
        self.rf_prefProds()

    def launchProdManager(self, twTree):
        """ Launch given prodManager
            @param twTree: (object) : QTreeWidgetItem """
        selItems = twTree.selectedItems()
        if not len(selItems) == 1:
            self.log.error("Select only one item !!!")
            pQt.errorDialog("Select only one item !!!", self.newProdDialog)
        else:
            print '\n'
            self.close()
            self.pm = ProdManagerUi(selItems[0].prodId)
            self.pm.show()

    def _newItem(self, prodAlias, prodName):
        """ Create new QTreeWidgetItem
            @param prodAlias: (str) : Prod alias
            @param prodName: (str) : Prod name
            @return: (object) : QTreeWidgetItem """
        self.log.debug("\t Creating new prod item: %s--%s" % (prodAlias, prodName))
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, prodAlias)
        newItem.setText(1, " -- ")
        newItem.setText(2, prodName)
        newItem.prodAlias = prodAlias
        newItem.prodName = prodName
        newItem.prodId = "%s--%s" % (prodAlias, prodName)
        newItem.prodPath = os.path.join(self._prodsPath, newItem.prodId, '%s.py' % newItem.prodId)
        return newItem

    def _checkPrefPath(self):
        """ Check if pref path exists """
        if not os.path.exists(self._prefFile):
            result = self.createPrefFile(self._prefFile)
            if not isinstance(result, bool):
                error = result.replace('error__', '')
                pQt.errorDialog(error, self.newProdDialog)
            else:
                self.log.info("New user pref file successfully created: %s" % self._user)


class ProdManagerUi(QtGui.QMainWindow, prodManagerUI.Ui_prodManager, pQt.Style):
    """ Class used for project edition
        @param prodId: (str) : Project Id
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, prodId, logLvl='info'):
        self.log = pFile.Logger(title="PM-ui", level=logLvl)
        self.log.info("#-- Launching ProdManager --#")
        self._currentStyle = 'darkOrange'
        self.pm = pm.ProdManager(prodId)
        super(ProdManagerUi, self).__init__()
        self._setupUi()

    # noinspection PyUnresolvedReferences
    def _setupUi(self):
        """ Setup prodManager mainUi """
        self.log.info("#-- Setup Main Ui --#")
        self.setupUi(self)
        self.setWindowTitle("ProdManager: %s" % self.pm._prodId)
        self.setStyleSheet(self.applyStyle(styleName=self._currentStyle))
        #-- Menu Pref --#
        self.miDefaultStyle.triggered.connect(partial(self.on_style, 'default'))
        self.miDarkGreyStyle.triggered.connect(partial(self.on_style, 'darkGrey'))
        self.miDarkOrangeStyle.triggered.connect(partial(self.on_style, 'darkOrange'))
        #-- Left Zone --#
        self.wgPreview = treeProject.Preview(self)
        self.vlLeftZone.insertWidget(0, self.wgPreview)
        self.wgTree = treeProject.ProjectTree(self)
        self.vlLeftZone.insertWidget(-1, self.wgTree)
        #-- Tabs --#
        self.wgProject = tabProject.ProjectTab(self)
        self.glTabProject.addWidget(self.wgProject)
        self.wgShots = tabShots.ShotsTab(self)
        self.glTabShots.addWidget(self.wgShots)
        self.wgLineTest = tabLineTest.LineTestTab(self)
        self.glTabLineTest.addWidget(self.wgLineTest)
        self.wgOverView = tabOverView.OverViewTab(self)
        self.glTabOverView.addWidget(self.wgOverView)
        self.tabManager.currentChanged.connect(self.wgTree.twTree.on_treeNode)

    def on_style(self, style):
        """ Pref style menu items command. switch style
            @param style: (str) : 'default', 'darkGrey', 'darkOrange' """
        self.log.debug("Switching ui style ...")
        if style == 'default':
            self.setStyleSheet("")
        else:
            self.setStyleSheet(self.applyStyle(styleName=style))
        self._currentStyle = style
        self.log.debug("Apply style: %s" % style)

    def getSelTab(self):
        """ Get selected tab
            @return: (str) : Selected tab text """
        return self.tabManager.tabText(self.tabManager.currentIndex())

    def getSelMode(self):
        """ Get selected treeMode
            @return: (str) : Tree mode """
        return self.wgTree.getSelMode()

    def getSelTree(self):
        """ Get selected tree
            @return: (str) : Tree name """
        return self.wgTree.getSelTree()


def launch(uiType='loader', prodId=None, logLvl='info'):
    """ ProdManager Launcher
        @param uiType: (str) : 'loader' or 'manager'
        @param prodId: (str) : Project id """
    app = QtGui.QApplication(sys.argv)
    if uiType == 'loader':
        window = ProdLoaderUi(logLvl=logLvl)
        window.show()
    elif uiType == 'manager':
        if prodId is None:
            raise KeyError, "ProdId can not be None."
        window = ProdManagerUi(prodId, logLvl=logLvl)
        window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # launch(logLvl='info')
    launch(uiType='manager', prodId='lv--Le_Voeu', logLvl='info')