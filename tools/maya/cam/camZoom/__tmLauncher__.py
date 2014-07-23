"""
Modul used by the ToolManager
"""

#-- Import And Reload --#
from tools.maya.cam import camZoom
from tools.maya.cam.camZoom.scripts import camZoomUi
reload(camZoom)
reload(camZoomUi)


#-- Tool Variables --#
camZoom.printToolInfo()
toolTask = "PROD"
toolComment = "Camera view helper."


#-- Launch Tool Ui --#
camZoomUi.launch()

