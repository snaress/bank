# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtLtCmtNode.ui'
#
# Created: Thu Oct 09 12:59:06 2014
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

class Ui_ltComment(object):
    def setupUi(self, ltComment):
        ltComment.setObjectName(_fromUtf8("ltComment"))
        ltComment.resize(816, 100)
        self.gridLayout = QtGui.QGridLayout(ltComment)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line_3 = QtGui.QFrame(ltComment)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 1)
        self.lTime = QtGui.QLabel(ltComment)
        self.lTime.setObjectName(_fromUtf8("lTime"))
        self.gridLayout.addWidget(self.lTime, 1, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(241, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 8, 1, 1)
        self.dtDate = QtGui.QDateTimeEdit(ltComment)
        self.dtDate.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dtDate.setObjectName(_fromUtf8("dtDate"))
        self.gridLayout.addWidget(self.dtDate, 1, 5, 1, 1)
        self.dtTime = QtGui.QDateTimeEdit(ltComment)
        self.dtTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dtTime.setObjectName(_fromUtf8("dtTime"))
        self.gridLayout.addWidget(self.dtTime, 1, 7, 1, 1)
        self.lUser = QtGui.QLabel(ltComment)
        self.lUser.setObjectName(_fromUtf8("lUser"))
        self.gridLayout.addWidget(self.lUser, 1, 1, 1, 1)
        self.lUserName = QtGui.QLabel(ltComment)
        self.lUserName.setObjectName(_fromUtf8("lUserName"))
        self.gridLayout.addWidget(self.lUserName, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.line = QtGui.QFrame(ltComment)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 12)
        self.line_2 = QtGui.QFrame(ltComment)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 12)
        self.lDate = QtGui.QLabel(ltComment)
        self.lDate.setObjectName(_fromUtf8("lDate"))
        self.gridLayout.addWidget(self.lDate, 1, 4, 1, 1)
        self.teComment = QtGui.QTextEdit(ltComment)
        self.teComment.setMaximumSize(QtCore.QSize(16777215, 80))
        self.teComment.setReadOnly(True)
        self.teComment.setObjectName(_fromUtf8("teComment"))
        self.gridLayout.addWidget(self.teComment, 3, 0, 1, 12)
        self.bDelCmt = QtGui.QPushButton(ltComment)
        self.bDelCmt.setMinimumSize(QtCore.QSize(0, 0))
        self.bDelCmt.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.bDelCmt.setFont(font)
        self.bDelCmt.setObjectName(_fromUtf8("bDelCmt"))
        self.gridLayout.addWidget(self.bDelCmt, 1, 10, 1, 1)
        self.bEdit = QtGui.QPushButton(ltComment)
        self.bEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.bEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.bEdit.setFont(font)
        self.bEdit.setCheckable(False)
        self.bEdit.setObjectName(_fromUtf8("bEdit"))
        self.gridLayout.addWidget(self.bEdit, 1, 9, 1, 1)

        self.retranslateUi(ltComment)
        QtCore.QMetaObject.connectSlotsByName(ltComment)

    def retranslateUi(self, ltComment):
        ltComment.setWindowTitle(_translate("ltComment", "Comment", None))
        self.lTime.setText(_translate("ltComment", "Time:", None))
        self.dtDate.setDisplayFormat(_translate("ltComment", "yyyy/MM/dd", None))
        self.dtTime.setDisplayFormat(_translate("ltComment", "HH:mm:ss", None))
        self.lUser.setText(_translate("ltComment", "User:", None))
        self.lUserName.setText(_translate("ltComment", "UserName", None))
        self.lDate.setText(_translate("ltComment", "Date:", None))
        self.bDelCmt.setText(_translate("ltComment", "DelCmt", None))
        self.bEdit.setText(_translate("ltComment", "Edit", None))

