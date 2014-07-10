import os, sys
from appli import grapher
from PyQt4 import QtGui, uic
from functools import partial
from lib.qt.scripts import procQt as pQt
from appli.grapher.scripts import grapher as gp
from lib.system.scripts import procFile as pFile
from appli.grapher.scripts import widgets, varTree, graphTree, cmds, core


grapherClass, grapherUiClass = uic.loadUiType(grapher.uiList['grapher'])
class GrapherUi(grapherClass, grapherUiClass, core.FileCmds, core.Style):
    """ Class containing all grapher's Ui actions for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self._lock = False
        self.grapher = gp.Grapher()
        self.cmds_menu = cmds.Menu(self)
        super(GrapherUi, self).__init__()
        self._setupUi()
        self.initUi()

    def __str__(self):
        txt = ["\n", "========== GRAPHER UI ==========\n", "#-- Comment --#\n"]
        txt.append(self.wgComment.__str__())
        txt.append("\n")
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
        #-- Menu Window --#
        self.miNodeEditor.triggered.connect(self.cmds_menu.on_nodeEditor)
        self.miNodeEditor.setShortcut("E")
        self.miXterm.triggered.connect(self.cmds_menu.on_xTerm)
        self.miXterm.setShortcut("Alt+O")
        self.miXplorer.triggered.connect(self.cmds_menu.on_xPlorer)
        self.miXplorer.setShortcut("Shift+O")
        #-- Menu Help --#
        self.miGrapherRepr.triggered.connect(self.cmds_menu.on_grapherRepr)
        self.miGrapherRepr.setShortcut("Ctrl+G")
        self.miGrapherStr.triggered.connect(self.cmds_menu.on_grapherStr)
        self.miGrapherStr.setShortcut("Shift+G")
        self.miGrapherUiStr.triggered.connect(self.cmds_menu.on_grapherUiStr)
        self.miGrapherUiStr.setShortcut("Alt+G")

    def _setupMain(self):
        #-- Comment --#
        self.wgComment = widgets.Comment(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(partial(self.rf_commentVis, self))
        #-- Variables --#
        self.wgVariables = varTree.VarEditor(self, self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(partial(self.rf_variablesVis, self))
        #-- Graph Tree --#
        self.wgGraph = graphTree.GraphTree(self)
        self.vlGraph.insertWidget(-1, self.wgGraph)
        #-- NodeEditor --#
        self.nodeEditor = NodeEditor(self)
        self.vlNodeEditor.addWidget(self.nodeEditor)

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


nodeEditorClass, nodeEditorUiClass = uic.loadUiType(grapher.uiList['nodeEditor'])
class NodeEditor(nodeEditorClass, nodeEditorUiClass):
    """ Class used for graph nodes edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.graphNode = None
        super(NodeEditor, self).__init__()
        self._setupUi()
        self.initUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupMain()

    def _setupMain(self):
        #-- Node Version --#
        self.leVersionTitle.returnPressed.connect(self.on_versionTitle)
        self.cbNodeVersion.currentIndexChanged.connect(self.on_version)
        self.bNewVersion.clicked.connect(self.on_newVersion)
        #-- Comment --#
        self.wgComment = widgets.Comment(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(partial(self.mainUi.rf_commentVis, self))
        #-- Variables --#
        self.wgVariables = varTree.VarEditor(self.mainUi, self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(partial(self.mainUi.rf_variablesVis, self))

    def initUi(self):
        """ Initialize ui """
        self.mainUi.rf_commentVis(self)
        self.mainUi.rf_variablesVis(self)

    def resetUi(self):
        """ Reset NodeEditor ui """
        self.wgComment.resetComment()
        self.wgVariables.resetTree()

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.mainUi.flNodeEditor.setVisible(self.mainUi.miNodeEditor.isChecked())

    def rf_versionTitle(self):
        """ Refresh node version title """
        title = self.graphNode._data.versionTitle[self.currentVersion]
        self.leVersionTitle.setText(title)

    def rf_versionList(self, versions):
        """ Refresh node version list
            @param versions: (list) : Version list """
        self.cbNodeVersion.clear()
        self.cbNodeVersion.addItems(versions)

    def connectToGraphNode(self, graphNode):
        """ Update nodeEditor with given graphNode
            @param graphNode: (object) : QTreeWidgetItem """
        self.graphNode = graphNode
        nodeDict = self.graphNode.__repr__()
        print "\n[grapherUI] : Connecting node editor to %s" % nodeDict['nodeName']
        self.leNodeName.setText(nodeDict['nodeName'])
        self.cbNodeType.setCurrentIndex(self.cbNodeType.findText(nodeDict['nodeType']))
        self.leVersionTitle.setText(nodeDict['versionTitle'][nodeDict['currentVersion']])
        self.rf_versionList(sorted(nodeDict['versionTitle'].keys()))
        self.cbNodeVersion.setCurrentIndex(self.cbNodeVersion.findText(nodeDict['currentVersion']))

    def on_versionTitle(self):
        """ Command launch when leVersionTitle has changed """
        self.graphNode._data.versionTitle[self.currentVersion] = str(self.leVersionTitle.text())

    def on_version(self):
        """ Command launch when cbNodeVersion has changed """
        self.graphNode._data.currentVersion = self.currentVersion
        self.rf_versionTitle()

    def on_newVersion(self):
        """ Command launch when bAddVersion is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            items = pQt.getComboBoxItems(self.cbNodeVersion)
            newVersion = str(int(max(items)) + 1).zfill(3)
            self.graphNode._data.versionTitle[newVersion] = "New Version"
            self.graphNode._data.currentVersion = newVersion
            self.cbNodeVersion.addItem(newVersion)
            self.cbNodeVersion.setCurrentIndex(self.cbNodeVersion.findText(newVersion))

    @property
    def currentVersion(self):
        """ Get current version from ui
            @return: (str) : Current version """
        return str(self.cbNodeVersion.itemText(self.cbNodeVersion.currentIndex()))


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