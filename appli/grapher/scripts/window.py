from PyQt4 import uic
from appli import grapher
from lib.qt.scripts import textEditor
from appli.grapher.scripts import refresh


nodeEditorClass, nodeEditorUiClass = uic.loadUiType(grapher.uiList['nodeEditor'])
class NodeEditor(nodeEditorClass, nodeEditorUiClass):
    """ Class used for graph nodes editing """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.rf_shared = refresh.SharedWidget(self.mainUi, self)
        super(NodeEditor, self).__init__()
        self._setupUi()
        self.initUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupMain()

    def _setupMain(self):
        #-- Comment Zone --#
        self.wgComment = TextEditor(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(self.rf_shared.rf_commentVis)
        #-- Variables Zone --#
        self.cbVariables.clicked.connect(self.rf_shared.rf_variablesVis)
        #-- Trash Zone --#
        self.cbTrash.clicked.connect(self.rf_shared.rf_trashVis)

    def initUi(self):
        """ Initialize ui """
        self.rf_shared.rf_commentVis()
        self.rf_shared.rf_commentBgc()
        self.rf_shared.rf_variablesVis()
        self.rf_shared.rf_variablesBgc()
        self.rf_shared.rf_trashVis()


class TextEditor(textEditor.TextEditorWidget):
    """ Class used by the grapherUi for text editing
        @param parent: (object) : QWidget parent """

    def __init__(self, parent):
        self.parent = parent
        self.stored = None
        super(TextEditor, self).__init__()
        self._setupWidget()
        self.rf_widgetVis()

    def _setupWidget(self):
        self.bClearText.setToolTip("Cancel Edition")
        self.bLoadFile.setToolTip("Start Edition")
        self.bSaveFile.setToolTip("Save Edition")

    def rf_widgetVis(self, state=False):
        """ Refresh widget visibility
            @param state: (bool) : Visibility state """
        self.bClearText.setEnabled(state)
        self.bLoadFile.setEnabled(not state)
        self.bSaveFile.setEnabled(state)
        self.flEdit.setEnabled(state)
        self.flSyntaxe.setEnabled(state)
        self.teText.setReadOnly(not state)

    def on_clearText(self):
        """ Switch widget visibility to disable edition and restore text """
        super(TextEditor, self).on_clearText()
        self.teText.setHtml(self.stored)
        self.rf_widgetVis()
        self.stored = None

    def on_loadFile(self):
        """ Switch widget visibility to enable edition """
        self.stored = self.teText.toHtml()
        self.rf_widgetVis(state=True)

    def on_saveFile(self):
        """ Switch widget visibility to disable edition and save text """
        self.stored = None
        self.rf_widgetVis()
        if str(self.parent.objectName()) == 'MainWindow':
            self.parent.grapher.ud_commentFromUi(self.parent)
