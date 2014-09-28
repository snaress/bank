# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtShotNode.ui'
#
# Created: Sun Sep 28 04:03:22 2014
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

class Ui_shotNode(object):
    def setupUi(self, shotNode):
        shotNode.setObjectName(_fromUtf8("shotNode"))
        shotNode.resize(365, 164)
        self.gridLayout_2 = QtGui.QGridLayout(shotNode)
        self.gridLayout_2.setMargin(1)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.hlShotNode = QtGui.QHBoxLayout()
        self.hlShotNode.setSpacing(2)
        self.hlShotNode.setObjectName(_fromUtf8("hlShotNode"))
        self.lPreview = QtGui.QLabel(shotNode)
        self.lPreview.setMinimumSize(QtCore.QSize(150, 150))
        self.lPreview.setMaximumSize(QtCore.QSize(150, 150))
        self.lPreview.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lPreview.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lPreview.setFrameShadow(QtGui.QFrame.Plain)
        self.lPreview.setLineWidth(1)
        self.lPreview.setMidLineWidth(0)
        self.lPreview.setScaledContents(True)
        self.lPreview.setAlignment(QtCore.Qt.AlignCenter)
        self.lPreview.setWordWrap(False)
        self.lPreview.setMargin(0)
        self.lPreview.setIndent(-1)
        self.lPreview.setObjectName(_fromUtf8("lPreview"))
        self.hlShotNode.addWidget(self.lPreview)
        self.glShotInfo = QtGui.QGridLayout()
        self.glShotInfo.setSpacing(2)
        self.glShotInfo.setObjectName(_fromUtf8("glShotInfo"))
        self.lLabel = QtGui.QLabel(shotNode)
        self.lLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lLabel.setFont(font)
        self.lLabel.setObjectName(_fromUtf8("lLabel"))
        self.glShotInfo.addWidget(self.lLabel, 0, 0, 1, 1)
        self.lLabelVal = QtGui.QLabel(shotNode)
        self.lLabelVal.setObjectName(_fromUtf8("lLabelVal"))
        self.glShotInfo.addWidget(self.lLabelVal, 0, 1, 1, 1)
        self.lName = QtGui.QLabel(shotNode)
        self.lName.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lName.setFont(font)
        self.lName.setObjectName(_fromUtf8("lName"))
        self.glShotInfo.addWidget(self.lName, 1, 0, 1, 1)
        self.lNameVal = QtGui.QLabel(shotNode)
        self.lNameVal.setObjectName(_fromUtf8("lNameVal"))
        self.glShotInfo.addWidget(self.lNameVal, 1, 1, 1, 1)
        self.lType = QtGui.QLabel(shotNode)
        self.lType.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lType.setFont(font)
        self.lType.setObjectName(_fromUtf8("lType"))
        self.glShotInfo.addWidget(self.lType, 2, 0, 1, 1)
        self.lTypeVal = QtGui.QLabel(shotNode)
        self.lTypeVal.setObjectName(_fromUtf8("lTypeVal"))
        self.glShotInfo.addWidget(self.lTypeVal, 2, 1, 1, 1)
        self.hlShotNode.addLayout(self.glShotInfo)
        self.gridLayout_2.addLayout(self.hlShotNode, 2, 0, 1, 1)
        self.line = QtGui.QFrame(shotNode)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 1)
        self.line_2 = QtGui.QFrame(shotNode)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 0, 0, 1, 1)

        self.retranslateUi(shotNode)
        QtCore.QMetaObject.connectSlotsByName(shotNode)

    def retranslateUi(self, shotNode):
        shotNode.setWindowTitle(_translate("shotNode", "Shot Node", None))
        self.lPreview.setText(_translate("shotNode", "Preview", None))
        self.lLabel.setText(_translate("shotNode", "Label", None))
        self.lLabelVal.setText(_translate("shotNode", "TextLabel", None))
        self.lName.setText(_translate("shotNode", "Name", None))
        self.lNameVal.setText(_translate("shotNode", "TextLabel", None))
        self.lType.setText(_translate("shotNode", "Type", None))
        self.lTypeVal.setText(_translate("shotNode", "TextLabel", None))

