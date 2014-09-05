import optparse


usage = "Framing usage ..."
parser = optparse.OptionParser(usage=usage)

parser.add_option('--in', type='string', help="[str] Input image path.")
parser.add_option('--out', type='string', help="[str] Output image path.")
parser.add_option('-f', '--frame', action='store_true', dest='range',
                  help="Enable unique frame to render.")
parser.add_option('-s', '--sequence', type='int', nargs=3, dest='range',
                  help="[int int int] Frame range to render (start, stop, step).")
parser.add_option('--sizeIn', type='int', nargs=2,
                  help="[int int] Input image width and height (pixel)")

grpFraming = optparse.OptionGroup(parser, '#-- Framing Options --#')
grpFraming.add_option('-F', '--framing', action='store_true', default=False,
                      help="Enable framing process (framing options needed)")
grpFraming.add_option('--prod', type='string', default='No Name', help="[str] Prod alias or name")
parser.add_option_group(grpFraming)

grpResize = optparse.OptionGroup(parser, '#-- Resize Options --#')
grpResize.add_option('--sizeOut', type='int', nargs=2,
                     help="[int int] Output image width and height (pixel)")
parser.add_option_group(grpResize)


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
    f = FramingOptions()
    f.printOptions()
