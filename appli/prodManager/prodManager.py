import os
from appli import prodManager
from lib.system import procFile as pFile


class ProdManager(object):
    """ Class used by ProdManagerUi. Can be used in standAlone
        @param prodId: (str) : Project Id
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, prodId=None, logLvl='info'):
        self.log = pFile.Logger(title="PM", level=logLvl)
        self._prodId = prodId
        self._prodPath = os.path.join(prodManager.binPath, 'prod')
        if self._prodId is not None:
            self.loadProd()

    def __getDict__(self):
        prodDict = {}
        for k, v in self.__dict__.iteritems():
            if not k.startswith('_') and k.startswith('prod'):
                prodDict[k] = v
        return prodDict

    def __getStr__(self):
        prodDict = self.__getDict__()
        txt = []
        for k, v in prodDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def loadProd(self, prodId=None):
        if prodId is None and self._prodId is None:
            raise KeyError, "[PM] | Error | prodId and _prodId can't be None."
        if prodId is None:
            prodId = self._prodId
        self.log.info("Loading project %r ..." % prodId)
        self._prodId = prodId
        self._prodFile = os.path.join(self._prodPath, self._prodId, "%s.py" % self._prodId)
        if not os.path.exists(self._prodFile):
            raise KeyError, "[PM] | Error | Prod id not found: %r." % self._prodId
        self.log.info("Parsing project ...")
        self._parseProdFile()

    def _parseProdFile(self):
        self.log.debug("Parsing prod file ...")
        prodDict = pFile.readPyFile(self._prodFile)
        for k, v in prodDict.iteritems():
            setattr(self, k, v)

    def listAllProds(self, printEnabled=False):
        prods = os.listdir(self._prodPath) or []
        if printEnabled:
            print "\n#-- Listing All Prods --#"
            for prod in prods:
                print '\t', prod
        return os.listdir(self._prodPath) or []

    def printDict(self):
        print "\n#----- ProdManager Dict -----#"
        print self.__getStr__()
        print "#----------------------------#\n"


class ProdTree(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __getDict__(self):
        return self.__dict__

    def __getStr__(self):
        treeDict = self.__getDict__()
        txt = []
        for k, v in treeDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)



if __name__ == '__main__':
    pm = ProdManager(prodId='lv--LeVoeu', logLvl='debug')
    pm.printDict()
