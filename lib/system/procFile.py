import os, sys, math, time, logging, subprocess


def conformPath(path):
    """ Comform path separator with '/'
        @param path: (str) : Path to conform
        @return: (str) : Conformed path """
    return path.replace('\\', '/')

def pathToDict(path):
    """ Translate directory contents to dict
        @param path: (str) : Absolut path
        @return: (dict) : Path contents """
    if not os.path.exists(path):
        raise IOError, "!!! ERROR: Path not found!!!\n%s" % path
    pathDict = {'_order': []}
    for root, flds, files in os.walk(path):
        pathDict['_order'].append(root)
        pathDict[root] = {'folders': flds, 'files': files}
    return pathDict

def mkPathFolders(rootPath, absPath, sep=None):
    """ Create absPath folders not in rootPath
        @param rootPath: (str) : Root path
        @param absPath: (str) : Absolut Path
        @param sep: (str) : Os separator """
    if not os.path.exists(rootPath):
        raise IOError, "!!! ERROR: rootPath not found !!!"
    if sep is None:
        sep = os.sep
    relPath = absPath.replace('%s%s' % (rootPath, sep), '')
    checkPath = rootPath
    for fld in relPath.split(sep):
        checkPath = "%s%s%s" % (checkPath, sep, fld)
        if not os.path.exists(checkPath):
            print "[sysInfo] : Create folder %s in %s" % (fld, sep.join(checkPath.split(sep)[:-1]))
            try:
                os.mkdir(checkPath)
            except:
                raise IOError, "!!! ERROR: Can not create %s !!!" % checkPath

def readFile(filePath):
    """ Get text from file
        @param filePath: (str) : File absolut path
        @return: (list) : Text line by line """
    if not os.path.exists(filePath):
        raise IOError, "!!! Error: Can't read, file doesn't exists !!!"
    fileId = open(filePath, 'r')
    getText = fileId.readlines()
    fileId.close()
    return getText

def readPyFile(filePath, filterIn=None, keepBuiltin=False):
    """ Get text from pyFile
        @param filePath: (str) : Python file absolut path
        @param filterIn: (list) : Keep only key starting with filterIn
        @param keepBuiltin: (bool) : Keep builtins key
        @return: (dict) : File dict """
    if not os.path.exists(filePath):
        raise IOError, "!!! Error: Can't read, file doesn't exists !!!"
    params = {}
    execfile(filePath, params)
    if filterIn is None:
        if keepBuiltin:
            return params
        else:
            if '__builtins__' in params.keys():
                params.pop('__builtins__')
                return params
    else:
        filterParams = {}
        for k, v in params.iteritems():
            check = False
            for ft in filterIn:
                if k.startswith(ft):
                    check = True
                    break
            if check:
                filterParams[k] = v
        if keepBuiltin:
            return filterParams
        else:
            if '__builtins__' in filterParams.keys():
                filterParams.pop('__builtins__')
                return filterParams

# noinspection PyTypeChecker
def writeFile(filePath, textToWrite, add=False):
    """ Create and edit text file. If file already exists, it is overwritten
        @param filePath: (str) : File absolut path
        @param textToWrite: (str or list) : Text to edit in file
        @param add: (bool) : Add text to existing one in file """
    oldTxt = ""
    if add:
        oldTxt = ''.join(readFile(filePath))
        if not oldTxt.endswith('\n'):
            oldTxt = "%s\n" % oldTxt
    fileId = open(filePath, 'w')
    if add:
        fileId.write(oldTxt)
    if isinstance(textToWrite, basestring):
        fileId.write(textToWrite)
    elif isinstance(textToWrite, (list, tuple)):
        fileId.writelines(textToWrite)
    fileId.close()

