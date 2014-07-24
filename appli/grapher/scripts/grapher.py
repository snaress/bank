import os
from appli import grapher
from appli.grapher.scripts import core
from lib.system.scripts import procFile as pFile


class Grapher(core.FileCmds):
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

    def __repr2__(self):
        txt = []
        for k, v in sorted(self.__dict__.iteritems()):
            if not k.startswith('_'):
                if isinstance(v, str):
                    txt.append("%s = %r" % (k, v))
                else:
                    txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def __str__(self):
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
        txtDict = mainUi.wgComment.__repr2__()
        self.commentHtml = txtDict['commentHtml']
        self.commentTxt = txtDict['commentTxt']

    def ud_variablesFromUi(self, mainUi):
        """ Update variables from mainUi
            @param mainUi: (object) : QMainWindow """
        print "[grapher] : #-- Update Variables From Ui --#"
        self.variables = mainUi.wgVariables.__repr2__()

    def ud_graphTreeFromUi(self, mainUi):
        """ Update graph tree from mainUi
            @param mainUi: (object) : QMainWindow """
        print "[grapher] : #-- Update Graph Tree From Ui --#"
        self.graphTree = mainUi.wgGraph.__repr2__()

    def execGraph(self):
        """ Execute graph """
        if self._absPath is not None:
            print "[grapher] : #-- Init Graph File --#"
            #-- Init Path --#
            eg = ExecGraph(self)
            self.initScriptPath(self._path, self._file)
            self.initTmpPath(self._path, self._file)
            exeFile = os.path.join(self.tmpPath, 'test.py').replace('\\', '/')
            #-- Init Grapher Files --#
            eg.graphNodesToFile()
            exeTxt = eg.execHeader()
            #-- Store Graph --#
            exeTxt.extend(eg.parseGraph())
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
                    pFile.writeFile(self._absPath, self.__repr2__())
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

    @staticmethod
    def _varDictToStr(varDict):
        """ Translate variable dict into string list
            @return: (list) : Variables as string """
        varStr = []
        for var in sorted(varDict.keys()):
            if varDict[var]['type'] == 'num':
                if '.' in varDict[var]['value']:
                    varLine = '%s = %s' % (varDict[var]['label'], float(varDict[var]['value']))
                else:
                    varLine = '%s = %s' % (varDict[var]['label'], int(varDict[var]['value']))
            else:
                varLine = '%s = %s' % (varDict[var]['label'], varDict[var]['value'])
            varStr.append(varLine)
        return varStr


class ExecGraph(object):

    def __init__(self, grapher):
        self.grapher = grapher
        self.graphTree = self.grapher.graphTree

    def graphNodesToFile(self):
        """ Write graph nodes to file """
        if not os.path.exists(self.grapher.scriptPath):
            raise IOError, "!!! ERROR: Script path not found: %s" % self.grapher.scriptPath
        else:
            for node in self.grapher.graphTree['_order']:
                print "\nWriting %s to file ..." % node
                nodeTxt = []
                print "\tGet grapher variables ..."
                nodeTxt.append("#-- Grapher Variables --#")
                nodeTxt.extend(self._getGrapherVar())
                print "\tGet global variables ..."
                nodeTxt.append("#-- Global Variables --#")
                nodeTxt.extend(self._getGlobalVar())
                print "\tGet parent node variables ..."
                nodeTxt.append("#-- Parent Variables --#")
                nodeTxt.extend(self._getParentsVar(node))
                print "\tGet node variables ..."
                nodeTxt.append("#-- %s variables --#" % node)
                nodeTxt.extend(self._getNodeVar(node))
                if self.graphTree[node]['nodeType'] in ['sysData', 'cmdData', 'purData']:
                    if self.graphTree[node]['nodeType'] == 'cmdData':
                        print "\tGet node init command ..."
                        nodeTxt.append("#-- %s cmd init --#" % node)
                        nodeTxt.extend(self.graphTree[node]['nodeCmdInit'].split('\n'))
                    print "\tGet node script ..."
                    nodeTxt.append("#-- %s script --#" % node)
                    v = self.grapher.nodeVersion(node)
                    nodeTxt.extend(self.graphTree[node]['nodeScript'][v].split('\n'))
                print "\tSave node to file ..."
                scriptFile = os.path.join(self.grapher.scriptPath, '%s.py' % node).replace('\\','/')
                try:
                    pFile.writeFile(scriptFile, '\n'.join(nodeTxt))
                    print '\t\t', scriptFile
                except:
                    raise IOError, "!!! ERROR: Can not create node file %s !!!" % node

    def execHeader(self):
        """ Init script header
            @return: (list) : Script header """
        txt = ['print "###################"',
               'print "##### GRAPHER #####"',
               'print "###################"',
               'print "ExecGraph %s"' % self.grapher._absPath,
               'print ""', 'execfile("%s")' % grapher.envFile,
               'print ""', 'print ""', 'print "#-- Import Grapher Var --#"',
               'print "GP_PATH = %r"' % self.grapher._path,
               'print "GP_FILE = %r"' % self.grapher._file,
               'print ""', 'print ""', 'print "#-- Import Global Var --#"']
        for var in self.grapher._varDictToStr(self.grapher.variables):
            txt.append('print %r' % var)
        txt.extend(['print ""', 'print ""', 'print "#-- Exec Graph --#"'])
        return txt

    def parseGraph(self):
        print "\n[grapher] : #-- Parse graph ---#"
        txt = []
        disable = []
        for node in self.graphTree['_order']:
            if not node in disable:
                if not self.graphTree[node]['nodeEnabled']:
                    disable.append(node)
                    for child in self.grapher.getAllChildren(node):
                        if not child in disable:
                            disable.append(child)
                else:
                    nodeFile = os.path.join(self.grapher.scriptPath, '%s.py' % node).replace('\\', '/')
                    txt.extend(['print ""', 'print ""',
                                'print "##### Exec Graph Node %s #####"' % node])
                    if self.graphTree[node]['nodeType'] == 'sysData':
                        txt.append('execfile("%s")' % nodeFile)
                    elif self.graphTree[node]['nodeType'] == 'cmdData':
                        melFile = self.grapher.createMelFromPy(nodeFile)
                        nodeCmd = self.graphTree[node]['nodeCmd'].replace('$script', melFile)
                        txt.append('print %r' % nodeCmd.replace(self.grapher._path, 'GP_PATH'))
                        txt.append('print ""')
                        txt.append('os.system("%s")' % nodeCmd)
        return txt

    def _getGrapherVar(self):
        """ Get internal grapher variables
            @return: (list) : Internal grapher variables """
        return ['GP_PATH = "%s"' % self.grapher._path,
                'GP_FILE = "%s"' % self.grapher._file]

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
                    nodeTxt.append("#-- %s variables --#" % p)
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
