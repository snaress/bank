# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\lib\qt\ui\promptDialog.ui'
#
# Created: Thu Sep 18 04:07:21 2014
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(260, 184)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 3)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 3)
        self.twPrompt = QtGui.QTreeWidget(Dialog)
        self.twPrompt.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.twPrompt.setIndentation(0)
        self.twPrompt.setItemsExpandable(False)
        self.twPrompt.setExpandsOnDoubleClick(False)
        self.twPrompt.setColumnCount(1)
        self.twPrompt.setObjectName(_fromUtf8("twPrompt"))
        self.twPrompt.headerItem().setText(0, _fromUtf8("1"))
        self.twPrompt.header().setVisible(False)
        self.gridLayout.addWidget(self.twPrompt, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(99, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.bAccept = QtGui.QPushButton(Dialog)
        self.bAccept.setObjectName(_fromUtf8("bAccept"))
        self.gridLayout.addWidget(self.bAccept, 4, 1, 1, 1)
        self.bCancel = QtGui.QPushButton(Dialog)
        self.bCancel.setObjectName(_fromUtf8("bCancel"))
        self.gridLayout.addWidget(self.bCancel, 4, 2, 1, 1)
        self.lMessage = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lMessage.setFont(font)
        self.lMessage.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lMessage.setObjectName(_fromUtf8("lMessage"))
        self.gridLayout.addWidget(self.lMessage, 1, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.bAccept.setText(_translate("Dialog", "Accept", None))
        self.bCancel.setText(_translate("Dialog", "Cancel", None))
        self.lMessage.setText(_translate("Dialog", "Message", None))

