# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\factory\ui\factory.ui'
#
# Created: Sun Oct 19 04:07:12 2014
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

class Ui_factory(object):
    def setupUi(self, factory):
        factory.setObjectName(_fromUtf8("factory"))
        factory.resize(1086, 637)
        self.centralwidget = QtGui.QWidget(factory)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.qfLeftZone = QtGui.QFrame(self.centralwidget)
        self.qfLeftZone.setMinimumSize(QtCore.QSize(252, 0))
        self.qfLeftZone.setMaximumSize(QtCore.QSize(252, 16777215))
        self.qfLeftZone.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfLeftZone.setObjectName(_fromUtf8("qfLeftZone"))
        self.vlLeftZone = QtGui.QVBoxLayout(self.qfLeftZone)
        self.vlLeftZone.setSpacing(2)
        self.vlLeftZone.setMargin(0)
        self.vlLeftZone.setObjectName(_fromUtf8("vlLeftZone"))
        self.qfSwitch = QtGui.QFrame(self.qfLeftZone)
        self.qfSwitch.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfSwitch.setObjectName(_fromUtf8("qfSwitch"))
        self.hlSwitch = QtGui.QHBoxLayout(self.qfSwitch)
        self.hlSwitch.setSpacing(0)
        self.hlSwitch.setContentsMargins(4, 0, 4, 0)
        self.hlSwitch.setObjectName(_fromUtf8("hlSwitch"))
        self.rbTexture = QtGui.QRadioButton(self.qfSwitch)
        self.rbTexture.setChecked(True)
        self.rbTexture.setObjectName(_fromUtf8("rbTexture"))
        self.bgSwitch = QtGui.QButtonGroup(factory)
        self.bgSwitch.setObjectName(_fromUtf8("bgSwitch"))
        self.bgSwitch.addButton(self.rbTexture)
        self.hlSwitch.addWidget(self.rbTexture)
        self.rbShader = QtGui.QRadioButton(self.qfSwitch)
        self.rbShader.setObjectName(_fromUtf8("rbShader"))
        self.bgSwitch.addButton(self.rbShader)
        self.hlSwitch.addWidget(self.rbShader)
        self.rbStockShot = QtGui.QRadioButton(self.qfSwitch)
        self.rbStockShot.setObjectName(_fromUtf8("rbStockShot"))
        self.bgSwitch.addButton(self.rbStockShot)
        self.hlSwitch.addWidget(self.rbStockShot)
        self.vlLeftZone.addWidget(self.qfSwitch)
        self.twTree = QtGui.QTreeWidget(self.qfLeftZone)
        self.twTree.setObjectName(_fromUtf8("twTree"))
        self.twTree.headerItem().setText(0, _fromUtf8("1"))
        self.twTree.header().setVisible(False)
        self.vlLeftZone.addWidget(self.twTree)
        self.gridLayout.addWidget(self.qfLeftZone, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QtGui.QFrame.StyledPanel)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.twThumbnail = QtGui.QTreeWidget(self.splitter)
        self.twThumbnail.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.twThumbnail.setIndentation(0)
        self.twThumbnail.setItemsExpandable(False)
        self.twThumbnail.setExpandsOnDoubleClick(False)
        self.twThumbnail.setColumnCount(5)
        self.twThumbnail.setObjectName(_fromUtf8("twThumbnail"))
        self.twThumbnail.headerItem().setText(0, _fromUtf8("1"))
        self.twThumbnail.headerItem().setText(1, _fromUtf8("2"))
        self.twThumbnail.headerItem().setText(2, _fromUtf8("3"))
        self.twThumbnail.headerItem().setText(3, _fromUtf8("4"))
        self.twThumbnail.headerItem().setText(4, _fromUtf8("5"))
        self.twThumbnail.header().setVisible(False)
        self.qfInfo = QtGui.QFrame(self.splitter)
        self.qfInfo.setMaximumSize(QtCore.QSize(16777215, 205))
        self.qfInfo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfInfo.setObjectName(_fromUtf8("qfInfo"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.qfInfo)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.sbColumns = QtGui.QSpinBox(self.qfInfo)
        self.sbColumns.setMinimum(1)
        self.sbColumns.setMaximum(20)
        self.sbColumns.setProperty("value", 5)
        self.sbColumns.setObjectName(_fromUtf8("sbColumns"))
        self.verticalLayout.addWidget(self.sbColumns)
        self.cbStorage = QtGui.QCheckBox(self.qfInfo)
        self.cbStorage.setChecked(True)
        self.cbStorage.setObjectName(_fromUtf8("cbStorage"))
        self.verticalLayout.addWidget(self.cbStorage)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.teInfo = QtGui.QTextEdit(self.qfInfo)
        self.teInfo.setMaximumSize(QtCore.QSize(16777215, 200))
        self.teInfo.setObjectName(_fromUtf8("teInfo"))
        self.horizontalLayout.addWidget(self.teInfo)
        self.gridLayout.addWidget(self.splitter, 0, 1, 1, 1)
        self.qfRightZone = QtGui.QFrame(self.centralwidget)
        self.qfRightZone.setMinimumSize(QtCore.QSize(250, 0))
        self.qfRightZone.setMaximumSize(QtCore.QSize(250, 16777215))
        self.qfRightZone.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfRightZone.setObjectName(_fromUtf8("qfRightZone"))
        self.vlRightZone = QtGui.QVBoxLayout(self.qfRightZone)
        self.vlRightZone.setSpacing(2)
        self.vlRightZone.setMargin(0)
        self.vlRightZone.setObjectName(_fromUtf8("vlRightZone"))
        self.splitter_2 = QtGui.QSplitter(self.qfRightZone)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.twTextures = QtGui.QTreeWidget(self.splitter_2)
        self.twTextures.setObjectName(_fromUtf8("twTextures"))
        self.twTextures.headerItem().setText(0, _fromUtf8("Stored Textures"))
        self.twTextures.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.twShaders = QtGui.QTreeWidget(self.splitter_2)
        self.twShaders.setObjectName(_fromUtf8("twShaders"))
        self.twShaders.headerItem().setText(0, _fromUtf8("Stored Shaders"))
        self.twShaders.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.twStockShots = QtGui.QTreeWidget(self.splitter_2)
        self.twStockShots.setObjectName(_fromUtf8("twStockShots"))
        self.twStockShots.headerItem().setText(0, _fromUtf8("Stored StockShots"))
        self.twStockShots.headerItem().setTextAlignment(0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.vlRightZone.addWidget(self.splitter_2)
        self.gridLayout.addWidget(self.qfRightZone, 0, 2, 1, 1)
        factory.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(factory)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1086, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.mThumbnail = QtGui.QMenu(self.menubar)
        self.mThumbnail.setObjectName(_fromUtf8("mThumbnail"))
        self.mTransfert = QtGui.QMenu(self.menubar)
        self.mTransfert.setObjectName(_fromUtf8("mTransfert"))
        factory.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(factory)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        factory.setStatusBar(self.statusbar)
        self.miCreateSelIcons = QtGui.QAction(factory)
        self.miCreateSelIcons.setObjectName(_fromUtf8("miCreateSelIcons"))
        self.miCreateAllIcons = QtGui.QAction(factory)
        self.miCreateAllIcons.setObjectName(_fromUtf8("miCreateAllIcons"))
        self.miCreateSelPreviews = QtGui.QAction(factory)
        self.miCreateSelPreviews.setObjectName(_fromUtf8("miCreateSelPreviews"))
        self.miCreateAllPreviews = QtGui.QAction(factory)
        self.miCreateAllPreviews.setObjectName(_fromUtf8("miCreateAllPreviews"))
        self.miCreateSelDatas = QtGui.QAction(factory)
        self.miCreateSelDatas.setObjectName(_fromUtf8("miCreateSelDatas"))
        self.miCreateAllDatas = QtGui.QAction(factory)
        self.miCreateAllDatas.setObjectName(_fromUtf8("miCreateAllDatas"))
        self.mThumbnail.addAction(self.miCreateSelIcons)
        self.mThumbnail.addAction(self.miCreateAllIcons)
        self.mThumbnail.addSeparator()
        self.mThumbnail.addAction(self.miCreateSelPreviews)
        self.mThumbnail.addAction(self.miCreateAllPreviews)
        self.menubar.addAction(self.mTransfert.menuAction())
        self.menubar.addAction(self.mThumbnail.menuAction())

        self.retranslateUi(factory)
        QtCore.QMetaObject.connectSlotsByName(factory)

    def retranslateUi(self, factory):
        factory.setWindowTitle(_translate("factory", "Factory", None))
        self.rbTexture.setText(_translate("factory", "Texture", None))
        self.rbShader.setText(_translate("factory", "Shader", None))
        self.rbStockShot.setText(_translate("factory", "StockShot", None))
        self.sbColumns.setPrefix(_translate("factory", "Columns = ", None))
        self.cbStorage.setText(_translate("factory", "Storage", None))
        self.mThumbnail.setTitle(_translate("factory", "Thumbnail", None))
        self.mTransfert.setTitle(_translate("factory", "Transfert", None))
        self.miCreateSelIcons.setText(_translate("factory", "Create Selected Icons", None))
        self.miCreateAllIcons.setText(_translate("factory", "Create All Icons", None))
        self.miCreateSelPreviews.setText(_translate("factory", "Create Selected Previews", None))
        self.miCreateAllPreviews.setText(_translate("factory", "Create All Previews", None))
        self.miCreateSelDatas.setText(_translate("factory", "Create Selected Datas", None))
        self.miCreateAllDatas.setText(_translate("factory", "Create All Datas", None))

