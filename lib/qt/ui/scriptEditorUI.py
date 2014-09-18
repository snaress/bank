# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\lib\qt\ui\scriptEditor.ui'
#
# Created: Wed Sep 17 23:54:57 2014
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

class Ui_mwScriptEditor(object):
    def setupUi(self, mwScriptEditor):
        mwScriptEditor.setObjectName(_fromUtf8("mwScriptEditor"))
        mwScriptEditor.resize(398, 216)
        self.centralwidget = QtGui.QWidget(mwScriptEditor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.glScriptEditor = QtGui.QGridLayout(self.centralwidget)
        self.glScriptEditor.setMargin(0)
        self.glScriptEditor.setSpacing(0)
        self.glScriptEditor.setObjectName(_fromUtf8("glScriptEditor"))
        mwScriptEditor.setCentralWidget(self.centralwidget)
        self.tbEdit = QtGui.QToolBar(mwScriptEditor)
        self.tbEdit.setObjectName(_fromUtf8("tbEdit"))
        mwScriptEditor.addToolBar(QtCore.Qt.TopToolBarArea, self.tbEdit)
        self.miAddTab = QtGui.QAction(mwScriptEditor)
        self.miAddTab.setObjectName(_fromUtf8("miAddTab"))

        self.retranslateUi(mwScriptEditor)
        QtCore.QMetaObject.connectSlotsByName(mwScriptEditor)

    def retranslateUi(self, mwScriptEditor):
        mwScriptEditor.setWindowTitle(_translate("mwScriptEditor", "Script Editor", None))
        self.tbEdit.setWindowTitle(_translate("mwScriptEditor", "toolBar", None))
        self.miAddTab.setText(_translate("mwScriptEditor", "Add Tabulation", None))

