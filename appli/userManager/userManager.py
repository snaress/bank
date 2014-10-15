import os, shutil
from appli import userManager
from lib.system import procFile as pFile


class UserManager(object):
    """ UserManager class object
        @param logLvl: (str) : Log level ('critical', 'error', 'warning', 'info', 'debug') """

    def __init__(self, logLvl='info'):
        self.log = pFile.Logger(title="UM", level=logLvl)
        self.binPath = userManager.binPath
        self.nConvert = userManager.nConvert
        self.users = []

    def __dictToStr__(self, dataDict):
        """ Convert dict to writable string
            @param dataDict: (dict) : User datas
            @return: (str) : User datas """
        txt = []
        for k, v in dataDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    @property
    def userAttrs(self):
        """ Default user attributes
            @return: (list) : User attributes """
        return ['photo', 'logo', 'name', 'firstName', 'alias', 'userGrp', 'status']

    @property
    def userGroups(self):
        """ Default user groups
            @return: (list) : User groups """
        return ['admin', 'spvG', 'spv', 'devG', 'dev', 'td', 'lead', 'grpS', 'grp', 'prodG', 'prod']

    @property
    def userStatus(self):
        """ Default user status
            @return: (list) : User status """
        return ['active', 'off']

    def userList(self, asDict=False):
        """ Get  user list
            @param asDict: (bool) : If True, return dict instead of list
            @return: (list) or (dict) : User list """
        if asDict:
            userDict = {}
            for user in self.users:
                userDict[user.alias] = user.__getDict__
            return userDict
        else:
            userList = []
            for user in self.users:
                userList.append(user.alias)
            return userList

    def parse(self):
        """ Parse UserManager bdd """
        self.log.info("#-- Parsing bdd --#")
        self.users = []
        path = os.path.join(self.binPath, 'users')
        for user in os.listdir(path) or []:
            userPath = os.path.join(path, user)
            if not user.startswith('.') and not user.startswith('_') and os.path.isdir(userPath):
                userFile = os.path.join(userPath, 'userData.py')
                if os.path.exists(userFile):
                    newNode = UserNode(userPath, userFile, self)
                    self.users.append(newNode)
        self.log.info("\t Parsing done.")

    def newUser(self, **kwargs):
        """ Create new user
            @param kwargs: (dict) : User Attributes
                @keyword name: (str) : User name
                @keyword firstName: (str) : User first name
                @keyword alias: (str) : User alias
                @keyword photo: (str) : User original photo absolute path
                @keyword logo: (str) : User original logo absolute path
                @keyword userGrp: (str) : User group
                @keyword status: (str) : 'active' or 'off'
            @return: (bool), (str) : True if success, Log text """
        self.log.info("#-- New User %s --#" % kwargs['alias'])
        #-- Check Alias --~#
        resultAlias, logAlias = self._checkNewAlias(kwargs['alias'])
        if not resultAlias:
            return resultAlias, logAlias
        else:
            #-- Check New User Path --#
            newPath = os.path.join(self.binPath, 'users', kwargs['alias'])
            resultPath, logPath = self._checkNewPath(newPath)
            if not resultPath:
                return resultPath, logPath
            else:
                #-- Create New User Folder --#
                resultFld, logFld = self._createNewFld(newPath)
                if not resultFld:
                    return resultFld, logFld
                else:
                    #-- Create New User File --#
                    userFile = os.path.join(newPath, "userData.py")
                    datas = self.__dictToStr__(self._checkUserDict(kwargs))
                    try:
                        pFile.writeFile(userFile, datas)
                        log = "New user file successfully created: %s" % kwargs['alias']
                        self.log.info(log)
                        #-- Update data --#
                        self.parse()
                        return True, log
                    except:
                        error = "Can not create new user file: %s" % kwargs['alias']
                        self.log.error(error)
                        return False, error

    def getNodeFromAlias(self, alias):
        """ Get userNode from given alias
            @param alias: (str) : User alias
            @return: (object) : User node """
        for user in self.users:
            if user.alias == alias:
                return user
        self.log.warning("User %r not found !!!" % alias)

    def _checkNewAlias(self, alias):
        """ Check if new alias is valid
            @param alias: (str) : Alias
            @return: (bool), (str) : True if success, Log text """
        self.log.debug("\t Checking new alias ...")
        if alias in ['', ' '] or alias is None:
            error = "Alias can not be empty !!!"
            self.log.error(error)
            return False, error
        else:
            for user in self.users:
                if user.alias == alias:
                    error = "Alias %r already exists !!!" % alias
                    self.log.error(error)
                    return False, error
        return True, "Alias is valide."

    def _checkNewPath(self, path):
        """ Check if new path is valid
            @param path: (str) : User absolute path
            @return: (bool), (str) : True if success, Log text """
        self.log.debug("\t Checking new path ...")
        if os.path.exists(path):
            error = "User path %s already exists !!!" % path
            self.log.error(error)
            return False, error
        return True, "Path is valide."

    def _createNewFld(self, path):
        """ Create new user folder
            @param path: (str) : New user absolute path
            @return: (bool), (str) : True if success, Log text """
        try:
            os.mkdir(path)
            log = "Creating folder %s ..." % os.path.basename(path)
            self.log.info(log)
            return True, log
        except:
            error = "Can not create folder %s !!!" % os.path.basename(path)
            self.log.error(error)
            return False, error

    def _checkUserDict(self, kwargs):
        """ Check if user dict is valid
            @param kwargs: (dict) : User Attributes
            @return: (dict) : User Attributes """
        self.log.debug("\t Checking new user dict ...")
        for attr in self.userAttrs:
            if not attr in kwargs.keys():
                kwargs[attr] = ""
        return kwargs


