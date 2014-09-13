import os, shutil

toolPath = os.path.normpath(os.path.dirname(__file__))
envFile = os.path.join(toolPath, 'envSysPath.py')
execfile(envFile)

from lib import env as libEnv
def syncAlias():
    """ Copy alias file from bank to user path """
    #-- Get Path --#
    aliasPath = os.path.normpath(libEnv.toolPath)
    aliasFile = os.path.join(aliasPath, 'alias.txt')
    user = os.environ.get('username')
    userPath = os.path.join('C:', os.sep, 'Users', user)
    userFile = os.path.join(userPath, 'alias.txt')
    #-- Verif User Path --#
    if not os.path.exists(userPath):
        print "!!! WARNING: User path doesn't exists !!!"
    else:
        print "\n#-- Alias Sync --#"
        print "Copy %s to %s" % (aliasFile, userFile)
        shutil.copy(aliasFile, userFile)


if __name__ == '__main__':
    syncAlias()
