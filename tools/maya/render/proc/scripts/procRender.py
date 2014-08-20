from lib.maya.scripts import procMaya as pMaya
try:
    import maya.cmds as mc
except:
    pass


def loadMentalRay(currentEngine=True):
    """ Load Mental Ray plugin
        @param currentEngine: (bool) : Set MentalRay as current render engine """
    name = "Mayatomr"
    #-- Load MentalRay PlugIn --#
    if not mc.pluginInfo(name, q=True, loaded=True):
        print "Load MentalRayPlugin() ..."
        mc.loadPlugin(name)
        mc.pluginInfo(name, edit=True, autoload=True)
    #-- Use MentalRay As Current Renderer --#
    if currentEngine:
        print "Set MentalRay as current render engine ..."
        mc.setAttr('defaultRenderGlobals.currentRenderer', 'mentalRay', type='string')
    print "# Result: mental ray Plugin loaded #"

def initMrDefaultNodes():
    """ Create mentalRay default nodes """
    mrNodes = {'mentalrayGlobals': 'mentalrayGlobals', 'mentalrayItemsList': 'mentalrayItemsList',
               'mentalrayOptions': 'miDefaultOptions', 'mentalrayFramebuffer': 'miDefaultFramebuffer'}
    #-- Create mrNodes --#
    for mrNode in mrNodes.keys():
        if not mc.objExists(mrNode):
            print "Create mrNode %s named %s" % (mrNode, mrNodes[mrNode])
            mc.createNode(mrNode, n=mrNodes[mrNode])
    #-- Link mrNodes --#
    print "Connect mrNodes ..."
    mc.connectAttr("miDefaultOptions.message", "mentalrayGlobals.options")
    mc.connectAttr("miDefaultOptions.message", "mentalrayItemsList.options[0]")
    mc.connectAttr("miDefaultFramebuffer.message", "mentalrayGlobals.framebuffer")
    mc.connectAttr("miDefaultFramebuffer.message", "mentalrayItemsList.framebuffers[0]")
    mc.connectAttr("mentalrayGlobals.message", "mentalrayItemsList.globals")


class MrRender(object):

    def __init__(self, **kwargs):
        self.params = kwargs
        self.mrParams = {}
        self._initMrParams()

    #============================================ INIT ============================================#

    def _initMrParams(self):
        """ Init mentalRay params """
        self._paramFiles()
        self._paramProject()
        self._paramCamera()
        self._paramMrVerbose()
        self._paramRVerbose()
        self._paramImagePrefix()
        self._paramImageFormat()

    def _paramFiles(self):
        """ Store files param """
        print "[MR]: Storing files ..."
        if 'files' in self.params.keys():
            print "\tFiles param detected."
            if isinstance(self.params['files'], str):
                print "\tStore single file ..."
                print "\t", self.params['files']
                self.mrParams['files'] = [self.params['files']]
            elif isinstance(self.params['files'], list):
                print "\tStore multi files ..."
                for f in self.params['files']:
                    print "\t\t", f
                self.mrParams['files'] = self.params['files']
            else:
                raise KeyError, "[MR]: Key: 'files' - Value must be str or list"
        else:
            print "\tUse current scene."
            self.mrParams['files'] = None
        print "\tfiles =", self.mrParams['files']

    def _paramProject(self):
        """ Store project param """
        print "[MR]: Storing project ..."
        if 'project' in self.params.keys():
            print "\tProject param detected."
            self.mrParams['project'] = self.params['project']
        else:
            print "\tUse current project."
            self.mrParams['project'] = mc.workspace(q=True, o=True)
        print "\tproject =", self.mrParams['project']

    def _paramCamera(self):
        """ Store camera param """
        print "[MR]: Storing camera ..."
        if 'camera' in self.params.keys():
            print "\tCamera param detected."
            self.mrParams['camera'] = self.params['camera']
        else:
            raise KeyError, "[MR]: Key: 'camera' - Key needed for process (camera name)"
        print "\tcamera =", self.params['camera']

    def _paramMrVerbose(self):
        """ Store mentalRay verbose param """
        print "[MR]: Storing mentalRay verbose ..."
        if 'mrVerbose' in self.params.keys():
            print "\tMrVerbose param detected."
            self.mrParams['mrVerbose'] = self.params['mrVerbose']
        else:
            self.mrParams['mrVerbose'] = 3
        print "\tmrVerbose =", self.mrParams['mrVerbose']

    def _paramRVerbose(self):
        """ Store render verbose param """
        print "[MR]: Storing render verbose ..."
        if 'rVerbose' in self.params.keys():
            print "\trVerbose param detected."
            self.mrParams['rVerbose'] = self.params['rVerbose']
        else:
            self.mrParams['rVerbose'] = 4
        print "\trVerbose =", self.mrParams['rVerbose']

    def _paramImagePrefix(self):
        """ Store image file prefix param """
        print "[MR]: Storing image file prefix ..."
        if 'imagePrefix' in self.params.keys():
            print "\tImageFilePrefix param detected."
            self.mrParams['imagePrefix'] = self.params['imagePrefix']
        else:
            self.mrParams['imagePrefix'] = self.mrParams['camera']
        print "\timagePrefix =", self.mrParams['imagePrefix']

    def _paramImageFormat(self):
        """ Store image file format param """
        print "[MR]: Storing image file format ..."
        if 'imageFormat' in self.params.keys():
            print "\tImageFileFormat param detected."
            self.mrParams['imageFormat'] = self.params['imageFormat']
        else:
            self.mrParams['imageFormat'] = 'png'
        print "\timageFormat =", self.mrParams['imageFormat']

    #============================================ SET ============================================#

    def setMrParams(self):
        """ Set mentalRay params """
        self.setFiles()
        self.setProject()
        self.setImageFileOut()

    def setFiles(self):
        """ Set files param """
        if self.mrParams['files'] is not None:
            print "[MR]: Load files ..."
            for n, f in enumerate(self.mrParams['files']):
                if n == 0:
                    pMaya.loadScene(f)
                else:
                    pMaya.importScene(f)

    def setProject(self):
        """ Set project param """
        print "[MR]: Set project param ..."
        mc.workspace(self.mrParams['project'], o=True)
        mc.workspace(dir=self.mrParams['project'])

    def setImageFileOut(self):
        """ Set imageFilePrefix param """
        print "[MR]: Set imageFilePrefix param ..."
        mc.setAttr("defaultRenderGlobals.imageFilePrefix", self.mrParams['imagePrefix'], type='string')
        mc.setAttr("defaultRenderGlobals.imfPluginKey", self.mrParams['imageFormat'], type='string')
        extIndex, dataIndex = self._getImageFormatIndex(self.mrParams['imageFormat'])
        mc.setAttr("defaultRenderGlobals.imageFormat", extIndex)
        mc.setAttr("miDefaultFramebuffer.datatype", dataIndex)
        mc.setAttr("defaultRenderGlobals.animation", 1)
        mc.setAttr("defaultRenderGlobals.outFormatControl", 0)
        mc.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
        mc.setAttr("defaultRenderGlobals.periodInExt", 1)

    def _getImageFormatIndex(self, format):
        """ Get format index
            @param format: (str) : Image file format
            @return: (int), (int) : Image format, Image data type """
        if format == 'tif':
            return 3, 2
        elif format == 'iff':
            return 7, 2
        elif format == 'jpg':
            return 8, 2
        elif format == 'tga':
            return 19, 2
        elif format == 'png':
            return 32, 2
        elif format == 'exr':
            return 51, 5
