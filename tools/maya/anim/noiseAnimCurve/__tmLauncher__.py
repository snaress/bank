"""
Modul used by the ToolManager
"""

#-- Import And Reload --#
from tools.maya.anim import noiseAnimCurve
from tools.maya.anim.noiseAnimCurve.scripts import noiseAnimCurveUi
reload(noiseAnimCurve)
reload(noiseAnimCurveUi)


#-- Tool Variables --#
noiseAnimCurve.printToolInfo()
toolTask = "WIP"
toolComment = "Tool editing selected anim curve with noise."


#-- Launch Tool Ui --#
# global window
window = noiseAnimCurveUi.NoiseAnimCurveUi()
window.show()
