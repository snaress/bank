import os
import sys
import math


def readFile(filePath):
    """ Get text from file
        @param filePath: (str) : File absolut path
        @return: (list) : Text line by line """
    if os.path.exists(filePath):
        fileId = open(filePath, 'r')
        getText = fileId.readlines()
        fileId.close()
        return getText
    else:
        print "!!! Error: Can't read, file doesn't exists !!!"

def readPyFile(filePath):
    """ Get text from pyFile
        @param filePath: (str) : Python file absolut path
        @return: (dict) : File dict """
    if os.path.exists(filePath):
        params = {}
        execfile(filePath, params)
        return params
    else:
        print "!!! Error: Can't read, file doesn't exists !!!"

def writeFile(filePath, textToWrite, add=False):
    """ Create and edit text file. If file already exists, it is overwritten
        @param filePath: (str) : File absolut path
        @param textToWrite: (str or list) : Text to edit in file
        @param add: (bool) : Add text to existing one in file """
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


class PathToDict(object):
    """ Convert treePath to dict
        @param rootPath: (str) : Absolut path """

    def __init__(self, rootPath):
        self.rootPath = rootPath

    @property
    def getPathDict(self):
        """ Get path
            @return: (dict) : Root path contents """
        pathDict = {'root': [], 'flds': [], 'files': []}
        for root, folders, files in os.walk(self.rootPath):
            if self._verifPath(root):
                pathDict['root'].append(root)
                pathDict['flds'].append(self._getFolders(folders))
                pathDict['files'].append(self._getFiles(files))
        return pathDict

    def _verifPath(self, path):
        """ Check path validity
            @param path: (str) : Path to check
            @return: (bool) : True if valid, else False """
        for item in path.split(os.sep):
            if item.startswith('.'):
                return False
        return True

    def _getFolders(self, folders):
        """ Get valif folders
            @param folders: (list) : Folders list
            @return: (list) : Valid folders list """
        Lflds = []
        for fld in folders:
            if not fld.startswith('.'):
                Lflds.append(fld)
        return Lflds

    def _getFiles(self, files):
        """ Get valif files
            @param files: (list) : files list
            @return: (list) : Valid files list """
        Lfiles = []
        for f in files:
            if not f.startswith('.'):
                Lfiles.append(f)
        return Lfiles


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
