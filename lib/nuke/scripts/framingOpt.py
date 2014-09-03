import optparse


usage = "Framing usage ..."
parser = optparse.OptionParser(usage=usage)

parser.add_option('--in', type='string', help="[str] Input image path.")
parser.add_option('--out', type='string', help="[str] Output image path.")
parser.add_option('--sizeIn', type='int', nargs=2,
                  help="[int int] Input image width and height (pixel)")

grpResize = optparse.OptionGroup(parser, 'Resize Options')
grpResize.add_option('--sizeOut', type='int', nargs=2,
                     help="[int int] Output image width and height (pixel)")
parser.add_option_group(grpResize)


class FramingOptions(object):

    def __init__(self):
        self.args = None
        self.parser = parser

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
