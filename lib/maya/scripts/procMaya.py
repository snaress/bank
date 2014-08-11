try:
    import maya.cmds as mc
except:
    pass


def loadMentalRay(currentEngine=True):
    """ Load Mental Ray plugin """
    name = "Mayatomr"
    if not mc.pluginInfo(name, q=True, loaded=True):
        print "Load MentalRayPlugin() ..."
        mc.loadPlugin(name)
        mc.pluginInfo(name, edit=True, autoload=True)
    if currentEngine:
        print "Set MentalRay as current render engine ..."
        mc.setAttr('defaultRenderGlobals.currentRenderer', 'mentalRay', type='string')
    print "# Result: mental ray Plugin loaded #"
