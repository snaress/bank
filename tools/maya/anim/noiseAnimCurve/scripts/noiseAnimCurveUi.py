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
        self.bNoise.clicked.connect(self.noiseCurve)

    def noiseCurve(self):
        curves = self.cmds.getSelAnimCurves()
        curveInfo = self.cmds.getCurveInfo(curves)
        randSeq = self.cmds.createRandomSeq(**self.getNoiseParams)
        self.cmds.createCurves(curveInfo, randSeq)

    @property
    def getNoiseParams(self):
        params = {}
        params['min'] = self.sbAmpMin.value()
        params['max'] = self.sbAmpMax.value()
        params['frequence'] = self.sbFreq.value()
        params['octaves'] = self.sbOctaves.value()
        params['Mmin'] = self.sbMaxMin.value()
        params['mMax'] = self.sbMinMax.value()
        params['KeepKeys'] = self.cbKeepKeys.isChecked()
        return params


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = NoiseAnimCurveUi()
    window.show()
    sys.exit(app.exec_())