# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtLtNode.ui'
#
# Created: Sat Oct 11 00:38:28 2014
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

class Ui_ltNode(object):
    def setupUi(self, ltNode):
        ltNode.setObjectName(_fromUtf8("ltNode"))
        ltNode.resize(790, 97)
        self.gridLayout = QtGui.QGridLayout(ltNode)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(ltNode)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 12)
        self.leTitle = QtGui.QLineEdit(ltNode)
        self.leTitle.setMinimumSize(QtCore.QSize(200, 0))
        self.leTitle.setObjectName(_fromUtf8("leTitle"))
        self.gridLayout.addWidget(self.leTitle, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.lUser = QtGui.QLabel(ltNode)
        self.lUser.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lUser.setAutoFillBackground(False)
        self.lUser.setFrameShape(QtGui.QFrame.NoFrame)
        self.lUser.setFrameShadow(QtGui.QFrame.Plain)
        self.lUser.setObjectName(_fromUtf8("lUser"))
        self.gridLayout.addWidget(self.lUser, 1, 2, 1, 1)
        self.lUserName = QtGui.QLabel(ltNode)
        self.lUserName.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lUserName.setObjectName(_fromUtf8("lUserName"))
        self.gridLayout.addWidget(self.lUserName, 1, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.lDate = QtGui.QLabel(ltNode)
        self.lDate.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lDate.setObjectName(_fromUtf8("lDate"))
        self.gridLayout.addWidget(self.lDate, 1, 5, 1, 1)
        self.dtDate = QtGui.QDateTimeEdit(ltNode)
        self.dtDate.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dtDate.setObjectName(_fromUtf8("dtDate"))
        self.gridLayout.addWidget(self.dtDate, 1, 6, 1, 1)
        self.lTime = QtGui.QLabel(ltNode)
        self.lTime.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lTime.setObjectName(_fromUtf8("lTime"))
        self.gridLayout.addWidget(self.lTime, 1, 7, 1, 1)
        self.dtTime = QtGui.QDateTimeEdit(ltNode)
        self.dtTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dtTime.setObjectName(_fromUtf8("dtTime"))
        self.gridLayout.addWidget(self.dtTime, 1, 8, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(66, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 9, 1, 1)
        self.bEdit = QtGui.QPushButton(ltNode)
        self.bEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.bEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.bEdit.setFont(font)
        self.bEdit.setCheckable(False)
        self.bEdit.setObjectName(_fromUtf8("bEdit"))
        self.gridLayout.addWidget(self.bEdit, 1, 10, 1, 1)
        self.bEdition = QtGui.QPushButton(ltNode)
        self.bEdition.setMinimumSize(QtCore.QSize(0, 0))
        self.bEdition.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.bEdition.setFont(font)
        self.bEdition.setObjectName(_fromUtf8("bEdition"))
        self.gridLayout.addWidget(self.bEdition, 1, 11, 1, 1)
        self.line_2 = QtGui.QFrame(ltNode)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 12)
        self.teComment = QtGui.QTextEdit(ltNode)
        self.teComment.setMaximumSize(QtCore.QSize(16777215, 80))
        self.teComment.setReadOnly(True)
        self.teComment.setObjectName(_fromUtf8("teComment"))
        self.gridLayout.addWidget(self.teComment, 3, 0, 1, 12)

        self.retranslateUi(ltNode)
        QtCore.QMetaObject.connectSlotsByName(ltNode)

    def retranslateUi(self, ltNode):
        ltNode.setWindowTitle(_translate("ltNode", "LineTest", None))
        self.leTitle.setText(_translate("ltNode", "Linetest Title", None))
        self.lUser.setText(_translate("ltNode", "User:", None))
        self.lUserName.setText(_translate("ltNode", "UserName", None))
        self.lDate.setText(_translate("ltNode", "Date:", None))
        self.dtDate.setDisplayFormat(_translate("ltNode", "yyyy/MM/dd", None))
        self.lTime.setText(_translate("ltNode", "Time:", None))
        self.dtTime.setDisplayFormat(_translate("ltNode", "HH:mm:ss", None))
        self.bEdit.setText(_translate("ltNode", "Edit", None))
        self.bEdition.setText(_translate("ltNode", "Edition", None))

