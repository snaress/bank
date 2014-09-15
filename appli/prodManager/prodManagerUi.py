import os, sys
from PyQt4 import QtGui, uic
from functools import partial
from appli import prodManager
from lib.qt import procQt as pQt
from lib.system import procFile as pFile
from appli.prodManager import prodManager as pm
from appli.prodManager import pmCmds, pmCore, pmWidget


prodLoaderClass, prodLoaderUiClass = uic.loadUiType(prodManager.uiList['prodLoader'])
class ProdLoaderUi(prodLoaderClass, prodLoaderUiClass, pmCore.Loader, pQt.UiStyle):
    """ PreLoad ui used by ProdManagerUi
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="PMui", level=logLvl)
        self.log.info("#-- Launching ProdLoader --#")
        self._user = prodManager.user
        self._binPath = prodManager.binPath
        self._prodsPath = os.path.join(prodManager.binPath, 'prod')
        self.cmds = pmCmds.LoaderCmds(self)
        super(ProdLoaderUi, self).__init__()
        self.setupUi(self)
        self._setupUi()
        self._initUi()

    def _setupUi(self):
        """ Setup Loader mainUi """
        self.setStyleSheet(self.darkGreyWidget())
        self.pbCreate.clicked.connect(self.cmds.on_createNewProd)
        #-- All Prods --#
        for n in range(3):
            self.twAll.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)
        self.twAll.header().setStyleSheet(self.darkGreyHeader())
        self.twAll.itemSelectionChanged.connect(partial(self.cmds.rf_itemStyle, self.twAll))
        self.twAll.itemDoubleClicked.connect(partial(self.launchProdManager, self.twAll))
        self.pbInclude.clicked.connect(self.cmds.on_includeToPref)
        #-- User Prods --#
        for n in range(3):
            self.twPref.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)
        self.twPref.header().setStyleSheet(self.darkGreyHeader())
        self.twPref.itemSelectionChanged.connect(partial(self.cmds.rf_itemStyle, self.twPref))
        self.twPref.itemDoubleClicked.connect(partial(self.launchProdManager, self.twPref))
        self.pbRemove.clicked.connect(self.cmds.on_removeFromPref)

    def _initUi(self):
        """ Init Loader mainUi """
        self.cmds.rf_allProds()
        self.cmds.rf_prefProds()

    def launchProdManager(self, twTree):
        """ Launch given prodManager
            @param twTree: (object) : QTreeWidgetItem """
        selItems = twTree.selectedItems()
        if not len(selItems) == 1:
            pQt.errorDialog("Select only one item !!!", self.newProdDialog)
        else:
            self.close()
            self.pm = ProdManagerUi(selItems[0].prodId)
            self.pm.show()


prodManagerClass, prodManagerUiClass = uic.loadUiType(prodManager.uiList['prodManager'])
class ProdManagerUi(prodManagerClass, prodManagerUiClass, pQt.UiStyle):
    """ Class used for project edition
        @param prodId: (str) : Project Id
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, prodId, logLvl='info'):
        self.log = pFile.Logger(title="PMui", level=logLvl)
        self.log.info("#-- Launching ProdManager --#")
        self.pm = pm.ProdManager(prodId)
        self.cmds = pmCmds.ManagerCmds(self)
        super(ProdManagerUi, self).__init__()
        self.setupUi(self)
        self._setupUi()
        self._initUi()

    def _setupUi(self):
        """ Setup prodManager mainUi """
        self.log.debug("Setup mainUi ...")
        self.setStyleSheet(self.darkGreyWidget())
        self.tabManager.setStyleSheet(self.darkGreyTabs())
        self.wgProject = pmWidget.ProjectTab(self)
        self.glTabProject.addWidget(self.wgProject)

    def _initUi(self):
        """ Init prodManager mainUi """
        self.log.debug("Init mainUi ...")
        self.setWindowTitle("ProdManager: %s" % self.pm._prodId)


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
    # launch()
    launch(uiType='manager', prodId='lv--Le_Voeu')