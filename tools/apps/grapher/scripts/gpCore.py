import os
import time
from PyQt4 import QtGui, QtCore
from tools.apps import grapher
from lib.system.scripts import procFile as pFile


def createLockFile(fileName):
    """ Create lock file
        @param fileName: Lock file absolut path
        @type fileName: str """
    fullDate = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
    txt = ["user = %s" % grapher.user, "station = %s" % grapher.station, "date = %s" % fullDate]
    pFile.writeFile(fileName, '\n'.join(txt), add=False)

def removeLockFile(fileName):
    """ Remove lock file
        @param fileName: Lock file absolut path
        @type fileName: str """
    if fileName is not None:
        if os.path.exists(fileName):
            os.remove(fileName)

def xTerm(rootPath):
    """ Launch Xterm
        @param rootPath: Grapher root path
        @type rootPath: str """
    cmd = "C:\Windows\System32\cmd.exe"
    macroFile = os.path.join('C:', os.sep, 'Users', grapher.user, 'alias.txt')
    if rootPath is None:
        defaultPath = os.path.join('C:', os.sep, 'Users', grapher.user)
        os.system("start /d %s %s /k doskey /macrofile=%s" % (defaultPath, cmd, macroFile))
    else:
        os.system("start /d %s %s /k doskey /macrofile=%s" % (rootPath, cmd, macroFile))

def xPlorer(rootPath):
    """ Launch Explorer
        @param rootPath: Grapher root path
        @type rootPath: str """
    if rootPath is None:
        os.system("explorer")
    else:
        os.system("explorer %s" % rootPath)

def createLibFld():
    """ Create user folders in grapher lib """
    user = grapher.user
    usersPath = os.path.join(grapher.libPath, 'users')
    #-- User Path --#
    userPath = os.path.join(usersPath, user)
    if not os.path.exists(userPath):
        print "Create user lib folder %r in %s" % (user, usersPath)
        os.mkdir(userPath)
    #-- Tmp Path --#
    tmpPath = os.path.join(userPath, 'tmp')
    if not os.path.exists(tmpPath):
        print "Create user folder 'tmp' in", userPath
        os.mkdir(tmpPath)
    #-- Pref Path --#
    prefPath = os.path.join(userPath, 'pref')
    if not os.path.exists(prefPath):
        print "Create user folder 'pref' in", userPath
        os.mkdir(prefPath)

def createGrapherFld(mainUi):
    """ Create folders needed by Grapher
        @param mainUi: Main ui QObject (QMainWindow)
        @type mainUi: object """
    rootPath = mainUi.GP_DIRPATH
    #-- Tmp Path --#
    tmpPath = os.path.join(rootPath, 'tmp')
    if not os.path.exists(tmpPath):
        print "Create grapher 'tmp' folder in", rootPath
        os.mkdir(tmpPath)
    #-- Tmp GraphName Path --#
    tmpGraphPath = os.path.join(tmpPath, mainUi.GP_NAME)
    if not os.path.exists(tmpGraphPath):
        print "Create grapher 'tmpName' folder in", tmpPath
        os.mkdir(tmpGraphPath)
    #-- Tmp User Path --#
    tmpUserPath = os.path.join(tmpGraphPath, grapher.user)
    if not os.path.exists(tmpUserPath):
        print "Create grapher %r folder in %s" % (grapher.user, tmpPath)
        os.mkdir(tmpUserPath)
    #-- Script Path --#
    scriptPath = os.path.join(rootPath, 'scripts')
    if not os.path.exists(scriptPath):
        print "Create grapher 'scripts' path in", rootPath
        os.mkdir(scriptPath)
    #-- Script GraphName Path --#
    scriptGraphPath = os.path.join(scriptPath, mainUi.GP_NAME)
    if not os.path.exists(scriptGraphPath):
        print "Create grapher 'scriptName' folder in", scriptPath
        os.mkdir(scriptGraphPath)

