# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\lib\qt\ui\textEditor.ui'
#
# Created: Wed Sep 17 22:45:29 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(398, 216)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.teText = QtGui.QTextEdit(self.centralwidget)
        self.teText.setTabStopWidth(10)
        self.teText.setObjectName(_fromUtf8("teText"))
        self.gridLayout.addWidget(self.teText, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBarUp = QtGui.QToolBar(MainWindow)
        self.toolBarUp.setObjectName(_fromUtf8("toolBarUp"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarUp)
        self.toolBarDn = QtGui.QToolBar(MainWindow)
        self.toolBarDn.setObjectName(_fromUtf8("toolBarDn"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarDn)
        MainWindow.insertToolBarBreak(self.toolBarDn)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.toolBarUp.setWindowTitle(_translate("MainWindow", "toolBarUp", None))
        self.toolBarDn.setWindowTitle(_translate("MainWindow", "toolBarDn", None))

