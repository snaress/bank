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
        pass

    def initMentalRay(self):
        loadMentalRay()
        initMrDefaultNodes()


class MayaRender(mRender.RenderOptions, MentalRay):

    def __init__(self):
        super(MayaRender, self).__init__()

    def initMayaScene(self):
        """ Launch maya render with given options """
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
        #-- Project --#
        if self.options['project'] is None:
            self.log("\tUse current project.")
        else:
            self.log("\tOption 'project' detected: %s" % self.options['project'])
            self.setProject()
        #-- Camera --#
        if self.options['camera'] is None:
            self.log("Option '-C' or '--camera' is needed !!!", lvl=1)
        else:
            self.log("\tOption 'camera' detected: %s." % self.options['camera'])
            self.setCamera()

    def initMayaRenderer(self):
        self.log("#-- Init Maya Renderer --#")
        self.setEngine()
        self.setOutput()
        if self.getOption('engine') in ['mr', 'mentalRay']:
            self.log("#-- Init Mental Ray Params --#")
        elif self.options('engine') in ['ms', 'mayaSoftware']:
            self.log("#-- Init Maya Software Params --#")
        elif self.options('engine') in ['mh', 'mayaHardware']:
            self.log("#-- Init Maya Hardware Params --#")

    def openScene(self):
        """ Option: 'open' = Scene to load """
        pMaya.loadScene(self.options['open'])

    def importScenes(self):
        """ Option: 'import' = Scene to import """
        for scene in self.options['import']:
            pMaya.importScene(scene)

    def setProject(self):
        """ Option: 'project' = Set maya project """
        mc.workspace(self.options['project'], o=True)
        mc.workspace(dir=self.options['project'])

    def setCamera(self):
        """ Option: 'camera' = Set camera renderable """
        mc.setAttr("%s.renderable" % self.options['camera'], 1)
        if self.options['alphaChannel'] is not None:
            self.log("\tOption 'alphaChannel' detected: %s." % self.options['alphaChannel'])
            mc.setAttr("%s.mask" % self.options['camera'], self.options['alphaChannel'])
        if self.options['depthChannel'] is not None:
            self.log("\tOption 'depthChannel' detected: %s." % self.options['depthChannel'])
            mc.setAttr("%s.depth" % self.options['camera'], self.options['depthChannel'])

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


class MrRenderOld(object):

    def __init__(self, **kwargs):
        self.params = kwargs
        self.mrParams = {}
        self._initMrParams()

    #============================================ INIT ============================================#

    def _initMrParams(self):
        """ Init mentalRay params """
        self._paramFrameRange()
        self._paramFrameSize()
        self._paramSamples()
        self._paramMotionBlur()

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
        self.setFrameRange()
        self.setFrameSize()
        self.setSamples()
        self.setMotionBlur()

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
