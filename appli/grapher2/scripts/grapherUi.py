import sys, os
from appli import grapher2
from PyQt4 import QtGui, uic
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import procFile as pFile
from appli.grapher2.scripts import grapher as gp
from appli.grapher2.scripts import cmds, widgets, core


grapherClass, grapherUiClass = uic.loadUiType(grapher2.uiList['grapher'])
class GrapherUi(grapherClass, grapherUiClass, core.FileCmds, widgets.Style):
    """ Class containing all grapher2's Ui actions for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self.grapher = gp.Grapher()
        self.rf_shared = cmds.SharedWidget(self, self)
        self.cmds_menu = cmds.Menu(self)
        self.window = widgets
        super(GrapherUi, self).__init__()
        self._lock = False
        self._setupUi()
        self.initUi()

    def __str__(self):
        txt = ["\n", "========== GRAPHER UI ==========\n"]
        txt.append(self.wgVariables.__str__())
        txt.append("\n")
        txt.append(self.wgGraph.__str__())
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
        self.miGrapherUiStr.triggered.connect(self.cmds_menu.on_grapherUiStr)
        self.miGrapherUiStr.setShortcut("Ctrl+Shift+G")

    def _setupMain(self):
        #-- Comment Zone --#
        self.wgComment = self.window.TextEditor(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(self.rf_shared.rf_commentVis)
        #-- Variables Zone --#
        self.wgVariables = self.window.VarEditor(self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(self.rf_shared.rf_variablesVis)
        #-- Graph Zone --#
        self.wgGraph = self.window.GraphZone(self)
        self.vlGraph.insertWidget(-1, self.wgGraph)
        #-- NodeEditor Zone --#
        self.nodeEditor = NodeEditor(self)
        self.vlNodeEditor.addWidget(self.nodeEditor)

    def initUi(self):
        """ Initialize ui """
        self.rf_shared.rf_commentVis()
        self.rf_shared.rf_variablesVis()
        self.wgGraph.rf_graphBgc()
        self.nodeEditor.rf_nodeEditorVis()

    def updateUi(self):
        """ Update ui from graphObject """
        print "\n[grapherUI] : #-- Update GrapherUi --#"
        self.setWindowTitle("Grapher - %s" % self.grapher._file)
        print "\tUpdating grapher2 comment ..."
        self.wgComment.rf_comment(self.grapher.commentHtml)
        print "\tUpdating grapher2 variables ..."
        self.wgVariables.rf_variables(**self.grapher.variables)
        print "\tUpdating grapher2 tree ..."
        self.wgGraph.rf_graphBgc()
        self.wgGraph.rf_graph()
        print "[grapherUI] : Graph successfully loaded."

    def resetUi(self):
        """ Reset Grapher ui """
        print "\n[grapherUI] : #-- Reset GrapherUi --#"
        self.setWindowTitle("Grapher")
        print "\tReseting lock state ..."
        self._lock = False
        print "\tReseting grapher2 comment ..."
        self.wgComment.resetComment()
        print "\tReseting grapher2 variables ..."
        self.wgVariables.resetVariables()
        print "\tReseting grapher2 tree ..."
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
        print "\n[grapherUI] : #-- Close GrapherUi --#"
        if self.lockFile is not None:
            if os.path.exists(self.lockFile):
                self.removeLockFile(self.lockFile)


nodeEditorClass, nodeEditorUiClass = uic.loadUiType(grapher2.uiList['nodeEditor'])
class NodeEditor(nodeEditorClass, nodeEditorUiClass):
    """ Class used for graph nodes edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.rf_shared = cmds.SharedWidget(self.mainUi, self)
        self.window = widgets
        super(NodeEditor, self).__init__()
        self._setupUi()
        self.initUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupMain()

    def _setupMain(self):
        #-- Comment Zone --#
        self.wgComment = self.window.TextEditor(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(self.rf_shared.rf_commentVis)
        #-- Variables Zone --#
        self.wgVariables = self.window.VarEditor(self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(self.rf_shared.rf_variablesVis)
        #-- Trash Zone --#
        self.cbTrash.clicked.connect(self.rf_trashVis)

    def initUi(self):
        """ Initialize ui """
        self.rf_shared.rf_commentVis()
        self.rf_shared.rf_variablesVis()
        self.rf_trashVis()

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.mainUi.flNodeEditor.setVisible(self.mainUi.miNodeEditor.isChecked())

    def rf_trashVis(self):
        """ Refresh nodeEditor trash visibility """
        widgets = [self.teTrash]
        self.mainUi.rf_zoneVisibility(self.cbTrash, widgets, self.flTrash)

    def resetUi(self):
        """ Reset NodeEditor ui """
        self.wgComment.resetComment()
        self.wgVariables.resetVariables()


def launch(graph=None):
    """ GrapherUi launcher """
    app = QtGui.QApplication(sys.argv)
    window = GrapherUi()
    window.cmds_menu.openGraph(graph=graph)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    fileName = "G:/ddd/assets/chars/main/anglaigus/gp_anglaigus.py"
    launch(graph=fileName)
    # launch()
