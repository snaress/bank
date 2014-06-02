import os, sys


def editSysPath():
    print "\n#-- Check SysPath --#"
    libPath = os.path.join('F:', os.sep, 'rnd', 'lib')
    bankPath = os.path.join('F:', os.sep, 'rnd', 'workspace', 'bank')
    for path in [libPath, bankPath]:
        if not path in sys.path:
            print "Add %s to sysPath ..." % path
            sys.path.insert(0, path)


if __name__ == '__main__':
    editSysPath()
