import sys
from PyQt4 import QtGui, uic
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
        self.bNoiseSimple.clicked.connect(self.noiseCurve)

    def rf_methodUi(self):
        """ Refresh Ui method """
        state = self.cbAdvancedMethod.isChecked()
        self.qfNoiseSimple.setVisible(not state)
        self.twCurves.setVisible(state)
        if state:
            self.setGeometry(self.pos().x()+8, self.pos().y()+30, 600, self.height())
        else:
            self.setGeometry(self.pos().x()+8, self.pos().y()+30, 400, self.height())

    def noiseCurve(self):
        """ Command launch when bNoise is clicked """
        curves = self.cmds.getSelAnimCurves()
        curveInfo = self.cmds.getCurveInfo(curves)
        randSeq = None
        if self.rbRandom.isChecked():
            randSeq = self.cmds.getRandomSeq(**self.getNoiseParams)
        elif self.rbSinRandom.isChecked():
            randSeq = self.cmds.getSinRandomSeq(**self.getNoiseParams)
        newCurves = self.cmds.getNewCurves(curveInfo, randSeq)
        self.cmds.applyOnCurves(newCurves)

    @property
    def getNoiseParams(self):
        """ Get noise params from ui
            @return: (dict) : Noise params """
        params = {}
        if self.rbRandom.isChecked():
            params['noiseType'] = 'random'
        elif self.rbSinRandom.isChecked():
            params['noiseType'] = 'sinRandom'
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
        toolTipDict['lNoiseType'] = "Noise type choice for random sequence creation"
        toolTipDict['rbRandom'] = "Uniform random"
        toolTipDict['rbSinRandom'] = "Sinusoidal random"
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