import maya.cmds as mc


def checkCamTrack(camTrackName):
    """ Check if cam track exists and is valid
        @param camTrackName: (str) : Camera track name
        @return: (bool) : True if success """
    cams = mc.ls(camTrackName, type="transform")
    if not cams:
        raise IOError, "!!! ERROR: Camera export failed !!!"
    else:
        print "CamTrack detected ..."
        camTrack = cams[0]
        camTrackShape = mc.listRelatives(camTrack, s=True, ni=True)[0]
        if not camTrackShape:
            raise IOError, "!!! ERROR: Camtrack shape not found !!!"
        return True

def camTrackToCamDisp(camTrackName, camDispName):
    """ Create new camera from camTrack
        @param camTrackName: (str) : Camera track name
        @param camDispName: (str) : Camera disp name
        @return: (str) : Camera disp real name """
    print "Cam track to cam disp ..."
    #-- New Cam --#
    print "\tCreate new cam %s ..." % camDispName
    newCam = mc.camera()
    camDisp = mc.rename(newCam[0], camDispName)
    if mc.objExists(camTrackName) and mc.objExists(camDisp):
        #-- Transform --#
        print "\tTransfert cam track attributes and connections ..."
        mc.copyAttr(camTrackName, camDisp, ic=True, v=True)
        #-- Shape --#
        camTrackShape = mc.listRelatives(camTrackName, s=True, ni=True)[0]
        camDispShape = mc.listRelatives(camDisp, s=True, ni=True)[0]
        print "\tTransfert cam track shape attributes and connections ..."
        mc.copyAttr(camTrackShape, camDispShape, ic=True, v=True)
        return camDisp
    else:
        raise IOError, "!!! ERROR: Camera not valid !!!"
