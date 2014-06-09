class MainUi(object):
    """ Class used by the grapherUi to refresh and update mainUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.style = self.mainUi.style

    def rf_comment(self):
        """ Refresh Grapher comment """
        print "\tUpdating grapher comment ..."
        self.mainUi.wgComment.teText.setHtml(self.grapher.commentHtml)

    def rf_graphBgc(self):
        """ Refresh graph background color """
        self.mainUi.twGraph.setStyleSheet(self.style.graphBgc)

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
        self.style = self.mainUi.style

    def rf_commentVis(self):
        """ Refresh Grapher comment visibility """
        widgets = [self.ui.wgComment]
        self.mainUi.rf_zoneVisibility(self.ui.cbComment, widgets, self.ui.flComment)

    def rf_commentBgc(self):
        """ Refresh comment background color """
        self.ui.flComment.setStyleSheet(self.style.commentBgc)

    def rf_variablesVis(self):
        """ Refresh Grapher variables visibility """
        widgets = [self.ui.flVarBtns, self.ui.twVariables]
        self.mainUi.rf_zoneVisibility(self.ui.cbVariables, widgets, self.ui.flVariables)

    def rf_variablesBgc(self):
        """ Refresh variables background color """
        self.ui.flVariables.setStyleSheet(self.style.variablesBgc)

    def rf_trashVis(self):
        """ Refresh Grapher trash visibility """
        widgets = [self.ui.teTrash]
        self.mainUi.rf_zoneVisibility(self.ui.cbTrash, widgets, self.ui.flTrash)


class Style(object):
    """ Class used for grapher style settings """

    def __init__(self):
        pass

    @property
    def commentBgc(self):
        return "background-color:DarkGrey;"

    @property
    def variablesBgc(self):
        return "background-color:LightCyan;"

    @property
    def graphBgc(self):
        return "background-color:Black;"
