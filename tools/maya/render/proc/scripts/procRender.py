from lib.maya.scripts import procMaya as pMaya
from lib.maya.scripts import mayaRender as mRender
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
    create = False
    for mrNode in mrNodes.keys():
        if not mc.objExists(mrNode):
            print "\tCreate mrNode %s named %s" % (mrNode, mrNodes[mrNode])
            mc.createNode(mrNode, n=mrNodes[mrNode])
            create = True
    #-- Link mrNodes --#
    if create:
        print "Connect mrNodes ..."
        conns = {'mentalrayGlobals.options': 'miDefaultOptions.message',
                 'mentalrayItemsList.options[0]': 'miDefaultOptions.message',
                 'mentalrayGlobals.framebuffer': 'miDefaultFramebuffer.message',
                 'mentalrayItemsList.framebuffers[0]': 'miDefaultFramebuffer.message',
                 'mentalrayItemsList.globals': 'mentalrayGlobals.message'}
        for dst, src in conns.iteritems():
            try:
                mc.connectAttr(src, dst)
                print "\tConnect %s to %s" % (src, dst)
            except:
                print "\tSkip connection %s to %s" % (src, dst)


class MentalRay(object):

    def __init__(self):
        pass

    def initMrParams(self):
        loadMentalRay()
        initMrDefaultNodes()


class MayaRender(mRender.RenderOptions, MentalRay):

    def __init__(self):
        super(MayaRender, self).__init__()

    def __exec__(self):
        if self.options['open'] is not None:
            self.log("Option 'open' detected ...")
            self.openScene()
        if self.options['import']:
            self.log("Option 'import' detected ...")
            self.importScenes()

    def openScene(self):
        pMaya.loadScene(self.options['open'])

    def importScenes(self):
        for scene in self.options['import']:
            pMaya.importScene(scene)

    def initMayaRender(self):
        self.log("#-- Init Maya Render --#")
        if self.getOption('engine') in ['mr', 'mentalRay']:
            self.log("#-- Init Mental Ray Params --#")
            self.initMrParams()
        elif self.options('engine') in ['ms', 'mayaSoftware']:
            self.log("#-- Init Maya Software Params --#")
        elif self.options('engine') in ['mh', 'mayaHardware']:
            self.log("#-- Init Maya Hardware Params --#")

    def log(self, message, lvl=4):
        levels = ['None', 'Fatal', 'Error', 'Warning', 'Info', 'Progress', 'details']
        if lvl <= self.options['pluginVerbose']:
            print "[mr]|%s|%s" % (levels[lvl], message)


