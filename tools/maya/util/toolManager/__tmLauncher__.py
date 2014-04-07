"""
Modul used by the ToolManager
"""

#-- Import And Reload --#
from tools.maya.util import toolManager
from tools.maya.util.toolManager.scripts import toolManagerUi
from tools.maya.util.toolManager.scripts import uiRefresh
reload(toolManager)
reload(toolManagerUi)
reload(uiRefresh)


#-- Tool Variables --#
toolManager.printToolInfo()
toolTask = "DEV"
toolComment = "Tool showing the listing of all the maya tools."


#-- Launch Tool Ui --#
# global window
window = toolManagerUi.ToolManagerUi()
window.show()
