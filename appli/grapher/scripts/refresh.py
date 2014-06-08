class MainUi(object):
    """ Class used by the grapherUi to refresh and update mainUi
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.style = self.mainUi.style

    def rf_graphBgc(self):
        """ Refresh graph background color """
        self.mainUi.twGraph.setStyleSheet(self.style.graphBgc)


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
        self.ui.twVariables.setStyleSheet(self.style.variablesBgc)

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.ui.flNodeEditor.setVisible(self.ui.miNodeEditor.isChecked())

    def rf_trashVis(self):
        """ Refresh Grapher trash visibility """
        widgets = [self.ui.teTrash]
        self.mainUi.rf_zoneVisibility(self.ui.cbTrash, widgets, self.ui.flTrash)


class TextEditor(object):
    """ Class used by the grapherUi for text editing
        @param textEditor: (object) : QWidget """

    def __init__(self, textEditor):
        self.textEditor = textEditor

    def widgetVis(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.textEditor.bClearText.setEnabled(state)
        self.textEditor.bLoadFile.setEnabled(not state)
        self.textEditor.bSaveFile.setEnabled(state)
        self.textEditor.flEdit.setEnabled(state)
        self.textEditor.flSyntaxe.setEnabled(state)
        self.textEditor.teText.setReadOnly(not state)


class Style(object):
    """ Class used for grapher style settings """

    def __init__(self):
        pass

    @property
    def commentBgc(self):
        return "background-color:DarkGrey;"

    @property
    def variablesBgc(self):
        return "background-color:AliceBlue;"

    @property
    def graphBgc(self):
        return "background-color:Black;"