def fileSizeFormat(bytes, precision=2):
    """ Returns a humanized string for a given amount of bytes
        @param bytes: (int) : File size in bytes
        @keyword precision: (int) : Precision after coma
        @return: (str) : Humanized string """
    bytes = int(bytes)
    if bytes is 0:
        return '0 b'
    log = math.floor(math.log(bytes, 1024))
    return "%.*f %s" % (precision, bytes / math.pow(1024, log),
                       ['b', 'kb', 'mb', 'gb', 'tb','pb', 'eb', 'zb', 'yb'][int(log)])

def secondsToStr(seconds):
    """ Convert number of seconds into humanized string
        @param seconds: (int) : Number of seconds
        @return: (str) : Humanized string """
    S = int(seconds)
    hours = S / 3600
    S = S - (hours * 3600)
    minutes = S / 60
    seconds = S - (minutes * 60)
    return "%s:%s:%s" % (hours, minutes, seconds)

def getDate():
    """ Get current date
        @return: (str) : yyyy_mm_dd """
    return time.strftime("%Y_%m_%d")

def getTime():
    """ Get current time
        @return: (str) : hh_mm_ss """
    return time.strftime("%H_%M_%S")

def dRange(start, stop, step, preci=3):
    """ Get decimal range list
        @param start: (float) : Range start
        @param stop: (float) : Range stop
        @param step: (float) : Range step
        @param preci: (int) : Decimals
        @return: (list) : Range list """
    iters = []
    rangeStart = start
    rangeStop = stop
    rangeStep = step
    if isinstance(rangeStart, float) or isinstance(rangeStop, float) or isinstance(rangeStep, float):
        r = rangeStart
        while r < rangeStop:
            iters.append(str(round(r, preci)))
            r += rangeStep
    else:
        for r in range(rangeStart, (rangeStop + 1), rangeStep):
            iters.append(r)
    return iters

def subProcessPrint(process, errorFilters, errorMessages, force=False):
    """ Print subprocess.Popen stdout in real time
        @param process: (object) : Subprocess
        @param errorFilters: (list) : String error filters
        @param errorMessages: (list) : Text error
        @param force: (bool) : Dont use filters if True """
    while True:
        checkProc = True
        for stdOutLine in iter(process.stdout.readline, ""):
            if not force:
                for n, err in enumerate(errorFilters):
                    if err in stdOutLine:
                        print "# PROCESS ERROR : %s" % errorMessages[n]
                        checkProc = False
                if checkProc:
                    sys.stdout.write(stdOutLine)
            else:
                sys.stdout.write(stdOutLine)
        if process.poll() is not None:
            break


