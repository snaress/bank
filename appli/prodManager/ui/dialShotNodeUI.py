# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\dialShotNode.ui'
#
# Created: Thu Sep 25 04:32:47 2014
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

class Ui_editProdTree(object):
    def setupUi(self, editProdTree):
        editProdTree.setObjectName(_fromUtf8("editProdTree"))
        editProdTree.resize(410, 177)
        self.gridLayout_2 = QtGui.QGridLayout(editProdTree)
        self.gridLayout_2.setMargin(1)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.line = QtGui.QFrame(editProdTree)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 0, 0, 1, 1)
        self.lMessage = QtGui.QLabel(editProdTree)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lMessage.setFont(font)
        self.lMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lMessage.setObjectName(_fromUtf8("lMessage"))
        self.gridLayout_2.addWidget(self.lMessage, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(editProdTree)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 2, 0, 1, 1)
        self.hlNodeType = QtGui.QHBoxLayout()
        self.hlNodeType.setObjectName(_fromUtf8("hlNodeType"))
        self.lNodeType = QtGui.QLabel(editProdTree)
        self.lNodeType.setObjectName(_fromUtf8("lNodeType"))
        self.hlNodeType.addWidget(self.lNodeType)
        self.rbContainer = QtGui.QRadioButton(editProdTree)
        self.rbContainer.setChecked(True)
        self.rbContainer.setObjectName(_fromUtf8("rbContainer"))
        self.rbgNodeType = QtGui.QButtonGroup(editProdTree)
        self.rbgNodeType.setObjectName(_fromUtf8("rbgNodeType"))
        self.rbgNodeType.addButton(self.rbContainer)
        self.hlNodeType.addWidget(self.rbContainer)
        self.rbShotNode = QtGui.QRadioButton(editProdTree)
        self.rbShotNode.setObjectName(_fromUtf8("rbShotNode"))
        self.rbgNodeType.addButton(self.rbShotNode)
        self.hlNodeType.addWidget(self.rbShotNode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlNodeType.addItem(spacerItem)
        self.lNameCvtn = QtGui.QLabel(editProdTree)
        self.lNameCvtn.setObjectName(_fromUtf8("lNameCvtn"))
        self.hlNodeType.addWidget(self.lNameCvtn)
        self.cbNameCvtn = QtGui.QComboBox(editProdTree)
        self.cbNameCvtn.setMinimumSize(QtCore.QSize(65, 0))
        self.cbNameCvtn.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cbNameCvtn.setObjectName(_fromUtf8("cbNameCvtn"))
        self.cbNameCvtn.addItem(_fromUtf8(""))
        self.cbNameCvtn.addItem(_fromUtf8(""))
        self.hlNodeType.addWidget(self.cbNameCvtn)
        self.gridLayout_2.addLayout(self.hlNodeType, 3, 0, 1, 1)
        self.line_3 = QtGui.QFrame(editProdTree)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_2.addWidget(self.line_3, 4, 0, 1, 1)
        self.hlMethode = QtGui.QHBoxLayout()
        self.hlMethode.setObjectName(_fromUtf8("hlMethode"))
        self.lMethode = QtGui.QLabel(editProdTree)
        self.lMethode.setObjectName(_fromUtf8("lMethode"))
        self.hlMethode.addWidget(self.lMethode)
        self.rbUnique = QtGui.QRadioButton(editProdTree)
        self.rbUnique.setChecked(True)
        self.rbUnique.setObjectName(_fromUtf8("rbUnique"))
        self.rbgMethode = QtGui.QButtonGroup(editProdTree)
        self.rbgMethode.setObjectName(_fromUtf8("rbgMethode"))
        self.rbgMethode.addButton(self.rbUnique)
        self.hlMethode.addWidget(self.rbUnique)
        self.rbMulti = QtGui.QRadioButton(editProdTree)
        self.rbMulti.setObjectName(_fromUtf8("rbMulti"))
        self.rbgMethode.addButton(self.rbMulti)
        self.hlMethode.addWidget(self.rbMulti)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlMethode.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.hlMethode, 5, 0, 1, 1)
        self.line_4 = QtGui.QFrame(editProdTree)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout_2.addWidget(self.line_4, 6, 0, 1, 1)
        self.fMulti = QtGui.QFrame(editProdTree)
        self.fMulti.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fMulti.setObjectName(_fromUtf8("fMulti"))
        self.gridLayout = QtGui.QGridLayout(self.fMulti)
        self.gridLayout.setMargin(1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lLoopRange = QtGui.QLabel(self.fMulti)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lLoopRange.sizePolicy().hasHeightForWidth())
        self.lLoopRange.setSizePolicy(sizePolicy)
        self.lLoopRange.setMinimumSize(QtCore.QSize(60, 0))
        self.lLoopRange.setObjectName(_fromUtf8("lLoopRange"))
        self.gridLayout.addWidget(self.lLoopRange, 0, 0, 1, 1)
        self.lPadd = QtGui.QLabel(self.fMulti)
        self.lPadd.setAlignment(QtCore.Qt.AlignCenter)
        self.lPadd.setObjectName(_fromUtf8("lPadd"))
        self.gridLayout.addWidget(self.lPadd, 1, 3, 1, 1)
        self.sbStep = QtGui.QSpinBox(self.fMulti)
        self.sbStep.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sbStep.setMaximum(1000)
        self.sbStep.setProperty("value", 1)
        self.sbStep.setObjectName(_fromUtf8("sbStep"))
        self.gridLayout.addWidget(self.sbStep, 0, 3, 1, 1)
        self.sbPadding = QtGui.QSpinBox(self.fMulti)
        self.sbPadding.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sbPadding.setProperty("value", 3)
        self.sbPadding.setObjectName(_fromUtf8("sbPadding"))
        self.gridLayout.addWidget(self.sbPadding, 0, 5, 1, 1)
        self.lPadding = QtGui.QLabel(self.fMulti)
        self.lPadding.setAlignment(QtCore.Qt.AlignCenter)
        self.lPadding.setObjectName(_fromUtf8("lPadding"))
        self.gridLayout.addWidget(self.lPadding, 0, 4, 1, 1)
        self.leSuffixe = QtGui.QLineEdit(self.fMulti)
        self.leSuffixe.setObjectName(_fromUtf8("leSuffixe"))
        self.gridLayout.addWidget(self.leSuffixe, 1, 4, 1, 2)
        self.lSuffixe = QtGui.QLabel(self.fMulti)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSuffixe.sizePolicy().hasHeightForWidth())
        self.lSuffixe.setSizePolicy(sizePolicy)
        self.lSuffixe.setMinimumSize(QtCore.QSize(60, 0))
        self.lSuffixe.setAlignment(QtCore.Qt.AlignCenter)
        self.lSuffixe.setObjectName(_fromUtf8("lSuffixe"))
        self.gridLayout.addWidget(self.lSuffixe, 1, 6, 1, 1)
        self.sbStop = QtGui.QSpinBox(self.fMulti)
        self.sbStop.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sbStop.setMaximum(1000)
        self.sbStop.setProperty("value", 10)
        self.sbStop.setObjectName(_fromUtf8("sbStop"))
        self.gridLayout.addWidget(self.sbStop, 0, 2, 1, 1)
        self.lPrefixe = QtGui.QLabel(self.fMulti)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lPrefixe.sizePolicy().hasHeightForWidth())
        self.lPrefixe.setSizePolicy(sizePolicy)
        self.lPrefixe.setMinimumSize(QtCore.QSize(60, 0))
        self.lPrefixe.setAlignment(QtCore.Qt.AlignCenter)
        self.lPrefixe.setObjectName(_fromUtf8("lPrefixe"))
        self.gridLayout.addWidget(self.lPrefixe, 1, 0, 1, 1)
        self.lePrefixe = QtGui.QLineEdit(self.fMulti)
        self.lePrefixe.setObjectName(_fromUtf8("lePrefixe"))
        self.gridLayout.addWidget(self.lePrefixe, 1, 1, 1, 2)
        self.sbStart = QtGui.QSpinBox(self.fMulti)
        self.sbStart.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sbStart.setMaximum(1000)
        self.sbStart.setProperty("value", 1)
        self.sbStart.setObjectName(_fromUtf8("sbStart"))
        self.gridLayout.addWidget(self.sbStart, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.fMulti, 8, 0, 1, 1)
        self.line_5 = QtGui.QFrame(editProdTree)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout_2.addWidget(self.line_5, 9, 0, 1, 1)
        self.hlButtons = QtGui.QHBoxLayout()
        self.hlButtons.setSpacing(2)
        self.hlButtons.setObjectName(_fromUtf8("hlButtons"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hlButtons.addItem(spacerItem2)
        self.bCreate = QtGui.QPushButton(editProdTree)
        self.bCreate.setObjectName(_fromUtf8("bCreate"))
        self.hlButtons.addWidget(self.bCreate)
        self.bCancel = QtGui.QPushButton(editProdTree)
        self.bCancel.setObjectName(_fromUtf8("bCancel"))
        self.hlButtons.addWidget(self.bCancel)
        self.gridLayout_2.addLayout(self.hlButtons, 10, 0, 1, 1)
        self.fUnique = QtGui.QFrame(editProdTree)
        self.fUnique.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fUnique.setObjectName(_fromUtf8("fUnique"))
        self.hlUnique = QtGui.QHBoxLayout(self.fUnique)
        self.hlUnique.setSpacing(0)
        self.hlUnique.setMargin(0)
        self.hlUnique.setObjectName(_fromUtf8("hlUnique"))
        self.lNodeName = QtGui.QLabel(self.fUnique)
        self.lNodeName.setObjectName(_fromUtf8("lNodeName"))
        self.hlUnique.addWidget(self.lNodeName)
        self.leNodeName = QtGui.QLineEdit(self.fUnique)
        self.leNodeName.setObjectName(_fromUtf8("leNodeName"))
        self.hlUnique.addWidget(self.leNodeName)
        self.gridLayout_2.addWidget(self.fUnique, 7, 0, 1, 1)

        self.retranslateUi(editProdTree)
        QtCore.QMetaObject.connectSlotsByName(editProdTree)

    def retranslateUi(self, editProdTree):
        editProdTree.setWindowTitle(_translate("editProdTree", "Dialog", None))
        self.lMessage.setText(_translate("editProdTree", "Message", None))
        self.lNodeType.setText(_translate("editProdTree", "Type: ", None))
        self.rbContainer.setText(_translate("editProdTree", "Container", None))
        self.rbShotNode.setText(_translate("editProdTree", "ShotNode", None))
        self.lNameCvtn.setText(_translate("editProdTree", "Name Convention: ", None))
        self.cbNameCvtn.setItemText(0, _translate("editProdTree", "Asset", None))
        self.cbNameCvtn.setItemText(1, _translate("editProdTree", "Shot", None))
        self.lMethode.setText(_translate("editProdTree", "Methode: ", None))
        self.rbUnique.setText(_translate("editProdTree", "Unique", None))
        self.rbMulti.setText(_translate("editProdTree", "Multi", None))
        self.lLoopRange.setText(_translate("editProdTree", "Loop Range : ", None))
        self.lPadd.setText(_translate("editProdTree", "###", None))
        self.lPadding.setText(_translate("editProdTree", "Padding : ", None))
        self.lSuffixe.setText(_translate("editProdTree", " : Suffixe", None))
        self.lPrefixe.setText(_translate("editProdTree", "Prefixe : ", None))
        self.bCreate.setText(_translate("editProdTree", "Create", None))
        self.bCancel.setText(_translate("editProdTree", "Cancel", None))
        self.lNodeName.setText(_translate("editProdTree", "New Node Name: ", None))