class MrRenderOld(object):

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
        self._paramImagePadding()
        self._paramFrameRange()
        self._paramFrameSize()
        self._paramSamples()
        self._paramMotionBlur()

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
            #-- Alpha --#
            if 'alphaChannel' in self.params.keys():
                print "\tCamera alpha channel detected."
                self.mrParams['alphaChannel'] = self.params['alphaChannel']
            else:
                self.mrParams['alphaChannel'] = 1
            #-- Depth --#
            if 'depthChannel' in self.params.keys():
                print "\tCamera depth channel detected."
                self.mrParams['depthChannel'] = self.params['depthChannel']
            else:
                self.mrParams['depthChannel'] = 0
        else:
            raise KeyError, "[MR]: Key: 'camera' - Key needed for process (camera name)"
        print "\tcamera =", self.mrParams['camera']
        print "\talpha channel =", self.mrParams['alphaChannel']
        print "\tdepth channel =", self.mrParams['depthChannel']

    def _paramMrVerbose(self):
        """ Store mentalRay verbose param """
        print "[MR]: Storing mentalRay verbose ..."
        if 'mrVerbose' in self.params.keys():
            print "\tMrVerbose param detected."
            self.mrParams['mrVerbose'] = self.params['mrVerbose']
        else:
            self.mrParams['mrVerbose'] = 4
        print "\tmrVerbose =", self.mrParams['mrVerbose']

    def _paramRVerbose(self):
        """ Store render verbose param """
        print "[MR]: Storing render verbose ..."
        if 'rVerbose' in self.params.keys():
            print "\trVerbose param detected."
            self.mrParams['rVerbose'] = self.params['rVerbose']
        else:
            self.mrParams['rVerbose'] = 5
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
            print "\tImageFormat param detected."
            self.mrParams['imageFormat'] = self.params['imageFormat']
        else:
            self.mrParams['imageFormat'] = 'png'
        print "\timageFormat =", self.mrParams['imageFormat']

    def _paramImagePadding(self):
        """ Store image file padding param """
        print "[MR]: Storing image file padding ..."
        if 'imagePadding' in self.params.keys():
            print "\tImagePadding param detected."
            self.mrParams['imagePadding'] = self.params['imagePadding']
        else:
            self.mrParams['imagePadding'] = 4
        print "\timagePadding =", self.mrParams['imagePadding']

    def _paramFrameRange(self):
        """ Store frameRange param """
        print "[MR]: Storing frameRange ..."
        if 'frameRange' in self.params.keys():
            print "\tFrameRange param detected."
            self.mrParams['frameRange'] = self.params['frameRange']
        else:
            self.mrParams['frameRange'] = [1, 5, 1]
        print "\tframeRange =", self.mrParams['frameRange']

    def _paramFrameSize(self):
        """ Store frameSize param """
        print "[MR]: Storing frameSize ..."
        if 'x' in self.params.keys():
            print "\tFrameSize X param detected."
            self.mrParams['x'] = self.params['x']
        else:
            self.mrParams['x'] = 960
        if 'y' in self.params.keys():
            print "\tFrameSize Y param detected."
            self.mrParams['y'] = self.params['y']
        else:
            self.mrParams['y'] = 540
        if 'pixelAspect' in self.params.keys():
            print "\tPixelAspect param detected."
            self.mrParams['pixelAspect'] = self.params['pixelAspect']
        else:
            self.mrParams['pixelAspect'] = 1
        print "\tsizeX =", self.mrParams['x']
        print "\tsizeY =", self.mrParams['y']
        print "\tpixelAspect = ", self.mrParams['pixelAspect']

    def _paramSamples(self):
        """ Store samples param """
        print "[MR]: Storing samples ..."
        if 'samples' in self.params.keys():
            print "\tSamples param detected."
            self.mrParams['samples'] = self.params['samples']
        else:
            self.mrParams['samples'] = [-2, 0]
        print "\tsamples =", self.mrParams['samples']

    def _paramMotionBlur(self):
        """ Store motionBlur param """
        print "[MR]: Storing motionBlur ..."
        if 'motionBlur' in self.params.keys():
            print "\tMotionBlur param detected."
            self.mrParams['motionBlur'] = self.params['motionBlur']
            if 'motionSteps' in self.params.keys():
                print "\tMotionSteps param detected."
                self.mrParams['motionSteps'] = self.params['motionSteps']
            else:
                self.mrParams['motionSteps'] = 1
            if 'motionContrast' in self.params.keys():
                print "\tMotionContrast param detected."
                self.mrParams['motionContrast'] = self.params['motionContrast']
            else:
                self.mrParams['motionContrast'] = [0.2, 0.2, 0.2, 0.2]
            print "\tmotionBlur =", self.mrParams['motionBlur']
            print "\tmotionSteps =", self.mrParams['motionSteps']
            print "\tmotionContrast =", self.mrParams['motionContrast']
        else:
            self.mrParams['motionBlur'] = 0
            print "\tmotionBlur =", self.mrParams['motionBlur']

    #============================================ SET ============================================#

    def setMrParams(self):
        """ Set mentalRay params """
        self.setFiles()
        self.setProject()
        self.setCamera()
        self.setImageFileOut()
        self.setImagePadding()
        self.setFrameRange()
        self.setFrameSize()
        self.setSamples()
        self.setMotionBlur()

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

    def setCamera(self):
        """ Set camera param """
        print "[MR]: Set camera param ..."
        mc.setAttr("%s.renderable" % self.mrParams['camera'], 1)
        mc.setAttr("%s.mask" % self.mrParams['camera'], self.mrParams['alphaChannel'])
        mc.setAttr("%s.depth" % self.mrParams['camera'], self.mrParams['depthChannel'])

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

    def setImagePadding(self):
        """ Set imageFilePrefix param """
        print "[MR]: Set imagePadding param ..."
        mc.setAttr("defaultRenderGlobals.extensionPadding", self.mrParams['imagePadding'])

    def setFrameRange(self):
        """ Set frameRange param """
        print "[MR]: Set frameRange param ..."
        mc.setAttr("defaultRenderGlobals.startFrame", self.mrParams['frameRange'][0])
        mc.setAttr("defaultRenderGlobals.endFrame", self.mrParams['frameRange'][1])
        mc.setAttr("defaultRenderGlobals.byFrameStep", self.mrParams['frameRange'][2])

    def setFrameSize(self):
        """ Set frameSize param """
        print "[MR]: Set frameSize param ..."
        mc.setAttr("defaultResolution.width", self.mrParams['x'])
        mc.setAttr("defaultResolution.height", self.mrParams['y'])
        mc.setAttr("defaultResolution.pixelAspect", self.mrParams['pixelAspect'])

    def setSamples(self):
        """ Set samples param """
        print "[MR]: Set samples param ..."
        mc.setAttr("miDefaultOptions.minSamples", self.mrParams['samples'][0])
        mc.setAttr("miDefaultOptions.maxSamples", self.mrParams['samples'][1])

    def setMotionBlur(self):
        """ Set motionBlur param """
        print "[MR]: Set motionBlur param ..."
        mc.setAttr("miDefaultOptions.motionBlur", self.mrParams['motionBlur'])
        if self.mrParams['motionBlur'] > 0:
            mc.setAttr("miDefaultOptions.motionSteps", self.mrParams['motionSteps'])
            mc.setAttr("miDefaultOptions.timeContrastR", self.mrParams['motionContrast'][0])
            mc.setAttr("miDefaultOptions.timeContrastG", self.mrParams['motionContrast'][1])
            mc.setAttr("miDefaultOptions.timeContrastB", self.mrParams['motionContrast'][2])
            mc.setAttr("miDefaultOptions.timeContrastA", self.mrParams['motionContrast'][3])

    #============================================ GET ============================================#

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

    def printParams(self):
        """ Print params """
        print "#----- MENTAL RAY PARAMS -----#"
        for k, v in sorted(self.mrParams.iteritems()):
            print k, "=", v
        print "-" * 30


# if __name__ == '__main__':
#     mr = MayaRender()
#     mr.help()
#     # mr.printOptions()
#     params = ["-O", "cam.ma", "-I", "decor.ma", "-I", "sfx.ma", "-C", "camDisp1",
#               "-o", "verifTrack"]
#     mr.setOptions(params)
#     mr.printOptions()
#     mr.initMayaRender()