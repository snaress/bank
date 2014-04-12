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

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)
        self.miToolTips.triggered.connect(self.on_toolTips)
        self.bNoise.clicked.connect(self.noiseCurve)

    def noiseCurve(self):
        """ Command launch when bNoise is clicked """
        curves = self.cmds.getSelAnimCurves()
        curveInfo = self.cmds.getCurveInfo(curves)
        randSeq = self.cmds.getRandomSeq(**self.getNoiseParams)
        newCurves = self.cmds.createCurves(curveInfo, randSeq)
        self.cmds.applyOnCurves(newCurves)

    @property
    def getNoiseParams(self):
        """ Get noise params from ui
            @return: (dict) : Noise params """
        params = {}
        if self.cbRandom.isChecked():
            params['noiseType'] = 'random'
        elif self.cbSinRandom.isChecked():
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
        toolTipDict['cbRandom'] = "Uniform random"
        toolTipDict['cbSinRandom'] = "Sinusoidal random"
        return toolTipDict


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = NoiseAnimCurveUi()
    window.show()
    sys.exit(app.exec_())