import os
from lib.system import procFile as pFile


typoExclusion = [' ', '  ', '__', '--', '/', '\\', ':', '.']


class Loader(object):
    """ Class used by ProdManager LoaderUi for project preload """

    def __init__(self):
        pass

    def createNewProd(self, rootPath, prodAlias, prodName, raiseError=False):
        """ Create New prod into dataBase
            @param rootPath: (str) : DataBase prods path
            @param prodAlias: (str) : Alias name
            @param prodName: (str) : Prod name
            @param raiseError: (bool) : Raise error if True, Return error if False
            @return: (str or bool) : Result """
        #-- Check Args --#
        for typo in typoExclusion:
            if typo in prodAlias or typo in prodName:
                error = "Special typo characters detected: %r | (%s)" % (typo, typoExclusion)
                if raiseError:
                    raise IOError, "[pmCore] | ERROR | %s" % error
                else:
                    return "error__%s" % error
        #-- Check Root Path --#
        if not os.path.exists(rootPath):
            error = "Root path not found: %s" % rootPath
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error
        #-- Check Prod Path --#
        prodPath = os.path.join(rootPath, "%s--%s" % (prodAlias, prodName))
        if os.path.exists(prodPath):
            error = "Prod already exists: %s--%s" % (prodAlias, prodName)
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error
        #-- Create Prod --#
        pathResult = self.createNewProdfolder(prodPath, raiseError=raiseError)
        if not isinstance(pathResult, bool):
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % pathResult
            else:
                return pathResult
        else:
            fileResult = self.createNewProdFile(prodPath, prodAlias, prodName, raiseError=raiseError)
            if not isinstance(fileResult, bool):
                if raiseError:
                    raise IOError, "[pmCore] | ERROR | %s" % fileResult
                else:
                    return fileResult
            else:
                return True

    @staticmethod
    def createNewProdfolder(prodPath, raiseError=False):
        """ Create New prod into dataBase
            @param prodPath: (str) : DataBase prod path
            @param raiseError: (bool) : Raise error if True, Return error if False
            @return: (str or bool) : Result """
        try:
            os.mkdir(prodPath)
            return True
        except:
            error = "Can not create folder: %s" % prodPath
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error

    def createNewProdFile(self, prodPath, prodAlias, prodName, raiseError=False):
        """ Create New prod into dataBase
            @param prodPath: (str) : DataBase prod path
            @param prodAlias: (str) : Alias name
            @param prodName: (str) : Prod name
            @param raiseError: (bool) : Raise error if True, Return error if False
            @return: (str or bool) : Result """
        treeDict = {'steps': [], 'tree': {'_order': []}, 'attr': {'_order': []}}
        txt = ["prodAlias = %r" % prodAlias, "prodName = %r" % prodName,
               "prodStartDate = '%s'" % pFile.getDate().replace('_', '/'),
               "prodStopDate = '%s'" % pFile.getDate().replace('_', '/'),
               "prodWorkDir = ''", "prodTasks = %s" % self.defaultTasks(),
               "prodTrees = {'_order': ['asset', 'shot'], 'asset': %s, 'shot': %s}" % (treeDict, treeDict)]
        fileName = os.path.join(prodPath, "%s--%s.py" % (prodAlias, prodName))
        try:
            pFile.writeFile(fileName, '\n'.join(txt))
            return True
        except:
            error = "Can not create file: %s--%s.py" % (prodAlias, prodName)
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error

    @staticmethod
    def createPrefFile(fileName, raiseError=False):
        """ Create user pref file into data base
            @param fileName: (str) : User pref file absolut path
            @param raiseError: (bool) : Raise error if True, Return error if False
            @return: (str or bool) : Result """
        txt = "prodBookMarks = []\n"
        try:
            pFile.writeFile(fileName, txt)
            return True
        except:
            error = "Can not create pref file: %s" % fileName
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error

    @staticmethod
    def defaultTasks():
        """ Default tasks
            @return: (dict) : Task dict """
        return {'_order': ['Out', 'StandBy', 'ToDo', 'Retake', 'InProgress', 'Warning',
                           'WaitApproval', 'ToReview', 'Final'],
                'Out': {'color': (0, 0, 0), 'stat': False},
                'StandBy': {'color': (229, 229, 229), 'stat': True},
                'ToDo': {'color': (155, 232, 232), 'stat': True},
                'Retake': {'color': (255, 170, 0), 'stat': True},
                'InProgress': {'color': (255, 255, 0), 'stat': True},
                'Warning': {'color': (255, 0, 0), 'stat': True},
                'WaitApproval': {'color': (255, 85, 255), 'stat': True},
                'ToReview': {'color': (85, 85, 255), 'stat': True},
                'Final':{'color': (85, 255, 0), 'stat': True}}


class Manager(object):
    """ Class used by ProdManagerUi for project management """

    def __init__(self):
        pass

    @staticmethod
    def checkDataPath(rootDir, dataPath):
        """ Check if all folders of given path exists
            @param rootDir: (str) : Absolut path
            @param dataPath: (str) : Absolut path
            @return: (bool) : True if success """
        _rootDir = pFile.conformPath(rootDir)
        _dataPath = pFile.conformPath(dataPath)
        if not os.path.exists(_rootDir):
            raise IOError, "RootDir not found: %s" % _rootDir
        if not _dataPath.startswith(_rootDir):
            raise IOError, "RootDir and dataFile don't have the same rootDir: %s" % _rootDir
        checkPath = _dataPath.replace('%s/' % _rootDir, '')
        _check = _rootDir
        for fld in checkPath.split('/'):
            _check = os.path.join(os.path.normpath(_check), fld)
            if not os.path.exists(_check):
                try:
                    os.mkdir(_check)
                    print "Create folder %s" % _check
                except:
                    raise IOError, "Can no create folder %s" % _check
        return True
