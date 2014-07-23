from lib import qt
from PyQt4 import QtGui, QtCore, uic


scriptEditorClass, scriptEditorUiClass = uic.loadUiType(qt.uiList['scriptEditor'])
class ScriptEditor(scriptEditorClass, scriptEditorUiClass):

    def __init__(self):
        super(ScriptEditor, self).__init__()
        self._setupUi()

    def _setupUi(self):
        self.setupUi(self)
        self._widget = ScriptZone()
        self.glScriptEditor.addWidget(self._widget, 1, 1, 1, 1)

    def resetScript(self):
        self._widget.clear()


class ScriptZone(QtGui.QTextEdit):

    def __init__(self):
        super(ScriptZone, self).__init__()
        self._setupUi()
        char_format = QtGui.QTextCharFormat()
        char_format.setFont(self.font())
        self.highlighter = PythonHighlighter(self.document(), char_format)

    def _setupUi(self):
        self.setStyleSheet("background-color:rgb(50, 50, 50)")
        self._setupScriptFont()

    def _setupScriptFont(self):
        scriptFont = QtGui.QFont()
        scriptFont.setFamily('Courier')
        scriptFont.setStyleHint(QtGui.QFont.Monospace)
        scriptFont.setFixedPitch(True)
        scriptFont.setPointSize(10)
        metrics = QtGui.QFontMetrics(scriptFont)
        self.setFont(scriptFont)
        self.setTextColor(QtGui.QColor(200, 200, 200))
        self.setTabStopWidth(4 * metrics.width(' '))

    def getCode(self):
        self._code = self.toPlainText()
        return self._code

    def setCode(self, text):
        self.setPlainText(text)

    code = QtCore.pyqtProperty(str, getCode, setCode)

    def getDisplayFont(self):
        return QtGui.QWidget.font(self)

    def setDisplayFont(self, font):
        QtGui.QWidget.setFont(self, font)
        self.highlighter.updateHighlighter(font)
        self.update()

    displayFont = QtCore.pyqtProperty(QtGui.QFont, getDisplayFont, setDisplayFont)


class PythonHighlighter(QtGui.QSyntaxHighlighter):

    keyWords1 = ("and", "assert", "break", "class", "continue", "def", "del", "elif", "else",
                 "except", "exec", "finally", "for", "from", "global", "if", "import", "in", "is",
                 "lambda", "not", "or", "pass", "print", "return", "try", "while", "yield")
    keyWords2 = ("basestring", "delattr", "dict", "execfile", "float", "getattr", "int",
                 "isinstance", "list", "map", "max", "min", "None", "object","setattr", "str",
                 "super")

    def __init__(self, document, base_format):
        super(PythonHighlighter, self).__init__(document)
        self.base_format = base_format
        self.document = document
        self.updateHighlighter(base_format.font())

    def highlightBlock(self, text):
        self.setCurrentBlockState(0)
        if text.trimmed().isEmpty():
            self.setFormat(0, len(text), self.empty_format)
            return
        self.setFormat(0, len(text), self.base_format)
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = text.indexOf(self.multiLineStringBegin)
        if startIndex > -1:
            self.highlightRules(text, 0, startIndex)
        else:
            self.highlightRules(text, 0, len(text))
        while startIndex >= 0:
            endIndex = text.indexOf(self.multiLineStringEnd,
                                    startIndex + len(self.multiLineStringBegin.pattern()))
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = text.length() - startIndex
            else:
                commentLength = endIndex - startIndex + self.multiLineStringEnd.matchedLength()
                self.highlightRules(text, endIndex, len(text))
            self.setFormat(startIndex, commentLength, self.multiLineStringFormat)
            startIndex = text.indexOf(self.multiLineStringBegin, startIndex + commentLength)

    def highlightRules(self, text, start, finish):
        for expression, format in self.rules:
            index = expression.indexIn(text, start)
            while index >= start and index < finish:
                length = expression.matchedLength()
                self.setFormat(index, min(length, finish - index), format)
                index = expression.indexIn(text, index + length)

    def updateFonts(self, font):
        self.base_format.setFont(font)
        self.empty_format = QtGui.QTextCharFormat(self.base_format)
        self.empty_format.setFontPointSize(font.pointSize()/4.0)
        self.keywordFormat1 = QtGui.QTextCharFormat(self.base_format)
        self.keywordFormat1.setForeground(QtGui.QColor(224, 128, 0))
        self.keywordFormat1.setFontWeight(QtGui.QFont.Bold)
        self.keywordFormat2 = QtGui.QTextCharFormat(self.base_format)
        self.keywordFormat2.setForeground(QtGui.QColor(25, 105, 255))
        self.keywordFormat2.setFontWeight(QtGui.QFont.Bold)
        self.magicFormat = QtGui.QTextCharFormat(self.base_format)
        self.magicFormat.setForeground(QtGui.QColor(170, 0, 255))
        self.selfFormat = QtGui.QTextCharFormat(self.base_format)
        self.selfFormat.setForeground(QtGui.QColor(170, 85, 255))
        self.singleLineCommentFormat = QtGui.QTextCharFormat(self.base_format)
        self.singleLineCommentFormat.setForeground(QtGui.QColor(150, 150, 150))
        self.multiLineStringFormat = QtGui.QTextCharFormat(self.base_format)
        self.multiLineStringFormat.setForeground(QtGui.QColor(90, 150, 40))
        self.quotationFormat = QtGui.QTextCharFormat(self.base_format)
        self.quotationFormat.setForeground(QtGui.QColor(200, 225, 55))

    def updateRules(self):
        self.rules = []
        self.rules += map(lambda s: (QtCore.QRegExp(r"\b"+s+r"\b"),
                                     self.keywordFormat1), self.keyWords1)
        self.rules += map(lambda s: (QtCore.QRegExp(r"\b"+s+r"\b"),
                                     self.keywordFormat2), self.keyWords2)
        self.rules.append((QtCore.QRegExp(r"\b__[a-z]+__\b"), self.magicFormat))
        self.rules.append((QtCore.QRegExp(r"\bself\b"), self.selfFormat))
        self.rules.append((QtCore.QRegExp(r"#[^\n]*"), self.singleLineCommentFormat))
        self.multiLineStringBegin = QtCore.QRegExp(r'\"\"\"')
        self.multiLineStringEnd = QtCore.QRegExp(r'\"\"\"')
        self.rules.append((QtCore.QRegExp(r'\"[^\n]*\"'), self.quotationFormat))
        self.rules.append((QtCore.QRegExp(r"'[^\n]*'"), self.quotationFormat))

    def updateHighlighter(self, font):
        self.updateFonts(font)
        self.updateRules()
        self.setDocument(self.document)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = ScriptEditor()
    window.resize(640, 512)
    window.show()
    sys.exit(app.exec_())