"""
Modul used by the ToolManager
"""

#-- Import And Reload --#
from tools.maya.anim import noiseAnimCurve
from tools.maya.anim.noiseAnimCurve.scripts import noiseAnimCurveUi
from tools.maya.anim.noiseAnimCurve.scripts import cmds as tmCmds
from lib.qt.scripts import procQt as pQt
reload(noiseAnimCurve)
reload(noiseAnimCurveUi)
reload(tmCmds)
reload(pQt)


#-- Tool Variables --#
noiseAnimCurve.printToolInfo()
toolTask = "WIP"
toolComment = "Tool adding noise on selected anim curve."


#-- Launch Tool Ui --#
window = noiseAnimCurveUi.NoiseAnimCurveUi()
window.show()
