import os
from appli import grapher
from lib.system import procFile as pFile
try:
    from PyQt4 import QtGui
except:
    pass


class FileCmds(object):
    """ File commands class used by grapher """

    def __init__(self):
        pass

    @staticmethod
    def createLockFile(lockFile):
        """ Create lockFile
            @param lockFile: (str) : LockFile absolut path
            @return: (bool) : True if success, False if failed """
        lockTxt = ["user = %r" % grapher.user,
                   "station = %r" % grapher.station,
                   "date = %r" % pFile.getDate(),
                   "time = %r" % pFile.getTime()]
        try:
            pFile.writeFile(lockFile, '\n'.join(lockTxt))
            print "\tCreating lockFile %s ..." % os.path.basename(lockFile)
            return True
        except:
            raise IOError, "!!! Error: Can't create lockFile: %s" % lockFile

    @staticmethod
    def removeLockFile(lockFile):
        """ Remove lockFile
            @param lockFile: (str) : LockFile absolut path
            @return: (bool) : True if success, False if failed """
        if os.path.exists(lockFile):
            try:
                os.remove(lockFile)
                print "\tRemoving lockFile %s ..." % os.path.basename(lockFile)
                return True
            except:
                raise IOError, "!!! Error: Can't remove lockFile: %s !!!" % lockFile
        else:
            raise IOError, "!!! Error: LockFile not found: %s !!!" % lockFile

    @staticmethod
    def xtermLauncher():
        """ Default xterm launcher
            return: (str) : Default xTerm launcher """
        return "cmd.exe"

    @staticmethod
    def scriptLauncher():
        """ Default script editor launcher
            @return: (str) : Script editor launcher """
        return "F:/rnd/soft/PyCharm/bin/pycharm.exe"

    @staticmethod
    def initGrapherPath(graphPath, graphFolder, graphFile):
        """ Initialize grapher path
            @param graphPath: (str) : Current graph path
            @param graphFolder: (str) : 'tmp' or 'scripts'
            @param graphFile: (str) : Current graph file name
            @return: (str) : Graph path """
        if not os.path.exists(graphPath):
            print "!!! ERROR: Graph path not found %s !!!" % graphPath
        else:
            tmpPath = os.path.join(graphPath, graphFolder)
            if not os.path.exists(tmpPath):
                print "\t\t\tCreate folder '%s'" % graphFolder
                os.mkdir(tmpPath)
            tmpGraphPath = os.path.join(tmpPath, graphFile.replace('.py', ''))
            if not os.path.exists(tmpGraphPath):
                print "\t\t\tCreate folder '%s'" % graphFile.replace('.py', '')
                os.mkdir(tmpGraphPath)
            tmpUserPath = os.path.join(tmpGraphPath, grapher.user)
            if not os.path.exists(tmpUserPath):
                print "\t\t\tCreate folder '%s'" % grapher.user
                os.mkdir(tmpUserPath)
            return tmpUserPath

    @staticmethod
    def initGrapherBinPath(binType):
        """ Initialise Grapher bin path
            @param binType: (str) : 'studio', 'prod', or 'users' """
        binPath = os.path.join(grapher.binPath, binType)
        if not os.path.exists(grapher.binPath):
            raise IOError, "!!! ERROR: rndBin path not found, check __init__.py !!!"
        if not os.path.exists(binPath):
            print "[grapher] : Create %s" % binPath
            try:
                os.mkdir(binPath)
                return binPath
            except:
                raise IOError, "!!! ERROR: Can not create %s" % binPath

    @staticmethod
    def createMelFromPy(pyFile, iterators, iters):
        """ Create mel file for mayabath using pyScript
            @param pyFile: (str) : Python file
            @param iterators: (list) : Iterators list
            @param iters: (list) : Iter value list
            @return: (str) : Mel file """
        txt = []
        if not iterators:
            melFile = pyFile.replace('/scripts/', '/tmp/').replace('.py', '.mel')
        else:
            ext = 'mel'
            for n, iterator in enumerate(iterators):
                ext = '%s.%s' % (iters[n], ext)
                if isinstance(iters[n], str):
                    txt.append('python("%s = %r");' % (iterator, iters[n]))
                else:
                    txt.append('python("%s = %s");' % (iterator, iters[n]))
            melFile = pyFile.replace('/scripts/', '/tmp/').replace('.py', '.%s' % ext)
        txt.append('python("execfile(%r)");' % pyFile)
        try:
            pFile.writeFile(melFile, '\n'.join(txt))
            return melFile
        except:
            raise IOError, "!!! Error: Can't create %s !!!" % os.path.basename(melFile)

    @staticmethod
    def checkLoopTmpFile(tmpFile, loopType, **kwargs):
        """ Check given loopNode tmp file
            @param tmpFile: (str) : Loop check file absolut path
            @param kwargs: (dict) : Loop params to write
            @return: (bool): True if checkFile doesn't exists, False if exists """
        txt = []
        for k, v in kwargs.iteritems():
            txt.append('%s = %s' % (k, v))
        if not os.path.exists(tmpFile):
            result = FileCmds.createLoopTmpFile(tmpFile, txt)
            return result
        else:
            if not loopType == 'single':
                print "Info: %s already exists, skip iter" % os.path.basename(tmpFile)
                return False
            else:
                result = FileCmds.createLoopTmpFile(tmpFile, txt)
                return result

    @staticmethod
    def createLoopTmpFile(tmpFile, txt):
        """ create given loopNode tmp file
            @param tmpFile: (str) : Loop check file absolut path
            @param txt: (list) : Text to write
            @return: (bool): True if success """
        print "Info: Create %s" % os.path.basename(tmpFile)
        try:
            pFile.writeFile(tmpFile, '\n'.join(txt))
            print "Info: %s successfully created, Launch child nodes" % os.path.basename(tmpFile)
            return True
        except:
            raise IOError, "!!! Error: Can't create %s !!!" % os.path.basename(tmpFile)

    @staticmethod
    def createExternScript(tmpFile, script):
        """ Create tmp extern script
            @param tmpFile: (str) : Script tmp file
            @param script: (str) : Script
            @return: (bool) : True if success, else False """
        try:
            pFile.writeFile(tmpFile, script)
            return True
        except:
            raise IOError, "!!! Error: Can't create external script %s" % tmpFile

    @staticmethod
    def _defaultErrorDialog(message, parent):
        """ Launch default error dialog
            @param message: (str or list): Message to print
            @param parent: (object) : Parent ui """
        errorDial = QtGui.QErrorMessage(parent)
        if isinstance(message, list):
            errorDial.showMessage('\n'.join(message))
        else:
            errorDial.showMessage(message)

    @staticmethod
    def _fileErrorDialog(fileName, parent):
        """ Launch fileDialog error message
            @param fileName: (str) : Grapher absolut path
            @param parent: (object) : Parent ui """
        warn = ["!!! Warning: FileName Not Valide !!!", "Should have path/file.py",
                "Got %s" % fileName]
        errorDial = QtGui.QErrorMessage(parent)
        errorDial.showMessage('\n'.join(warn))

    @staticmethod
    def _fileLockErrorDialog(fileName, lockFile, parent):
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


