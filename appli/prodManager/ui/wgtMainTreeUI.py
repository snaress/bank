# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtMainTree.ui'
#
# Created: Mon Sep 29 02:42:00 2014
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
        self.hlTreeMode = QtGui.QHBoxLayout(self.qfTreeMode)
        self.hlTreeMode.setSpacing(12)
        self.hlTreeMode.setContentsMargins(2, 0, 0, 0)
        self.hlTreeMode.setObjectName(_fromUtf8("hlTreeMode"))
        self.lTreeMode = QtGui.QLabel(self.qfTreeMode)
        self.lTreeMode.setObjectName(_fromUtf8("lTreeMode"))
        self.hlTreeMode.addWidget(self.lTreeMode)
        self.rbTreeMode = QtGui.QRadioButton(self.qfTreeMode)
        self.rbTreeMode.setChecked(True)
        self.rbTreeMode.setObjectName(_fromUtf8("rbTreeMode"))
        self.rbgTreeMode = QtGui.QButtonGroup(mainTree)
        self.rbgTreeMode.setObjectName(_fromUtf8("rbgTreeMode"))
        self.rbgTreeMode.addButton(self.rbTreeMode)
        self.hlTreeMode.addWidget(self.rbTreeMode)
        self.rbStepMode = QtGui.QRadioButton(self.qfTreeMode)
        self.rbStepMode.setObjectName(_fromUtf8("rbStepMode"))
        self.rbgTreeMode.addButton(self.rbStepMode)
        self.hlTreeMode.addWidget(self.rbStepMode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlTreeMode.addItem(spacerItem)
        self.gridLayout.addWidget(self.qfTreeMode, 0, 0, 1, 1)
        self.qfTreeSwitch = QtGui.QFrame(mainTree)
        self.qfTreeSwitch.setMinimumSize(QtCore.QSize(0, 25))
        self.qfTreeSwitch.setMaximumSize(QtCore.QSize(16777215, 20))
        self.qfTreeSwitch.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTreeSwitch.setObjectName(_fromUtf8("qfTreeSwitch"))
        self.hlTreeSwitch = QtGui.QHBoxLayout(self.qfTreeSwitch)
        self.hlTreeSwitch.setSpacing(12)
        self.hlTreeSwitch.setContentsMargins(2, 0, 0, 0)
        self.hlTreeSwitch.setObjectName(_fromUtf8("hlTreeSwitch"))
        self.lTreeType = QtGui.QLabel(self.qfTreeSwitch)
        self.lTreeType.setObjectName(_fromUtf8("lTreeType"))
        self.hlTreeSwitch.addWidget(self.lTreeType)
        self.rbAsset = QtGui.QRadioButton(self.qfTreeSwitch)
        self.rbAsset.setChecked(True)
        self.rbAsset.setObjectName(_fromUtf8("rbAsset"))
        self.rbgTreeType = QtGui.QButtonGroup(mainTree)
        self.rbgTreeType.setObjectName(_fromUtf8("rbgTreeType"))
        self.rbgTreeType.addButton(self.rbAsset)
        self.hlTreeSwitch.addWidget(self.rbAsset)
        self.rbShot = QtGui.QRadioButton(self.qfTreeSwitch)
        self.rbShot.setObjectName(_fromUtf8("rbShot"))
        self.rbgTreeType.addButton(self.rbShot)
        self.hlTreeSwitch.addWidget(self.rbShot)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlTreeSwitch.addItem(spacerItem1)
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
        self.lTreeMode.setText(_translate("mainTree", "Tree Mode: ", None))
        self.rbTreeMode.setText(_translate("mainTree", "Tree", None))
        self.rbStepMode.setText(_translate("mainTree", "Step", None))
        self.lTreeType.setText(_translate("mainTree", "Tree Type: ", None))
        self.rbAsset.setText(_translate("mainTree", "Asset", None))
        self.rbShot.setText(_translate("mainTree", "Shot", None))

