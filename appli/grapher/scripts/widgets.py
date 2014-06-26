from lib.qt.scripts import textEditor


class Comment(textEditor.TextEditor):
    """ Class used by the grapherUi for text edition
        @param parent: (object) : QWidget parent """

    def __init__(self, parent):
        self.parent = parent
        self.stored = None
        super(Comment, self).__init__()
        self._setupWidget()
        self.rf_widgetVis()

    def __repr__(self):
        return {'commentHtml': str(self.teText.toHtml()),
                'commentTxt': str(self.teText.toPlainText())}

    def __str__(self):
        return self.__repr__()['commentTxt']

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
        for grp in [self.editActionGrp, self.textActionGrp, self.fontActionGrp]:
            for widget in grp:
                widget.setEnabled(state)
        self.teText.setReadOnly(not state)

    def rf_comment(self, textHtml):
        """ Refresh Grapher comment
            @param textHtml: (str) : Comment in html form """
        self.teText.setHtml(textHtml)

    def on_clearText(self):
        """ Switch widget visibility to disable edition and restore text """
        super(Comment, self).on_clearText()
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
        if str(self.parent.objectName()) == 'grapherUi':
            self.parent.grapher.ud_commentFromUi(self.parent)

    def resetComment(self):
        """ Reset Grapher comment """
        self.teText.clear()

