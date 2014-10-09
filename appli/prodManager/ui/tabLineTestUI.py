# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\tabLineTest.ui'
#
# Created: Wed Oct 08 17:44:24 2014
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

class Ui_ltTab(object):
    def setupUi(self, ltTab):
        ltTab.setObjectName(_fromUtf8("ltTab"))
        ltTab.resize(695, 551)
        self.gridLayout = QtGui.QGridLayout(ltTab)
        self.gridLayout.setMargin(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(ltTab)
        self.splitter.setBaseSize(QtCore.QSize(0, 200))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.vlLtZone = QtGui.QVBoxLayout(self.layoutWidget)
        self.vlLtZone.setSpacing(2)
        self.vlLtZone.setMargin(0)
        self.vlLtZone.setObjectName(_fromUtf8("vlLtZone"))
        self.hlLtBtns = QtGui.QHBoxLayout()
        self.hlLtBtns.setSpacing(2)
        self.hlLtBtns.setObjectName(_fromUtf8("hlLtBtns"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlLtBtns.addItem(spacerItem)
        self.bLtNew = QtGui.QPushButton(self.layoutWidget)
        self.bLtNew.setMinimumSize(QtCore.QSize(0, 0))
        self.bLtNew.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bLtNew.setObjectName(_fromUtf8("bLtNew"))
        self.hlLtBtns.addWidget(self.bLtNew)
        self.bLtDel = QtGui.QPushButton(self.layoutWidget)
        self.bLtDel.setMinimumSize(QtCore.QSize(0, 0))
        self.bLtDel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bLtDel.setObjectName(_fromUtf8("bLtDel"))
        self.hlLtBtns.addWidget(self.bLtDel)
        self.vlLtZone.addLayout(self.hlLtBtns)
        self.line_2 = QtGui.QFrame(self.layoutWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.vlLtZone.addWidget(self.line_2)
        self.twLtTree = QtGui.QTreeWidget(self.layoutWidget)
        self.twLtTree.setIndentation(0)
        self.twLtTree.setObjectName(_fromUtf8("twLtTree"))
        self.twLtTree.headerItem().setText(0, _fromUtf8("1"))
        self.twLtTree.header().setVisible(False)
        self.vlLtZone.addWidget(self.twLtTree)
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.vlLtZone.addWidget(self.line)
        self.layoutWidget_2 = QtGui.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.hlLtShots = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.hlLtShots.setSpacing(2)
        self.hlLtShots.setMargin(0)
        self.hlLtShots.setObjectName(_fromUtf8("hlLtShots"))
        self.vlLtShotsColumn = QtGui.QVBoxLayout()
        self.vlLtShotsColumn.setObjectName(_fromUtf8("vlLtShotsColumn"))
        self.sbLtColumns = QtGui.QSpinBox(self.layoutWidget_2)
        self.sbLtColumns.setWrapping(False)
        self.sbLtColumns.setAlignment(QtCore.Qt.AlignCenter)
        self.sbLtColumns.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.sbLtColumns.setProperty("value", 5)
        self.sbLtColumns.setObjectName(_fromUtf8("sbLtColumns"))
        self.vlLtShotsColumn.addWidget(self.sbLtColumns)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlLtShotsColumn.addItem(spacerItem1)
        self.hlLtShots.addLayout(self.vlLtShotsColumn)
        self.tabLtShots = QtGui.QTabWidget(self.layoutWidget_2)
        self.tabLtShots.setMinimumSize(QtCore.QSize(0, 150))
        self.tabLtShots.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabLtShots.setTabsClosable(False)
        self.tabLtShots.setMovable(True)
        self.tabLtShots.setObjectName(_fromUtf8("tabLtShots"))
        self.ltShotTab1 = QtGui.QWidget()
        self.ltShotTab1.setObjectName(_fromUtf8("ltShotTab1"))
        self.glLtShotTab1 = QtGui.QGridLayout(self.ltShotTab1)
        self.glLtShotTab1.setMargin(1)
        self.glLtShotTab1.setSpacing(1)
        self.glLtShotTab1.setObjectName(_fromUtf8("glLtShotTab1"))
        self.tabLtShots.addTab(self.ltShotTab1, _fromUtf8(""))
        self.hlLtShots.addWidget(self.tabLtShots)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(ltTab)
        self.tabLtShots.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ltTab)

    def retranslateUi(self, ltTab):
        ltTab.setWindowTitle(_translate("ltTab", "LineTest", None))
        self.bLtNew.setText(_translate("ltTab", "New LT", None))
        self.bLtDel.setText(_translate("ltTab", "Del LT", None))
        self.sbLtColumns.setPrefix(_translate("ltTab", "Columns = ", None))
        self.tabLtShots.setTabText(self.tabLtShots.indexOf(self.ltShotTab1), _translate("ltTab", "Tab 1", None))

