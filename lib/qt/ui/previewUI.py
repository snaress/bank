# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\lib\qt\ui\preview.ui'
#
# Created: Fri Oct 17 13:53:20 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_preview(object):
    def setupUi(self, preview):
        preview.setObjectName(_fromUtf8("preview"))
        preview.resize(200, 250)
        self.gridLayout = QtGui.QGridLayout(preview)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.qfButtonsUp = QtGui.QFrame(preview)
        self.qfButtonsUp.setMaximumSize(QtCore.QSize(200, 16777215))
        self.qfButtonsUp.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfButtonsUp.setObjectName(_fromUtf8("qfButtonsUp"))
        self.hlButtonsUp = QtGui.QHBoxLayout(self.qfButtonsUp)
        self.hlButtonsUp.setSpacing(0)
        self.hlButtonsUp.setMargin(0)
        self.hlButtonsUp.setObjectName(_fromUtf8("hlButtonsUp"))
        self.bImage = QtGui.QPushButton(self.qfButtonsUp)
        self.bImage.setMinimumSize(QtCore.QSize(0, 0))
        self.bImage.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bImage.setObjectName(_fromUtf8("bImage"))
        self.hlButtonsUp.addWidget(self.bImage)
        self.bSequence = QtGui.QPushButton(self.qfButtonsUp)
        self.bSequence.setMinimumSize(QtCore.QSize(0, 0))
        self.bSequence.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bSequence.setObjectName(_fromUtf8("bSequence"))
        self.hlButtonsUp.addWidget(self.bSequence)
        self.bMovie = QtGui.QPushButton(self.qfButtonsUp)
        self.bMovie.setMinimumSize(QtCore.QSize(0, 0))
        self.bMovie.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bMovie.setObjectName(_fromUtf8("bMovie"))
        self.hlButtonsUp.addWidget(self.bMovie)
        self.gridLayout.addWidget(self.qfButtonsUp, 0, 0, 1, 1)
        self.bPreview = QtGui.QPushButton(preview)
        self.bPreview.setMinimumSize(QtCore.QSize(200, 200))
        self.bPreview.setMaximumSize(QtCore.QSize(200, 200))
        self.bPreview.setText(_fromUtf8(""))
        self.bPreview.setIconSize(QtCore.QSize(100, 100))
        self.bPreview.setCheckable(True)
        self.bPreview.setFlat(False)
        self.bPreview.setObjectName(_fromUtf8("bPreview"))
        self.gridLayout.addWidget(self.bPreview, 1, 0, 1, 1)
        self.qfButtonsDn = QtGui.QFrame(preview)
        self.qfButtonsDn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.qfButtonsDn.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfButtonsDn.setObjectName(_fromUtf8("qfButtonsDn"))
        self.hlButtonsDn = QtGui.QHBoxLayout(self.qfButtonsDn)
        self.hlButtonsDn.setSpacing(0)
        self.hlButtonsDn.setMargin(0)
        self.hlButtonsDn.setObjectName(_fromUtf8("hlButtonsDn"))
        self.bExplorer = QtGui.QPushButton(self.qfButtonsDn)
        self.bExplorer.setMinimumSize(QtCore.QSize(0, 0))
        self.bExplorer.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bExplorer.setObjectName(_fromUtf8("bExplorer"))
        self.hlButtonsDn.addWidget(self.bExplorer)
        self.bXterm = QtGui.QPushButton(self.qfButtonsDn)
        self.bXterm.setMinimumSize(QtCore.QSize(0, 0))
        self.bXterm.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bXterm.setObjectName(_fromUtf8("bXterm"))
        self.hlButtonsDn.addWidget(self.bXterm)
        self.bGrapher = QtGui.QPushButton(self.qfButtonsDn)
        self.bGrapher.setMinimumSize(QtCore.QSize(0, 0))
        self.bGrapher.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bGrapher.setObjectName(_fromUtf8("bGrapher"))
        self.hlButtonsDn.addWidget(self.bGrapher)
        self.gridLayout.addWidget(self.qfButtonsDn, 2, 0, 1, 1)

        self.retranslateUi(preview)
        QtCore.QMetaObject.connectSlotsByName(preview)

    def retranslateUi(self, preview):
        preview.setWindowTitle(_translate("preview", "Preview", None))
        self.bImage.setText(_translate("preview", "Image", None))
        self.bSequence.setText(_translate("preview", "Sequence", None))
        self.bMovie.setText(_translate("preview", "Movie", None))
        self.bExplorer.setText(_translate("preview", "Explorer", None))
        self.bXterm.setText(_translate("preview", "Xterm", None))
        self.bGrapher.setText(_translate("preview", "Grapher", None))

