from appli import prodManager
from PyQt4 import QtGui, QtCore, uic


tapProjectClass, tapProjectUiClass = uic.loadUiType(prodManager.uiList['tabProject'])
class ProjectTab(tapProjectClass, tapProjectUiClass):
    """ Project settings ui used by ProdManagerUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
        self.log = self.mainUi.log
        self.cmds = self.mainUi.cmds
        super(ProjectTab, self).__init__()
        self.setupUi(self)
        self._setupUi()
        self._initUi()

    def _setupUi(self):
        pass

    def _initUi(self):
        self.rf_title()
        self.rf_date()

    def rf_title(self):
        self.lProd.setText("%s (%s)" % (self.pm.prodName, self.pm.prodAlias))

    def rf_date(self):
        self.deStart.setDate(QtCore.QDate(int(self.pm.prodStartDate.split('/')[0]),
                                          int(self.pm.prodStartDate.split('/')[1]),
                                          int(self.pm.prodStartDate.split('/')[2])))
        self.deEnd.setDate(QtCore.QDate(int(self.pm.prodStopDate.split('/')[0]),
                                        int(self.pm.prodStopDate.split('/')[1]),
                                        int(self.pm.prodStopDate.split('/')[2])))
