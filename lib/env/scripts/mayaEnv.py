import os
import sys


def editSysPath():
    print "#-- Check SysPath --#"
    libPath = os.path.join('F:', os.sep, 'rnd', 'lib')
    bankPath = os.path.join('F:', os.sep, 'rnd', 'workspace', 'bank')
    for path in [libPath, bankPath]:
        if not path in sys.path:
            print "Add %s in sysPath ..." % path
            sys.path.insert(0, path)

editSysPath()