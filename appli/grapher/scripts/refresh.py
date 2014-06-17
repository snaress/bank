class SharedWidget(object):
    """ Class used by the grapherUi to refresh and update shared widgets
        @param mainUi: (object) : QMainWindow
        @param ui: (object) : Widgets parent """

    def __init__(self, mainUi, ui):
        self.ui = ui
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher

    def rf_commentVis(self):
        """ Refresh Grapher comment visibility """
        widgets = [self.ui.wgComment]
        self.mainUi.rf_zoneVisibility(self.ui.cbComment, widgets, self.ui.flComment)

    def rf_variablesVis(self):
        """ Refresh Grapher variables visibility """
        widgets = [self.ui.wgVariables.flVarBtns, self.ui.wgVariables.twVariables]
        self.mainUi.rf_zoneVisibility(self.ui.cbVariables, widgets, self.ui.flVariables)

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.mainUi.flNodeEditor.setVisible(self.mainUi.miNodeEditor.isChecked())

    def rf_graphBgc(self):
        """ Refresh graph background color """
        if not self.mainUi._lock:
            self.mainUi.twGraph.setStyleSheet(self.mainUi.graphBgc)
        else:
            self.mainUi.twGraph.setStyleSheet(self.mainUi.lockColor)
