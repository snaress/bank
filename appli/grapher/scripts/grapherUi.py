import sys, os
from appli import grapher
from PyQt4 import QtGui, uic
from lib.qt.scripts import dialog2
from lib.system.scripts import procFile as pFile
from appli.grapher.scripts import grapher as gp
from appli.grapher.scripts import refresh, cmds, window, core


grapherClass, grapherUiClass = uic.loadUiType(grapher.uiList['grapher'])
class GrapherUi(grapherClass, grapherUiClass, core.FileCmds, window.Style):
    """ Class containing all grapher's Ui actions for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self.grapher = gp.Grapher()
        self.rf_mainUi = refresh.MainUi(self)
        self.rf_shared = refresh.SharedWidget(self, self)
        self.cmds_menu = cmds.Menu(self)
        self.window = window
        super(GrapherUi, self).__init__()
        self._lock = False
        self._setupUi()
        self.initUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupMenu()
        self._setupMain()

    def _setupMenu(self):
        #-- Menu File --#
        self.miOpenGraph.triggered.connect(self.cmds_menu.on_openGraph)
        self.miOpenGraph.setShortcut("Ctrl+O")
        self.miSaveGraph.triggered.connect(self.cmds_menu.on_saveGraph)
        self.miSaveGraph.setShortcut("Ctrl+S")
        self.miSaveGraphAs.triggered.connect(self.cmds_menu.on_saveGraphAs)
        self.miSaveGraphAs.setShortcut("Ctrl+Shift+S")
        self.miQuitGrapher.triggered.connect(self.cmds_menu.on_quitGrapher)
        self.miQuitGrapher.setShortcut("Ctrl+Shift+W")
        #-- Menu Tool --#
        self.miNodeEditor.triggered.connect(self.cmds_menu.on_nodeEditor)
        self.miNodeEditor.setShortcut("E")
        #-- Menu Help --#
        self.miGrapherRepr.triggered.connect(self.cmds_menu.on_grapherRepr)
        self.miGrapherRepr.setShortcut("Ctrl+G")
        self.miGrapherStr.triggered.connect(self.cmds_menu.on_grapherStr)
        self.miGrapherStr.setShortcut("Shift+G")
        self.miGrapherDict.triggered.connect(self.cmds_menu.on_grapherDict)
        self.miGrapherDict.setShortcut("Alt+G")

    def _setupMain(self):
        #-- Comment Zone --#
        self.wgComment = self.window.TextEditor(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(self.rf_shared.rf_commentVis)
        #-- Variables Zone --#
        self.cbVariables.clicked.connect(self.rf_shared.rf_variablesVis)
        #-- NodeEditor Zone --#
        self.nodeEditor = self.window.NodeEditor(self)
        self.vlNodeEditor.addWidget(self.nodeEditor)

    def initUi(self):
        """ Initialize ui """
        self.rf_shared.rf_commentVis()
        self.rf_shared.rf_commentBgc()
        self.rf_shared.rf_variablesVis()
        self.rf_shared.rf_variablesBgc()
        self.rf_mainUi.rf_graphBgc()
        self.rf_mainUi.rf_nodeEditorVis()

    def updateUi(self):
        """ Update ui from graphObject """
        print "\n#-- Updating GrapherUi --#"
        self.rf_mainUi.rf_comment()
        self.rf_mainUi.rf_graphBgc()

    def getLockFile(self):
        """ Get lock file from GrapherObject
            @return: (str) : Lock file absolut path """
        if self.grapher._path is not None and self.grapher._file is not None:
            lockFile = self.grapher._file.replace('gp_', 'gpLock_')
            return os.path.join(self.grapher._path, lockFile)

    def checkLockFile(self):
        """ Check if lockFile exists """
        print "\n#-- Check Lock File --#"
        lockFile = self.getLockFile()
        if lockFile is not None:
            if not os.path.exists(lockFile):
                if self.createLockFile(lockFile):
                    self._lock = False
                    print "Lockfile successfully created."
                    self.updateUi()
            else:
                print "\tLockfile detected ..."
                lockParams = pFile.readPyFile(lockFile)
                mess = ["!!! WARNING !!!",
                        "Graph %s is already open:" % os.path.basename(lockFile).replace('gpLock_', 'gp_'),
                        "Locked by %s on %s" % (lockParams['user'], lockParams['station']),
                        "Date: %s" % lockParams['date'], "Time: %s" % lockParams['time']]
                self.lockDialog = dialog2.ConfirmDialog('\n'.join(mess),
                                  ["Read Only", "Break Lock", "Cancel"],
                                  [self.cmds_menu.openReadOnly, self.cmds_menu.breakLock,
                                   self.cmds_menu.openAbort], cancelBtn=False)
                self.lockDialog.exec_()

    @staticmethod
    def rf_zoneVisibility(checkBox, widgets, frameLayout):
        """ Refresh comment visibility
            @param checkBox: (object) : QCheckBox zone
            @param widgets: (list) : Widget list zone
            @param frameLayout: (object) : QFramLayout zone """
        for w in widgets:
            w.setVisible(checkBox.isChecked())
        if checkBox.isChecked():
            frameLayout.setMinimumHeight(50)
            frameLayout.setMaximumHeight(400)
        else:
            frameLayout.setMinimumHeight(40)
            frameLayout.setMaximumHeight(40)


def launch(graph=None):
    """ GrapherUi launcher """
    app = QtGui.QApplication(sys.argv)
    window = GrapherUi()
    window.cmds_menu.openGraph(graph=graph)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # fileName = "G:/ddd/assets/chars/main/anglaigus/gp_anglaigus.py"
    # launch(graph=fileName)
    launch()
