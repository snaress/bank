# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\bank\appli\prodManager\ui\wgtLtShotNode.ui'
#
# Created: Sun Oct 05 16:54:14 2014
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

class Ui_LineTestShot(object):
    def setupUi(self, LineTestShot):
        LineTestShot.setObjectName(_fromUtf8("LineTestShot"))
        LineTestShot.resize(190, 48)
        self.gridLayout = QtGui.QGridLayout(LineTestShot)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lPreview = QtGui.QLabel(LineTestShot)
        self.lPreview.setScaledContents(True)
        self.lPreview.setAlignment(QtCore.Qt.AlignCenter)
        self.lPreview.setObjectName(_fromUtf8("lPreview"))
        self.gridLayout.addWidget(self.lPreview, 0, 0, 1, 1)
        self.bShotName = QtGui.QPushButton(LineTestShot)
        self.bShotName.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.bShotName.setFont(font)
        self.bShotName.setFlat(True)
        self.bShotName.setObjectName(_fromUtf8("bShotName"))
        self.gridLayout.addWidget(self.bShotName, 1, 0, 1, 1)
        self.pbShot = QtGui.QProgressBar(LineTestShot)
        self.pbShot.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pbShot.setFont(font)
        self.pbShot.setProperty("value", 24)
        self.pbShot.setAlignment(QtCore.Qt.AlignCenter)
        self.pbShot.setObjectName(_fromUtf8("pbShot"))
        self.gridLayout.addWidget(self.pbShot, 2, 0, 1, 1)

        self.retranslateUi(LineTestShot)
        QtCore.QMetaObject.connectSlotsByName(LineTestShot)

    def retranslateUi(self, LineTestShot):
        LineTestShot.setWindowTitle(_translate("LineTestShot", "Linetest Shot", None))
        self.lPreview.setText(_translate("LineTestShot", "Shot Preview", None))
        self.bShotName.setText(_translate("LineTestShot", "ShotNode Name", None))

