# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\tabLineTest.ui'
#
# Created: Thu Oct 02 15:40:18 2014
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
        ltTab.resize(695, 300)
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
        self.cbLtAutoRf = QtGui.QCheckBox(self.layoutWidget_2)
        self.cbLtAutoRf.setChecked(True)
        self.cbLtAutoRf.setObjectName(_fromUtf8("cbLtAutoRf"))
        self.vlLtShotsColumn.addWidget(self.cbLtAutoRf)
        self.cbLtEditMode = QtGui.QCheckBox(self.layoutWidget_2)
        self.cbLtEditMode.setObjectName(_fromUtf8("cbLtEditMode"))
        self.vlLtShotsColumn.addWidget(self.cbLtEditMode)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlLtShotsColumn.addItem(spacerItem1)
        self.hlLtShots.addLayout(self.vlLtShotsColumn)
        self.tabLtShots = QtGui.QTabWidget(self.layoutWidget_2)
        self.tabLtShots.setMinimumSize(QtCore.QSize(0, 150))
        self.tabLtShots.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabLtShots.setTabsClosable(False)
        self.tabLtShots.setMovable(True)
        self.tabLtShots.setObjectName(_fromUtf8("tabLtShots"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab)
        self.gridLayout_6.setMargin(1)
        self.gridLayout_6.setSpacing(1)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.twLtShots = QtGui.QTreeWidget(self.tab)
        self.twLtShots.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.twLtShots.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.twLtShots.setIndentation(0)
        self.twLtShots.setColumnCount(5)
        self.twLtShots.setObjectName(_fromUtf8("twLtShots"))
        self.twLtShots.headerItem().setText(0, _fromUtf8("1"))
        self.twLtShots.headerItem().setText(1, _fromUtf8("2"))
        self.twLtShots.headerItem().setText(2, _fromUtf8("3"))
        self.twLtShots.headerItem().setText(3, _fromUtf8("4"))
        self.twLtShots.headerItem().setText(4, _fromUtf8("5"))
        self.twLtShots.header().setVisible(False)
        self.gridLayout_6.addWidget(self.twLtShots, 0, 0, 1, 1)
        self.tabLtShots.addTab(self.tab, _fromUtf8(""))
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
        self.cbLtAutoRf.setText(_translate("ltTab", "Auto Refresh", None))
        self.cbLtEditMode.setText(_translate("ltTab", "Edit Mode", None))
        self.tabLtShots.setTabText(self.tabLtShots.indexOf(self.tab), _translate("ltTab", "Tab 1", None))