def getAllItems(twTree):
    """ Get all QTreeWidgetItem of given QTreeWidget
        @param twTree: QTreeWidget object
        @type twTree: object
        @return: All QTreeWidgetItem list
        @rtype: list """
    items = []
    allItems = QtGui.QTreeWidgetItemIterator(twTree, QtGui.QTreeWidgetItemIterator.All) or None
    if allItems is not None:
        while allItems.value():
            item = allItems.value()
            items.append(item)
            allItems += 1
    return items


class GrapherStyle(object):

    @property
    def defaultWndGeometry(self):
        """ Get default main window geometry
            @return: MainWindow geometry (QtCore.QRect(int, int, int, int))
            @rtype: object """
        return QtCore.QRect(30, 30, 1000, 800)

    @property
    def defaultFrameBgc(self):
        """ Get default frame bg color
            @return: CCS color name
            @rtype: str """
        return "background-color:LightGrey;"

    @property
    def lockFrameBgc(self):
        """ Get lock frame bg color
            @return: CCS color name
            @rtype: str """
        return "background-color:Tomato;"

    @property
    def defaultVersionTitle(self):
        """ Get default version title
            @return: Default version title
            @rtype: str """
        return "New Version"

    @property
    def notesBgc(self):
        """ Get default note bg color
            @return: CCS color name
            @rtype: str """
        return "background-color:DarkGrey;"

    @property
    def defaultNotes(self):
        """ Get default notes
            @return: Notes line by line
            @rtype: list """
        return ['Add Notes :', '--------------']

    @staticmethod
    def varHeaderSize(twTree):
        """ Init variable Zone QTreeWidget headers
            @param twTree: Graph tree object (QTreeWidget)
            @type twTree: object """
        for n in range(twTree.columnCount()):
            if n == 0:
                twTree.setColumnWidth(n, 25)
            elif n == 1:
                twTree.setColumnWidth(n, 15)
            elif n == 2:
                twTree.setColumnWidth(n, 150)
            elif n == 3:
                twTree.setColumnWidth(n, 60)
            elif n == 4:
                twTree.setColumnWidth(n, 250)
            elif n == 5:
                twTree.setColumnWidth(n, 300)

    @property
    def remoteBgc(self):
        """ Get remote bg color
            @return: CCS color name
            @rtype: str """
        return "background-color:Tomato;"

    @property
    def loopBgc(self):
        """ Get loop bg color
            @return: CCS color name
            @rtype: str """
        return "background-color:Peru;"

    @staticmethod
    def scriptFont(scriptZone):
        """ Set script font and tabulation
            @param scriptZone: Script QTextEdit
            @type scriptZone: object """
        scriptFont = QtGui.QFont()
        scriptFont.setFamily('Courier')
        scriptFont.setStyleHint(QtGui.QFont.Monospace)
        scriptFont.setFixedPitch(True)
        scriptFont.setPointSize(10)
        metric = QtGui.QFontMetrics(scriptFont)
        scriptZone.setFont(scriptFont)
        scriptZone.setTabStopWidth(4*metric.width(' '))

    @property
    def trashBgc(self):
        """ get default trash bg color
            @return: CCS color name
            @rtype: str"""
        return "background-color:DarkGrey;"

    @property
    def defaultTrash(self):
        """ Get default trash
            @return: (list[str]) : Notes
            @rtype: list """
        return ['Trash Zone :', '---------------']

    @property
    def graphZoneBgc(self):
        """ Get graph zone bg color
            @return: CCS color name
            @rtype: str """
        return "background-color:Black;"

    @property
    def graphZoneColumns(self):
        """ get graph column number
            @return: Column number
            @rtype: int """
        return 30

    @staticmethod
    def graphHeaderSize(twTree):
        """ Init Graph Zone QTreeWidget headers
            @param twTree: Graph tree object (QTreeWidget)
            @type twTree: object """
        for n in range(0, twTree.columnCount(), 3):
            twTree.setColumnWidth(n, 15)
        for n in range(1, twTree.columnCount(), 3):
            twTree.header().setResizeMode(n, QtGui.QHeaderView.ResizeToContents)
        for n in range(2, twTree.columnCount(), 3):
            twTree.setColumnWidth(n, 15)

    @staticmethod
    def graphNodeBgc(nodeType):
        """ Get graph node color
            @param nodeType: New graph node type ('sysData', 'cmdData', 'purData', 'modul', 'loop')
            @type nodeType: str
            @return: CCS color name
            @rtype: str """
        if nodeType == 'modul':
            return "background-color:Silver;"
        elif nodeType == 'sysData':
            return "background-color:SkyBlue;"
        elif nodeType == 'cmdData':
            return "background-color:DodgerBlue;"
        elif nodeType == 'purData':
            return "background-color:MediumSeaGreen;"
        elif nodeType == 'loop':
            return "background-color:Peru;"


