import os
import sys
import shutil

wsPath = 'F:/rnd/workspace/bank'
if not wsPath in sys.path:
    sys.path.insert(0, wsPath)

from lib import env as libEnv


def syncAlias():
    """ Copy alias file from bank to user path """
    #-- Get Path --#
    aliasPath = os.path.normpath(libEnv.toolPath)
    aliasFile = os.path.join(aliasPath, '_lib', 'alias', 'alias.txt')
    user = os.environ.get('username')
    userPath = os.path.join('C:', os.sep, 'Users', user)
    userFile = os.path.join(userPath, 'alias.txt')
    #-- Verif User Path --#
    if not os.path.exists(userPath):
        print "!!! WARNING: User path doesn't exists !!!"
    else:
        print "\n##### ALIAS SYNC #####"
        print "Copy %s to %s" % (aliasFile, userFile)
        shutil.copy(aliasFile, userFile)


if __name__ == '__main__':
    syncAlias()