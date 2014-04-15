import sys
from PyQt4 import QtGui, uic, QtCore
from lib.qt.scripts import procQt as pQt
from tools.maya.anim import noiseAnimCurve
from tools.maya.anim.noiseAnimCurve.scripts import cmds as tmCmds


noiseAnimCurveClass, noiseAnimCurveUiClass = uic.loadUiType(noiseAnimCurve.uiList['noiseAnimCurve'])
class NoiseAnimCurveUi(noiseAnimCurveClass, noiseAnimCurveUiClass):
    """ Class containing all noiseAnimCurve's Ui actions """

    def __init__(self):
        print "##### Launching NoiseAnimCurve Ui #####"
        self.cmds = tmCmds
        super(NoiseAnimCurveUi, self).__init__()
        self._setupUi()
        self.rf_methodUi()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)
        self.miToolTips.triggered.connect(self.on_toolTips)
        self.cbAdvancedMethod.clicked.connect(self.rf_methodUi)
        self.bNoiseSimple.clicked.connect(self.noiseCurveSimple)
        self.pop_twCurvesMenu()

    def rf_methodUi(self):
        """ Refresh Ui method """
        state = self.cbAdvancedMethod.isChecked()
        self.bNoiseSimple.setVisible(not state)
        self.twCurves.setVisible(state)
        if state:
            self.setGeometry(self.pos().x()+8, self.pos().y()+30, 600, self.height())
        else:
            self.setGeometry(self.pos().x()+8, self.pos().y()+30, 300, self.height())

    def noiseCurveSimple(self):
        """ Command launch when bNoise is clicked """
        curves = self.cmds.getSelAnimCurves()
        curveInfo = self.cmds.getCurveInfo(curves)
        randSeq = self.cmds.getRandomSeq(**self.getNoiseParams)
        newCurves = self.cmds.getNewCurves(curveInfo, randSeq)
        self.cmds.applyOnCurves(newCurves)

    def pop_twCurvesMenu(self):
        """ Curve listing popUp menu """
        self.tbCurves = QtGui.QToolBar()
        self.miListNacCurves =  self.tbCurves.addAction("List NAC Curves", self.on_listNacCurves)
        self.miAddSelCurves = self.tbCurves.addAction("Add Selected Curves", self.on_addSelCurves)
        self.miConvertToChoice = self.tbCurves.addAction("Convert To Choice", self.on_convertToChoice)
        self.miConvertToBlend = self.tbCurves.addAction("Convert To Blend")
        self.miNewNacCurve = self.tbCurves.addAction("New Curve", self.on_newNacCurve)
        self.twCurves.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.twCurves,
                     QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_popCurvesMenu)
        self.pmCurves = QtGui.QMenu(self)
        self.pmCurves.addAction(self.miListNacCurves)
        self.pmCurves.addAction(self.miAddSelCurves)
        self.pmCurves.addSeparator()
        self.pmCurves.addAction(self.miConvertToChoice)
        self.pmCurves.addAction(self.miConvertToBlend)
        self.pmCurves.addSeparator()
        self.pmCurves.addAction(self.miNewNacCurve)

    def on_popCurvesMenu(self, point):
        """ Curve listing popUp menu launcher """
        selItems = self.twCurves.selectedItems()
        self.miNewNacCurve.setEnabled(False)
        if selItems:
            if selItems[0].curveStatus == 'init':
                self.miConvertToChoice.setEnabled(True)
                self.miConvertToBlend.setEnabled(True)
            elif selItems[0].curveStatus == 'choice':
                self.miConvertToChoice.setEnabled(False)
                self.miConvertToBlend.setEnabled(True)
                self.miNewNacCurve.setText("New Choice Curve")
                self.miNewNacCurve.setEnabled(True)
            elif selItems[0].curveStatus == 'blend':
                self.miConvertToChoice.setEnabled(True)
                self.miConvertToBlend.setEnabled(False)
                self.miNewNacCurve.setText("New Blend Curve")
                self.miNewNacCurve.setEnabled(True)
        self.pmCurves.exec_(self.twCurves.mapToGlobal(point))

    def on_addSelCurves(self):
        """ Command launch when miAddSelCurves is clicked """
        items = self.newCurveItems(self.cmds.getSelAnimCurves())
        self.twCurves.addTopLevelItems(items)

    def on_listNacCurves(self):
        """ Command launch when miListNacCurves is clicked """
        self.twCurves.clear()
        items = self.newCurveItems(self.cmds.getNacCurves())
        self.twCurves.addTopLevelItems(items)

    def on_convertToChoice(self):
        """ Command launch when miConvertToChoice is clicked """
        selItems = self.twCurves.selectedItems()
        if selItems:
            if not selItems[0].curveStatus == 'choice':
                self.cmds.convertToChoice(selItems[0].curveName, selItems[0].curveStatus)
                selItems[0].setTextColor(0, QtGui.QColor(100, 100, 255))
            else:
                print "NAC Warning: %s is already in choice mode !!!"

    def on_newNacCurve(self):
        """ Command launch when miNewNacCurve is clicked """
        selItems = self.twCurves.selectedItems()
        if selItems:
            curve = selItems[0]

    def newCurveItems(self, curves):
        """ Create new curve item for given curves
            @param curves: (list) : Nac curves in scene
            @return: (list) : QTreeWidgetItem list """
        items = []
        allItems = pQt.getTopItems(self.twCurves)
        for curve in curves:
            check = True
            for treeItem in allItems:
                if str(treeItem.text(0)) == curve:
                    check = False
                    print "NAC: %s already in listing !!!" % curve
                    break
            if check:
                status = self.cmds.checkCurveStatus(curve)
                newItem = self.newItem(curveName=curve, status=status)
                items.append(newItem)
        return items

    @staticmethod
    def newItem(**kwargs):
        """ Create QTreeWidgetItem from given params
            @param kwargs: (dict) : New item params
            @return: (object) : New QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, kwargs['curveName'])
        newItem.curveName = kwargs['curveName']
        newItem.curveStatus = kwargs['status']
        if kwargs['status'] == 'init':
            newItem.setTextColor(0, QtGui.QColor(200, 200, 200))
        elif kwargs['status'] == 'choice':
            newItem.setTextColor(0, QtGui.QColor(125, 125, 255))
        return newItem

    @property
    def getNoiseParams(self):
        """ Get noise params from ui
            @return: (dict) : Noise params """
        params = {}
        if self.rbUniform.isChecked():
            params['randType'] = 'uniform'
        elif self.rbSinusoidal.isChecked():
            params['randType'] = 'sinusoidal'
        params['min'] = self.sbAmpMin.value()
        params['max'] = self.sbAmpMax.value()
        params['bias'] = self.gbBias.isChecked()
        params['biasMin'] = self.sbBiasMin.value()
        params['biasMax'] = self.sbBiasMax.value()
        params['octaves'] = self.sbOctaves.value()
        params['frequence'] = self.sbFreq.value()
        return params

    def on_toolTips(self):
        """ Command launch when help menu action 'Tool Tips' is triggered """
        for k, v in self.toolTips.iteritems():
            if self.miToolTips.isChecked():
                exec("self.%s.setToolTip(%r)" % (k, v))
            else:
                exec("self.%s.setToolTip('')" % k)

    @property
    def toolTips(self):
        """ Store tool tips in dict
            @return: (dict) : Tool tips str """
        toolTipDict = {}
        toolTipDict['cbAdvancedMethod'] = "Switch to 'simple'/'advanced' curve edition"
        toolTipDict['lNoiseType'] = "Noise type choice for random sequence creation"
        toolTipDict['rbUniform'] = "Uniform random"
        toolTipDict['rbSinusoidal'] = "Sinusoidal random"
        toolTipDict['lAmp'] = "New keys min and max value"
        toolTipDict['gbBias'] = "Activate amplitude bias"
        toolTipDict['lBiasMin'] = "Amplitude highest minimum value"
        toolTipDict['lBiasMax'] = "Amplitude lowest maximum value"
        toolTipDict['lOctaves'] = "Number of random value to create"
        toolTipDict['lFrequence'] = "Number of octaves repetition"
        return toolTipDict



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = NoiseAnimCurveUi()
    window.show()
    sys.exit(app.exec_())