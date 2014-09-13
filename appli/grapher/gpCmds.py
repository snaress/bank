import os
from PyQt4 import QtGui
from appli import grapher
from functools import partial
from lib.qt import procQt as pQt
from appli.grapher import gpWidget
from lib.system import procFile as pFile


class Menu(object):
    """ Class used by the grapherUi to launch commands
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.menuStorage = self.mainUi.menuStorage

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

    #====================================== MENU LIB ==========================================#

    def rf_studioMenu(self):
        """ refresh studio menuItem """
        self.mainUi.menuStudio.clear()
        studioPath = os.path.join(grapher.binPath, 'studio')
        miAddCat = self.mainUi.menuStudio.addAction("Add Category")
        miAddCat.triggered.connect(partial(self.on_addCategory, 'studio', studioPath))
        self.menuStorage['studio']['newCat'] = miAddCat
        self.mainUi.menuStudio.addSeparator()
        self._addCategory(studioPath, self.mainUi.menuStudio, 'studio')

    def rf_prodMenu(self):
        """ refresh project menuItem """
        self.mainUi.menuProd.clear()
        #-- Default Prod Action --#
        prodPath = os.path.join(grapher.binPath, 'prod')
        self.mainUi.miAddProject = self.mainUi.menuProd.addAction("Add Project")
        self.mainUi.miAddProject.triggered.connect(self.on_addProject)
        self.mainUi.menuProd.addSeparator()
        #-- Populate Prod --#
        prods = os.listdir(prodPath) or []
        for prod in prods:
            catPath = os.path.join(prodPath, prod)
            if os.path.isdir(catPath):
                newProdMenu = self._addSubMenu(prod, self.mainUi.menuProd)
                self.menuStorage['prod'][prod] = newProdMenu
                #-- Default Category Action --#
                miAddCat = newProdMenu.addAction("Add Category")
                miAddCat.triggered.connect(partial(self.on_addCategory, prod, catPath))
                self.menuStorage['prod']['%s/%s' % (prod, 'newCat')] = miAddCat
                newProdMenu.addSeparator()
                self._addCategory(catPath, newProdMenu, 'prod', rootKey=prod)

    def rf_usersMenu(self):
        """ refresh users menuItem """
        self.mainUi.menuUsers.clear()
        #-- Populate User Menu --#
        self.mainUi.menuUser = self.mainUi.menuUsers.addMenu(grapher.user)
        self.mainUi.menuUser.setTearOffEnabled(True)
        userPath = os.path.join(self.grapher.userBinPath, 'lib')
        miAddCat = self.mainUi.menuUser.addAction("Add Category")
        miAddCat.triggered.connect(partial(self.on_addCategory, grapher.user, userPath))
        self.mainUi.menuUser.addSeparator()
        self._addCategory(userPath, self.mainUi.menuUser, 'users')
        #-- Populate All Users Menu --#
        self.mainUi.menuUsers.addSeparator()
        rootPath = os.path.join(grapher.binPath, 'users')
        roots = os.listdir(rootPath) or []
        for root in roots:
            userPath = os.path.join(rootPath, root)
            if os.path.isdir(userPath):
                newRootMenu = self._addSubMenu(root, self.mainUi.menuUsers)
                self.menuStorage['users'][root] = newRootMenu
                users = os.listdir(userPath) or []
                for user in users:
                    catPath = os.path.join(userPath, user, 'lib')
                    if os.path.isdir(catPath):
                        newUserMenu = self._addSubMenu(user, newRootMenu)
                        self.menuStorage['users']['%s/%s' % (root, user)] = newUserMenu
                        miAddUserCat = newUserMenu.addAction("Add Category")
                        miAddUserCat.triggered.connect(partial(self.on_addCategory, user, catPath))
                        self.menuStorage['users']['%s/%s' % (root, user)] = newUserMenu
                        newUserMenu.addSeparator()
                        self._addCategory(catPath, newUserMenu, 'users', rootKey='%s/%s' % (root, user))

    def _addCategory(self, catPath, _parent, libType, rootKey=None):
        """ Add category and libType items
            @param catPath: (str) : Category root path
            @param _parent: (object) : Parent QMenu
            @param libType: (str) : 'studio', 'prod' or 'users'
            @param rootKey: (str) : Item storage key """
        cats = os.listdir(catPath) or []
        for cat in cats:
            libPath = os.path.join(catPath, cat)
            if os.path.isdir(libPath):
                newCatMenu = self._addSubMenu(cat, _parent)
                if rootKey is None:
                    self.menuStorage[libType][cat] = newCatMenu
                else:
                    self.menuStorage[libType]['%s/%s' % (rootKey, cat)] = newCatMenu
                #-- Populate Lib Type --#
                libs = os.listdir(libPath) or []
                for lib in libs:
                    newLibMenu = self._addSubMenu(lib, newCatMenu)
                    if rootKey is None:
                        self.menuStorage[libType]['%s/%s' % (cat, lib)] = newLibMenu
                    else:
                        self.menuStorage[libType]['%s/%s/%s' % (rootKey, cat, lib)] = newLibMenu
                    #-- Populate Files --#
                    filePath = os.path.join(libPath, lib)
                    files = os.listdir(filePath)
                    for f in files:
                        libFile = os.path.join(filePath, f)
                        miLibAction = newLibMenu.addAction(f.replace('.py', ''))
                        miLibAction.triggered.connect(partial(self.on_libFile, libFile, lib))
                        if rootKey is None:
                            self.menuStorage[libType]['%s/%s/%s' % (cat, lib, f)] = miLibAction
                        else:
                            self.menuStorage[libType]['%s/%s/%s/%s' % (rootKey, cat, lib, f)] = miLibAction

    def _addSubMenu(self, prod, _parent):
        """ Add project menu
            @param prod: (str) : Project name
            @param _parent: (object) : Parent QMenu
            @return: (object) : QMenu """
        newProdMenu = QtGui.QMenu(prod)
        newProdMenu.setTearOffEnabled(True)
        _parent.addMenu(newProdMenu)
        return newProdMenu

    def on_addProject(self):
        """ Command launch when 'lib/prod/addProject' is clicked """
        message = "Enter New Project Name"
        self.addProjectDialog = pQt.PromptDialog(message, self.addProject)
        self.addProjectDialog.exec_()

    def addProject(self):
        """ Add given project to lib """
        result = self.addProjectDialog.result()['result_1']
        prodPath = os.path.join(grapher.binPath, 'prod')
        prods = os.listdir(prodPath) or []
        if result in prods:
            mess = "!!! Error: Project %s already exists !!!" % result
            self.mainUi._defaultErrorDialog(mess, self.addProjectDialog)
        else:
            newProdPath = os.path.join(prodPath, result)
            print "[grapherUI] : Add project %s" % newProdPath
            os.mkdir(newProdPath)
            self.addProjectDialog.close()

    def on_addCategory(self, parentFld, catPath):
        """ Command launch when 'lib/prod/addProject/addCategory' is clicked
            @param parentFld: (str) : Parent fodler name
            @param catPath: (str) : Category root path """
        message = "Enter new category name for %s" % parentFld
        self.addCatDialog = pQt.PromptDialog(message, partial(self.addCategory, catPath))
        self.addCatDialog.exec_()

    def addCategory(self, catPath):
        """ Add given category to lib
            @param catPath: (str) : Category root path """
        result = self.addCatDialog.result()['result_1']
        cats = os.listdir(catPath) or []
        if result in cats:
            mess = "!!! Error: Category %s already exists !!!" % result
            self.mainUi._defaultErrorDialog(mess, self.addCatDialog)
        else:
            newCatPath = os.path.join(catPath, result)
            print "[grapherUI] : Add category %s" % newCatPath
            os.mkdir(newCatPath)
            for libType in ['script', 'node', 'branch']:
                print "[grapherUI] : Add libType %s" % libType
                os.mkdir(os.path.join(newCatPath, libType))
            self.addCatDialog.close()

    def on_libFile(self, libFile, libType):
        """ Command launch when a libFile is clicked
            @param libFile: (str) : File absolut path
            @param libType: (str) : 'script' or 'node' or 'branch' """
        selItems = self.mainUi.wgGraph.selectedItems()
        if libType == 'script':
            script = pFile.readFile(libFile)
            self.scriptPopUp = gpWidget.ScriptEditor(self.mainUi)
            self.scriptPopUp._widget.setText(''.join(script))
            self.scriptPopUp.show()
        elif libType == 'node':
            nodesDict = pFile.readPyFile(libFile)
            self.mainUi.wgGraph._pasteNode(nodesDict, selItems)
        elif libType == 'branch':
            nodesDict = pFile.readPyFile(libFile)
            self.mainUi.wgGraph._pasteBranch(nodesDict, selItems)

    #===================================== MENU WINDOW ========================================#

    def on_nodeEditor(self):
        """ Command launched when miNodeEditor is clicked """
        self.mainUi.nodeEditor.rf_nodeEditorVis()

    def on_libEditor(self):
        """ Command launch when 'editLib' is clicked """
        self.libEditor = gpWidget.LibEditor(self.mainUi)
        self.libEditor.show()

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
        print self.grapher.__getDict__()

    def on_grapherStr(self):
        """ Command launched when miGrapherStr is clicked """
        print self.grapher.__getStr__()

    def on_grapherUiStr(self):
        """ Command launched when miGrapherUiStr is clicked """
        print self.mainUi.__getStr__()
