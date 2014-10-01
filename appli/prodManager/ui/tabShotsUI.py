# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\tabShots.ui'
#
# Created: Sun Sep 28 16:11:22 2014
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

class Ui_shotsTab(object):
    def setupUi(self, shotsTab):
        shotsTab.setObjectName(_fromUtf8("shotsTab"))
        shotsTab.resize(943, 702)
        self.gridLayout = QtGui.QGridLayout(shotsTab)
        self.gridLayout.setMargin(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter_2 = QtGui.QSplitter(shotsTab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.qfTreeShots = QtGui.QFrame(self.splitter_2)
        self.qfTreeShots.setMinimumSize(QtCore.QSize(350, 0))
        self.qfTreeShots.setObjectName(_fromUtf8("qfTreeShots"))
        self.vlTreeShots = QtGui.QVBoxLayout(self.qfTreeShots)
        self.vlTreeShots.setSpacing(1)
        self.vlTreeShots.setMargin(0)
        self.vlTreeShots.setObjectName(_fromUtf8("vlTreeShots"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.vlShotParams = QtGui.QVBoxLayout(self.layoutWidget)
        self.vlShotParams.setSpacing(2)
        self.vlShotParams.setMargin(0)
        self.vlShotParams.setObjectName(_fromUtf8("vlShotParams"))
        self.hlShotParamsBtns = QtGui.QHBoxLayout()
        self.hlShotParamsBtns.setSpacing(2)
        self.hlShotParamsBtns.setObjectName(_fromUtf8("hlShotParamsBtns"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlShotParamsBtns.addItem(spacerItem)
        self.bCancelEdit = QtGui.QPushButton(self.layoutWidget)
        self.bCancelEdit.setMaximumSize(QtCore.QSize(50, 20))
        self.bCancelEdit.setObjectName(_fromUtf8("bCancelEdit"))
        self.hlShotParamsBtns.addWidget(self.bCancelEdit)
        self.bEditShotParams = QtGui.QPushButton(self.layoutWidget)
        self.bEditShotParams.setMaximumSize(QtCore.QSize(40, 20))
        self.bEditShotParams.setCheckable(True)
        self.bEditShotParams.setObjectName(_fromUtf8("bEditShotParams"))
        self.hlShotParamsBtns.addWidget(self.bEditShotParams)
        self.vlShotParams.addLayout(self.hlShotParamsBtns)
        self.hlWorkDir = QtGui.QHBoxLayout()
        self.hlWorkDir.setSpacing(2)
        self.hlWorkDir.setObjectName(_fromUtf8("hlWorkDir"))
        self.lWorkDir = QtGui.QLabel(self.layoutWidget)
        self.lWorkDir.setMinimumSize(QtCore.QSize(0, 0))
        self.lWorkDir.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lWorkDir.setFont(font)
        self.lWorkDir.setObjectName(_fromUtf8("lWorkDir"))
        self.hlWorkDir.addWidget(self.lWorkDir)
        self.leWorkDir = QtGui.QLineEdit(self.layoutWidget)
        self.leWorkDir.setMinimumSize(QtCore.QSize(0, 0))
        self.leWorkDir.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.leWorkDir.setObjectName(_fromUtf8("leWorkDir"))
        self.hlWorkDir.addWidget(self.leWorkDir)
        self.bOpenWorkDir = QtGui.QPushButton(self.layoutWidget)
        self.bOpenWorkDir.setMaximumSize(QtCore.QSize(40, 20))
        self.bOpenWorkDir.setObjectName(_fromUtf8("bOpenWorkDir"))
        self.hlWorkDir.addWidget(self.bOpenWorkDir)
        self.vlShotParams.addLayout(self.hlWorkDir)
        self.hlImaDir = QtGui.QHBoxLayout()
        self.hlImaDir.setSpacing(2)
        self.hlImaDir.setObjectName(_fromUtf8("hlImaDir"))
        self.lImaDir = QtGui.QLabel(self.layoutWidget)
        self.lImaDir.setMinimumSize(QtCore.QSize(45, 0))
        self.lImaDir.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lImaDir.setFont(font)
        self.lImaDir.setObjectName(_fromUtf8("lImaDir"))
        self.hlImaDir.addWidget(self.lImaDir)
        self.leImaDir = QtGui.QLineEdit(self.layoutWidget)
        self.leImaDir.setMinimumSize(QtCore.QSize(0, 0))
        self.leImaDir.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.leImaDir.setObjectName(_fromUtf8("leImaDir"))
        self.hlImaDir.addWidget(self.leImaDir)
        self.bOpenImaDir = QtGui.QPushButton(self.layoutWidget)
        self.bOpenImaDir.setMaximumSize(QtCore.QSize(40, 20))
        self.bOpenImaDir.setObjectName(_fromUtf8("bOpenImaDir"))
        self.hlImaDir.addWidget(self.bOpenImaDir)
        self.vlShotParams.addLayout(self.hlImaDir)
        self.twShotParams = QtGui.QTreeWidget(self.layoutWidget)
        self.twShotParams.setMinimumSize(QtCore.QSize(0, 0))
        self.twShotParams.setIndentation(0)
        self.twShotParams.setObjectName(_fromUtf8("twShotParams"))
        self.vlShotParams.addWidget(self.twShotParams)
        self.qfShotComment = QtGui.QFrame(self.splitter)
        self.qfShotComment.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfShotComment.setObjectName(_fromUtf8("qfShotComment"))
        self.glShotComment = QtGui.QGridLayout(self.qfShotComment)
        self.glShotComment.setMargin(1)
        self.glShotComment.setSpacing(1)
        self.glShotComment.setObjectName(_fromUtf8("glShotComment"))
        self.lShotComment = QtGui.QLabel(self.qfShotComment)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lShotComment.setFont(font)
        self.lShotComment.setObjectName(_fromUtf8("lShotComment"))
        self.glShotComment.addWidget(self.lShotComment, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(shotsTab)
        QtCore.QMetaObject.connectSlotsByName(shotsTab)

    def retranslateUi(self, shotsTab):
        shotsTab.setWindowTitle(_translate("shotsTab", "Tab Shots", None))
        self.bCancelEdit.setText(_translate("shotsTab", "Cancel", None))
        self.bEditShotParams.setText(_translate("shotsTab", "Edit", None))
        self.lWorkDir.setText(_translate("shotsTab", "Work Dir:", None))
        self.bOpenWorkDir.setText(_translate("shotsTab", "Open", None))
        self.lImaDir.setText(_translate("shotsTab", "Ima Dir:", None))
        self.bOpenImaDir.setText(_translate("shotsTab", "Open", None))
        self.twShotParams.headerItem().setText(0, _translate("shotsTab", "Name", None))
        self.twShotParams.headerItem().setText(1, _translate("shotsTab", "Value", None))
        self.lShotComment.setText(_translate("shotsTab", "Comment", None))

