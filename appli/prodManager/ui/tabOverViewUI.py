# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\tabOverView.ui'
#
# Created: Mon Oct 13 03:19:07 2014
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

class Ui_overViewTab(object):
    def setupUi(self, overViewTab):
        overViewTab.setObjectName(_fromUtf8("overViewTab"))
        overViewTab.resize(675, 497)
        self.gridLayout = QtGui.QGridLayout(overViewTab)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.twTree = QtGui.QTreeWidget(overViewTab)
        self.twTree.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.twTree.setObjectName(_fromUtf8("twTree"))
        self.twTree.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout.addWidget(self.twTree, 0, 0, 1, 1)

        self.retranslateUi(overViewTab)
        QtCore.QMetaObject.connectSlotsByName(overViewTab)

    def retranslateUi(self, overViewTab):
        overViewTab.setWindowTitle(_translate("overViewTab", "Tab OverView", None))

