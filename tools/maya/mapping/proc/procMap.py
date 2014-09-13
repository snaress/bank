try:
    import maya.cmds as mc
except:
    pass


def newMat(matType, matName):
    """ Create new material
        @param matType: (str) : New material type
        @param matName: (str) : New material name
        @return: (str), (str) : matName, matSgName """
    print "Creating new %s material named %s" % (matType, matName)
    #-- Create New Shader --#
    mat = mc.shadingNode(matType, asShader=True, n=matName)
    if mat is None:
        print "info: Create new mat via createNode ..."
        mat = mc.createNode(matType, n=matName)
    matSg = mc.sets(n="%sSG" % mat, r=True, nss=True, em=True)
    #-- Connect Shader To Sg --#
    mc.connectAttr("%s.outColor" % mat, "%s.surfaceShader" % matSg, f=True)
    return mat, matSg

def assignMat(shaderSg, objects=None):
    """ Assign given shader to the object list
        @param shaderSg: (str) : ShaderSg name
        @param objects: (list) : Objects list """
    if objects is not None:
        for mesh in objects:
            try:
                mc.sets(mesh, e=True, fe=shaderSg)
                print "%s connected to %s" % (mesh, shaderSg)
            except:
                pass