class Grapher(object):

    def __init__(self, **kwargs):
        """ @param kwargs: {'gp_GlobalNotes': [str()], 'gp_globalVar': [dict{}],
                            'gp_graphRootList': [str()], 'gp_graphNodeList': {dict{}}}
            @type kwargs: dict """
        for k, v in kwargs.iteritems():
            if k.startswith('gp_'):
                setattr(self, k, v)

    def readGraph(self, fileName):
        """ Read the given graphFile
            @param fileName: Graph file absolut path
            @type fileName: str
            @return: graph dict
            @rtype: dict """
        print "Reading file %s" % fileName
        params = {}
        execfile(fileName, params)
        for k, v in params.iteritems():
            if k.startswith('gp_'):
                setattr(self, k, v)
        return self.__dict__

    def writeGraph(self, fileName):
        """ Write graph to the given file
            @param fileName : Graph file absolut path
            @type fileName: str """
        print "Writing file %s" % fileName
        gpDict = self.__dict__
        f = open(fileName, 'w')
        for k, v in gpDict.iteritems():
            f.write("%s = %s\n" % (k, v))
        f.close()


class GrapherEnv(object):

    @property
    def grapherSysPath(self):
        """ Get grapher sysPath
            @return: Grapher sysPath
            @rtype: list """
        return [grapher.wsPath]

    @property
    def mayaEnv(self):
        """ Get Maya env
            @return: Maya env
            @rtype: dict """
        mayaPath = os.path.join('C:', os.sep, '\"Program Files\"', 'Autodesk', 'Maya2012')
        return {'maya': os.path.join(mayaPath, 'bin', 'maya.exe'),
                'mayaPy': os.path.join(mayaPath, 'bin', 'mayapy.exe'),
                'mayaBatch': os.path.join(mayaPath, 'bin', 'mayabatch.exe')}

    @property
    def grapherEnv(self):
        """ Get Grapher env
            @return: Grapher env
            @rtype: dict """
        grapherEnv = {}
        #-- Maya Env --#
        for k, v in self.mayaEnv.iteritems():
            grapherEnv[k] = v
        return grapherEnv


