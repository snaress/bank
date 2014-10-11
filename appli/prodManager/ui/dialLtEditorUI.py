# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\dialLtEditor.ui'
#
# Created: Fri Oct 10 17:29:27 2014
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

class Ui_editLt(object):
    def setupUi(self, editLt):
        editLt.setObjectName(_fromUtf8("editLt"))
        editLt.resize(372, 91)
        self.gridLayout = QtGui.QGridLayout(editLt)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(2, 0, 2, 0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hlButtons = QtGui.QHBoxLayout()
        self.hlButtons.setSpacing(2)
        self.hlButtons.setObjectName(_fromUtf8("hlButtons"))
        spacerItem = QtGui.QSpacerItem(266, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlButtons.addItem(spacerItem)
        self.bSave = QtGui.QPushButton(editLt)
        self.bSave.setMinimumSize(QtCore.QSize(50, 20))
        self.bSave.setMaximumSize(QtCore.QSize(50, 20))
        self.bSave.setObjectName(_fromUtf8("bSave"))
        self.hlButtons.addWidget(self.bSave)
        self.bCancel = QtGui.QPushButton(editLt)
        self.bCancel.setMinimumSize(QtCore.QSize(50, 20))
        self.bCancel.setMaximumSize(QtCore.QSize(50, 20))
        self.bCancel.setObjectName(_fromUtf8("bCancel"))
        self.hlButtons.addWidget(self.bCancel)
        self.gridLayout.addLayout(self.hlButtons, 2, 0, 1, 1)
        self.glLtPath = QtGui.QGridLayout()
        self.glLtPath.setVerticalSpacing(2)
        self.glLtPath.setObjectName(_fromUtf8("glLtPath"))
        self.lImaPath = QtGui.QLabel(editLt)
        self.lImaPath.setMinimumSize(QtCore.QSize(90, 0))
        self.lImaPath.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lImaPath.setObjectName(_fromUtf8("lImaPath"))
        self.glLtPath.addWidget(self.lImaPath, 0, 0, 1, 1)
        self.leImaPath = QtGui.QLineEdit(editLt)
        self.leImaPath.setMinimumSize(QtCore.QSize(200, 0))
        self.leImaPath.setText(_fromUtf8(""))
        self.leImaPath.setObjectName(_fromUtf8("leImaPath"))
        self.glLtPath.addWidget(self.leImaPath, 0, 1, 1, 1)
        self.bImaOpen = QtGui.QPushButton(editLt)
        self.bImaOpen.setMinimumSize(QtCore.QSize(40, 20))
        self.bImaOpen.setMaximumSize(QtCore.QSize(40, 20))
        self.bImaOpen.setObjectName(_fromUtf8("bImaOpen"))
        self.glLtPath.addWidget(self.bImaOpen, 0, 2, 1, 1)
        self.lSeqPath = QtGui.QLabel(editLt)
        self.lSeqPath.setMinimumSize(QtCore.QSize(90, 0))
        self.lSeqPath.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lSeqPath.setObjectName(_fromUtf8("lSeqPath"))
        self.glLtPath.addWidget(self.lSeqPath, 1, 0, 1, 1)
        self.leSeqPath = QtGui.QLineEdit(editLt)
        self.leSeqPath.setMinimumSize(QtCore.QSize(200, 0))
        self.leSeqPath.setText(_fromUtf8(""))
        self.leSeqPath.setObjectName(_fromUtf8("leSeqPath"))
        self.glLtPath.addWidget(self.leSeqPath, 1, 1, 1, 1)
        self.bSeqOpen = QtGui.QPushButton(editLt)
        self.bSeqOpen.setMinimumSize(QtCore.QSize(40, 20))
        self.bSeqOpen.setMaximumSize(QtCore.QSize(40, 20))
        self.bSeqOpen.setObjectName(_fromUtf8("bSeqOpen"))
        self.glLtPath.addWidget(self.bSeqOpen, 1, 2, 1, 1)
        self.lMovPath = QtGui.QLabel(editLt)
        self.lMovPath.setMinimumSize(QtCore.QSize(90, 0))
        self.lMovPath.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lMovPath.setObjectName(_fromUtf8("lMovPath"))
        self.glLtPath.addWidget(self.lMovPath, 2, 0, 1, 1)
        self.leMovPath = QtGui.QLineEdit(editLt)
        self.leMovPath.setMinimumSize(QtCore.QSize(200, 0))
        self.leMovPath.setText(_fromUtf8(""))
        self.leMovPath.setObjectName(_fromUtf8("leMovPath"))
        self.glLtPath.addWidget(self.leMovPath, 2, 1, 1, 1)
        self.bMovOpen = QtGui.QPushButton(editLt)
        self.bMovOpen.setMinimumSize(QtCore.QSize(40, 20))
        self.bMovOpen.setMaximumSize(QtCore.QSize(40, 20))
        self.bMovOpen.setObjectName(_fromUtf8("bMovOpen"))
        self.glLtPath.addWidget(self.bMovOpen, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.glLtPath, 0, 0, 1, 1)
        self.line = QtGui.QFrame(editLt)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.retranslateUi(editLt)
        QtCore.QMetaObject.connectSlotsByName(editLt)

    def retranslateUi(self, editLt):
        editLt.setWindowTitle(_translate("editLt", "LineTest Editor", None))
        self.bSave.setText(_translate("editLt", "Save", None))
        self.bCancel.setText(_translate("editLt", "Cancel", None))
        self.lImaPath.setText(_translate("editLt", "LT Image Path:", None))
        self.bImaOpen.setText(_translate("editLt", "Open", None))
        self.lSeqPath.setText(_translate("editLt", "LT Sequence Path:", None))
        self.bSeqOpen.setText(_translate("editLt", "Open", None))
        self.lMovPath.setText(_translate("editLt", "LT Movie Path:", None))
        self.bMovOpen.setText(_translate("editLt", "Open", None))

