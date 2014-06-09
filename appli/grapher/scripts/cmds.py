import os
from PyQt4 import QtGui
from lib.qt.scripts import dialog


class Menu(object):
    """ Class used by the grapherUi to launch commands
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher

    #===================================== MENU FILE =========================================#

    def on_openGraph(self):
        """ Command launched when miOpenGraph is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            rootDir = os.path.join('G:', os.sep)
        else:
            rootDir = self.grapher._path
        self.fdOpen = dialog.fileDialog(fdMode='open', fdFileMode='ExistingFile', fdRoot=rootDir,
                                        fdFilters=['*.py'], fdCmd=self.openGraph)
        self.fdOpen.show()

    def openGraph(self):
        """ Open selected graph """
        selPath = self.fdOpen.selectedFiles()
        if selPath:
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                self.fdOpen.close()
                self.grapher._lock = True
                self.grapher.loadGraph(fileName)
                self.mainUi.updateUi()
            else:
                self._fileErrorDialog(fileName, self.fdOpen)

    def on_saveGraph(self):
        """ Command launched when miSaveGraph is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            self.on_saveGraphAs()
        else:
            self.grapher.writeToFile()

    def on_saveGraphAs(self):
        """ Command launched when miSaveGraphAs is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            rootDir = os.path.join('G:', os.sep)
        else:
            rootDir = self.grapher._path
        self.fdSaveAs = dialog.fileDialog(fdMode='save', fdFileMode='AnyFile', fdRoot=rootDir,
                                          fdFilters=['*.py'], fdCmd=self.saveGraphAs)
        self.fdSaveAs.show()

    def saveGraphAs(self):
        """ Save grapher as selected fileName """
        selPath = self.fdSaveAs.selectedFiles()
        if selPath:
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                self.fdSaveAs.close()
                self.grapher._path = os.path.dirname(fileName)
                self.grapher._file = os.path.basename(fileName)
                self.grapher._absPath = fileName
                self.grapher.writeToFile()
            else:
                self._fileErrorDialog(fileName, self.fdSaveAs)

    def _fileErrorDialog(self, fileName, parent):
        """ Launch error dialog
            @param fileName: (str) : Grapher absolut path
            @param parent: (object) : Parent ui """
        warn = ["!!! Warning: FileName not valide !!!", "Should have path/file.py",
                "Got %s" % fileName]
        errorDial = QtGui.QErrorMessage(parent)
        errorDial.showMessage('\n'.join(warn))

    #===================================== MENU TOOL =========================================#

    def on_nodeEditor(self):
        """ Command launched when miNodeEditor is clicked """
        self.mainUi.rf_mainUi.rf_nodeEditorVis()

    #===================================== MENU HELP =========================================#

    def on_grapherRepr(self):
        """ Command launched when miGrapherRepr is clicked """
        print self.grapher.__repr__()

    def on_grapherStr(self):
        """ Command launched when miGrapherStr is clicked """
        print self.grapher.__str__()

    def on_grapherDict(self):
        """ Command launched when miGrapherDict is clicked """
        print self.grapher.__dict__
