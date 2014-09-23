# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtProdTree.ui'
#
# Created: Sun Sep 21 15:12:51 2014
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

class Ui_prodTree(object):
    def setupUi(self, prodTree):
        prodTree.setObjectName(_fromUtf8("prodTree"))
        prodTree.resize(267, 88)
        self.gridLayout = QtGui.QGridLayout(prodTree)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.qfBtns = QtGui.QFrame(prodTree)
        self.qfBtns.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfBtns.setObjectName(_fromUtf8("qfBtns"))
        self.vlTreeBtns = QtGui.QVBoxLayout(self.qfBtns)
        self.vlTreeBtns.setSpacing(0)
        self.vlTreeBtns.setMargin(0)
        self.vlTreeBtns.setObjectName(_fromUtf8("vlTreeBtns"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTreeBtns.addItem(spacerItem)
        self.bAddItem = QtGui.QPushButton(self.qfBtns)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bAddItem.sizePolicy().hasHeightForWidth())
        self.bAddItem.setSizePolicy(sizePolicy)
        self.bAddItem.setMinimumSize(QtCore.QSize(0, 0))
        self.bAddItem.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bAddItem.setObjectName(_fromUtf8("bAddItem"))
        self.vlTreeBtns.addWidget(self.bAddItem)
        self.bDelItem = QtGui.QPushButton(self.qfBtns)
        self.bDelItem.setEnabled(True)
        self.bDelItem.setObjectName(_fromUtf8("bDelItem"))
        self.vlTreeBtns.addWidget(self.bDelItem)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTreeBtns.addItem(spacerItem1)
        self.bItemUp = QtGui.QPushButton(self.qfBtns)
        self.bItemUp.setMinimumSize(QtCore.QSize(50, 20))
        self.bItemUp.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bItemUp.setObjectName(_fromUtf8("bItemUp"))
        self.vlTreeBtns.addWidget(self.bItemUp)
        self.bItemDn = QtGui.QPushButton(self.qfBtns)
        self.bItemDn.setMinimumSize(QtCore.QSize(50, 20))
        self.bItemDn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bItemDn.setObjectName(_fromUtf8("bItemDn"))
        self.vlTreeBtns.addWidget(self.bItemDn)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTreeBtns.addItem(spacerItem2)
        self.gridLayout.addWidget(self.qfBtns, 0, 0, 1, 1)
        self.twTree = QtGui.QTreeWidget(prodTree)
        self.twTree.setMinimumSize(QtCore.QSize(0, 0))
        self.twTree.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.twTree.setAlternatingRowColors(False)
        self.twTree.setIndentation(2)
        self.twTree.setObjectName(_fromUtf8("twTree"))
        self.twTree.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.twTree.headerItem().setTextAlignment(1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.twTree.headerItem().setTextAlignment(2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.twTree.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.twTree, 0, 1, 1, 1)

        self.retranslateUi(prodTree)
        QtCore.QMetaObject.connectSlotsByName(prodTree)

    def retranslateUi(self, prodTree):
        prodTree.setWindowTitle(_translate("prodTree", "ProdTree", None))
        self.bAddItem.setText(_translate("prodTree", "Add Item", None))
        self.bDelItem.setText(_translate("prodTree", "Del Item", None))
        self.bItemUp.setText(_translate("prodTree", "Up", None))
        self.bItemDn.setText(_translate("prodTree", "Down", None))
        self.twTree.headerItem().setText(0, _translate("prodTree", "Header1", None))
        self.twTree.headerItem().setText(1, _translate("prodTree", "Header2", None))
        self.twTree.headerItem().setText(2, _translate("prodTree", "Header3", None))

