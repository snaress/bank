import os
import sys
from lib import qt
from PyQt4 import QtGui, QtCore, uic
from lib.system.scripts import procFile as pFile


textEditorClass, textEditorUiClass = uic.loadUiType(qt.uiList['textEditorWidget2'])
class TextEditorWidget(textEditorClass, textEditorUiClass):

    def __init__(self):
        self.iconDir = os.path.join(qt.toolPath, '_lib', 'ima', 'textEditor')
        super(TextEditorWidget, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup Widget """
        self.setupUi(self)
        self._setupToolBarUp()
        self._setupToolBarDn()

    def _setupToolBarUp(self):
        """ Setup widget toolBar up """
        #-- Clear --#
        self.bClearText.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'textClear.png')))
        self.bClearText.clicked.connect(self.on_clearText)
        self.bClearText.setToolTip("Clear text")
        #-- Load File --#
        self.bLoadFile.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fileLoad.png')))
        self.bLoadFile.clicked.connect(self.on_loadFile)
        self.bLoadFile.setToolTip("Load file")
        #-- Save File --#
        self.bSaveFile.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fileSave.png')))
        self.bSaveFile.clicked.connect(self.on_saveFile)
        self.bSaveFile.setToolTip("Save file")
        #-- Copy Text --#
        self.bTextCopy.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'textCopy.png')))
        self.bTextCopy.clicked.connect(self.on_textCopy)
        self.bTextCopy.setToolTip("Copy text")
        #-- Cut Text --#
        self.bTextCut.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'textCut.png')))
        self.bTextCut.clicked.connect(self.on_textCut)
        self.bTextCut.setToolTip("Cut text")
        #-- Paste Text --#
        self.bTextPaste.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'textPaste.png')))
        self.bTextPaste.clicked.connect(self.on_textPaste)
        self.bTextPaste.setToolTip("Paste text")
        #-- Undo --#
        self.bUndo.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'undo.png')))
        self.bUndo.clicked.connect(self.on_undo)
        self.bUndo.setToolTip("Undo")
        #-- Redo --#
        self.bRedo.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'redo.png')))
        self.bRedo.clicked.connect(self.on_undo)
        self.bRedo.setToolTip("Redo")

    def _setupToolBarDn(self):
        """ Setup widget toolBar down """
        #-- Font Size --#
        sizeList = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,44,48,54,60,66,72,80,88,96]
        self.cbFontSize.addItems([str(s) for s in sizeList])
        self.cbFontSize.setCurrentIndex(2)
        self.cbFontSize.currentIndexChanged.connect(self.on_fontSize)
        self.cbFontSize.setToolTip("Font size")
        #-- Font Color --#
        self.bFontColor.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fontColor.png')))
        self.bFontColor.clicked.connect(self.on_fontColor)
        self.bFontColor.setToolTip("Font color")
        #-- Font Bg Color --#
        self.bFontBgColor.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fontBgColor.png')))
        self.bFontBgColor.clicked.connect(self.on_fontBgColor)
        self.bFontBgColor.setToolTip("Font bg color")
        #-- Font Bold --#
        self.bFontBold.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fontBold.png')))
        self.bFontBold.clicked.connect(self.on_fontBold)
        self.bFontBold.setToolTip("Bold")
        #-- Font Italic --#
        self.bFontItalic.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fontItalic.png')))
        self.bFontItalic.clicked.connect(self.on_fontItalic)
        self.bFontItalic.setToolTip("Italic")
        #-- Font Underline --#
        self.bFontUnderline.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'fontUnderline.png')))
        self.bFontUnderline.clicked.connect(self.on_fontUnderline)
        self.bFontUnderline.setToolTip("Underline")
        #-- Align Left --#
        self.bAlignLeft.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'alignLeft.png')))
        self.bAlignLeft.clicked.connect(self.on_alignLeft)
        self.bAlignLeft.setToolTip("Align left")
        #-- Align Center --#
        self.bAlignCenter.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'alignCenter.png')))
        self.bAlignCenter.clicked.connect(self.on_alignCenter)
        self.bAlignCenter.setToolTip("Align center")
        #-- Align Right --#
        self.bAlignRight.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'alignRight.png')))
        self.bAlignRight.clicked.connect(self.on_alignRight)
        self.bAlignRight.setToolTip("Align right")
        #-- Align Justify --#
        self.bAlignJustify.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'alignJustify.png')))
        self.bAlignJustify.clicked.connect(self.on_alignJustify)
        self.bAlignJustify.setToolTip("Align justify")

    def on_clearText(self):
        """ Clear text cmd """
        self.teText.clear()

    def on_loadFile(self):
        """ Launch the load fileDialog """
        self.fdLoad = QtGui.QFileDialog()
        self.fdLoad.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        self.fdLoad.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdLoad.accepted.connect(self.fd_loadAccept)
        self.fdLoad.exec_()

    def fd_loadAccept(self):
        """ Load text from given file """
        fileIn = self.fdLoad.selectedFiles()
        if fileIn and not str(fileIn[0]) in ['', ' ']:
            fileName = str(fileIn[0]).split(os.sep)[-1]
            text = pFile.readFile(str(fileIn[0]))
            if fileName.endswith('.html'):
                self.teText.setHtml(''.join(text))
            else:
                self.teText.setText(''.join(text))

    def on_saveFile(self):
        """ Launch the save fileDialog """
        self.fdSave = QtGui.QFileDialog()
        self.fdSave.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        self.fdSave.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdSave.accepted.connect(self.fd_saveAccept)
        self.fdSave.exec_()

    def fd_saveAccept(self):
        """ Save text to given file (default extension is html) """
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
        """ Copy text cmd """
        self.teText.copy()

    def on_textCut(self):
        """ Cut text cmd """
        self.teText.cut()

    def on_textPaste(self):
        """ Paste text cmd """
        self.teText.paste()

    def on_undo(self):
        """ Undo cmd """
        self.teText.undo()

    def on_redo(self):
        """ Undo cmd """
        self.teText.redo()

    def on_fontSize(self):
        """ Change font size cmd """
        size = int(self.cbFontSize.itemText(self.cbFontSize.currentIndex()))
        self.teText.setFontPointSize(size)

    # noinspection PyArgumentList
    def on_fontColor(self):
        """ Change font color cmd """
        color = QtGui.QColorDialog.getColor()
        self.teText.setTextColor(color)

    # noinspection PyArgumentList
    def on_fontBgColor(self):
        """ Change font background color cmd """
        color = QtGui.QColorDialog.getColor()
        self.teText.setTextBackgroundColor(color)

    def on_fontBold(self):
        """ Change font to bold cmd """
        if self.teText.fontWeight() == 50:
            self.teText.setFontWeight(QtGui.QFont.Bold)
        else:
            self.teText.setFontWeight(QtGui.QFont.Normal)

    def on_fontItalic(self):
        """ Change font to italic cmd """
        self.teText.setFontItalic(not self.teText.fontItalic())

    def on_fontUnderline(self):
        """ Change font to underline cmd """
        self.teText.setFontUnderline(not self.teText.fontUnderline())

    def on_alignLeft(self):
        """ Align text left side """
        self.teText.setAlignment(QtCore.Qt.AlignLeft)

    def on_alignCenter(self):
        """ Align text center """
        self.teText.setAlignment(QtCore.Qt.AlignCenter)

    def on_alignRight(self):
        """ Align text right side """
        self.teText.setAlignment(QtCore.Qt.AlignRight)

    def on_alignJustify(self):
        """ Align text justify """
        self.teText.setAlignment(QtCore.Qt.AlignJustify)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = TextEditorWidget()
    window.show()
    sys.exit(app.exec_())
