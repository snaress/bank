# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\tools\maya\util\toolManager\ui\toolManager.ui'
#
# Created: Wed Oct 22 16:21:31 2014
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

class Ui_toolManager(object):
    def setupUi(self, toolManager):
        toolManager.setObjectName(_fromUtf8("toolManager"))
        toolManager.resize(294, 600)
        self.centralwidget = QtGui.QWidget(toolManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.twTree = QtGui.QTreeWidget(self.centralwidget)
        self.twTree.setObjectName(_fromUtf8("twTree"))
        self.twTree.headerItem().setText(0, _fromUtf8("1"))
        self.twTree.header().setVisible(False)
        self.gridLayout.addWidget(self.twTree, 0, 0, 1, 1)
        toolManager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(toolManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 294, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        toolManager.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(toolManager)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        toolManager.setStatusBar(self.statusbar)

        self.retranslateUi(toolManager)
        QtCore.QMetaObject.connectSlotsByName(toolManager)

    def retranslateUi(self, toolManager):
        toolManager.setWindowTitle(_translate("toolManager", "ToolManager", None))

