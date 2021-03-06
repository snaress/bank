import os, sys
from appli import grapher
from PyQt4 import QtGui, uic
from functools import partial
from lib.qt import procQt as pQt
from appli.grapher import grapher as gp
from lib.system import procFile as pFile
from appli.grapher import gpWidget, graphTree, nodeEditor, gpCmds, gpCore


grapherClass, grapherUiClass = uic.loadUiType(grapher.uiList['grapher'])
class GrapherUi(grapherClass, grapherUiClass, gpCore.FileCmds, gpCore.Style):
    """ Class containing all grapher's Ui actions for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self._lock = False
        self.grapher = gp.Grapher()
        self.menuStorage = {'studio': {}, 'prod': {}, 'users': {}}
        self.cmds_menu = gpCmds.Menu(self)
        super(GrapherUi, self).__init__()
        self._setupUi()
        self.initUi()

    def __getStr__(self):
        txt = ["\n", "========== GRAPHER UI ==========\n", "#-- Comment --#\n"]
        txt.append(self.wgComment.__getStr__())
        txt.append("\n")
        txt.append(self.wgVariables.__getStr__())
        txt.append("\n")
        txt.append(self.wgGraph.__getStr__())
        return ''.join(txt)

    def _setupUi(self):
        self.setupUi(self)
        self._setupMenu()
        self._setupMain()

    def _setupMenu(self):
        #-- Menu File --#
        self.miNewGraph.triggered.connect(self.cmds_menu.on_newGraph)
        self.miNewGraph.setShortcut("Ctrl+N")
        self.miOpenGraph.triggered.connect(self.cmds_menu.on_openGraph)
        self.miOpenGraph.setShortcut("Ctrl+O")
        self.miSaveGraph.triggered.connect(self.cmds_menu.on_saveGraph)
        self.miSaveGraph.setShortcut("Ctrl+S")
        self.miSaveGraphAs.triggered.connect(self.cmds_menu.on_saveGraphAs)
        self.miSaveGraphAs.setShortcut("Ctrl+Shift+S")
        self.miQuitGrapher.triggered.connect(self.cmds_menu.on_quitGrapher)
        self.miQuitGrapher.setShortcut("Ctrl+Shift+W")
        #-- Menu Lib --#
        self.menuStudio.aboutToShow.connect(self.cmds_menu.rf_studioMenu)
        self.menuProd.aboutToShow.connect(self.cmds_menu.rf_prodMenu)
        self.menuUsers.aboutToShow.connect(self.cmds_menu.rf_usersMenu)
        #-- Menu Window --#
        self.miNodeEditor.triggered.connect(self.cmds_menu.on_nodeEditor)
        self.miNodeEditor.setShortcut("Ctrl+E")
        self.miLibEditor.triggered.connect(self.cmds_menu.on_libEditor)
        self.miLibEditor.setShortcut("Ctrl+L")
        self.miXterm.triggered.connect(self.cmds_menu.on_xTerm)
        self.miXterm.setShortcut("Alt+O")
        self.miXplorer.triggered.connect(self.cmds_menu.on_xPlorer)
        self.miXplorer.setShortcut("Shift+O")
        self.miExecGraph.triggered.connect(self.cmds_menu.on_execGraph)
        self.miExecGraph.setShortcut("Alt+E")
        #-- Menu Help --#
        self.miGrapherRepr.triggered.connect(self.cmds_menu.on_grapherRepr)
        self.miGrapherRepr.setShortcut("Ctrl+G")
        self.miGrapherStr.triggered.connect(self.cmds_menu.on_grapherStr)
        self.miGrapherStr.setShortcut("Shift+G")
        self.miGrapherUiStr.triggered.connect(self.cmds_menu.on_grapherUiStr)
        self.miGrapherUiStr.setShortcut("Alt+G")

    def _setupMain(self):
        #-- Comment --#
        self.wgComment = gpWidget.Comment(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(partial(self.rf_commentVis, self))
        #-- Variables --#
        self.wgVariables = gpWidget.VarEditor(self, self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(partial(self.rf_variablesVis, self))
        #-- NodeEditor --#
        self.nodeEditor = nodeEditor.NodeEditor(self)
        self.vlNodeEditor.addWidget(self.nodeEditor)
        #-- Graph Tree --#
        self.wgGraph = graphTree.GraphTree(self)
        self.vlGraph.insertWidget(-1, self.wgGraph)

    def initUi(self):
        """ Initialize ui """
        self.rf_commentVis(self)
        self.rf_variablesVis(self)
        self.wgGraph.rf_graphBgc()
        self.nodeEditor.rf_nodeEditorVis()

    def updateUi(self):
        """ Update ui from graphObject """
        print "\n[grapherUI] : #-- Update GrapherUi --#"
        self.setWindowTitle("Grapher - %s" % self.grapher._file)
        print "\tUpdating grapher comment ..."
        self.wgComment.rf_comment(self.grapher.commentHtml)
        print "\tUpdating grapher variables ..."
        self.wgVariables.rf_variables(**self.grapher.variables)
        print "\tUpdating grapher tree ..."
        self.wgGraph.rf_graphBgc()
        self.wgGraph.rf_graph()
        print "[grapherUI] : Graph successfully loaded."

    def resetUi(self):
        """ Reset Grapher ui """
        print "\n[grapherUI] : #-- Reset GrapherUi --#"
        self.setWindowTitle("Grapher")
        print "\tReseting lock state ..."
        self._lock = False
        print "\tReseting grapher comment ..."
        self.wgComment.resetComment()
        print "\tReseting grapher variables ..."
        self.wgVariables.resetTree()
        print "\tReseting grapher tree ..."
        self.wgGraph.resetGraph()
        print "\tReseting node editor ..."
        self.nodeEditor.resetUi()

    @property
    def lockFile(self):
        """ Get lock file from GrapherObject
            @return: (str) : Lock file absolut path """
        if self.grapher._path is not None and self.grapher._file is not None:
            lockFile = self.grapher._file.replace('gp_', 'gpLock_')
            return os.path.join(self.grapher._path, lockFile)

    def checkLockFile(self):
        """ Check if lockFile exists """
        print "\n[grapherUI] : #-- Check Lock File --#"
        if self.lockFile is not None:
            if not os.path.exists(self.lockFile):
                if self.createLockFile(self.lockFile):
                    self._lock = False
                    print "[grapherUI] : Lockfile successfully created."
                    self.updateUi()
            else:
                print "\tLockfile detected ..."
                graph = os.path.basename(self.lockFile).replace('gpLock_', 'gp_')
                lockParams = pFile.readPyFile(self.lockFile)
                mess = ["!!! WARNING !!!",
                        "Graph %s is already open:" % graph,
                        "Locked by %s on %s" % (lockParams['user'], lockParams['station']),
                        "Date: %s" % lockParams['date'], "Time: %s" % lockParams['time']]
                self.lockDialog = pQt.ConfirmDialog('\n'.join(mess),
                                  ["Read Only", "Break Lock", "Cancel"],
                                  [self.cmds_menu.openReadOnly, self.cmds_menu.breakLock,
                                   self.cmds_menu.openAbort], cancelBtn=False)
                self.lockDialog.exec_()

    def rf_commentVis(self, parent):
        """ Refresh Grapher comment visibility """
        widgets = [parent.wgComment]
        self.rf_zoneVisibility(parent.cbComment, widgets, parent.flComment)

    def rf_variablesVis(self, parent):
        """ Refresh Grapher variables visibility """
        widgets = [parent.wgVariables.flVarBtns, parent.wgVariables.twVariables]
        self.rf_zoneVisibility(parent.cbVariables, widgets, parent.flVariables)

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

    def closeEvent(self, event):
        """ Command launch when GrapherUi is closed """
        print "\n[grapherUI] : #-- Close GrapherUi --#"
        if self.lockFile is not None:
            if os.path.exists(self.lockFile):
                self.removeLockFile(self.lockFile)


def launch(graph=None):
    """ GrapherUi launcher """
    app = QtGui.QApplication(sys.argv)
    window = GrapherUi()
    window.cmds_menu.openGraph(graph=graph)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # fileName = "F:/devZone/leVoeu/shots/s0020/p0010/gp_s0020_p0010.py"
    fileName = "G:/prods/rspn/logo/gp_logo.py"
    launch(graph=fileName)
    # launch()