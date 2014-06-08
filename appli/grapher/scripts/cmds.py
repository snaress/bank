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

    def on_saveGraphAs(self):
        """ Command launched when miSaveGraphAs is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            rootDir = os.path.join('G:', os.sep)
        else:
            rootDir = self.grapher._path
        self.fdSaveAs = dialog.fileDialog(fdRoot=rootDir, fdCmd=self.saveGraphAs)
        self.fdSaveAs.setFileMode(QtGui.QFileDialog.AnyFile)
        self.fdSaveAs.show()

    def saveGraphAs(self):
        """ Save grapher as selected fileName
            @return: (str) : Selected fileName """
        selPath = self.fdSaveAs.selectedFiles()
        if selPath:
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                self.fdSaveAs.close()
                self.grapher._path = os.path.dirname(fileName)
                self.grapher._file = os.path.basename(fileName)
                self.grapher._absPath = fileName
                self.grapher.writeToFile()
                return fileName
            else:
                warn = ["!!! Warning: FileName not valide !!!", "Should have path/file.py",
                        "Got %s" % fileName]
                errorDial = QtGui.QErrorMessage(self.fdSaveAs)
                errorDial.showMessage('\n'.join(warn))
                return False

    #===================================== MENU TOOL =========================================#

    def on_nodeEditor(self):
        """ Command launched when miNodeEditor is clicked """
        self.mainUi.rf_shared.rf_nodeEditorVis()

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


class TextEditor(object):
    
    def __init__(self, ui, textEditor):
        self.ui = ui
        self.grapher = self.ui.grapher
        self.textEditor = textEditor
