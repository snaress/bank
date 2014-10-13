# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\tabLineTest.ui'
#
# Created: Sun Oct 12 15:44:13 2014
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
        self.qfLtColumns = QtGui.QFrame(self.layoutWidget_2)
        self.qfLtColumns.setMinimumSize(QtCore.QSize(180, 0))
        self.qfLtColumns.setMaximumSize(QtCore.QSize(180, 16777215))
        self.qfLtColumns.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfLtColumns.setObjectName(_fromUtf8("qfLtColumns"))
        self.vlLtShotsColumn = QtGui.QVBoxLayout(self.qfLtColumns)
        self.vlLtShotsColumn.setSpacing(2)
        self.vlLtShotsColumn.setMargin(0)
        self.vlLtShotsColumn.setObjectName(_fromUtf8("vlLtShotsColumn"))
        self.sbLtColumns = QtGui.QSpinBox(self.qfLtColumns)
        self.sbLtColumns.setMinimumSize(QtCore.QSize(0, 0))
        self.sbLtColumns.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sbLtColumns.setWrapping(False)
        self.sbLtColumns.setAlignment(QtCore.Qt.AlignCenter)
        self.sbLtColumns.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.sbLtColumns.setProperty("value", 5)
        self.sbLtColumns.setObjectName(_fromUtf8("sbLtColumns"))
        self.vlLtShotsColumn.addWidget(self.sbLtColumns)
        self.twShotPref = QtGui.QTreeWidget(self.qfLtColumns)
        self.twShotPref.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.twShotPref.setIndentation(0)
        self.twShotPref.setItemsExpandable(False)
        self.twShotPref.setExpandsOnDoubleClick(False)
        self.twShotPref.setColumnCount(3)
        self.twShotPref.setObjectName(_fromUtf8("twShotPref"))
        self.twShotPref.headerItem().setText(0, _fromUtf8("Tree"))
        self.twShotPref.header().setVisible(True)
        self.twShotPref.header().setStretchLastSection(False)
        self.vlLtShotsColumn.addWidget(self.twShotPref)
        self.hlPrefBtns = QtGui.QHBoxLayout()
        self.hlPrefBtns.setSpacing(0)
        self.hlPrefBtns.setContentsMargins(-1, 0, -1, 0)
        self.hlPrefBtns.setObjectName(_fromUtf8("hlPrefBtns"))
        self.bStore = QtGui.QPushButton(self.qfLtColumns)
        self.bStore.setMaximumSize(QtCore.QSize(16777215, 20))
        self.bStore.setObjectName(_fromUtf8("bStore"))
        self.hlPrefBtns.addWidget(self.bStore)
        self.bRemove = QtGui.QPushButton(self.qfLtColumns)
        self.bRemove.setMaximumSize(QtCore.QSize(16777215, 20))
        self.bRemove.setObjectName(_fromUtf8("bRemove"))
        self.hlPrefBtns.addWidget(self.bRemove)
        self.vlLtShotsColumn.addLayout(self.hlPrefBtns)
        self.hlLtShots.addWidget(self.qfLtColumns)
        self.twShotTree = QtGui.QTreeWidget(self.layoutWidget_2)
        self.twShotTree.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.twShotTree.setIndentation(0)
        self.twShotTree.setItemsExpandable(False)
        self.twShotTree.setExpandsOnDoubleClick(False)
        self.twShotTree.setObjectName(_fromUtf8("twShotTree"))
        self.twShotTree.headerItem().setText(0, _fromUtf8("1"))
        self.twShotTree.header().setVisible(False)
        self.hlLtShots.addWidget(self.twShotTree)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(ltTab)
        QtCore.QMetaObject.connectSlotsByName(ltTab)

    def retranslateUi(self, ltTab):
        ltTab.setWindowTitle(_translate("ltTab", "LineTest", None))
        self.bLtNew.setText(_translate("ltTab", "New LT", None))
        self.bLtDel.setText(_translate("ltTab", "Del LT", None))
        self.sbLtColumns.setPrefix(_translate("ltTab", "Columns = ", None))
        self.twShotPref.setSortingEnabled(True)
        self.twShotPref.headerItem().setText(1, _translate("ltTab", "Step", None))
        self.twShotPref.headerItem().setText(2, _translate("ltTab", "ShotNode", None))
        self.bStore.setText(_translate("ltTab", "Store", None))
        self.bRemove.setText(_translate("ltTab", "Remove", None))

