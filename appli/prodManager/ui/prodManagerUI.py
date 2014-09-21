# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\prodManager.ui'
#
# Created: Fri Sep 19 03:05:22 2014
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

class Ui_prodManager(object):
    def setupUi(self, prodManager):
        prodManager.setObjectName(_fromUtf8("prodManager"))
        prodManager.resize(1038, 764)
        self.centralwidget = QtGui.QWidget(prodManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.qfLeft = QtGui.QFrame(self.splitter)
        self.qfLeft.setMinimumSize(QtCore.QSize(300, 0))
        self.qfLeft.setMaximumSize(QtCore.QSize(300, 16777215))
        self.qfLeft.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfLeft.setObjectName(_fromUtf8("qfLeft"))
        self.verticalLayout = QtGui.QVBoxLayout(self.qfLeft)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.hfPreview = QtGui.QFrame(self.qfLeft)
        self.hfPreview.setMinimumSize(QtCore.QSize(0, 200))
        self.hfPreview.setFrameShape(QtGui.QFrame.StyledPanel)
        self.hfPreview.setObjectName(_fromUtf8("hfPreview"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.hfPreview)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout.addWidget(self.hfPreview)
        self.line = QtGui.QFrame(self.qfLeft)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.hfTree = QtGui.QFrame(self.qfLeft)
        self.hfTree.setMinimumSize(QtCore.QSize(0, 20))
        self.hfTree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.hfTree.setObjectName(_fromUtf8("hfTree"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.hfTree)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout.addWidget(self.hfTree)
        self.twTree = QtGui.QTreeView(self.qfLeft)
        self.twTree.setObjectName(_fromUtf8("twTree"))
        self.verticalLayout.addWidget(self.twTree)
        self.tabManager = QtGui.QTabWidget(self.splitter)
        self.tabManager.setObjectName(_fromUtf8("tabManager"))
        self.tabProject = QtGui.QWidget()
        self.tabProject.setObjectName(_fromUtf8("tabProject"))
        self.glTabProject = QtGui.QGridLayout(self.tabProject)
        self.glTabProject.setMargin(2)
        self.glTabProject.setSpacing(1)
        self.glTabProject.setObjectName(_fromUtf8("glTabProject"))
        self.tabManager.addTab(self.tabProject, _fromUtf8(""))
        self.tabShots = QtGui.QWidget()
        self.tabShots.setObjectName(_fromUtf8("tabShots"))
        self.tabManager.addTab(self.tabShots, _fromUtf8(""))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        prodManager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(prodManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1038, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuPref = QtGui.QMenu(self.menubar)
        self.menuPref.setObjectName(_fromUtf8("menuPref"))
        self.menuStyle = QtGui.QMenu(self.menuPref)
        self.menuStyle.setObjectName(_fromUtf8("menuStyle"))
        prodManager.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(prodManager)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        prodManager.setStatusBar(self.statusbar)
        self.miDefaultStyle = QtGui.QAction(prodManager)
        self.miDefaultStyle.setObjectName(_fromUtf8("miDefaultStyle"))
        self.miDarkGreyStyle = QtGui.QAction(prodManager)
        self.miDarkGreyStyle.setObjectName(_fromUtf8("miDarkGreyStyle"))
        self.miDarkOrangeStyle = QtGui.QAction(prodManager)
        self.miDarkOrangeStyle.setObjectName(_fromUtf8("miDarkOrangeStyle"))
        self.menuStyle.addAction(self.miDefaultStyle)
        self.menuStyle.addAction(self.miDarkGreyStyle)
        self.menuStyle.addAction(self.miDarkOrangeStyle)
        self.menuPref.addAction(self.menuStyle.menuAction())
        self.menubar.addAction(self.menuPref.menuAction())

        self.retranslateUi(prodManager)
        self.tabManager.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(prodManager)

    def retranslateUi(self, prodManager):
        prodManager.setWindowTitle(_translate("prodManager", "ProdManager", None))
        self.tabManager.setTabText(self.tabManager.indexOf(self.tabProject), _translate("prodManager", "Project", None))
        self.tabManager.setTabText(self.tabManager.indexOf(self.tabShots), _translate("prodManager", "Shots", None))
        self.menuPref.setTitle(_translate("prodManager", "Pref", None))
        self.menuStyle.setTitle(_translate("prodManager", "Style", None))
        self.miDefaultStyle.setText(_translate("prodManager", "Default", None))
        self.miDarkGreyStyle.setText(_translate("prodManager", "DarkGrey", None))
        self.miDarkOrangeStyle.setText(_translate("prodManager", "DarkOrange", None))

