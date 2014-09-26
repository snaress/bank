# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtMainTree.ui'
#
# Created: Sat Sep 27 00:12:48 2014
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

class Ui_mainTree(object):
    def setupUi(self, mainTree):
        mainTree.setObjectName(_fromUtf8("mainTree"))
        mainTree.resize(400, 582)
        self.glMainTree = QtGui.QGridLayout(mainTree)
        self.glMainTree.setMargin(1)
        self.glMainTree.setSpacing(1)
        self.glMainTree.setObjectName(_fromUtf8("glMainTree"))
        self.qfTreeSwitch = QtGui.QFrame(mainTree)
        self.qfTreeSwitch.setMinimumSize(QtCore.QSize(0, 25))
        self.qfTreeSwitch.setMaximumSize(QtCore.QSize(16777215, 20))
        self.qfTreeSwitch.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTreeSwitch.setObjectName(_fromUtf8("qfTreeSwitch"))
        self.hlTreeSwitch = QtGui.QHBoxLayout(self.qfTreeSwitch)
        self.hlTreeSwitch.setSpacing(0)
        self.hlTreeSwitch.setMargin(0)
        self.hlTreeSwitch.setObjectName(_fromUtf8("hlTreeSwitch"))
        self.glMainTree.addWidget(self.qfTreeSwitch, 0, 0, 1, 1)
        self.qfTree = QtGui.QFrame(mainTree)
        self.qfTree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTree.setObjectName(_fromUtf8("qfTree"))
        self.vlTree = QtGui.QVBoxLayout(self.qfTree)
        self.vlTree.setSpacing(0)
        self.vlTree.setMargin(0)
        self.vlTree.setObjectName(_fromUtf8("vlTree"))
        self.glMainTree.addWidget(self.qfTree, 1, 0, 1, 1)

        self.retranslateUi(mainTree)
        QtCore.QMetaObject.connectSlotsByName(mainTree)

    def retranslateUi(self, mainTree):
        mainTree.setWindowTitle(_translate("mainTree", "MainTree", None))

