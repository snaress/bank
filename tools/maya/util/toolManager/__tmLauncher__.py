"""
Modul used by the ToolManager
"""
import os
import sys


print "#-- Check SysPath --#"
libPath = os.path.join('F:', os.sep, 'rnd', 'lib')
bankPath = os.path.join('F:', os.sep, 'rnd', 'workspace', 'bank')
for path in [libPath, bankPath]:
    if not path in sys.path:
        print "Add %s in sysPath ..." % path
        sys.path.insert(0, path)


print "#-- Import And Reload --#"
from tools.maya.util import toolManager
from tools.maya.util.toolManager.scripts import toolManagerUi
from tools.maya.util.toolManager.scripts import uiRefresh
reload(toolManager)
reload(toolManagerUi)
reload(uiRefresh)
print 'end reload'
toolManager.printToolInfo()


print "#-- Launch Tool Ui --#"
# global window
window = toolManagerUi.ToolManagerUi()
window.show()
