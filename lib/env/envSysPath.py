import os, sys

print "\n#-- Env Sys Path --#"
toolPath = os.path.normpath(os.path.dirname(__file__))
wsPath = os.sep.join(toolPath.split(os.sep)[:-2])
if not wsPath in sys.path:
    print "[sys] | Info | Add %s to sysPath\n" % wsPath
    sys.path.insert(0, wsPath)

