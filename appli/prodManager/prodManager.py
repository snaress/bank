import os, shutil
from appli import prodManager
from appli.prodManager import pmCore
from lib.system import procFile as pFile


class ProdManager(object):
    """ Class used by ProdManagerUi. Can be used in standAlone
        @param prodId: (str) : Project Id
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, prodId=None, logLvl='info'):
        self.log = pFile.Logger(title="PM", level=logLvl)
        self._prodId = prodId
        self._prodPath = os.path.join(prodManager.binPath, 'prod')
        self._treePath = None
        self._prodFile = None
        if self._prodId is not None:
            self.loadProd()

    def __getDict__(self):
        """ Get prod params writtable dict
            @return: (dict) : Prod params """
        prodDict = {}
        for k, v in self.__dict__.iteritems():
            if not k.startswith('_') and k.startswith('prod'):
                prodDict[k] = v
        return prodDict

    def __getStr__(self):
        """ Get prod params writtable string
            @return: (str) : Prod Params """
        prodDict = self.__getDict__()
        txt = []
        for k, v in prodDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def loadProd(self, prodId=None):
        """ Load given project
            @param prodId: (str) : prodId """
        if prodId is None and self._prodId is None:
            raise KeyError, "[PM] | Error | prodId and _prodId can't be None."
        if prodId is None:
            prodId = self._prodId
        self.log.info("Loading project %r ..." % prodId)
        self._prodId = prodId
        self._treePath = os.path.join(self._prodPath, self._prodId, 'tree')
        self._prodFile = os.path.join(self._prodPath, self._prodId, "%s.py" % self._prodId)
        if not os.path.exists(self._prodFile):
            raise KeyError, "[PM] | Error | Prod id not found: %r." % self._prodId
        self.log.info("Parsing project ...")
        self._parseProject()

    def writeProject(self):
        """ Write project file """
        self.log.info("Writing project params ...")
        try:
            pFile.writeFile(self._prodFile, self.__getStr__())
            self.log.debug("Project params successfully written.")
        except:
            self.log.error("Can't write project params: %s" % self._prodFile)
            raise IOError, "[PM] | Error | Can't write project params: %s" % self._prodFile

    def writeShotData(self, dataFile, data):
        """ Write Shot data file
            @param dataFile: (str) : Data file absolut path
            @param data: (str) : Shot data """
        root = os.path.join(self._prodPath, self._prodId)
        if pmCore.Manager.checkDataPath(root, os.path.dirname(dataFile)):
            shotNode = os.path.basename(dataFile).replace('.py', '')
            try:
                pFile.writeFile(dataFile, data)
                self.log.info("Data Successfully written: %s" % shotNode)
            except:
                self.log.error("Can't write data: %s" % shotNode)
                raise IOError, "[PM] | Error | Can't write data: %s" % shotNode

    def writeLineTest(self, ltFile, data):
        """ Write LineTest data file
            @param ltFile: (str) : LineTest file absolut path
            @param data: (str) : LineTest data
            @return: (bool) : True if success """
        root = os.path.join(self._prodPath, self._prodId)
        if pmCore.Manager.checkDataPath(root, os.path.dirname(ltFile)):
            try:
                pFile.writeFile(ltFile, data)
                self.log.info("LineTest Successfully written")
                return True
            except:
                self.log.error("Can't write lineTest")
                raise IOError, "[PM] | Error | Can't write lineTest !!!"

    @staticmethod
    def editLtDateTime(ltFile, data):
        """ Write LineTest data file
            @param ltFile: (str) : LineTest file absolut path
            @param data: (dict) : LineTest data """
        oldLtPath = os.path.dirname(pFile.conformPath(ltFile))
        newFolder = "lt__%s__%s" % (data['ltDate'], data['ltTime'])
        path = os.sep.join(os.path.dirname(pFile.conformPath(ltFile)).split('/')[:-1])
        ltPath = os.path.join(path, newFolder)
        if not os.path.exists(ltPath):
            os.rename(oldLtPath, ltPath)
            return ltPath

    def deleteLt(self, ltPath):
        """ Delete given lineTest
            @param ltPath: (str) : LineTest path
            @return: (bool) : True if success """
        lt = '/'.join(pFile.conformPath(ltPath).split('/')[-2:])
        self.log.info("Deleting lineTest %s ..." % lt)
        if os.path.exists(ltPath):
            try:
                shutil.rmtree(ltPath)
                self.log.info("\t LineTest %s deleted." % lt)
                return True
            except:
                self.log.error("Can't delete lineTest %s" % lt)
                raise IOError, "[PM] | Error | Can't delete lineTest %s !!!" % lt

    def _parseProject(self):
        """ Parse project """
        self.log.debug("Parsing prod file ...")
        prodDict = pFile.readPyFile(self._prodFile)
        for k, v in prodDict.iteritems():
            setattr(self, k, v)

    def listAllProds(self, _print=False):
        """ List all prods
            @param _print: (bool) : Print result
            @return: (list) : prodId list """
        prods = os.listdir(self._prodPath) or []
        prodList = []
        if _print:
            print "\n#-- Listing All Prods --#"
            for prod in prods:
                absPath = os.path.join(self._prodPath, prod)
                if os.path.isdir(absPath):
                    print '\t', prod
                    prodList.append(prod)
        return prodList

    def printDict(self):
        """ Print current params """
        print "\n#----- ProdManager Dict -----#"
        print self.__getStr__()
        print "#----------------------------#\n"


if __name__ == '__main__':
    pm = ProdManager(prodId='lv--Le_Voeu', logLvl='debug')
    pm.printDict()
