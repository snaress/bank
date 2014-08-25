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
        print "Load MentalRayPlugin ..."
        mc.loadPlugin(name)
        mc.pluginInfo(name, edit=True, autoload=True)
    #-- Use MentalRay As Current Renderer --#
    if currentEngine:
        print "Set MentalRay as current render engine ..."
        mc.setAttr('defaultRenderGlobals.currentRenderer', 'mentalRay', type='string')
    print "# Result: mental ray Plugin loaded #"

def initMrDefaultNodes():
    """ Create mentalRay default nodes """
    print "Init Mentalray default nodes ..."
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
        self._mrOptions = None

    def initMentalRay(self):
        loadMentalRay()
        initMrDefaultNodes()

    def setMentalRayOptions(self, options):
        self._mrOptions = options
        self.mrLog("#-- Init Mental Ray Params --#")
        self.setSamples()
        self.setShadows()
        self.setMotionBlur()

    def setSamples(self):
        """ Option: 'samples' = Set mentalRay samples """
        if self._mrOptions['samples'] is None:
            self.mrLog("\tUse current samples.")
        else:
            self.mrLog("\tOption 'samples' detected: %s" % str(self._mrOptions['samples']))
            mc.setAttr("miDefaultOptions.minSamples", self._mrOptions['samples'][0])
            mc.setAttr("miDefaultOptions.maxSamples", self._mrOptions['samples'][1])

    def setShadows(self):
        """ Option: 'shadows' = Set mentalRay shadows """
        #-- Shadows --#
        if self._mrOptions['shadow'] is None:
            self.mrLog("\tUse current shadow.")
        else:
            self.mrLog("\tOption 'shadow' detected: %s" % self._mrOptions['shadow'])
            mc.setAttr("miDefaultOptions.shadowMethod", self._mrOptions['shadow'])
        #-- Shadow Maps --#
        if self._mrOptions['shadowMap'] is None:
            self.mrLog("\tUse current shadowMap.")
        else:
            self.mrLog("\tOption 'shadowMap' detected: %s" % self._mrOptions['shadowMap'])
            mc.setAttr("miDefaultOptions.shadowMaps", self._mrOptions['shadowMap'])
        #-- Shadow Maps Rebuild --#
        if self._mrOptions['shadowMapRebuild'] is None:
            self.mrLog("\tUse current shadowMapRebuild.")
        else:
            self.mrLog("\tOption 'shadowMapRebuild' detected: %s" % self._mrOptions['shadowMapRebuild'])
            mc.setAttr("miDefaultOptions.rebuildShadowMaps", self._mrOptions['shadowMapRebuild'])

    def setMotionBlur(self):
        """ Option: 'motionBlur' = Enable mentalRay motionBlur """
        #-- Motion Blur --#
        if self._mrOptions['motionBlur'] is None:
            self.mrLog("\tUse current motionBlur.")
        else:
            self.mrLog("\tOption 'motionBlur' detected: %s" % self._mrOptions['motionBlur'])
            mc.setAttr("miDefaultOptions.motionBlur", self._mrOptions['motionBlur'])
        #-- Motion Steps --#
        if self._mrOptions['motionSteps'] is None:
            self.mrLog("\tUse current motionSteps.")
        else:
            self.mrLog("\tOption 'motionSteps' detected: %s" % self._mrOptions['motionSteps'])
            mc.setAttr("miDefaultOptions.motionSteps", self._mrOptions['motionSteps'])
        #-- Motion Contrast --#
        if self._mrOptions['motionContrast'] is None:
            self.mrLog("\tUse current motionContrast.")
        else:
            self.mrLog("\tOption 'motionContrast' detected: %s" % self._mrOptions['motionContrast'])
            mc.setAttr("miDefaultOptions.timeContrastR", self._mrOptions['motionContrast'])
            mc.setAttr("miDefaultOptions.timeContrastG", self._mrOptions['motionContrast'])
            mc.setAttr("miDefaultOptions.timeContrastB", self._mrOptions['motionContrast'])
            mc.setAttr("miDefaultOptions.timeContrastA", self._mrOptions['motionContrast'])
        #-- Motion Coef --#
        if self._mrOptions['motionCoef'] is None:
            self.mrLog("\tUse current motionCoef.")
        else:
            self.mrLog("\tOption 'motionCoef' detected: %s" % self._mrOptions['motionCoef'])
            mc.setAttr("miDefaultOptions.motionBlurBy", self._mrOptions['motionCoef'])
        #-- Shutter --#
        if self._mrOptions['shutter'] is None:
            self.mrLog("\tUse current shutter.")
        else:
            self.mrLog("\tOption 'shutter' detected: %s" % self._mrOptions['shutter'])
            mc.setAttr("miDefaultOptions.shutter", self._mrOptions['shutter'])
        #-- Shutter Delay --#
        if self._mrOptions['shutterDelay'] is None:
            self.mrLog("\tUse current shutterDelay.")
        else:
            self.mrLog("\tOption 'shutterDelay' detected: %s" % self._mrOptions['shutterDelay'])
            mc.setAttr("miDefaultOptions.shutterDelay", self._mrOptions['shutterDelay'])

    def mrLog(self, message, lvl=4):
        """ Print message at given level
            @param message: (str) : Text to print
            @param lvl: (int) : Level (0-6) """
        levels = ['None', 'Fatal', 'Error', 'Warning', 'Info', 'Progress', 'details']
        if lvl <= self._mrOptions['pluginVerbose']:
            print "[mr]|%s|%s" % (levels[lvl], message)


