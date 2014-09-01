import sys, optparse


usage = ''.join(["\nstandAlone Usage: \n", "\tpython mayaRender.py -E [engine] -P [project] ",
                 "-O [file.ma] -I [file.ma] -I [file.ma] -C [camera] [options]\n",
                 "FromMaya Usage: \n", "\tmr = MayaRender()\n", "\tmr.setOptions(params)\n",
                 "\tmr.printOptions()\n", "\tmr.initMayaRender()"])
parser = optparse.OptionParser(usage=usage)

#-- Global Options --#
parser.add_option('-E', '--engine', type='choice', default='mentalRay',
                  choices=['mr', 'mentalRay', 'ms', 'mayaSoftaware', 'mh', 'mayaHardware'],
                  help=''.join(["[str] Render engine type [choices=['mr', 'mentalRay', ",
                                "'ms', 'mayaSoftaware', 'mh', 'mayaHardware']] [Default='%default']"]))
parser.add_option('-P', '--project', type='string',
                  help=''.join(["[file] Project used to override mayaProject. If None, ",
                                "project from opened scene wil be used."]))
parser.add_option('-O', '--open', type='string', help="[file] Open maya scene.")
parser.add_option('-I', '--import', action='append', default=[], help="[file] Import maya scenes.")
parser.add_option('-C', '--camera', type='string', help="[str] Camera name.")
parser.add_option('-R', '--range', type='int', nargs=3,
                  help="[int int int] Frame range (start, stop, step).")
parser.add_option('-S', '--size', type='int', nargs=2, help="[int int] Frame size in pixel (x, y)")
parser.add_option('--pixelAspect', type='int', help="[int] Pixel aspect")

#-- Verbose Options --#
grpVerbose = optparse.OptionGroup(parser, 'Verbose',
                                  "0=none, 1=fatal, 2=error, 3=warning, 4=info, 5=progress, 6=details")
grpVerbose.add_option('-V', '--pluginVerbose', type='int', default=4,
                      help="[int] Set the plug-in message verbosity level [Default=%default].")
grpVerbose.add_option('-v', '--renderVerbose', type='int', default=5,
                      help="[int] Set the mental ray message verbosity level [Default=%default].")
parser.add_option_group(grpVerbose)

#-- Camera Options --#
grpCamera = optparse.OptionGroup(parser, 'Camera', "Camera settings")
grpCamera.add_option('--alphaChannel', type='int', help="[int] Enable alpha channel.")
grpCamera.add_option('--depthChannel', type='int', help="[int] Enable depth channel.")
parser.add_option_group(grpCamera)

#-- Output Options --#
grpOutput = optparse.OptionGroup(parser, 'Output',
                                 "Output file settings. If used, output.padding.format")
grpOutput.add_option('-o', '--output', type='string',
                     help="[str] Image file name (without extension or padding).")
grpOutput.add_option('-f', '--format', type='choice', choices=['png','jpg','tif','iff','tga','exr'],
                     help="[choices=['png','jpg','tif','iff','tga','exr']] Image file extension.")
grpOutput.add_option('-p', '--padding', type='int', help="[int] Frame padding.")
grpOutput.add_option('--anim', type='int', help="[int] Enable images sequence.")
parser.add_option_group(grpOutput)

#-- Mental Ray Options --#
grpMentalRay = optparse.OptionGroup(parser, 'Mental Ray', "Mental Ray specific options.")
grpMentalRay.add_option('--samples', type='int', nargs=2,
                        help="[int int] Mental Ray samples (minSamples, maxSamples).")
grpMentalRay.add_option('--shadow', type='choice', choices=[0,1,2,3],
                        help="[choice=[0,1,2,3]] Shadow method (0=None, 1=simple, 2=sorted, 3=segments).")
grpMentalRay.add_option('--shadowMap', type='choice', choices=[0,1,2,3],
                        help="[choice=[0,1,2,3]] Shadow map method (0=None, 1=regular, 2=openGL, 3=detail).")
grpMentalRay.add_option('--shadowMapRebuild', type='choice', choices=[0,1,2],
                        help=''.join(["[choice=[0,1,2]] Shadow map rebuild method ",
                                      "(0=Reuse existing maps, 1=Rebuild all and overwrite, ",
                                      "2=Rebuild all and merge)."]))
grpMentalRay.add_option('--motionBlur', type='choice', choices=[0,1,2],
                        help="[choices=[0,1,2]] MotionBlur (0=None, 1=NoDeformation, 2=Full).")
grpMentalRay.add_option('--motionSteps', type='int', help="[int] Set motionBlur steps.")
grpMentalRay.add_option('--motionContrast', type='float', help="[float] Set MotionBlur contrast.")
grpMentalRay.add_option('--motionCoef', type='float', help="[float] Set MotionBlur by.")
grpMentalRay.add_option('--shutter', type='float', help="[float] Set MotionBlur shutter.")
grpMentalRay.add_option('--shutterDelay', type='float', help="[float] Set MotionBlur shutter delay.")
parser.add_option_group(grpMentalRay)

#-- Script Options --#
grpRenderScript = optparse.OptionGroup(parser, 'Render Script', "Pre render and post render scripts.")
grpRenderScript.add_option('--preRenderScript', type='string', help="[file] Pre render script")
grpRenderScript.add_option('--postRenderScript', type='string', help="[file] Post render script")
parser.add_option_group(grpRenderScript)


class RenderOptions():
    """ Class used for maya render settings and process launcher """

    def __init__(self):
        self.args = None
        self.parser = parser

    def help(self, file=None):
        """ Print parser help
            @param file: (str) : Write help to file (absolute path) """
        print "\n#################### MAYA RENDER HELP ####################"
        self.parser.print_help(file=file)
        print "##########################################################\n"

    def usage(self, file=None):
        """ Print parser usage
            @param file: (str) : Write usage to file (absolute path) """
        print "\n#################### MAYA RENDER USAGE ####################"
        self.parser.print_usage(file=file)
        print "###########################################################\n"

    def setOptions(self, args):
        """ Set parser arguments
            @param args: (list) : MayaRender Arguments """
        self.args = args

    def resetOptions(self):
        """ Reset parser arguments """
        self.args = None

    def getOption(self, option):
        """ Get option value
            @param option: (str) : Option label
            @return: (instance) : Option value """
        if option in self.options.keys():
            return self.options[option]
        else:
            return "KeyError"

    @property
    def options(self):
        """ Get mayaRender parser options
            @return: (dict) : Parser options """
        if self.args is None:
            options, args = self.parser.parse_args()
        else:
            options, args = self.parser.parse_args(self.args)
        return eval(str(options))

    def printOptions(self):
        """ Print MayaRender options """
        print "\n#---------- Render Options ----------#"
        for k, v in self.options.iteritems():
            print k, "=", v
        print '#%s#\n' % ("-" * 36)



if __name__ == '__main__':
    parser.parse_args()
    wsPath = "F:/rnd/workspace/bank"
    if not wsPath in sys.path:
        print "Adding %s to sysPath ..." % wsPath
        sys.path.insert(0, wsPath)
    from tools.maya.render.proc.scripts import procRender as pRender
    mr = pRender.MayaRender()
    mr.printOptions()
    mr.initMayaRenderer()