class GetGrapher(object):

    def __init__(self, mainUi):
        """ @param mainUi: Grapher ui object (QMainWindow)
            @type mainUi: object """
        self.mainUi = mainUi
        self.params = {}
        self._getGlobalNotes()
        self._getGlobalVar()
        self._getGraphZone()

    def _getGlobalNotes(self):
        """ Get Global Notes from ui """
        self.params['gp_globalNotes'] = str(self.mainUi.teGlobalNotes.toPlainText()).split('\n')

    def _getGlobalVar(self):
        """ Get Global Variables from ui """
        self.params['gp_globalVar'] = self.mainUi.twGlobalVar.varList

    def _getGraphZone(self):
        """ Get Graph Zone from ui """
        self.params['gp_graphRootList'] = self.mainUi.twGraph.rootList
        self.params['gp_graphNodeList'] = self.mainUi.twGraph.nodeList

    @staticmethod
    def varListToString(varList):
        """ Convert varList to string list
            @param varList: Variables dict list
            @type varList: list
            @return: Variables string list
            @rtype: list """
        varStr = []
        for var in varList:
            if var['active']:
                if var['type'] == 0:
                    varStr.append("%s = %s" % (var['label'], var['value']))
                elif var['type'] == 1:
                    varStr.append("%s.append(%s)" % (var['label'], var['value']))
        return varStr

    def getObjFromName(self, nodeName):
        """ Get QTreeWidgetItem from node name
            @param nodeName: Graph node name
            @type nodeName: str
            @return: Graph node object (QTreeWidgetItem)
            @rtype: object """
        allItems = QtGui.QTreeWidgetItemIterator(self.mainUi.twGraph,
                                                 QtGui.QTreeWidgetItemIterator.All) or None
        if allItems is not None:
            while allItems.value():
                item = allItems.value()
                if item.nodeName == nodeName:
                    return item
                allItems += 1

    @property
    def uiToDict(self):
        """ Translate ui to dict
            @return: {'gp_GlobalNotes': [str()], 'gp_globalVar': [dict{}],
                      'gp_graphRootList': [str()], 'gp_graphNodeList': {dict{}}}
            @type kwargs: dict """
        return self.params


