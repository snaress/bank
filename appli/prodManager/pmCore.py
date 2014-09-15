import os
from lib.system import procFile as pFile


typoExclusion = [' ', '  ', '__', '--', '/', '\\', ':', '.']


class Loader(object):

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
        pathResult = self.createNewProdfolder(prodPath, prodAlias, prodName, raiseError=raiseError)
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
    def createNewProdfolder(prodPath, prodAlias, prodName, raiseError=False):
        """ Create New prod into dataBase
            @param prodPath: (str) : DataBase prod path
            @param prodAlias: (str) : Alias name
            @param prodName: (str) : Prod name
            @param raiseError: (bool) : Raise error if True, Return error if False
            @return: (str or bool) : Result """
        try:
            os.mkdir(prodPath)
            print "New prod folder successfully created: %s--%s" % (prodAlias, prodName)
            return True
        except:
            error = "Can not create folder: %s" % prodPath
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error

    @staticmethod
    def createNewProdFile(prodPath, prodAlias, prodName, raiseError=False):
        """ Create New prod into dataBase
            @param prodPath: (str) : DataBase prod path
            @param prodAlias: (str) : Alias name
            @param prodName: (str) : Prod name
            @param raiseError: (bool) : Raise error if True, Return error if False
            @return: (str or bool) : Result """
        txt = ["prodAlias = %r" % prodAlias, "prodName = %r" % prodName,
               "prodStartDate = '%s'" % pFile.getDate().replace('_', '/'),
               "prodStopDate = '%s'" % pFile.getDate().replace('_', '/'),
               "prodWorkDir = None", "prodSteps = {'_order': []}",
               "prodTasks = {'_order': []}", "prodTrees = []"]
        fileName = os.path.join(prodPath, "%s--%s.py" % (prodAlias, prodName))
        try:
            pFile.writeFile(fileName, '\n'.join(txt))
            print "New prod file successfully created: %s--%s.py" % (prodAlias, prodName)
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
            print "New pref file successfully created: %s" % fileName
            return True
        except:
            error = "Can not create pref file: %s" % fileName
            if raiseError:
                raise IOError, "[pmCore] | ERROR | %s" % error
            else:
                return "error__%s" % error
