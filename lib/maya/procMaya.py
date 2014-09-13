try:
    import maya.cmds as mc
except:
    pass


def loadScene(sceneName, force=True):
    """ Open given scene
        @param sceneName: (str) : Scene absolut path
        @param force: (bool) : Force opening """
    print "Opening Maya Scene: %s" % sceneName
    mc.file(sceneName, o=True, f=force)

def importScene(sceneName, force=True):
    """ Import given scene
        @param sceneName: (str) : Scene absolut path
        @param force: (bool) : Force opening """
    print "Importing Maya Scene: %s" % sceneName
    mc.file(sceneName, i=True, type="mayaAscii", pr=True, lrd="all", f=force)

def saveSceneAs(sceneName, force=True, keepCurrentName=False):
    """ Save scene with given name
        @param sceneName: (str) : Scene absolut path
        @param force: (bool) : Force opening
        @param keepCurrentName: (bool) : Keep original scene name """
    print "Saving Maya Scene: %s" % sceneName
    currentSceneName = mc.file(q=True, sn=True)
    mc.file(rn=sceneName)
    mc.file(s=True, type="mayaAscii", f=force)
    if keepCurrentName:
        print "Keep Scene Name: %s" % currentSceneName
        mc.file(rn=currentSceneName)

def exportSel(sceneName, force=True):
    """ Save selection with given name
        @param sceneName: (str) : Scene absolut path
        @param force: (bool) : Force opening """
    print "Saving Maya Scene: %s" % sceneName
    mc.file(sceneName, es=True, f=force, op="v=0", typ="mayaAscii", pr=True)

