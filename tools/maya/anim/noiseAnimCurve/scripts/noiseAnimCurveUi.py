import sys
from PyQt4 import QtGui, uic
from tools.maya.anim import noiseAnimCurve


noiseAnimCurveClass, noiseAnimCurveUiClass = uic.loadUiType(noiseAnimCurve.uiList['noiseAnimCurve'])
class NoiseAnimCurveUi(noiseAnimCurveClass, noiseAnimCurveUiClass):
    """ Class containing all noiseAnimCurve's Ui actions """

    def __init__(self):
        print "##### Launching NoiseAnimCurve Ui #####"
        super(NoiseAnimCurveUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """ Setup main window """
        self.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = NoiseAnimCurveUi()
    window.show()
    sys.exit(app.exec_())