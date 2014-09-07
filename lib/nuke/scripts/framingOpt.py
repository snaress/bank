import os, sys, optparse


user = os.environ.get('username')
usage = "framing --in imaPath --out imaPath -f/-s --sizeIn x y [Framing Options] [Resize Options]"
parser = optparse.OptionParser(usage=usage)

parser.add_option('--in', type='string', help="[str] Input image path.")
parser.add_option('--out', type='string', help="[str] Output image path.")
parser.add_option('-f', '--frame', action='store_true', dest='range',
                  help="Enable unique frame to render.")
parser.add_option('-s', '--sequence', type='int', nargs=3, dest='range',
                  help="[int int int] Frame range to render (start, stop, step).")
parser.add_option('--sizeIn', type='int', nargs=2,
                  help="[int int] Input image width and height (pixel).")

grpFraming = optparse.OptionGroup(parser, '#-- Framing Options --#')
grpFraming.add_option('-F', '--framing', action='store_true', default=False,
                      help="Enable framing process.")
grpFraming.add_option('--title', type='string', default='No Title', help="[str] Framing title.")
grpFraming.add_option('--prod', type='string', default='No Prod', help="[str] Prod alias or name.")
grpFraming.add_option('--file', type='string', default='No File', help="[str] Framing file.")
grpFraming.add_option('--user', type='string', default=user, help="[str] Framing user.")
grpFraming.add_option('--bandeSize', type='int', default=60,
                      help="[int] Framing bande size (default=60).")
grpFraming.add_option('--fontSize', type='int', default=25,
                      help="[int] Framing font size (default=25).")
grpFraming.add_option('--framingOpacity', type='int', default=0.9,
                      help="[int] Framing opacity (default=0.9).")
parser.add_option_group(grpFraming)

grpResize = optparse.OptionGroup(parser, '#-- Resize Options --#')
grpResize.add_option('--sizeOut', type='int', nargs=2,
                     help="[int int] Output image width and height (pixel).")
parser.add_option_group(grpResize)

grpWrite = optparse.OptionGroup(parser, '#-- Write Options --#')
grpWrite.add_option('--dataType', type='choice',
                    choices=['8 bit', '10 bit', '12 bit', '16 bit', '16 bit float', '32 bit float'],
                    help=''.join(["[choice png:['8 bit', '16 bit']] (default='8 bit').",
                                  "[choice dpx:['8 bit', '10 bit', '12 bit', '16 bit'] (default='16 bit')",
                                  "[choice exr:['16 bit float', '32 bit float'] (default='16 bit float')"]))
grpWrite.add_option('--jpgQuality', type='float', default=1,
                    help="[float] Compression quality (range 0.0-1.0, default=1.0).")
grpWrite.add_option('--codec', type='choice', choices=['h261', 'h263', 'avc1', '"png "', 'mp4v'],
                    default='avc1',
                    help="[choice:['h261', 'h263', 'avc1', '\"png \"', 'mp4v']] (default='mp4v').")
grpWrite.add_option('--fps', type='int', default='24', help="[int] Movie frame by seconds (default=24).")
grpWrite.add_option('--movQuality', type='choice', choices=['Min', 'Low', 'Normal', 'High', 'Max', 'Lossless'],
                    default='High', help="[choice:['Min', 'Low', 'Normal', 'High', 'Max', 'Lossless']].")
grpWrite.add_option('--tmpPath', type='string', help="[str] Tmp path. If None, use image file path.")
grpWrite.add_option('--keepNkFile', action='store_true', default=False,
                    help="Disable tmp file cleaning (default='false').")
parser.add_option_group(grpWrite)


class FramingOptions(object):

    def __init__(self):
        self.args = None
        self.parser = parser

    def help(self, file=None):
        """ Print parser help
            @param file: (str) : Write help to file (absolute path) """
        print "\n#################### FRAMING HELP ####################"
        self.parser.print_help(file=file)
        print "######################################################\n"

    def usage(self, file=None):
        """ Print parser usage
            @param file: (str) : Write usage to file (absolute path) """
        print "\n#################### FRAMING USAGE ####################"
        self.parser.print_usage(file=file)
        print "#######################################################\n"

    def setOptions(self, args):
        """ Set parser arguments
            @param args: (list) : MayaRender Arguments """
        self.args = args

    def resetOptions(self):
        """ Reset parser arguments """
        self.args = None

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
        """ Print framing options """
        print "\n#---------- Framing Options ----------#"
        for k, v in self.options.iteritems():
            print k, "=", v
        print '#%s#\n' % ("-" * 36)



if __name__ == '__main__':
    parser.parse_args()
    wsPath = "F:/rnd/workspace/bank"
    if not wsPath in sys.path:
        print "Adding %s to sysPath ..." % wsPath
        sys.path.insert(0, wsPath)
    from lib.nuke.scripts import framing
    f = framing.Framing()
    f.printOptions()
