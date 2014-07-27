import os
from PyQt4 import QtGui
from appli import grapher
from lib.qt.scripts import procQt as pQt
from lib.system.scripts import procFile as pFile


class Menu(object):
    """ Class used by the grapherUi to launch commands
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher

    #===================================== MENU FILE =========================================#

    def on_newGraph(self):
        """ Command launched when miNewGraph is clicked """
        mess = "Are you sure you want to close current Graph ?"
        self.newDialog = pQt.ConfirmDialog(mess, ["Yes"], [self.newGraph])
        self.newDialog.exec_()

    def newGraph(self):
        """ Close current graph and reset all params """
        print "\n[grapherUI] : #-- New Graph --#"
        self.newDialog.close()
        if self.mainUi.lockFile is not None and not self.mainUi._lock:
            if os.path.exists(self.mainUi.lockFile):
                self.mainUi.removeLockFile(self.mainUi.lockFile)
        self.grapher.reset()
        self.mainUi.resetUi()

    def on_openGraph(self):
        """ Command launched when miOpenGraph is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            rootDir = grapher.rootDir
        else:
            rootDir = self.grapher._path
        self.fdOpen = pQt.fileDialog(fdMode='open', fdFileMode='ExistingFile', fdRoot=rootDir,
                                     fdFilters=['gp_*.py'], fdCmd=self.openGraph)
        self.fdOpen.exec_()

    def openGraph(self, graph=None):
        """ Open selected graph
            @param graph: (str) : Graph absolut path """
        #-- Get Graph Path --#
        if graph is None:
            try:
                selPath = self.fdOpen.selectedFiles()
                self.fdOpen.close()
            except:
                selPath = None
        else:
            selPath = [graph]
        #-- Open Graph --#
        if selPath:
            print "\n[grapherUI] : #-- Open Graph --#"
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                self.grapher.loadGraph(fileName)
                self.mainUi.checkLockFile()
            else:
                self.mainUi._fileErrorDialog(fileName, self.fdOpen)

    def openAbort(self):
        """ Cancel graph opening """
        self.mainUi.lockDialog.close()
        self.grapher.reset()

    def openReadOnly(self):
        """ Open graph in read only """
        print "\tOpen graph in read only..."
        self.mainUi.lockDialog.close()
        self.mainUi._lock = True
        if self.mainUi.lockFile is not None:
            lockParams = pFile.readPyFile(self.mainUi.lockFile)
            if grapher.user == lockParams['user']:
                self.mainUi.removeLockFile(self.mainUi.lockFile)
        self.mainUi.updateUi()

    def breakLock(self):
        """ Break lock and open graph """
        self.mainUi.lockDialog.close()
        self.mainUi.removeLockFile(self.mainUi.lockFile)
        self.mainUi._lock = False
        self.mainUi.createLockFile(self.mainUi.lockFile)
        self.mainUi.updateUi()

    def on_saveGraph(self):
        """ Command launched when miSaveGraph is clicked """
        if self.grapher._path is None or self.grapher._file is None:
            self.on_saveGraphAs()
        else:
            if not self.mainUi._lock:
                print "\n[grapherUI] : #-- Save Graph --#"
                self.grapher.ud_commentFromUi(self.mainUi)
                self.grapher.ud_variablesFromUi(self.mainUi)
                self.grapher.ud_graphTreeFromUi(self.mainUi)
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
        self.fdSaveAs = pQt.fileDialog(fdMode='save', fdFileMode='AnyFile', fdRoot=rootDir,
                                       fdFilters=['gp_*.py'], fdCmd=self.saveGraphAs)
        self.fdSaveAs.exec_()

    def saveGraphAs(self):
        """ Save grapher2 as selected fileName """
        print "\n[grapherUI] : #-- Save Graph As --#"
        selPath = self.fdSaveAs.selectedFiles()
        if selPath:
            fileName = str(selPath[0])
            if fileName.endswith('.py'):
                #-- Get LockFiles --#
                futurLockFile = fileName.replace('gp_', 'gpLock_')
                if os.path.exists(futurLockFile):
                    self.mainUi._fileLockErrorDialog(fileName, futurLockFile, self.fdSaveAs)
                else:
                    self.fdSaveAs.close()
                    #-- Remove Current LockFile --#
                    if not self.mainUi._lock:
                        if self.mainUi.lockFile is not None:
                            self.mainUi.removeLockFile(self.mainUi.lockFile)
                    #-- Save Graph --#
                    self.grapher._path = os.path.dirname(fileName)
                    self.grapher._file = os.path.basename(fileName)
                    self.grapher._absPath = fileName
                    self.grapher.ud_commentFromUi(self.mainUi)
                    self.grapher.ud_variablesFromUi(self.mainUi)
                    self.grapher.ud_graphTreeFromUi(self.mainUi)
                    self.grapher.writeToFile()
                    self.mainUi.setWindowTitle("Grapher - %s" % self.grapher._file)
                    self.mainUi.createLockFile(self.mainUi.lockFile)
                    self.mainUi._lock = False
                    self.mainUi.wgGraph.rf_graphBgc()
            else:
                self.mainUi._fileErrorDialog(fileName, self.fdSaveAs)

    def on_quitGrapher(self):
        """ Command launched when miQuitGraph is clicked """
        mess = "Are you sure you want to close Grapher ?"
        self.quitDialog = pQt.ConfirmDialog(mess, ["Close"], [self.quitGrapher])
        self.quitDialog.exec_()

    def quitGrapher(self):
        """ Ask confirmaton before closing """
        print "\n[grapherUI] : #-- Exit Grapher --#"
        if not self.mainUi._lock and self.mainUi.lockFile is not None:
            if os.path.exists(self.mainUi.lockFile):
                self.mainUi.removeLockFile(self.mainUi.lockFile)
        self.quitDialog.close()
        self.mainUi.close()

    #===================================== MENU WINDOW ========================================#

    def on_nodeEditor(self):
        """ Command launched when miNodeEditor is clicked """
        self.mainUi.nodeEditor.rf_nodeEditorVis()

    def on_xTerm(self):
        """ Command launched when miXterm is clicked """
        if self.grapher._path is None:
            os.system('start %s' % self.mainUi.xtermLauncher())
        else:
            os.system('start %s /K "cd /d %s"' % (self.mainUi.xtermLauncher(),
                                                  os.path.normpath(self.grapher._path)))

    def on_xPlorer(self):
        """ Command launched when miXplorer is clicked """
        if self.grapher._path is None:
            os.system('start %s' % os.path.normpath(grapher.rootDir))
        else:
            os.system('start %s' % os.path.normpath(self.grapher._path))

    def on_execGraph(self):
        """ Command launched when miExecGraph is clicked """
        print "\n[grapherUI] : #-- Execute Graph --#"
        self.grapher.ud_commentFromUi(self.mainUi)
        self.grapher.ud_variablesFromUi(self.mainUi)
        self.grapher.ud_graphTreeFromUi(self.mainUi)
        self.grapher.execGraph()

    #====================================== MENU HELP =========================================#

    def on_grapherRepr(self):
        """ Command launched when miGrapherRepr is clicked """
        print self.grapher.__repr2__()

    def on_grapherStr(self):
        """ Command launched when miGrapherStr is clicked """
        print self.grapher.__str__()

    def on_grapherUiStr(self):
        """ Command launched when miGrapherUiStr is clicked """
        print self.mainUi.__str__()
