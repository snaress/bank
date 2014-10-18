import os, sys, subprocess
from lib import qt
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
if __name__ == '__main__':
    pQt.CompileUi(uiFile=qt.uiList['preview'])
from lib.qt.ui import previewUI


class Preview(QtGui.QWidget, previewUI.Ui_preview):
    """ Preview widget
        @param widgetSize: (int, int) : Widget size width and height
        @param previewSize: (int, int) : Preview icon size width and height """

    noImage = os.path.join(qt.libPath, 'ima', 'noImage_500.jpg')
    djvView = os.path.normpath("C:/Program Files/djv-1.0.2-Windows-64/bin/djv_view.exe")
    djvInfo = os.path.normpath("C:/Program Files/djv-1.0.2-Windows-64/bin/djv_info.exe")

    def __init__(self, widgetSize=(200, 200), previewSize=(200, 200)):
        super(Preview, self).__init__()
        self._widgetSize = widgetSize
        self._previewSize = previewSize
        self._previewFile = None
        self.imagePath = None
        self.sequencePath = None
        self.moviePath = None
        self.xplorerPath = None
        self.xtermPath = None
        self.graphPath = None
        self._setupUi()

    @property
    def widgetSize(self):
        return self._widgetSize

    @widgetSize.setter
    def widgetSize(self, value):
        self._widgetSize = value

    @property
    def previewSize(self):
        return self._previewSize

    @previewSize.setter
    def previewSize(self, value):
        self._previewSize = value

    @property
    def previewFile(self):
        return self._previewFile

    @previewFile.setter
    def previewFile(self, value):
        self._previewFile = value

    def _setupUi(self):
        """ Setup ui """
        self.setupUi(self)
        self.bImage.clicked.connect(self.on_image)
        self.bSequence.clicked.connect(self.on_sequence)
        self.bMovie.clicked.connect(self.on_movie)
        self.bExplorer.clicked.connect(self.on_explorer)
        self.bXterm.clicked.connect(self.on_xTerm)
        self.bGrapher.clicked.connect(self.on_grapher)
        self.rf_widgetSize()
        self.rf_previewSize()
        self.rf_preview()

    def rf_widgetSize(self):
        """ Refresh widget size """
        self.bPreview.setMinimumSize(QtCore.QSize(self.widgetSize[0], self.widgetSize[1]))
        self.bPreview.setMaximumSize(QtCore.QSize(self.widgetSize[0], self.widgetSize[1]))
        self.qfButtonsUp.setMinimumWidth(self.widgetSize[0])
        self.qfButtonsUp.setMaximumWidth(self.widgetSize[0])
        self.qfButtonsDn.setMinimumWidth(self.widgetSize[0])
        self.qfButtonsDn.setMaximumWidth(self.widgetSize[0])

    def rf_previewSize(self):
        """ Refresh preview icon size """
        self.bPreview.setIconSize(QtCore.QSize(self.previewSize[0], self.previewSize[1]))

    def rf_preview(self):
        """ Refresh preview icon """
        self._checkIma()
        self.bPreview.setIcon(QtGui.QIcon(self._previewFile))

    def rf_btnsVisibility(self):
        """ Refresh Preview buttons visibility """
        if self.qfButtonsUp.isVisible():
            self._setBtnVis(self.imagePath, self.bImage)
            self._setBtnVis(self.sequencePath, self.bSequence)
            self._setBtnVis(self.moviePath, self.bMovie)
        if self.qfButtonsDn.isVisible():
            self._setBtnVis(self.xplorerPath, self.bExplorer)
            self._setBtnVis(self.xtermPath, self.bXterm)
            self._setBtnVis(self.graphPath, self.bGrapher)

    def on_image(self):
        """ Command launched when 'Image' QPushButton is clicked """
        proc = subprocess.Popen([self.djvView, os.path.normcase(self.imagePath)])
        proc.poll()

    def on_sequence(self):
        """ Command launched when 'Sequence' QPushButton is clicked """
        pass

    def on_movie(self):
        """ Command launched when 'Movie' QPushButton is clicked """
        pass

    def on_explorer(self):
        """ Command launched when 'Explorer' QPushButton is clicked """
        os.system('explorer "%s"' % os.path.normpath(self.xplorerPath))

    def on_xTerm(self):
        """ Command launched when 'Xterm' QPushButton is clicked """
        os.system('start "Toto" /d "%s"' % os.path.normpath(self.xtermPath))

    def on_grapher(self):
        """ Command launched when 'Grapher' QPushButton is clicked """
        pass

    def _checkIma(self):
        """ Check current preview imaFile """
        if self.previewFile is None or self.previewFile == '' or self.previewFile == ' ':
            self.previewFile = self.noImage

    @staticmethod
    def _setBtnVis(path, btn):
        """ Set given QPushButton visibility
            @param path: (str) : Absolut path
            @param btn: (object) : QPushButton """
        if path is None or path == '' or path == ' ':
            btn.setEnabled(False)
        else:
            if os.path.exists(path):
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Preview()
    window.show()
    sys.exit(app.exec_())