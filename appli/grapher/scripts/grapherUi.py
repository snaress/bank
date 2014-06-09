import sys
from appli import grapher
from PyQt4 import QtGui, uic
from appli.grapher.scripts import grapher as gp
from appli.grapher.scripts import refresh, cmds, window


grapherClass, grapherUiClass = uic.loadUiType(grapher.uiList['grapher'])
class GrapherUi(grapherClass, grapherUiClass):
    """ Class containing all grapher's Ui actions for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self.grapher = gp.Grapher()
        self.style = refresh.Style()
        self.rf_mainUi = refresh.MainUi(self)
        self.rf_shared = refresh.SharedWidget(self, self)
        self.cmds_menu = cmds.Menu(self)
        self.window = window
        super(GrapherUi, self).__init__()
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

    def closeEvent(self, event):
        """ Set QMainWindow closeEvent, called when GrapherUi is closed """
        QtGui.QMainWindow.closeEvent(self, event)
        print 'Exit Grapher ...'

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


def launch():
    """ GrapherUi launcher """
    app = QtGui.QApplication(sys.argv)
    window = GrapherUi()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