class ExecGrapher(object):

    def __init__(self, mainUi):
        """ @param mainUi: Grapher ui object (QMainWindow)
            @type mainUi: object """
        self.mainUi = mainUi
        self.graph = self.mainUi.twGraph
        print "\n##### EXEC GRAPH #####"
        createGrapherFld(self.mainUi)
        self.execFile = self.getExecFile
        self.scriptPath = self.getScriptPath

    def execGraph(self):
        """ Execute Grapher """
        if self.execFile is not None:
            self.saveNodeToFile()
            self.initExecFile()
            self.initInternalVar()
            self.initGlobalVar()
            self.initGraphNode()
            self.endExecFile()
            if self.mainUi.miDebug.isChecked():
                print "!!! Debug On !!!"
                os.system("mayapy.exe %s" % self.execFile)
                # os.system("python -i %s" % self.execFile)
            else:
                os.system("start mayapy.exe %s" % self.execFile)
                # os.system("start python -i %s" % self.execFile)

    def saveNodeToFile(self):
        """ Save grapher contentes to files """
        print "#-- Save GraphNode To File --#"
        internVarFile = self._saveInternalVarToFile()
        globalVarFile = self._saveGlobalVarToFile()
        self._saveNodeToFile(internVarFile, globalVarFile)

    def _saveInternalVarToFile(self):
        """ Save internal var to files
            @return: Intern var file absolut path
            @rtype: file """
        internVarFile = os.path.join(self.scriptPath, "%s--internVar.py" % self.mainUi.GP_NAME)
        #-- Write Env --#
        env = GrapherEnv().mayaEnv
        scriptTxt = []
        for k, v in env.iteritems():
            scriptTxt.append("%s = %r" % (k, v))
        #-- Write internal Var --#
        scriptTxt.extend(["GP_NAME = %r" % self.mainUi.GP_NAME,
                          "GP_FILENAME = %r" % self.mainUi.GP_FILENAME,
                          "GP_DIRPATH = %r" % self.mainUi.GP_DIRPATH,
                          "GP_ABSPATH = %r" % self.mainUi.GP_ABSPATH,
                          "\n"])
        pFile.writeFile(internVarFile, '\n'.join(scriptTxt), add=False)
        return internVarFile

    def _saveGlobalVarToFile(self):
        """ Save global var to files
            @return: Global var file absolut path
            @rtype: file """
        varList = GetGrapher(self.mainUi).varListToString(self.mainUi.twGlobalVar.varList)
        globalVarFile = os.path.join(self.scriptPath, "%s--globalVar.py" % self.mainUi.GP_NAME)
        pFile.writeFile(globalVarFile, '\n'.join(varList), add=False)
        return globalVarFile

    def _saveNodeToFile(self, internVarFile, globalVarFile):
        """ Save node params to files
            @param internVarFile: Internal variable file absolut path
            @type internVarFile: file
            @param globalVarFile: Global variable file absolut path
            @type globalVarFile: file """
        allItems = getAllItems(self.graph)
        for item in allItems:
            #-- Save Node Var --#
            varList = GetGrapher(self.mainUi).varListToString(item.nodeVarList[item.nodeVersion])
            varFile = os.path.join(self.scriptPath, "%s--nodeVar.py" % item.nodeName)
            pFile.writeFile(varFile, '\n'.join(varList), add=False)
            #-- Save Node Script --#
            if item.nodeType in ['sysData', 'cmdData', 'purData']:
                scriptFile = os.path.join(self.scriptPath, "%s--nodeScript.py" % item.nodeName)
                script = item.nodeScript[item.nodeVersion]
                pFile.writeFile(scriptFile, '\n'.join(script), add=False)
                if item.nodeType == 'cmdData':
                    #-- Save Cmd Launcher --#
                    melFile = os.path.join(self.scriptPath, "%s--mayaExec.mel" % item.nodeName)
                    melTxt = ['python("execfile(%r)");' % internVarFile,
                              'python("execfile(%r)");' % globalVarFile]
                    for nodeName in item.nodePath.split('/')[1:]:
                        nodeVarFile = os.path.join(self.scriptPath, "%s--nodeVar.py" % nodeName)
                        melTxt.append('python("execfile(%r)");' % nodeVarFile)
                    melTxt.append('python("execfile(%r)");' % scriptFile)
                    pFile.writeFile(melFile, '\n'.join(melTxt), add=False)

    def initExecFile(self):
        """ Init Grapher exec file """
        print "#-- Init Exec File --#"
        initTxt = ["import time",
                   "launchTime = time.time()",
                   "import os", "import sys", "print ' '",
                   "print '#############################'",
                   "print '########## GRAPHER ##########'",
                   "print '#############################'",
                   "print 'Date: %s' % time.strftime(\"%Y/%m/%d\", time.localtime())",
                   "print 'Time: %s' % time.strftime(\"%H:%M:%S\", time.localtime())",
                   "print ' '",
                   "print '#-- Init Grapher Env --#'",
                   "for path in %s:" % GrapherEnv().grapherSysPath,
                   "    if not path in sys.path:",
                   "        print 'Add %s to sysPath' % path",
                   "        sys.path.insert(0, path)",
                   "from lib.system.scripts import procMath as pMath",
                   "print ' '"]
        pFile.writeFile(self.execFile, '\n'.join(initTxt), add=False)

    def initInternalVar(self):
        """ Init grapher internal variables """
        print "#-- Init Internal Variables --#"
        internFile = os.path.join(self.scriptPath, "%s--internVar.py" % self.mainUi.GP_NAME)
        initTxt = ["print '#-- Init Internal Variables --#'",
                   "execfile(%r)" % internFile,
                   "print 'GP_NAME = %s' % GP_NAME",
                   "print 'GP_FILENAME = %s' % GP_FILENAME",
                   "print 'GP_DIRPATH = %s' % GP_DIRPATH",
                   "print 'GP_ABSPATH = %s' % GP_ABSPATH",
                   "print ' '"]
        pFile.writeFile(self.execFile, '\n'.join(initTxt), add=True)

    def initGlobalVar(self):
        """ Init grapher global variables """
        print "#-- Init Global Variables --#"
        globalFile = os.path.join(self.scriptPath, "%s--globalVar.py" % self.mainUi.GP_NAME)
        initTxt = ["print '#-- Init Global Variables --#'",
                   "execfile(%r)" % globalFile]
        varList = GetGrapher(self.mainUi).varListToString(self.mainUi.twGlobalVar.varList)
        for var in varList:
            initTxt.append("print %r" % var)
        initTxt.extend(["print ' '", "print ' '", "print ' '"])
        pFile.writeFile(self.execFile, '\n'.join(initTxt), add=True)

    def initGraphNode(self):
        """ Init graph Node """
        print "#-- Init Graph Node --#"
        loopList = []
        for node in self.getActiveGraphNode:
            #-- Exec Node Var --#
            varFile = os.path.join(self.scriptPath, "%s--nodeVar.py" % node.nodeName)
            Ntab = self.getNtab(loopList, node)
            nodeTxt = ["%sprint '##### Exec Node %s #####'" % ('\t'*Ntab, node.nodeName),
                       "%snodeTime = time.time()" % ('\t'*Ntab),
                       "\t"*Ntab + "print 'Date: %s' % time.strftime(\"%Y/%m/%d\", time.localtime())",
                       "\t"*Ntab + "print 'Time: %s' % time.strftime(\"%H:%M:%S\", time.localtime())"]
            if node.nodeType not in ['modul', 'loop']:
                nodeTxt.extend(["%sprint '// Node Start'" % ('\t'*Ntab), "%sprint ' '" % ('\t'*Ntab)])
            nodeTxt.append("%sexecfile(%r)" % ('\t'*Ntab, varFile))
            #-- Exec Node Script --#
            if node.nodeType == 'sysData':
                scriptFile = os.path.join(self.scriptPath, "%s--nodeScript.py" % node.nodeName)
                nodeTxt.append("%sexecfile(%r)" % ('\t'*Ntab, scriptFile))
            elif node.nodeType == 'cmdData':
                scriptFile = os.path.join(self.scriptPath, "%s--mayaExec.mel" % node.nodeName)
                nodeCmd = node.nodeCmd[node.nodeVersion]
                nodeCmdOpt = node.nodeCmdOpt[node.nodeVersion]
                # cmd = '\"%s\" %s' % (GrapherEnv().mayaEnv[nodeCmd], scriptFile)
                nodeTxt.extend(["%sprint '%s %s'" % ('\t'*Ntab, GrapherEnv().mayaEnv[nodeCmd], scriptFile),
                                "%sprint ' '" % ('\t'*Ntab),
                                "%sos.system('mayabatch -script %s')" % ('\t'*Ntab,
                                                                  # GrapherEnv().mayaEnv[nodeCmd].replace('\\', '\\\\'),
                                                                  scriptFile.replace('\\', '\\\\'))])
            #-- Exec Loop Node --#
            elif node.nodeType == 'loop':
                loopList.append(node)
                iterStr = self.getLoopIteration(node)
                nodeTxt.extend(["%s%s" % ('\t'*Ntab, iterStr),
                                "%sprint ' '" % ('\t'*(Ntab+1)),
                                "%sprint '//===== %s Iter: ' + str(%s) + ' %s'" % ('\t'*(Ntab+1),
                                                                            node.nodeName,
                                                                            node.nodeLoop['iter'],
                                                                            '='*40),
                                "%sprint ' '" % ('\t'*(Ntab+1))])
            if node.nodeType not in ['modul', 'loop']:
                nodeTxt.extend(["%sprint ' '" % ('\t'*Ntab), "%sprint '// Node End'" % ('\t'*Ntab),
                                "\t"*Ntab + "print 'Duration: %s' % pMath.secondsToStr(time.time() - nodeTime)",])
            nodeTxt.extend(self.endExecNode(node, Ntab))
            pFile.writeFile(self.execFile, '\n'.join(nodeTxt), add=True)

    def endExecNode(self, node, Ntab):
        """ end node return line
            @param node: Graph QTreeWidgetItem
            @type node: object
            @param Ntab: Number of loop tag
            @type Ntab: int
            @return: Node end text
            @rtype: str """
        endTxt = []
        if node.nodeType == 'loop':
            if Ntab > 0:
                endTxt.append("%sprint ' '" % ('\t'*(Ntab+1)))
        else:
            if Ntab > 0:
                endTxt.extend(["%sprint ' '" % ('\t'*Ntab),
                               "%sprint ' '" % ('\t'*Ntab)])
            else:
                endTxt.extend(["%sprint ' '" % ('\t'*Ntab),
                               "%sprint ' '" % ('\t'*Ntab),
                               "%sprint ' '" % ('\t'*Ntab)])
        return endTxt

    def endExecFile(self):
        """ Ending Grapher exec file """
        print "#-- Ending Exec File --#"
        messTxt = " !:) GRAPHER DONE (:! "
        mess = "%s%s%s" % ('='*int((80-len(messTxt))/2), messTxt, '='*int((80-len(messTxt))/2))
        execTxt = ["print ' '", "print ' '", "print ' '", "print %r" % mess, "print ' '",
                   "print 'Date: %s' % time.strftime(\"%Y/%m/%d\", time.localtime())",
                   "print 'Time: %s' % time.strftime(\"%H:%M:%S\", time.localtime())",
                   "print 'Duration: %s' % pMath.secondsToStr(time.time() - launchTime)"]
        if not self.mainUi.miDebug.isChecked():
            execTxt.append("os.remove(%r)" % self.execFile)
            execTxt.append("time.sleep(1000000)")
        pFile.writeFile(self.execFile, '\n'.join(execTxt), add=True)

    @property
    def getExecPath(self):
        """ Get exec file path
            @return: Exec file path
            @rtype: str """
        execPath = os.path.join(self.mainUi.GP_DIRPATH, 'tmp', self.mainUi.GP_NAME, grapher.user)
        if os.path.exists(execPath):
            return execPath
        else:
            print "!!! WARNING: Exec path doesn't exists !!!"
            return None

    @property
    def getExecFile(self):
        """ Create exec file
            @return: Exec file absolut path
            @rtype: str """
        execPath = self.getExecPath
        fullDate = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
        if execPath is not None:
            fileName = "exec-%s-%s.py" % (self.mainUi.GP_NAME, fullDate)
            execFile = os.path.join(execPath, fileName)
            return execFile
        else:
            return None

    @staticmethod
    def getNtab(loopList, node):
        """ Get number of loop tab
            @param loopList: Graph loop node list
            @type loopList: list
            @param node: Graph QTreeWidgetItem
            @type node: object
            @return: Number of loop tab
            @rtype: int """
        Ntab = 0
        for loop in loopList:
            if not node.nodeName == loop.nodeName:
                if loop.nodeName in node.nodePath:
                    Ntab += 1
        return Ntab

    @staticmethod
    def getLoopIteration(node):
        """ Get loop iteration list
            @param node: Graph QTreeWidgetItem
            @type node: object
            @return: Loop iteration string
            @rtype: str """
        if node.nodeLoop['mode'] == 'range':
            return "for %s in range(int(%s), int(%s)+1, int(%s)):" % (node.nodeLoop['iter'],
                                                                      node.nodeLoop['range'][0],
                                                                      node.nodeLoop['range'][1],
                                                                      node.nodeLoop['range'][2])
        if node.nodeLoop['mode'] == 'list':
            return "for %s in %s:" % (node.nodeLoop['iter'], node.nodeLoop['list'])
        if node.nodeLoop['mode'] == 'single':
            return "for %s in [%s]:" % (node.nodeLoop['iter'], node.nodeLoop['single'])

    @property
    def getScriptPath(self):
        """ Get scripts path
            @return: Script path
            @rtype: str """
        scriptPath = os.path.join(self.mainUi.GP_DIRPATH, 'scripts', self.mainUi.GP_NAME)
        if os.path.exists(scriptPath):
            return scriptPath
        else:
            print "!!! WARNING: Exec path doesn't exists !!!"
            return None

    @property
    def getActiveGraphNode(self):
        """ Get active QTreeWidgetItem from graph
            @return: Selected graphNode list(QTreeWidgetItem)
            @rtype: list"""
        nodeList = []
        skipList = []
        allItems = getAllItems(self.graph)
        #-- Get Active Node List --#
        for item in allItems:
            verif = True
            for node in item.nodePath.split('/'):
                if node in skipList:
                    verif = False
            if verif:
                if item.nodeActive:
                    nodeList.append(item)
                else:
                    skipList.append(item.nodeName)
        return nodeList
