# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtProdTask.ui'
#
# Created: Sun Sep 21 00:40:51 2014
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

class Ui_prodTask(object):
    def setupUi(self, prodTask):
        prodTask.setObjectName(_fromUtf8("prodTask"))
        prodTask.resize(230, 95)
        prodTask.setMinimumSize(QtCore.QSize(230, 0))
        prodTask.setMaximumSize(QtCore.QSize(300, 16777215))
        self.gridLayout = QtGui.QGridLayout(prodTask)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.twTasks = QtGui.QTreeWidget(prodTask)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twTasks.sizePolicy().hasHeightForWidth())
        self.twTasks.setSizePolicy(sizePolicy)
        self.twTasks.setMinimumSize(QtCore.QSize(0, 0))
        self.twTasks.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.twTasks.setAlternatingRowColors(False)
        self.twTasks.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.twTasks.setIndentation(2)
        self.twTasks.setObjectName(_fromUtf8("twTasks"))
        self.twTasks.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.twTasks.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.twTasks.headerItem().setTextAlignment(2, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.twTasks.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.twTasks, 0, 2, 1, 1)
        self.qfTask = QtGui.QFrame(prodTask)
        self.qfTask.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qfTask.setObjectName(_fromUtf8("qfTask"))
        self.vlTaskBtns = QtGui.QVBoxLayout(self.qfTask)
        self.vlTaskBtns.setSpacing(0)
        self.vlTaskBtns.setMargin(0)
        self.vlTaskBtns.setObjectName(_fromUtf8("vlTaskBtns"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTaskBtns.addItem(spacerItem)
        self.bAddTask = QtGui.QPushButton(self.qfTask)
        self.bAddTask.setMinimumSize(QtCore.QSize(0, 0))
        self.bAddTask.setMaximumSize(QtCore.QSize(70, 22))
        self.bAddTask.setObjectName(_fromUtf8("bAddTask"))
        self.vlTaskBtns.addWidget(self.bAddTask)
        self.bDelTask = QtGui.QPushButton(self.qfTask)
        self.bDelTask.setMinimumSize(QtCore.QSize(0, 0))
        self.bDelTask.setMaximumSize(QtCore.QSize(70, 22))
        self.bDelTask.setObjectName(_fromUtf8("bDelTask"))
        self.vlTaskBtns.addWidget(self.bDelTask)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTaskBtns.addItem(spacerItem1)
        self.bTaskUp = QtGui.QPushButton(self.qfTask)
        self.bTaskUp.setMinimumSize(QtCore.QSize(0, 0))
        self.bTaskUp.setMaximumSize(QtCore.QSize(70, 22))
        self.bTaskUp.setObjectName(_fromUtf8("bTaskUp"))
        self.vlTaskBtns.addWidget(self.bTaskUp)
        self.bTaskDn = QtGui.QPushButton(self.qfTask)
        self.bTaskDn.setMinimumSize(QtCore.QSize(0, 0))
        self.bTaskDn.setMaximumSize(QtCore.QSize(70, 22))
        self.bTaskDn.setObjectName(_fromUtf8("bTaskDn"))
        self.vlTaskBtns.addWidget(self.bTaskDn)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vlTaskBtns.addItem(spacerItem2)
        self.gridLayout.addWidget(self.qfTask, 0, 1, 1, 1)

        self.retranslateUi(prodTask)
        QtCore.QMetaObject.connectSlotsByName(prodTask)

    def retranslateUi(self, prodTask):
        prodTask.setWindowTitle(_translate("prodTask", "Tasks", None))
        self.twTasks.headerItem().setText(0, _translate("prodTask", "Tasks", None))
        self.twTasks.headerItem().setText(1, _translate("prodTask", "Color", None))
        self.twTasks.headerItem().setText(2, _translate("prodTask", "Stats", None))
        self.bAddTask.setText(_translate("prodTask", "Add Task", None))
        self.bDelTask.setText(_translate("prodTask", "Del Task", None))
        self.bTaskUp.setText(_translate("prodTask", "Up", None))
        self.bTaskDn.setText(_translate("prodTask", "Down", None))

