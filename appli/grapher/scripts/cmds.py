import os
from PyQt4 import QtGui
from appli import grapher
from functools import partial
from lib.qt.scripts import dialog2
from lib.system.scripts import procFile as pFile


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
            rootDir = grapher.rootDir
        else:
            rootDir = self.grapher._path
        self.fdOpen = dialog2.fileDialog(fdMode='open', fdFileMode='ExistingFile', fdRoot=rootDir,
                                        fdFilters=['gp_*.py'], fdCmd=self.openGraph)
        self.fdOpen.exec_()

    def openGraph(self, graph=None):
        """ Open selected graph """
        if graph is None:
            try:
                selPath = self.fdOpen.selectedFiles()
                self.fdOpen.close()
            except:
                selPath = None
        else:
            selPath = [graph]
        if selPath:
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                self.grapher.loadGraph(fileName)
                self.mainUi.checkLockFile()
            else:
                self._fileErrorDialog(fileName, self.fdOpen)

    def openAbort(self):
        """ Cancel graph opening """
        self.mainUi.lockDialog.close()
        self.grapher.reset()

    def openReadOnly(self):
        """ Open graph in read only """
        print "\tOpen graph in read only..."
        self.mainUi.lockDialog.close()
        self.mainUi._lock = True
        lockFile = self.mainUi.getLockFile()
        if lockFile is not None:
            lockParams = pFile.readPyFile(lockFile)
            if grapher.user == lockParams['user']:
                self.mainUi.removeLockFile(lockFile)
        self.mainUi.updateUi()

    def breakLock(self):
        """ Break lock and open graph """
        self.mainUi.lockDialog.close()
        self.mainUi.removeLockFile(self.mainUi.getLockFile())
        self.mainUi._lock = False
        self.mainUi.createLockFile(self.mainUi.getLockFile())
        self.mainUi.updateUi()

    def on_saveGraph(self):
        """ Command launched when miSaveGraph is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            self.on_saveGraphAs()
        else:
            if not self.mainUi._lock:
                self.grapher.writeToFile()
            else:
                warn = ["!!! Warning: Destination Graph Locked !!!", "Can't overwrite locked graph"]
                errorDial = QtGui.QErrorMessage(self.mainUi)
                errorDial.showMessage('\n'.join(warn))

    def on_saveGraphAs(self):
        """ Command launched when miSaveGraphAs is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            rootDir = grapher.rootDir
        else:
            rootDir = self.grapher._path
        self.fdSaveAs = dialog2.fileDialog(fdMode='save', fdFileMode='AnyFile', fdRoot=rootDir,
                                           fdFilters=['gp_*.py'], fdCmd=self.saveGraphAs)
        self.fdSaveAs.exec_()

    def saveGraphAs(self):
        """ Save grapher as selected fileName """
        print "\n#-- Saving Graph As --#"
        selPath = self.fdSaveAs.selectedFiles()
        if selPath:
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                futurLockFile = fileName.replace('gp_', 'gpLock_')
                currLockFile = self.mainUi.getLockFile()
                if os.path.exists(futurLockFile):
                    self._fileLockErrorDialog(fileName, futurLockFile, self.fdSaveAs)
                else:
                    if fileName == self.grapher._absPath and self.mainUi._lock:
                        warn = ["!!! Warning: Destination Graph Locked !!!",
                                "Can't overwrite locked graph"]
                        errorDial = QtGui.QErrorMessage(self.mainUi)
                        errorDial.showMessage('\n'.join(warn))
                    else:
                        self.fdSaveAs.close()
                        if not self.mainUi._lock:
                            if currLockFile is not None:
                                self.mainUi.removeLockFile(currLockFile)
                        self.grapher._path = os.path.dirname(fileName)
                        self.grapher._file = os.path.basename(fileName)
                        self.grapher._absPath = fileName
                        self.grapher.writeToFile()
                        self.mainUi.createLockFile(self.mainUi.getLockFile())
                        self.mainUi._lock = False
                        self.mainUi.rf_mainUi.rf_graphBgc()
            else:
                self._fileErrorDialog(fileName, self.fdSaveAs)

    def on_quitGrapher(self):
        """ Command launched when miQuitGraph is clicked """
        mess = "Save before closing ?"
        self.quitDialog = dialog2.ConfirmDialog(mess, ["Save", "Save As", "Don't Save"],
                          [partial(self.quitGrapher, option="Save"),
                           partial(self.quitGrapher, option="Save As"), self.quitGrapher])
        self.quitDialog.exec_()

    def quitGrapher(self, option="Don't Save"):
        """ Ask to save before closing
            @param option: (str) : "Save", "Save As" or "Don't Save" """
        if option == "Save":
            self.on_saveGraph()
        elif option == "Save As":
            self.on_saveGraphAs()
        # lockFile = self.mainUi.getLockFile()
        # if not self.mainUi._lock and lockFile is not None:
        #     if os.path.exists(lockFile):
        #         self.mainUi.removeLockFile(lockFile)
        # self.quitDialog.close()
        # self.mainUi.close()

    def _fileErrorDialog(self, fileName, parent):
        """ Launch fileDialog error message
            @param fileName: (str) : Grapher absolut path
            @param parent: (object) : Parent ui """
        warn = ["!!! Warning: FileName Not Valide !!!", "Should have path/file.py",
                "Got %s" % fileName]
        errorDial = QtGui.QErrorMessage(parent)
        errorDial.showMessage('\n'.join(warn))

    def _fileLockErrorDialog(self, fileName, lockFile, parent):
        """ Launch fileLockDialog error message
            @param fileName: (str) : Grapher absolut path
            @param lockFile: (str) : Lock file absolut path
            @param parent: (object) : Parent ui """
        lockParams = pFile.readPyFile(lockFile)
        warn = ["!!! WARNING: %s is already locked !!!" % os.path.basename(fileName),
                "Locked by %s on %s" % (lockParams['user'], lockParams['station']),
                "Date: %s" % lockParams['date'], "Time: %s" % lockParams['time'],
                "Unlock before saving or choose a different fileName."]
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
