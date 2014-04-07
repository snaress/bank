"""
Modul used by the ToolManager
"""


print "#-- Import And Reload --#"
from tools.maya.anim import noiseAnimCurve
from tools.maya.anim.noiseAnimCurve.scripts import noiseAnimCurveUi
reload(noiseAnimCurve)
reload(noiseAnimCurveUi)
noiseAnimCurve.printToolInfo()


print "#-- Tool Variables --#"
toolTask = "WIP"
toolComment = "Tool editing selected anim curve with noise."


print "#-- Launch Tool Ui --#"
# global window
window = noiseAnimCurveUi.NoiseAnimCurveUi()
window.show()
