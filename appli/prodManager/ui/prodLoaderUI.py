# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\prodLoader.ui'
#
# Created: Fri Sep 19 01:58:35 2014
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

class Ui_prodLoader(object):
    def setupUi(self, prodLoader):
        prodLoader.setObjectName(_fromUtf8("prodLoader"))
        prodLoader.resize(365, 204)
        self.centralwidget = QtGui.QWidget(prodLoader)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.vlAll = QtGui.QVBoxLayout(self.layoutWidget)
        self.vlAll.setSpacing(1)
        self.vlAll.setMargin(0)
        self.vlAll.setObjectName(_fromUtf8("vlAll"))
        self.lAll = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lAll.setFont(font)
        self.lAll.setAlignment(QtCore.Qt.AlignCenter)
        self.lAll.setObjectName(_fromUtf8("lAll"))
        self.vlAll.addWidget(self.lAll)
        self.twAll = QtGui.QTreeWidget(self.layoutWidget)
        self.twAll.setAlternatingRowColors(False)
        self.twAll.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.twAll.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.twAll.setIndentation(2)
        self.twAll.setItemsExpandable(False)
        self.twAll.setExpandsOnDoubleClick(False)
        self.twAll.setObjectName(_fromUtf8("twAll"))
        self.twAll.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.twAll.headerItem().setFont(0, font)
        self.twAll.headerItem().setTextAlignment(1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.twAll.headerItem().setFont(1, font)
        self.twAll.headerItem().setTextAlignment(2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.twAll.headerItem().setFont(2, font)
        self.twAll.header().setVisible(True)
        self.twAll.header().setHighlightSections(False)
        self.twAll.header().setSortIndicatorShown(True)
        self.twAll.header().setStretchLastSection(True)
        self.vlAll.addWidget(self.twAll)
        self.bInclude = QtGui.QPushButton(self.layoutWidget)
        self.bInclude.setObjectName(_fromUtf8("bInclude"))
        self.vlAll.addWidget(self.bInclude)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.vlPref = QtGui.QVBoxLayout(self.layoutWidget1)
        self.vlPref.setSpacing(1)
        self.vlPref.setMargin(0)
        self.vlPref.setObjectName(_fromUtf8("vlPref"))
        self.lPref = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lPref.setFont(font)
        self.lPref.setAlignment(QtCore.Qt.AlignCenter)
        self.lPref.setObjectName(_fromUtf8("lPref"))
        self.vlPref.addWidget(self.lPref)
        self.twPref = QtGui.QTreeWidget(self.layoutWidget1)
        self.twPref.setAlternatingRowColors(False)
        self.twPref.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.twPref.setIndentation(2)
        self.twPref.setItemsExpandable(False)
        self.twPref.setExpandsOnDoubleClick(False)
        self.twPref.setObjectName(_fromUtf8("twPref"))
        self.twPref.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.twPref.headerItem().setFont(0, font)
        self.twPref.headerItem().setTextAlignment(1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.twPref.headerItem().setFont(1, font)
        self.twPref.headerItem().setTextAlignment(2, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.twPref.headerItem().setFont(2, font)
        self.twPref.header().setVisible(True)
        self.twPref.header().setSortIndicatorShown(True)
        self.twPref.header().setStretchLastSection(True)
        self.vlPref.addWidget(self.twPref)
        self.bRemove = QtGui.QPushButton(self.layoutWidget1)
        self.bRemove.setObjectName(_fromUtf8("bRemove"))
        self.vlPref.addWidget(self.bRemove)
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.bCreate = QtGui.QPushButton(self.centralwidget)
        self.bCreate.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bCreate.setObjectName(_fromUtf8("bCreate"))
        self.gridLayout.addWidget(self.bCreate, 0, 0, 1, 1)
        prodLoader.setCentralWidget(self.centralwidget)

        self.retranslateUi(prodLoader)
        QtCore.QMetaObject.connectSlotsByName(prodLoader)

    def retranslateUi(self, prodLoader):
        prodLoader.setWindowTitle(_translate("prodLoader", "ProdLoader", None))
        self.lAll.setText(_translate("prodLoader", "All Prods", None))
        self.twAll.setSortingEnabled(True)
        self.twAll.headerItem().setText(0, _translate("prodLoader", "Alias", None))
        self.twAll.headerItem().setText(1, _translate("prodLoader", "--", None))
        self.twAll.headerItem().setText(2, _translate("prodLoader", "Name", None))
        self.bInclude.setText(_translate("prodLoader", "Include To Pref", None))
        self.lPref.setText(_translate("prodLoader", "User Pref", None))
        self.twPref.setSortingEnabled(True)
        self.twPref.headerItem().setText(0, _translate("prodLoader", "Alias", None))
        self.twPref.headerItem().setText(1, _translate("prodLoader", "--", None))
        self.twPref.headerItem().setText(2, _translate("prodLoader", "Name", None))
        self.bRemove.setText(_translate("prodLoader", "Remove From Pref", None))
        self.bCreate.setText(_translate("prodLoader", "Create New Project", None))