class Logger(logging.Logger):
    """ Print given message with log levels
        @param title: (str) : Log title
        @param level: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, title='LOG', level='info'):
        self._level = self._setLevel(level)
        super(Logger, self).__init__(title, level=self._level)
        self.addHandler(self._setFormat())

    def _setFormat(self):
        """ Set log format
            @return: (object) : Log streamHandler """
        console = logging.StreamHandler()
        console.setLevel(self._level)
        formatter = logging.Formatter('[%(name)s] | %(levelname)s | %(message)s')
        console.setFormatter(formatter)
        return console

    def _setLevel(self, lvl):
        """ Set log level
            @param lvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug')
            @return: (object) : Log level
        """
        if lvl == 'critical':
            return logging.CRITICAL
        elif lvl == 'error':
            return logging.ERROR
        elif lvl == 'warning':
            return logging.WARNING
        elif lvl == 'info':
            return logging.INFO
        elif lvl == 'debug':
            return logging.DEBUG


class Image(object):
    """ Class to manipulate image or get info from file """

    djvInfo = os.path.normpath("C:/Program Files/djv-1.0.2-Windows-64/bin/djv_info.exe")
    djvList = os.path.normpath("C:/Program Files/djv-1.0.2-Windows-64/bin/djv_ls.exe")
    djvConvert = os.path.normpath("C:/Program Files/djv-1.0.2-Windows-64/bin/djv_convert.exe")
    nConvert = "F:/rnd/worspace/bank/lib/system/_lib/nConvert/nconvert.exe"

    def __init__(self):
        pass

    def getInfo(self, path, options=None, returnAs='dict'):
        """ get image file info
            @param path: (str) : Directory or image file absolute path
            @param options: (list) : Options from djv_info.exe
            @param returnAs: (str) : 'dict' or 'str'
            @return: (dict or str) : Image file info """
        proc = self._getInfoProc(path, options)
        result = proc.communicate()[0]
        if not result.startswith('[ERROR]'):
            info = self._getInfoDict(result, path)
            if returnAs == 'dict':
                return info
            elif returnAs == 'str':
                return self._getInfoString(result, path)

    def _getInfoProc(self, path, options):
        """ Get info subprocess cmdArgs
            @param path: (str) : Directory or image file absolute path
            @param options: (list) : Options from djv_info.exe
            @return: (object) : Subprocess """
        cmd = [self.djvInfo, os.path.normpath(path)]
        if options is not None:
            for opt in options:
                cmd.append(opt)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return proc

    def _getInfoDict(self, result, path):
        """ Translate info subprocess result to dict
            @param result: Subprocess result
            @param path: (str) : Directory or image file absolute path
            @return: (dict) : Info dict """
        info = {'_order': []}
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        for line in result.split('\r'):
            l = line.strip().replace('\n', '')
            if not l == '' or l == ' ':
                datas = self._cleanResultLine(l)
                info['_order'].append(datas[0])
                info[datas[0]] = {'name': datas[0], 'path': path,
                                  'width': datas[1].split(':')[0].split('x')[0],
                                  'height': datas[1].split(':')[0].split('x')[1],
                                  'ratio': datas[1].split(':')[1],
                                  'channel': datas[2],
                                  'depth': datas[3].replace('U', ''),
                                  'duration': datas[4].split('@')[0],
                                  'speed': datas[4].split('@')[1]}
        return info

    # noinspection PyTypeChecker
    def _getInfoString(self, result, path):
        """ Translate info subprocess result to string
            @param result: Subprocess result
            @param path: (str) : Directory or image file absolute path
            @return: (str) : Info string """
        txt = []
        infoOrder = ['path', 'name', 'width', 'height', 'ratio', 'channel', 'depth',
                     'duration', 'speed']
        infoDict = self._getInfoDict(result, path)
        for ima in infoDict['_order']:
            txt.append("#-- %s --#" % ima)
            for info in infoOrder:
                if isinstance(infoDict[ima][info], str):
                    txt.append("%s = %r" % (info, infoDict[ima][info]))
                else:
                    txt.append("%s = %s" % (info, infoDict[ima][info]))
        return '\n'.join(txt)

    def _cleanResultLine(self, line):
        """ Get clean line from result line
            @param line: (str) : result line
            @return: (list) : Clean line args """
        datas = line.split(' ')
        cleanLine = []
        for n in range(len(datas)):
            if not datas[n] == '':
                cleanLine.append(datas[n])
        return cleanLine


class ProgressBar(object):
    """ Create a progress bar
        @param valMax: (int) : Max iteration
        @param maxBar: (int) : Max bar size
        @param title: (str) : Progress bar title """

    def __init__(self, valMax, maxBar, title):
        if valMax == 0:
            valMax = 1
        if maxBar > 200:
            maxBar = 200
        self.valMax = valMax
        self.maxBar = maxBar
        self.title = title

    def update(self, val):
        """ Update progress bar
            @param val: (int) : Progress bar iteration """
        if val > self.valMax:
            val = self.valMax
        perc = round((float(val) / float(self.valMax)) * 100)
        scale = 100.0 / float(self.maxBar)
        bar = int(perc / scale)
        out = "\r %10s [%s%s] %3d %%" % (self.title, '=' * bar, ' ' * (self.maxBar - bar), perc)
        sys.stdout.write(out)