class UserNode(object):
    """ UserNode class object
        @param userPath: (str) : User dir absolute path
        @param userFile: (str) : User file absolute path
        @param parent: (object) : UserManager class object """

    def __init__(self, userPath, userFile, parent):
        self._parent = parent
        self._userPath = userPath
        self._userFile = userFile
        self.storeData()

    @property
    def __getDict__(self):
        """ Get user data dict
            @return: (dict) : User data """
        data = {}
        for k, v in self.__dict__.iteritems():
            if not k.startswith('_'):
                data[k] = v
        return data

    @property
    def __getStr__(self):
        """ Convert user data dict into writable string
            @return: (str) : User data """
        txt = []
        for k, v in self.__getDict__.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def storeData(self):
        """ Store user data from file into userNode class object """
        if os.path.exists(self._userFile):
            data = pFile.readPyFile(self._userFile)
            for k, v in data.iteritems():
                setattr(self, k, v)

    def updateData(self, **kwargs):
        """ Store user data from given dict into userNode class object
            @param kwargs: (dict) : User data
                @keyword name: (str) : User name
                @keyword firstName: (str) : User first name
                @keyword alias: (str) : User alias
                @keyword photo: (str) : User original photo absolute path
                @keyword logo: (str) : User original logo absolute path
                @keyword userGrp: (str) : User group
                @keyword status: (str) : 'active' or 'off' """
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self._parent.log.warning("%s not found, skip !!!" % k)

    def updateIcone(self, imaType):
        """ Convert original image to thumbnail icone
            @param imaType: (str) : 'photo' or 'logo' """
        convert = False
        ima = os.path.normpath(getattr(self, imaType))
        icone = os.path.normpath(os.path.join(self._userPath, '%s.png' % imaType))
        if not os.path.exists(icone):
            convert = True
        else:
            if os.path.exists(ima):
                if os.path.getmtime(ima) < os.path.getmtime(icone):
                    convert = True
                else:
                    self._parent.log.debug("Icone %s is up to date, skip." % imaType)
        if convert and os.path.exists(ima):
            os.system("%s -out png -ratio -resize 150 150 -overwrite -o %s %s" % (self._parent.nConvert,
                                                                                  icone, ima))

    def writeData(self):
        """ Write user data file
            @return: (bool), (str) : True if success, log text """
        try:
            pFile.writeFile(self._userFile, self.__getStr__)
            log = "User file successfully written: %s" % getattr(self, 'alias')
            self._parent.log.info(log)
            return True, log
        except:
            error = "Can not write user file: %s" % getattr(self, 'alias')
            self._parent.log.error(error)
            return False, error

    def remove(self):
        """ Remove user
            @return: (bool), (str) : True if success, log text """
        try:
            shutil.rmtree(self._userPath)
            log = "User successfully removed: %s" % getattr(self, 'alias')
            self._parent.log.info(log)
            return True, log
        except:
            error = "Can not remove user: %s" % getattr(self, 'alias')
            self._parent.log.error(error)
            return False, error

    def printData(self):
        """ Print user data """
        print "\n#----- UserNode: %s -----#" % getattr(self, 'alias')
        for attr in self._parent.userAttrs:
            if attr in self.__getDict__.keys():
                print attr, '=', self.__getDict__[attr]
            else:
                print attr, '=', None


if __name__ == '__main__':
    um = UserManager()
    um.parse()
    for user in um.users:
        user.printData()
#     users = um.userList()
#     for user in users:
#         print user
#     um.getNodeFromAlias('tt').remove()
