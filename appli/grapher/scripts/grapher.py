import os
from appli import grapher
from lib.system.scripts import procFile as pFile


class Grapher(object):
    """ Class containing all grapher's commands for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
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
        print "[grapher] : #-- Init Graph File --#"
        gpFolder = self._file.replace('.py', '')
        exeFile = os.path.join(self._path, 'tmp', gpFolder, grapher.user, 'test.py')
        script = ['print "######################"',
                  'print "##### EXEC GRAPH #####"',
                  'print "######################"',
                  'print "Graph Path: %s"' % self._path,
                  'print "Graph File: %s"' % self._file,
                  'execfile("%s")' % grapher.envFile,
                  'print ""', 'print "#-- Import Global Var --#"']
        script.extend(self._varDictToStr())
        pFile.writeFile(exeFile, '\n'.join(script))
        os.system('start python -i %s' % exeFile)

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

    def _varDictToStr(self):
        script = []
        for var in sorted(self.variables.keys()):
            if self.variables[var]['type'] == 'num':
                print 'num'
                if '.' in self.variables[var]['value']:
                    varLine = '%s = %s' % (self.variables[var]['label'],
                                           float(self.variables[var]['value']))
                else:
                    varLine = '%s = %s' % (self.variables[var]['label'],
                                           int(self.variables[var]['value']))
            else:
                varLine = '%s = %s' % (self.variables[var]['label'],
                                       self.variables[var]['value'])
            script.append('print %r' % varLine)
            script.append(varLine)
        if script:
            return script


class GraphNodeData(object):
    """ Class used by Grapher for graphNode data storage """

    def __init__(self):
        self.nodeType = None
        self.currentVersion = None
        self.versionTitle = {}
        self.nodeComment = {}
        self.nodeVariables = {}
        self.nodeLoop = {}
        self.nodeScript = {}
        self.nodeNotes = {}

    def __repr2__(self):
        return self.__dict__

    def __str__(self):
        txt = []
        for k, v in self.__repr2__().iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)
