import os, sys


RND_PATH = os.path.join('F:', os.sep, 'rnd')
LIB_PATH = os.path.join(RND_PATH, 'lib')
WORKSPACE = os.path.join(RND_PATH, 'workspace')
WS_BANK = os.path.join(WORKSPACE, 'bank')
MAYA_VERSION = "2012"
MAYA_LOCATION = os.path.join("C:", os.sep, "Program Files", "Autodesk", "Maya%s" % MAYA_VERSION)

def editSysPath():
    print "\n#-- Edit SysPath --#"
    for path in [LIB_PATH, WS_BANK]:
        if not path in sys.path:
            print "Add %s to sysPath ..." % path
            sys.path.insert(0, path)


if __name__ == '__main__':
    editSysPath()
