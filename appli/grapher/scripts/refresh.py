class MainUi(object):
    """ Class used by the grapherUi to refresh and update mainUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher

    def rf_comment(self):
        """ Refresh Grapher comment """
        print "\tUpdating grapher comment ..."
        self.mainUi.wgComment.teText.setHtml(self.grapher.commentHtml)

    def rf_graphBgc(self):
        """ Refresh graph background color """
        if not self.mainUi._lock:
            self.mainUi.twGraph.setStyleSheet(self.mainUi.graphBgc)
        else:
            self.mainUi.twGraph.setStyleSheet(self.mainUi.lockColor)

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.mainUi.flNodeEditor.setVisible(self.mainUi.miNodeEditor.isChecked())


class SharedWidget(object):
    """ Class used by the grapherUi to refresh and update shared widgets
        @param mainUi: (object) : QMainWindow
        @param ui: (object) : Widgets parent """

    def __init__(self, mainUi, ui):
        self.mainUi = mainUi
        self.ui = ui

    def rf_commentVis(self):
        """ Refresh Grapher comment visibility """
        widgets = [self.ui.wgComment]
        self.mainUi.rf_zoneVisibility(self.ui.cbComment, widgets, self.ui.flComment)

    def rf_commentBgc(self):
        """ Refresh comment background color """
        self.ui.flComment.setStyleSheet(self.mainUi.commentBgc)

    def rf_variablesVis(self):
        """ Refresh Grapher variables visibility """
        widgets = [self.ui.flVarBtns, self.ui.twVariables]
        self.mainUi.rf_zoneVisibility(self.ui.cbVariables, widgets, self.ui.flVariables)

    def rf_variablesBgc(self):
        """ Refresh variables background color """
        self.ui.flVariables.setStyleSheet(self.mainUi.variablesBgc)


class NodeEditor(object):
    """ Class used by the nodeEditor to refresh and update widgets
        @param mainUi: (object) : QMainWindow
        @param ui: (object) : Widgets parent """

    def __init__(self, mainUi, ui):
        self.mainUi = mainUi
        self.ui = ui

    def rf_trashVis(self):
        """ Refresh Grapher trash visibility """
        widgets = [self.ui.teTrash]
        self.mainUi.rf_zoneVisibility(self.ui.cbTrash, widgets, self.ui.flTrash)
