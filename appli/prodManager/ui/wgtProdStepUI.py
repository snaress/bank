# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtProdStep.ui'
#
# Created: Sun Sep 21 03:04:41 2014
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

class Ui_stepTree(object):
    def setupUi(self, stepTree):
        stepTree.setObjectName(_fromUtf8("stepTree"))
        stepTree.resize(244, 94)
        self.gridLayout = QtGui.QGridLayout(stepTree)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.qfSteps = QtGui.QFrame(stepTree)
        self.qfSteps.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfSteps.setObjectName(_fromUtf8("qfSteps"))
        self.vlTaskBtns = QtGui.QVBoxLayout(self.qfSteps)
        self.vlTaskBtns.setSpacing(0)
        self.vlTaskBtns.setMargin(0)
        self.vlTaskBtns.setObjectName(_fromUtf8("vlTaskBtns"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTaskBtns.addItem(spacerItem)
        self.bAddStep = QtGui.QPushButton(self.qfSteps)
        self.bAddStep.setMinimumSize(QtCore.QSize(0, 0))
        self.bAddStep.setMaximumSize(QtCore.QSize(70, 22))
        self.bAddStep.setObjectName(_fromUtf8("bAddStep"))
        self.vlTaskBtns.addWidget(self.bAddStep)
        self.bDelStep = QtGui.QPushButton(self.qfSteps)
        self.bDelStep.setMinimumSize(QtCore.QSize(0, 0))
        self.bDelStep.setMaximumSize(QtCore.QSize(70, 22))
        self.bDelStep.setObjectName(_fromUtf8("bDelStep"))
        self.vlTaskBtns.addWidget(self.bDelStep)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTaskBtns.addItem(spacerItem1)
        self.bStepUp = QtGui.QPushButton(self.qfSteps)
        self.bStepUp.setMinimumSize(QtCore.QSize(0, 0))
        self.bStepUp.setMaximumSize(QtCore.QSize(70, 22))
        self.bStepUp.setObjectName(_fromUtf8("bStepUp"))
        self.vlTaskBtns.addWidget(self.bStepUp)
        self.bStepDn = QtGui.QPushButton(self.qfSteps)
        self.bStepDn.setMinimumSize(QtCore.QSize(0, 0))
        self.bStepDn.setMaximumSize(QtCore.QSize(70, 22))
        self.bStepDn.setObjectName(_fromUtf8("bStepDn"))
        self.vlTaskBtns.addWidget(self.bStepDn)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTaskBtns.addItem(spacerItem2)
        self.gridLayout.addWidget(self.qfSteps, 0, 0, 1, 1)
        self.twSteps = QtGui.QTreeWidget(stepTree)
        self.twSteps.setMinimumSize(QtCore.QSize(0, 0))
        self.twSteps.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.twSteps.setAlternatingRowColors(True)
        self.twSteps.setIndentation(2)
        self.twSteps.setObjectName(_fromUtf8("twSteps"))
        self.twSteps.headerItem().setText(0, _fromUtf8("Steps"))
        self.twSteps.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.twSteps.header().setVisible(True)
        self.gridLayout.addWidget(self.twSteps, 0, 1, 1, 1)

        self.retranslateUi(stepTree)
        QtCore.QMetaObject.connectSlotsByName(stepTree)

    def retranslateUi(self, stepTree):
        stepTree.setWindowTitle(_translate("stepTree", "Steps", None))
        self.bAddStep.setText(_translate("stepTree", "Add Step", None))
        self.bDelStep.setText(_translate("stepTree", "Del Step", None))
        self.bStepUp.setText(_translate("stepTree", "Up", None))
        self.bStepDn.setText(_translate("stepTree", "Down", None))

