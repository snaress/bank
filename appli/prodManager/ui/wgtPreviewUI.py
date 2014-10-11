# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtPreview.ui'
#
# Created: Fri Oct 10 15:01:35 2014
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
        preview.resize(279, 201)
        self.gridLayout = QtGui.QGridLayout(preview)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.bImage = QtGui.QPushButton(preview)
        self.bImage.setMinimumSize(QtCore.QSize(0, 0))
        self.bImage.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bImage.setObjectName(_fromUtf8("bImage"))
        self.gridLayout.addWidget(self.bImage, 0, 0, 1, 1)
        self.bSequence = QtGui.QPushButton(preview)
        self.bSequence.setMinimumSize(QtCore.QSize(0, 0))
        self.bSequence.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bSequence.setObjectName(_fromUtf8("bSequence"))
        self.gridLayout.addWidget(self.bSequence, 0, 1, 1, 1)
        self.bMovie = QtGui.QPushButton(preview)
        self.bMovie.setMinimumSize(QtCore.QSize(0, 0))
        self.bMovie.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bMovie.setObjectName(_fromUtf8("bMovie"))
        self.gridLayout.addWidget(self.bMovie, 0, 2, 1, 1)
        self.lPreview = QtGui.QLabel(preview)
        self.lPreview.setMinimumSize(QtCore.QSize(0, 0))
        self.lPreview.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lPreview.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lPreview.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lPreview.setFrameShadow(QtGui.QFrame.Plain)
        self.lPreview.setLineWidth(1)
        self.lPreview.setMidLineWidth(0)
        self.lPreview.setScaledContents(False)
        self.lPreview.setAlignment(QtCore.Qt.AlignCenter)
        self.lPreview.setWordWrap(False)
        self.lPreview.setMargin(0)
        self.lPreview.setIndent(-1)
        self.lPreview.setObjectName(_fromUtf8("lPreview"))
        self.gridLayout.addWidget(self.lPreview, 1, 0, 1, 3)
        self.bExplorer = QtGui.QPushButton(preview)
        self.bExplorer.setMinimumSize(QtCore.QSize(0, 0))
        self.bExplorer.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bExplorer.setObjectName(_fromUtf8("bExplorer"))
        self.gridLayout.addWidget(self.bExplorer, 2, 0, 1, 1)
        self.bXterm = QtGui.QPushButton(preview)
        self.bXterm.setMinimumSize(QtCore.QSize(0, 0))
        self.bXterm.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bXterm.setObjectName(_fromUtf8("bXterm"))
        self.gridLayout.addWidget(self.bXterm, 2, 1, 1, 1)
        self.bGrapher = QtGui.QPushButton(preview)
        self.bGrapher.setMinimumSize(QtCore.QSize(0, 0))
        self.bGrapher.setMaximumSize(QtCore.QSize(1000, 1000))
        self.bGrapher.setObjectName(_fromUtf8("bGrapher"))
        self.gridLayout.addWidget(self.bGrapher, 2, 2, 1, 1)

        self.retranslateUi(preview)
        QtCore.QMetaObject.connectSlotsByName(preview)

    def retranslateUi(self, preview):
        preview.setWindowTitle(_translate("preview", "Preview", None))
        self.bImage.setText(_translate("preview", "Image", None))
        self.bSequence.setText(_translate("preview", "Sequence", None))
        self.bMovie.setText(_translate("preview", "Movie", None))
        self.lPreview.setText(_translate("preview", "Preview", None))
        self.bExplorer.setText(_translate("preview", "Explorer", None))
        self.bXterm.setText(_translate("preview", "Xterm", None))
        self.bGrapher.setText(_translate("preview", "Grapher", None))