class MayaRender(mRender.RenderOptions, MentalRay):

    def __init__(self):
        super(MayaRender, self).__init__()

    def initMayaScene(self):
        """ Init maya scene """
        self.log("#-- Init Maya Scene --#")
        #-- Load & Import --#
        if self.options['open'] is None and not self.options['import']:
            self.log("\tUse current scene.")
        else:
            if self.options['open'] is not None:
                self.log("\tOption 'open' detected: %s" % self.options['open'])
                self.openScene()
            if self.options['import']:
                self.log("\tOption 'import' detected: %s" % self.options['import'])
                self.importScenes()
        #-- Param Globals --#
        self.setProject()
        self.setCamera()
        self.setRange()
        self.setSize()
        self.setPixelAspect()

    def initMayaRenderer(self):
        """ Init Maya Render """
        self.log("#-- Init Maya Renderer --#")
        self.setEngine()
        self.setOutput()
        if self.getOption('engine') in ['mr', 'mentalRay']:
            self.setMentalRayOptions(self.options)
        elif self.options('engine') in ['ms', 'mayaSoftware']:
            self.log("#-- Init Maya Software Params --#")
        elif self.options('engine') in ['mh', 'mayaHardware']:
            self.log("#-- Init Maya Hardware Params --#")

    def render(self):
        pass

    def openScene(self):
        """ Option: 'open' = Scene to load """
        pMaya.loadScene(self.options['open'])

    def importScenes(self):
        """ Option: 'import' = Scene to import """
        for scene in self.options['import']:
            pMaya.importScene(scene)

    def setProject(self):
        """ Option: 'project' = Set maya project """
        if self.options['project'] is None:
            self.log("\tUse current project.")
        else:
            self.log("\tOption 'project' detected: %s" % self.options['project'])
            mc.workspace(self.options['project'], o=True)
            mc.workspace(dir=self.options['project'])

    def setCamera(self):
        """ Option: 'camera' = Set camera renderable """
        if self.options['camera'] is None:
            self.log("Option '-C' or '--camera' is needed !!!", lvl=1)
        else:
            self.log("\tOption 'camera' detected: %s." % self.options['camera'])
            mc.setAttr("%s.renderable" % self.options['camera'], 1)
        if self.options['alphaChannel'] is not None:
            self.log("\tOption 'alphaChannel' detected: %s." % self.options['alphaChannel'])
            mc.setAttr("%s.mask" % self.options['camera'], self.options['alphaChannel'])
        if self.options['depthChannel'] is not None:
            self.log("\tOption 'depthChannel' detected: %s." % self.options['depthChannel'])
            mc.setAttr("%s.depth" % self.options['camera'], self.options['depthChannel'])

    def setRange(self):
        """ Option: 'range' = Set maya frame range """
        if self.options['range'] is None:
            self.log("\tUse current frame range.")
        else:
            self.log("\tOption 'range' detected: %s" % str(self.options['range']))
            mc.setAttr("defaultRenderGlobals.startFrame", self.options['range'][0])
            mc.setAttr("defaultRenderGlobals.endFrame", self.options['range'][1])
            mc.setAttr("defaultRenderGlobals.byFrameStep", self.options['range'][2])

    def setSize(self):
        """ Option: 'size' = Set frame size """
        if self.options['size'] is None:
            self.log("\tUse current frame size.")
        else:
            self.log("\tOption 'size' detected: %s" % str(self.options['size']))
            mc.setAttr("defaultResolution.width", self.options['size'][0])
            mc.setAttr("defaultResolution.height", self.options['size'][1])

    def setPixelAspect(self):
        """ Option: 'pixelAspect' = Set frame pixelAspect """
        if self.options['pixelAspect'] is None:
            self.log("\tUse current frame pixel aspect.")
        else:
            self.log("\tOption 'pixelAspect' detected: %s" % str(self.options['pixelAspect']))
            mc.setAttr("defaultResolution.pixelAspect", self.options['pixelAspect'])

    def setEngine(self):
        """ Option: 'engine' = Set maya renderer """
        if self.options['engine'] in ['mr', 'mentalRay']:
            self.initMentalRay()

    def setOutput(self):
        """ Option: 'output' = Set image file """
        #-- Image Prefix --#
        if self.options['output'] is None:
            self.log("\tUse current output.")
        else:
            self.log("\tOption 'output' detected: %s." % self.options['output'])
            mc.setAttr("defaultRenderGlobals.imageFilePrefix", self.options['output'], type='string')
        #-- Image Sequence --#
        if self.options['anim'] is None:
            self.log("\tUse current anim.")
        else:
            self.log("\tOption 'anim' detected: %s." % self.options['anim'])
            mc.setAttr("defaultRenderGlobals.animation", self.options['anim'])
            if self.options['anim']:
                mc.setAttr("defaultRenderGlobals.outFormatControl", 0)
                mc.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
                mc.setAttr("defaultRenderGlobals.periodInExt", 1)
            else:
                mc.setAttr("defaultRenderGlobals.outFormatControl", 0)
        #-- Image Format --#
        if self.options['format'] is None:
            self.log("\tUse current format.")
        else:
            self.log("\tOption 'format' detected: %s." % self.options['format'])
            mc.setAttr("defaultRenderGlobals.imfPluginKey", self.options['format'], type='string')
            extIndex, dataIndex = self.getImageFormatIndex(self.options['format'])
            mc.setAttr("defaultRenderGlobals.imageFormat", extIndex)
            mc.setAttr("miDefaultFramebuffer.datatype", dataIndex)
        #-- Image Padding --#
        if self.options['padding'] is None:
            self.log("\tUse current padding.")
        else:
            self.log("\tOption 'padding' detected: %s." % self.options['padding'])
            mc.setAttr("defaultRenderGlobals.extensionPadding", self.options['padding'])

    def getImageFormatIndex(self, format):
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

    def log(self, message, lvl=4):
        """ Print message at given level
            @param message: (str) : Text to print
            @param lvl: (int) : Level (0-6) """
        levels = ['None', 'Fatal', 'Error', 'Warning', 'Info', 'Progress', 'details']
        if lvl <= self.options['pluginVerbose']:
            print "[mr]|%s|%s" % (levels[lvl], message)
