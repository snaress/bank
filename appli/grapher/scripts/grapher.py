import os
from appli import grapher
from appli.grapher.scripts import gpCore
from lib.system.scripts import procFile as pFile


class Grapher(gpCore.FileCmds):
    """ Class containing all grapher's commands for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        super(Grapher, self).__init__()
        self._path = None
        self._file = None
        self._absPath = None
        self.commentHtml = ""
        self.commentTxt = ""
        self.variables = {}
        self.graphTree = {}

    def __getDict__(self):
        txt = []
        for k, v in sorted(self.__dict__.iteritems()):
            if not k.startswith('_'):
                if isinstance(v, str):
                    txt.append("%s = %r" % (k, v))
                else:
                    txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def __getStr__(self):
        txt = ["", "========== GRAPHER =========="]
        #-- General --#
        txt.append("#-- General --#")
        for k, v in sorted(self.__dict__.iteritems()):
            if k.startswith('_'):
                if isinstance(v, str):
                    txt.append("%s = %r" % (k, v))
                else:
                    txt.append("%s = %s" % (k, v))
        #-- Comment --#
        txt.append("#-- Comment --#")
        txt.append(self.commentTxt)
        #-- Variables --#
        txt.append("#-- Variables--#")
        for k, v in sorted(self.variables.iteritems()):
            txt.append("%s = %s" % (k, v))
        #-- Graph Tree --#
        txt.append("#-- Graph Tree--#")
        for node in self.graphTree['_order']:
            txt.append("%s :" % node)
            for k, v in self.graphTree[node].iteritems():
                txt.append("\t\t%s = %s" % (k, v))
        return '\n'.join(txt)

    def loadGraph(self, fileName):
        """ Load given grapher file
            @param fileName: (str) : Grapher absolut path """
        print "\n[grapher] : #-- Load Graph: %s --#" % os.path.basename(fileName)
        params = pFile.readPyFile(fileName)
        self._path = os.path.dirname(fileName)
        self._file = os.path.basename(fileName)
        self._absPath = fileName
        for k in sorted(self.__dict__.keys()):
            if k in params:
                print "\tUpdating %s ..." % k
                setattr(self, k, params[k])
        print "[grapher] : Graph successfully loaded."

    def ud_commentFromUi(self, mainUi):
        """ Update comment from mainUi
            @param mainUi: (object) : QMainWindow """
        print "[grapher] : #-- Update Comment From Ui --#"
        txtDict = mainUi.wgComment.__getDict__()
        self.commentHtml = txtDict['commentHtml']
        self.commentTxt = txtDict['commentTxt']

    def ud_variablesFromUi(self, mainUi):
        """ Update variables from mainUi
            @param mainUi: (object) : QMainWindow """
        print "[grapher] : #-- Update Variables From Ui --#"
        self.variables = mainUi.wgVariables.__getDict__()

    def ud_graphTreeFromUi(self, mainUi):
        """ Update graph tree from mainUi
            @param mainUi: (object) : QMainWindow """
        print "[grapher] : #-- Update Graph Tree From Ui --#"
        self.graphTree = mainUi.wgGraph.__getDict__()

    def execGraph(self):
        """ Execute graph """
        if self._absPath is not None:
            print "[grapher] : #-- Init Graph File --#"
            #-- Init Path --#
            eg = ExecGraph(self)
            self.initGrapherPath(self._path, 'scripts', self._file)
            self.initGrapherPath(self._path, 'tmp', self._file)
            pyFileName = "exec__%s__%s.py" % (pFile.getDate(), pFile.getTime())
            exeFile = pFile.conformPath(os.path.join(self.tmpPath, pyFileName))
            #-- Init Grapher Files --#
            graphLoops = eg.graphNodesToFile()
            exeTxt = eg.execHeader(graphLoops)
            #-- Store Graph --#
            exeTxt.extend(eg.parseGraph(graphLoops))
            #-- End Graph --#
            exeTxt.extend(eg.execEnd())
            #-- Write & Launch --#
            pFile.writeFile(exeFile, '\n'.join(exeTxt))
            print "\n[grapher] : #-- Launch Graph File --#"
            print "\tLaunching %s" % exeFile
            os.system('start /i python -i %s' % exeFile)
        else:
            print "[grapher] : !!! ERROR: Save graph before exec !!!"

    def writeToFile(self):
        """ Write grapher2 to file """
        if self._absPath is not None:
            if os.path.exists(self._path):
                print "\n[grapher] : #-- Write Graph --#"
                try:
                    pFile.writeFile(self._absPath, self.__getDict__())
                    print "Result: %s" % self._absPath
                except:
                    raise IOError, "Result: Failed to write file %s" % self._absPath
            else:
                raise IOError, "Path not found: %s" % self._path
        else:
            raise ValueError, "Grapher._absPath = %s" % self._absPath

    def reset(self):
        """ Reset all params """
        print "\n[grapher] : #-- Reset All Params --#"
        self._path = None
        self._file = None
        self._absPath = None
        self.commentHtml = ""
        self.commentTxt = ""
        self.variables = {}
        self.graphTree = {}
        print "[grapher] : Params successfully reseted."

    def nodeVersion(self, nodeName):
        """ Get given node current version
            @param nodeName: (str) : Node name
            @return: (str) : node version """
        return self.graphTree[nodeName]['currentVersion']

    def getAllParent(self, nodeName, depth=-1):
        """ Get all parent of given node
            @param nodeName: (str) : Recusion start nodeName
            @param depth: (int) : Number of recursion (-1 = infinite)
            @return: (list) : Parent nodeName list """
        items = []

        def recurse(currentItem, depth):
            items.append(currentItem)
            if depth != 0:
                if self.graphTree[currentItem]['nodeParent'] is not None:
                    recurse(self.graphTree[currentItem]['nodeParent'], depth-1)

        recurse(nodeName, depth)
        return items

    def getAllChildren(self, nodeName):
        """ Get all children of given node
            @param nodeName: (str) : Recusion start nodeName
            @return: (list) : Children nodeName list """
        items = []
        for node in self.graphTree['_order']:
            allParents = self.getAllParent(node)
            if nodeName in allParents:
                if not node in items:
                    items.append(node)
        return items

    @property
    def userBinPath(self):
        """ Get user bin path
            @return: (str) : User bin path """
        return os.path.join(grapher.binPath, 'users', grapher.user[0], grapher.user)

    @property
    def scriptPath(self):
        """ Get grapher script path
            @return: (str) : Grapher script path """
        return os.path.join(self._path, 'scripts', self._file.replace('.py', ''), grapher.user)

    @property
    def tmpPath(self):
        """ Get grapher tmp path
            @return: (str) : Grapher tmp path """
        return os.path.join(self._path, 'tmp', self._file.replace('.py', ''), grapher.user)

    @staticmethod
    def _varDictToStr(varDict):
        """ Translate variable dict into string list
            @return: (list) : Variables as string """
        varStr = []
        for var in sorted(varDict.keys()):
            if varDict[var]['enabled']:
                if varDict[var]['type'] == '=':
                    varLine = '%s = %s' % (varDict[var]['label'], varDict[var]['value'])
                elif varDict[var]['type'] == 'num':
                    if '.' in varDict[var]['value']:
                        varLine = '%s = %s' % (varDict[var]['label'], float(varDict[var]['value']))
                    else:
                        varLine = '%s = %s' % (varDict[var]['label'], int(varDict[var]['value']))
                else:
                    varLine = '%s.append(%s)' % (varDict[var]['label'], varDict[var]['value'])
                varStr.append(varLine)
        return varStr


class ExecGraph(object):

    def __init__(self, grapher):
        self.grapher = grapher
        self.graphTree = self.grapher.graphTree

    def graphNodesToFile(self):
        """ Write graph nodes to file
            @return: (dict) : Loop's children nodes """
        if not os.path.exists(self.grapher.scriptPath):
            raise IOError, "!!! ERROR: Script path not found: %s" % self.grapher.scriptPath
        else:
            graphLoops = {}
            for node in self.graphTree['_order']:
                nodeTxt = []
                if self.graphTree[node]['instanceFrom'] is None:
                    refName = node
                else:
                    refName = self.graphTree[node]['instanceFrom']
                if not self.graphTree[refName]['nodeType'] in ['modul', 'loop']:
                    print "\nWriting %s to file ..." % node
                    nodeTxt.append("#-- Grapher Variables --#")
                    nodeTxt.extend(self._getGrapherVar())
                    nodeTxt.append("#-- Global Variables --#")
                    nodeTxt.extend(self._getGlobalVar())
                    nodeTxt.append("#-- Parent Variables --#")
                    nodeTxt.extend(self._getParentsVar(node))
                    nodeTxt.append("#-- %s variables --#" % refName)
                    nodeTxt.extend(self._getNodeVar(refName))
                    if self.graphTree[refName]['nodeType'] in ['sysData', 'cmdData', 'purData']:
                        if self.graphTree[refName]['nodeType'] == 'cmdData':
                            nodeTxt.append("#-- %s cmd init --#" % refName)
                            nodeTxt.append('print "Info: Init cmdData ..."')
                            nodeTxt.extend(self.graphTree[refName]['nodeCmdInit'].split('\n'))
                            nodeTxt.extend(['print "Info: Init cmdData done"', 'print ""'])
                        nodeTxt.append("#-- %s script --#" % refName)
                        v = self.grapher.nodeVersion(refName)
                        nodeTxt.extend(self.graphTree[refName]['nodeScript'][v].split('\n'))
                    scriptFile = pFile.conformPath(os.path.join(self.grapher.scriptPath,
                                                                '%s.py' % node))
                    try:
                        pFile.writeFile(scriptFile, '\n'.join(nodeTxt))
                        print '\t', scriptFile
                    except:
                        raise IOError, "!!! ERROR: Can not create node file %s !!!" % node
                else:
                    if self.graphTree[refName]['nodeType'] == 'loop':
                        nodeTxt.append("#-- %s params --#" % refName)
                        graphLoops[node] = self.grapher.getAllChildren(node)
                        if node in graphLoops[node]:
                            graphLoops[node].pop(graphLoops[node].index(node))
            return graphLoops

    def execHeader(self, graphLoops):
        """ Init script header
            @param graphLoops: (dict) : Loop's children
            @return: (list) : Script header """
        txt = ['graphLoops = %s' % graphLoops,
               'print "###################"',
               'print "##### GRAPHER #####"',
               'print "###################"',
               'print ""', 'execfile("%s")' % grapher.envFile,
               'import os',
               'from lib.system.scripts import procFile as pFile',
               'from appli.grapher.scripts import gpCore',
               'print "ExecGraph started on %s at %s" % (pFile.getDate(), pFile.getTime())',
               'print ""', 'print ""', 'print "#-- Import Grapher Var --#"']
        for gVar in self._getGrapherVar():
            txt.append(gVar)
            txt.append('print %r' % gVar)
        txt.extend(['print ""', 'print ""', 'print "#-- Import Global Var --#"'])
        for var in self.grapher._varDictToStr(self.grapher.variables):
            txt.append(var)
            txt.append('print %r' % var)
        txt.extend(['print ""', 'print ""', 'print "#-- Exec Graph --#"'])
        return txt

    def execEnd(self):
        """ Init script end """
        txt = ['print ""', 'print ""', 'print "#" * 50',
               'print "#-- Grapher End --#"',
               'print "ExecGraph finished on %s at %s" % (pFile.getDate(), pFile.getTime())']
        return txt

    def parseGraph(self, graphLoops):
        """ Parsing graphTree
            @param graphLoops: (dict) : Loop's children
            @return: (list) : Graph node params """
        print "\n[grapher] : #-- Parse graph ---#"
        txt = []
        disable = []
        for node in self.graphTree['_order']:
            if not node in disable:
                if not self.graphTree[node]['nodeEnabled']:
                    disable = self._parseDisabled(disable, node)
                else:
                    if self.graphTree[node]['instanceFrom'] is None:
                        refName = node
                    else:
                        refName = self.graphTree[node]['instanceFrom']
                    if not self.graphTree[refName]['nodeType'] == 'purData':
                        nodeFile = os.path.join(self.grapher.scriptPath, '%s.py' % node)
                        nodeFile = pFile.conformPath(nodeFile)
                        tab = self._getTab(node, graphLoops)
                        txt.extend(['%sprint ""' % tab, '%sprint ""' % tab, '%sprint ""' % tab,
                                    '%sprint "##### Exec Graph Node %s #####"' % (tab, node),
                                    '%sprint "ExecNode started on", pFile.getDate(), "at", pFile.getTime()' % tab,
                                    '%sprint ""' % tab, '%sprint "#-- Import Node Variables --#"' % tab])
                        txt.extend(self._parseAllVars(tab, refName))
                        if self.graphTree[refName]['nodeType'] == 'loop':
                            txt.extend(self._parseLoop(tab, refName))
                        elif self.graphTree[refName]['nodeType'] == 'sysData':
                            txt.extend(self._parseSysData(tab, nodeFile))
                            txt.extend(['%sprint ""' % tab,
                                        '%sprint "ExecNode finished on", pFile.getDate(), "at", pFile.getTime()' % tab])
                        elif self.graphTree[refName]['nodeType'] == 'cmdData':
                            txt.extend(self._parseCmdData(tab, nodeFile, node, graphLoops))
                            txt.extend(['%sprint ""' % tab,
                                        '%sprint "ExecNode finished on", pFile.getDate(), "at", pFile.getTime()' % tab])
        return txt

    def _parseDisabled(self, disabledNodes, nodeName):
        """ Store disabled graph nodes
            @param disabledNodes: (list) : Disabled Nodes list
            @param nodeName: (str) : Node name
            @return: (list) : Disabled Nodes list """
        disabledNodes.append(nodeName)
        for child in self.grapher.getAllChildren(nodeName):
            if not child in disabledNodes:
                disabledNodes.append(child)
        return disabledNodes

    def _parseAllVars(self, tab, nodeName):
        """ Store node variables
            @param tab: (str) : Text tabulation (space)
            @param nodeName: (str) : Node name
            @return: (list) : Graph exec text """
        varList = []
        nodeVar = self._getNodeVar(nodeName)
        for var in nodeVar:
            varList.append('%s%s' % (tab, var))
            varList.append('%sprint %r' % (tab, var))
        return varList

    def _parseLoop(self, tab, nodeName):
        """ Store loop params
            @param tab: (str) : Text tabulation (space)
            @param nodeName: (str) : Node name
            @return: (list) : Graph exec text """
        loopList = ['%sprint ""' % tab, '%sprint "#-- Import Loop Params --#"' % tab]
        loopType = self.graphTree[nodeName]['nodeLoop']['type']
        loopIter = self.graphTree[nodeName]['nodeLoop']['iter']
        loopCheck = self.graphTree[nodeName]['nodeLoop']['checkFile']
        loopParams = self._getLoopParams(nodeName)
        #-- Variables And Params --#
        for lVar in loopParams:
            loopList.append('%s%s' % (tab, lVar))
            loopList.append('%sprint %r' % (tab, lVar))
        if loopType == 'range':
            loopList.append('%s%s_iterList = pFile.dRange(%s_start, %s_stop, %s_step)'
                            % (tab, nodeName, nodeName, nodeName, nodeName))
        elif loopType == 'list':
            loopList.append('%s%s_iterList = %s_list' % (tab, nodeName, nodeName))
        elif loopType == 'single':
            loopList.append('%s%s_iterList = [%s_single]' % (tab, nodeName, nodeName))
        #-- Exec Loop Text --#
        lTab = '%s    ' % tab
        loopList.extend(['%sfor %s in %s_iterList:' % (tab, loopIter, nodeName),
                         '%sprint ""' % lTab, '%sprint "%s"' % (lTab, ('-' * 100)),
                         '%sprint "%s =", %s' % (lTab, loopIter, loopIter),
                         '%sprint "Info: Check Tmp Loop File ..."' % lTab,
                         '%sGP_%s__file = "checkFile__%s."+str(%s)+".py"' % (lTab, nodeName, loopCheck, loopIter),
                         '%sGP_%s__checkFile = os.path.join(GP_TMP, GP_%s__file)' % (lTab, nodeName, nodeName),
                         '%sGP_%s__checkDict = {"%s": %s}' % (lTab, nodeName, loopIter, loopIter),
                         '%sGP_%s__checkResult = gpCore.FileCmds.checkLoopTmpFile(GP_%s__checkFile, %r, **GP_%s__checkDict)'
                                                 % (lTab, nodeName, nodeName, loopType, nodeName),
                         '%sprint "%s"' % (lTab, ('-' * 100)),
                         '%sif not GP_%s__checkResult:' % (lTab, nodeName),
                         '%s    continue' % lTab])
        return loopList

    def _parseSysData(self, tab, nodeFile):
        """ Store sysData
            @param tab: (str) : Text tabulation (space)
            @param nodeFile: (str) : Node script file
            @return: (list) : Graph exec text """
        return ['%sprint ""' % tab, '%sprint "#-- Execute Node Script --#"' % tab,
                '%sexecfile("%s")' % (tab, nodeFile)]

    def _parseCmdData(self, tab, nodeFile, nodeName, graphLoops):
        """ Store cmdData
            @param tab: (str) : Text tabulation (space)
            @param nodeFile: (str) : Node script file
            @param nodeName: (str) : Node name
            @param graphLoops: (dict) : Loop's children
            @return: (list) : Graph exec text """
        iterators = []
        for loop in graphLoops:
            if nodeName in graphLoops[loop]:
                iterators.append(self.graphTree[loop]['nodeLoop']['iter'])
        return ['%siters = []' % tab,
                '%sfor nodeLoopIter in %s:' % (tab, iterators),
                '%s    iters.append(eval(nodeLoopIter))' % tab,
                '%sGP_melFile = gpCore.FileCmds.createMelFromPy("%s", %s, iters)' % (tab, nodeFile, iterators),
                '%sGP_nodeCmd = "%s".replace("$script", GP_melFile)' % (tab, self.graphTree[nodeName]['nodeCmd']),
                '%sprint GP_nodeCmd.replace("%s", GP_PATH)' % (tab, self.grapher._path),
                '%sprint ""' % tab, '%sos.system(GP_nodeCmd)' % tab]

    def _getGrapherVar(self):
        """ Get internal grapher variables
            @return: (list) : Internal grapher variables """
        return ['GP_USER = "%s"' % grapher.user,
                'GP_PATH = "%s"' % self.grapher._path,
                'GP_FILE = "%s"' % self.grapher._file,
                'GP_TMP = "%s"' % pFile.conformPath(self.grapher.tmpPath),
                'GP_SCRIPTS = "%s"' % pFile.conformPath(self.grapher.scriptPath)]

    def _getGlobalVar(self):
        """ Get grapher global variables
            @return: (list) : Grapher global variables """
        return self.grapher._varDictToStr(self.grapher.variables)

    def _getParentsVar(self, nodeName):
        """ Get all graph node parent variables
            @param nodeName: (str) : Node name
            @return: (list) : All parents variables """
        parents = self.grapher.getAllParent(nodeName)
        parents.reverse()
        nodeTxt = []
        for p in parents:
            if not p == nodeName:
                v = self.grapher.nodeVersion(p)
                if v in self.graphTree[p]['nodeVariables'].keys():
                    nodeTxt.append("# %s variables #" % p)
                    varDict = self.grapher._varDictToStr(self.graphTree[p]['nodeVariables'][v])
                    nodeTxt.extend(varDict)
        return nodeTxt

    def _getNodeVar(self, nodeName):
        """ Get graph node variables
            @param nodeName: (str) : Node name
            @return: (list) : Graph node variables """
        nodeTxt = []
        v = self.grapher.nodeVersion(nodeName)
        if v in self.graphTree[nodeName]['nodeVariables'].keys():
            nodeVarDict = self.grapher._varDictToStr(self.graphTree[nodeName]['nodeVariables'][v])
            nodeTxt.extend(nodeVarDict)
        return nodeTxt

    def _getLoopParams(self, nodeName):
        """ Get loop node params
            @param nodeName: (str) : Loop node name
            @return: (dict) : Loop node params """
        loopParams = self.graphTree[nodeName]['nodeLoop']
        nodeTxt = ['%s_loopType = "%s"' % (nodeName, loopParams['type']),
                   '%s_loopIter = "%s"' % (nodeName, loopParams['iter']),
                   '%s_loopCheckFile = "%s"' % (nodeName, loopParams['checkFile'])]
        if loopParams['type'] == 'range':
            nodeTxt.extend(['%s_start = %s' % (nodeName, loopParams['start']),
                            '%s_stop = %s' % (nodeName, loopParams['stop']),
                            '%s_step = %s' % (nodeName, loopParams['step'])])
        elif loopParams['type'] == 'list':
            nodeTxt.append('%s_list = %s' % (nodeName, loopParams['list']))
        elif loopParams['type'] == 'single':
            nodeTxt.append('%s_single = %s' % (nodeName, loopParams['single']))
        return nodeTxt

    def _getTab(self, nodeName, graphLoops):
        """ Get loop tabulation
            @param nodeName: (str) : Loop node name
            @param graphLoops: (dict) : Loop's children
            @return: (str) : Loop tabulation """
        tab = ''
        for loop in graphLoops.keys():
            if nodeName in graphLoops[loop]:
                tab = '%s    ' % tab
        return tab


if __name__ == '__main__':
    print "Test Exec Graph"
    fileName = "G:/ddd/assets/chars/main/anglaigus/gp_anglaigus.py"
    print os.path.dirname(fileName)
    # gp = Grapher()
    # gp.loadGraph(fileName)
    # gp.execGraph()
