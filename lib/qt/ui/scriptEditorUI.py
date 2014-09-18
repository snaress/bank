# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\lib\qt\ui\scriptEditor.ui'
#
# Created: Thu Sep 18 04:31:02 2014
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
        self.glScriptEditor = QtGui.QGridLayout(self.centralwidget)
        self.glScriptEditor.setMargin(0)
        self.glScriptEditor.setSpacing(0)
        self.glScriptEditor.setObjectName(_fromUtf8("glScriptEditor"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.tbEdit = QtGui.QToolBar(MainWindow)
        self.tbEdit.setObjectName(_fromUtf8("tbEdit"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tbEdit)
        self.miAddTab = QtGui.QAction(MainWindow)
        self.miAddTab.setObjectName(_fromUtf8("miAddTab"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Script Editor", None))
        self.tbEdit.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.miAddTab.setText(_translate("MainWindow", "Add Tabulation", None))

