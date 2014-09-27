# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtMainTree.ui'
#
# Created: Sat Sep 27 03:41:42 2014
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
        mainTree.resize(400, 483)
        self.gridLayout = QtGui.QGridLayout(mainTree)
        self.gridLayout.setMargin(1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.qfTreeMode = QtGui.QFrame(mainTree)
        self.qfTreeMode.setMinimumSize(QtCore.QSize(0, 25))
        self.qfTreeMode.setMaximumSize(QtCore.QSize(16777215, 20))
        self.qfTreeMode.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTreeMode.setObjectName(_fromUtf8("qfTreeMode"))
        self.hlTreeSwitch_2 = QtGui.QHBoxLayout(self.qfTreeMode)
        self.hlTreeSwitch_2.setSpacing(6)
        self.hlTreeSwitch_2.setContentsMargins(2, 0, 0, 0)
        self.hlTreeSwitch_2.setObjectName(_fromUtf8("hlTreeSwitch_2"))
        self.label = QtGui.QLabel(self.qfTreeMode)
        self.label.setObjectName(_fromUtf8("label"))
        self.hlTreeSwitch_2.addWidget(self.label)
        self.rbTreeMode = QtGui.QRadioButton(self.qfTreeMode)
        self.rbTreeMode.setChecked(True)
        self.rbTreeMode.setObjectName(_fromUtf8("rbTreeMode"))
        self.rbgTreeMode = QtGui.QButtonGroup(mainTree)
        self.rbgTreeMode.setObjectName(_fromUtf8("rbgTreeMode"))
        self.rbgTreeMode.addButton(self.rbTreeMode)
        self.hlTreeSwitch_2.addWidget(self.rbTreeMode)
        self.rbStepMode = QtGui.QRadioButton(self.qfTreeMode)
        self.rbStepMode.setObjectName(_fromUtf8("rbStepMode"))
        self.rbgTreeMode.addButton(self.rbStepMode)
        self.hlTreeSwitch_2.addWidget(self.rbStepMode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlTreeSwitch_2.addItem(spacerItem)
        self.gridLayout.addWidget(self.qfTreeMode, 0, 0, 1, 1)
        self.qfTreeSwitch = QtGui.QFrame(mainTree)
        self.qfTreeSwitch.setMinimumSize(QtCore.QSize(0, 25))
        self.qfTreeSwitch.setMaximumSize(QtCore.QSize(16777215, 20))
        self.qfTreeSwitch.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTreeSwitch.setObjectName(_fromUtf8("qfTreeSwitch"))
        self.hlTreeSwitch = QtGui.QHBoxLayout(self.qfTreeSwitch)
        self.hlTreeSwitch.setSpacing(6)
        self.hlTreeSwitch.setContentsMargins(2, 0, 0, 0)
        self.hlTreeSwitch.setObjectName(_fromUtf8("hlTreeSwitch"))
        self.gridLayout.addWidget(self.qfTreeSwitch, 1, 0, 1, 1)
        self.qfTree = QtGui.QFrame(mainTree)
        self.qfTree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTree.setObjectName(_fromUtf8("qfTree"))
        self.vlTree = QtGui.QVBoxLayout(self.qfTree)
        self.vlTree.setSpacing(0)
        self.vlTree.setMargin(0)
        self.vlTree.setObjectName(_fromUtf8("vlTree"))
        self.gridLayout.addWidget(self.qfTree, 2, 0, 1, 1)

        self.retranslateUi(mainTree)
        QtCore.QMetaObject.connectSlotsByName(mainTree)

    def retranslateUi(self, mainTree):
        mainTree.setWindowTitle(_translate("mainTree", "MainTree", None))
        self.label.setText(_translate("mainTree", "Tree Mode: ", None))
        self.rbTreeMode.setText(_translate("mainTree", "Tree", None))
        self.rbStepMode.setText(_translate("mainTree", "Step", None))

