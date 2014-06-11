import os, sys
from lib import qt
from lib.qt.scripts import dialog2
from PyQt4 import QtGui, QtCore, uic
from lib.system.scripts import procFile as pFile


textEditorClass, textEditorUiClass = uic.loadUiType(qt.uiList['textEditor'])
class TextEditor(textEditorClass, textEditorUiClass):

    def __init__(self):
        super(TextEditor, self).__init__()
        self.iconDir = os.path.join(qt.toolPath, '_lib', 'ima', 'textEditor')
        self.sizeList = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,44,48,
                         54,60,66,72,80,88,96]
        self._setupUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupToolBarUp()
        self._setupToolBarDn()

    def _setupToolBarUp(self):
        #-- Clear Text --#
        self.bClearText = self.newToolBarBtn(os.path.join(self.iconDir, 'textClear.png'),
                                             self.on_clearText, "Clear text")
        self.toolBarUp.addWidget(self.bClearText)
        #-- Load File --#
        self.bLoadFile = self.newToolBarBtn(os.path.join(self.iconDir, 'fileLoad.png'),
                                            self.on_loadFile, "Load file")
        self.toolBarUp.addWidget(self.bLoadFile)
        #-- Save File --#
        self.bSaveFile = self.newToolBarBtn(os.path.join(self.iconDir, 'fileSave.png'),
                                            self.on_saveFile, "Save file")
        self.toolBarUp.addWidget(self.bSaveFile)
        #-- Copy Text --#
        self.toolBarUp.addSeparator()
        self.bTextCopy = self.newToolBarBtn(os.path.join(self.iconDir, 'textCopy.png'),
                                            self.on_textCopy, "Copy text")
        self.toolBarUp.addWidget(self.bTextCopy)
        #-- Cut Text --#
        self.bTextCut = self.newToolBarBtn(os.path.join(self.iconDir, 'textCut.png'),
                                           self.on_textCut, "Cut text")
        self.toolBarUp.addWidget(self.bTextCut)
        #-- Paste Text --#
        self.bTextPaste = self.newToolBarBtn(os.path.join(self.iconDir, 'textPaste.png'),
                                             self.on_textPaste, "Paste text")
        self.toolBarUp.addWidget(self.bTextPaste)
        #-- Undo --#
        self.toolBarUp.addSeparator()
        self.bUndo = self.newToolBarBtn(os.path.join(self.iconDir, 'undo.png'), self.on_undo, "Undo")
        self.toolBarUp.addWidget(self.bUndo)
        #-- Redo --#
        self.bRedo = self.newToolBarBtn(os.path.join(self.iconDir, 'redo.png'), self.on_undo, "Redo")
        self.toolBarUp.addWidget(self.bRedo)

    # noinspection PyUnresolvedReferences
    def _setupToolBarDn(self):
        #-- Font Style --#
        self.cbFontStyle = QtGui.QFontComboBox()
        self.cbFontStyle.setMaximumWidth(130)
        self.cbFontStyle.currentFontChanged.connect(self.on_fontStyle)
        self.cbFontStyle.setToolTip("Font style")
        self.toolBarDn.addWidget(self.cbFontStyle)
        #-- Font Size --#
        self.cbFontSize = QtGui.QComboBox()
        self.cbFontSize.addItems([str(s) for s in self.sizeList])
        self.cbFontSize.setCurrentIndex(2)
        self.cbFontSize.currentIndexChanged.connect(self.on_fontSize)
        self.cbFontSize.setToolTip("Font size")
        self.toolBarDn.addWidget(self.cbFontSize)
        #-- Font Color --#
        self.toolBarDn.addSeparator()
        self.bFontColor = self.newToolBarBtn(os.path.join(self.iconDir, 'fontColor.png'),
                                             self.on_fontColor, "Font color")
        self.toolBarDn.addWidget(self.bFontColor)
        #-- Font Bg Color --#
        self.bFontBgColor = self.newToolBarBtn(os.path.join(self.iconDir, 'fontBgColor.png'),
                                               self.on_fontBgColor, "Font bg color")
        self.toolBarDn.addWidget(self.bFontBgColor)
        #-- Font Bold --#
        self.toolBarDn.addSeparator()
        self.bFontBold = self.newToolBarBtn(os.path.join(self.iconDir, 'fontBold.png'),
                                            self.on_fontBold, "Bold")
        self.toolBarDn.addWidget(self.bFontBold)
        #-- Font Italic --#
        self.bFontItalic = self.newToolBarBtn(os.path.join(self.iconDir, 'fontItalic.png'),
                                              self.on_fontItalic, "Italic")
        self.toolBarDn.addWidget(self.bFontItalic)
        #-- Font Underline --#
        self.bFontUnderline = self.newToolBarBtn(os.path.join(self.iconDir, 'fontUnderline.png'),
                                                 self.on_fontUnderline, "Underline")
        self.toolBarDn.addWidget(self.bFontUnderline)
        #-- Align Left --#
        self.toolBarDn.addSeparator()
        self.bAlignLeft = self.newToolBarBtn(os.path.join(self.iconDir, 'alignLeft.png'),
                                             self.on_alignLeft, "Align left")
        self.toolBarDn.addWidget(self.bAlignLeft)
        #-- Align Center --#
        self.bAlignCenter = self.newToolBarBtn(os.path.join(self.iconDir, 'alignCenter.png'),
                                               self.on_alignCenter, "Align center")
        self.toolBarDn.addWidget(self.bAlignCenter)
        #-- Align Right --#
        self.bAlignRight = self.newToolBarBtn(os.path.join(self.iconDir, 'alignRight.png'),
                                              self.on_alignRight, "Align right")
        self.toolBarDn.addWidget(self.bAlignRight)
        #-- Align Justify --#
        self.bAlignJustify = self.newToolBarBtn(os.path.join(self.iconDir, 'alignJustify.png'),
                                                self.on_alignJustify, "Align justify")
        self.toolBarDn.addWidget(self.bAlignJustify)

    def on_clearText(self):
        self.teText.clear()

    def on_loadFile(self):
        self.fdLoad = dialog2.fileDialog(fdMode='open', fdFileMode='AnyFile', fdCmd=self.fd_loadAccept)
        self.fdLoad.exec_()

    def fd_loadAccept(self):
        fileIn = self.fdLoad.selectedFiles()
        if fileIn and not str(fileIn[0]) in ['', ' ']:
            fileName = str(fileIn[0]).split(os.sep)[-1]
            text = pFile.readFile(str(fileIn[0]))
            if fileName.endswith('.html'):
                self.teText.setHtml(''.join(text))
            else:
                self.teText.setText(''.join(text))

    def on_saveFile(self):
        self.fdSave = dialog2.fileDialog(fdMode='save', fdFileMode='AnyFile', fdCmd=self.fd_saveAccept)
        self.fdSave.exec_()

    def fd_saveAccept(self):
        fileOut = self.fdSave.selectedFiles()
        if fileOut and not str(fileOut[0]) in ['', ' ']:
            fileName = str(fileOut[0]).split(os.sep)[-1]
            if not '.' in fileName:
                fileName = '%s.html' % fileName
            try:
                if fileName.endswith('.html'):
                    pFile.writeFile(str(fileOut[0]), str(self.teText.toHtml()))
                else:
                    pFile.writeFile(str(fileOut[0]), str(self.teText.toPlainText()))
                print "File saved in %s" % str(fileOut[0])
            except:
                raise IOError("Can not write file !!!")

    def on_textCopy(self):
        self.teText.copy()

    def on_textCut(self):
        self.teText.cut()

    def on_textPaste(self):
        self.teText.paste()

    def on_undo(self):
        self.teText.undo()

    def on_redo(self):
        self.teText.redo()

    def on_fontStyle(self):
        font = QtGui.QFont(self.cbFontStyle.currentFont())
        self.teText.setCurrentFont(font)

    def on_fontSize(self):
        size = int(self.cbFontSize.itemText(self.cbFontSize.currentIndex()))
        self.teText.setFontPointSize(size)

    # noinspection PyArgumentList
    def on_fontColor(self):
        color = QtGui.QColorDialog.getColor()
        self.teText.setTextColor(color)

    # noinspection PyArgumentList
    def on_fontBgColor(self):
        color = QtGui.QColorDialog.getColor()
        self.teText.setTextBackgroundColor(color)

    def on_fontBold(self):
        if self.teText.fontWeight() == 50:
            self.teText.setFontWeight(QtGui.QFont.Bold)
        else:
            self.teText.setFontWeight(QtGui.QFont.Normal)

    def on_fontItalic(self):
        self.teText.setFontItalic(not self.teText.fontItalic())

    def on_fontUnderline(self):
        self.teText.setFontUnderline(not self.teText.fontUnderline())

    def on_alignLeft(self):
        self.teText.setAlignment(QtCore.Qt.AlignLeft)

    def on_alignCenter(self):
        self.teText.setAlignment(QtCore.Qt.AlignCenter)

    def on_alignRight(self):
        self.teText.setAlignment(QtCore.Qt.AlignRight)

    def on_alignJustify(self):
        self.teText.setAlignment(QtCore.Qt.AlignJustify)

    @staticmethod
    def newToolBarBtn(iconPath, cmd, toolTip):
        """ Create new toolBar action
            @param iconPath: (str) : Icon absolut path
            @param cmd: (object) : Command to connect
            @param toolTip: (str) : Tool tip
            @return: (object) : New toolBar button """
        newBtn = QtGui.QPushButton()
        newBtn.setIcon(QtGui.QIcon(iconPath))
        newBtn.clicked.connect(cmd)
        newBtn.setToolTip(toolTip)
        return newBtn

    @property
    def fileActionGrp(self):
        """ Get Actions of the group 'File'
            @return: (list) : List of file actions """
        return [self.bClearText, self.bLoadFile, self.bSaveFile]

    @property
    def editActionGrp(self):
        """ Get Actions of the group 'Edit'
            @return: (list) : List of edit actions """
        return [self.bTextCopy, self.bTextCut, self.bTextPaste, self.bUndo, self.bRedo]

    @property
    def textActionGrp(self):
        """ Get Actions of the group 'Text'
            @return: (list) : List of text actions """
        return [self.bAlignLeft, self.bAlignCenter, self.bAlignRight, self.bAlignJustify]

    @property
    def fontActionGrp(self):
        """ Get Actions of the group 'Font'
            @return: (list) : List of font actions """
        return [self.cbFontStyle, self.cbFontSize, self.bFontColor, self.bFontBgColor,
                self.bFontBold, self.bFontItalic, self.bFontUnderline]


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())