class Style(object):
    """ Class used by grapher for style settings """

    def __init__(self):
        pass

    @property
    def lockColor(self):
        """ Lock background color
            @return: (str) : Red color """
        return "background-color:Tomato;"

    @property
    def graphBgc(self):
        """ GraphTree background color
            @return: (str) : Black color """
        return "background-color:Black;"

    @staticmethod
    def graphNodeBgc(nodeType):
        """ Graph node background color
            @param nodeType: (str) : 'modul', 'loop', 'sysData', 'cmdData', 'purData'
            @return: (str) : Background color """
        if nodeType == 'modul':
            return "background-color:LightGrey;"
        elif nodeType == 'loop':
            return "background-color:ForestGreen;"
        elif nodeType == 'sysData':
            return "background-color:PaleTurquoise;"
        elif nodeType == 'cmdData':
            return "background-color:CornFlowerBlue;"
        elif nodeType == 'purData':
            return "background-color:GreenYellow;"

    @property
    def graphInstanceBgc(self):
        """ Graph instance background color
            @return: (str) : Background color """
        return "background-color:Plum;"

    @property
    def graphExecNodeBgc(self):
        """ Graph execNode background color
            @return: (str) : Background color """
        return "background-color:Tomato;"

    @property
    def nodeEditorScriptFont(self):
        """ Node editor script font params
            @return: (object) : Qfont """
        scriptFont = QtGui.QFont()
        scriptFont.setFamily('Courier')
        scriptFont.setStyleHint(QtGui.QFont.Monospace)
        scriptFont.setFixedPitch(True)
        scriptFont.setPointSize(10)
        return scriptFont

    @property
    def nodeEditorScriptMetrics(self):
        """ Node editor script font metric
            @return: (object) : QFontMetrics """
        return QtGui.QFontMetrics(self.nodeEditorScriptFont)

    @property
    def nodeEditorNotesBgc(self):
        """ Node editor notes background color
            @return: (str) : Grey color """
        return "background-color:LightGrey;"
