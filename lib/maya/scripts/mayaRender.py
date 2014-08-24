import sys, optparse


usage = ''.join(["\nstandAlone Usage: \n", "\tpython mayaRender.py -E [engine] -P [project] ",
                 "-O [file.ma] -I [file.ma] -I [file.ma] -C [camera] [options]\n",
                 "FromMaya Usage: \n", "\tmr = MayaRender()\n", "\tmr.setOptions(params)\n",
                 "\tmr.printOptions()\n", "\tmr.initMayaRender()"])
parser = optparse.OptionParser(usage=usage)

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

grpVerboseHelp = "0=none, 1=fatal, 2=error, 3=warning, 4=info, 5=progress, 6=details"
grpVerbose = optparse.OptionGroup(parser, 'Verbose', grpVerboseHelp)
grpVerbose.add_option('-V', '--pluginVerbose', type='int', default=4,
                      help="[int] Set the plug-in message verbosity level [Default=%default].")
grpVerbose.add_option('-v', '--renderVerbose', type='int', default=5,
                      help="[int] Set the mental ray message verbosity level [Default=%default].")
parser.add_option_group(grpVerbose)

grpOutput = optparse.OptionGroup(parser, 'Output', "Output file settings.")
grpOutput.add_option('-o', '--output', type='string',
                     help="[str] Image file name (without extension or padding).")
grpOutput.add_option('-f', '--format', type='choice', choices=['png', 'jpg', 'dpx', 'exr'],
                     help="[choices=['png', 'jpg', 'dpx', 'exr']] Image file extension ")
grpOutput.add_option('-p', '--padding', type='int', help="[int] Frame padding.")
parser.add_option_group(grpOutput)


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
    mr.initMayaRender()
