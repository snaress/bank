# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtLtNode.ui'
#
# Created: Thu Oct 09 12:59:07 2014
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

class Ui_LineTest(object):
    def setupUi(self, LineTest):
        LineTest.setObjectName(_fromUtf8("LineTest"))
        LineTest.resize(814, 26)
        self.gridLayout = QtGui.QGridLayout(LineTest)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dtTime = QtGui.QDateTimeEdit(LineTest)
        self.dtTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dtTime.setObjectName(_fromUtf8("dtTime"))
        self.gridLayout.addWidget(self.dtTime, 1, 8, 1, 1)
        self.line = QtGui.QFrame(LineTest)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 12)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.line_2 = QtGui.QFrame(LineTest)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 12)
        self.dtDate = QtGui.QDateTimeEdit(LineTest)
        self.dtDate.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dtDate.setObjectName(_fromUtf8("dtDate"))
        self.gridLayout.addWidget(self.dtDate, 1, 6, 1, 1)
        self.leTitle = QtGui.QLineEdit(LineTest)
        self.leTitle.setMinimumSize(QtCore.QSize(200, 0))
        self.leTitle.setObjectName(_fromUtf8("leTitle"))
        self.gridLayout.addWidget(self.leTitle, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.lDate = QtGui.QLabel(LineTest)
        self.lDate.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lDate.setObjectName(_fromUtf8("lDate"))
        self.gridLayout.addWidget(self.lDate, 1, 5, 1, 1)
        self.bAddCmt = QtGui.QPushButton(LineTest)
        self.bAddCmt.setMinimumSize(QtCore.QSize(0, 0))
        self.bAddCmt.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.bAddCmt.setFont(font)
        self.bAddCmt.setObjectName(_fromUtf8("bAddCmt"))
        self.gridLayout.addWidget(self.bAddCmt, 1, 10, 1, 1)
        self.lTime = QtGui.QLabel(LineTest)
        self.lTime.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lTime.setObjectName(_fromUtf8("lTime"))
        self.gridLayout.addWidget(self.lTime, 1, 7, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(66, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 9, 1, 1)
        self.lUser = QtGui.QLabel(LineTest)
        self.lUser.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lUser.setAutoFillBackground(False)
        self.lUser.setFrameShape(QtGui.QFrame.NoFrame)
        self.lUser.setFrameShadow(QtGui.QFrame.Plain)
        self.lUser.setObjectName(_fromUtf8("lUser"))
        self.gridLayout.addWidget(self.lUser, 1, 2, 1, 1)
        self.lUserName = QtGui.QLabel(LineTest)
        self.lUserName.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lUserName.setObjectName(_fromUtf8("lUserName"))
        self.gridLayout.addWidget(self.lUserName, 1, 3, 1, 1)

        self.retranslateUi(LineTest)
        QtCore.QMetaObject.connectSlotsByName(LineTest)

    def retranslateUi(self, LineTest):
        LineTest.setWindowTitle(_translate("LineTest", "LineTest", None))
        self.dtTime.setDisplayFormat(_translate("LineTest", "HH:mm:ss", None))
        self.dtDate.setDisplayFormat(_translate("LineTest", "yyyy/MM/dd", None))
        self.leTitle.setText(_translate("LineTest", "Linetest Title", None))
        self.lDate.setText(_translate("LineTest", "Date:", None))
        self.bAddCmt.setText(_translate("LineTest", "AddCmt", None))
        self.lTime.setText(_translate("LineTest", "Time:", None))
        self.lUser.setText(_translate("LineTest", "User:", None))
        self.lUserName.setText(_translate("LineTest", "UserName", None))

