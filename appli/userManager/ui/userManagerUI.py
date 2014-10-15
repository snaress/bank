# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\userManager\ui\userManager.ui'
#
# Created: Tue Oct 14 02:27:03 2014
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

class Ui_userManager(object):
    def setupUi(self, userManager):
        userManager.setObjectName(_fromUtf8("userManager"))
        userManager.resize(536, 133)
        self.centralwidget = QtGui.QWidget(userManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.glUserManager = QtGui.QGridLayout(self.centralwidget)
        self.glUserManager.setMargin(0)
        self.glUserManager.setSpacing(0)
        self.glUserManager.setObjectName(_fromUtf8("glUserManager"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.glUserManager.addWidget(self.line, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bNewUser = QtGui.QPushButton(self.centralwidget)
        self.bNewUser.setObjectName(_fromUtf8("bNewUser"))
        self.horizontalLayout.addWidget(self.bNewUser)
        self.bEditUser = QtGui.QPushButton(self.centralwidget)
        self.bEditUser.setObjectName(_fromUtf8("bEditUser"))
        self.horizontalLayout.addWidget(self.bEditUser)
        self.bDelUser = QtGui.QPushButton(self.centralwidget)
        self.bDelUser.setObjectName(_fromUtf8("bDelUser"))
        self.horizontalLayout.addWidget(self.bDelUser)
        self.glUserManager.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        userManager.setCentralWidget(self.centralwidget)

        self.retranslateUi(userManager)
        QtCore.QMetaObject.connectSlotsByName(userManager)

    def retranslateUi(self, userManager):
        userManager.setWindowTitle(_translate("userManager", "UserManager", None))
        self.bNewUser.setText(_translate("userManager", "New User", None))
        self.bEditUser.setText(_translate("userManager", "Edit User", None))
        self.bDelUser.setText(_translate("userManager", "Del User", None))

