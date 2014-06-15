import os, time
from appli import grapher
from lib.system.scripts import procFile as pFile


class FileCmds(object):

    @staticmethod
    def createLockFile(lockFile):
        """ Create lockFile
            @param lockFile: (str) : LockFile absolut path
            @return: (bool) : True if success, False if failed """
        lockTxt = ["user = %r" % grapher.user,
                   "station = %r" % grapher.station,
                   "date = %r" % time.strftime("%Y/%m/%d", time.localtime()),
                   "time = %r" % time.strftime("%H:%M:%S", time.localtime())]
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
                raise IOError, "!!! Error: Can't remove lockFile: %s" % lockFile
        else:
            raise IOError, "!!! Error: LockFile not found: %s" % lockFile
