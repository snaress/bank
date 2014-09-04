import os
from lib.nuke.scripts import framingOpt, nkFile
from lib.system.scripts import procFile as pFile


toolPath = os.sep.join(os.path.normpath(os.path.dirname(__file__)).split(os.sep)[0:-1])
nkFileName = pFile.conformPath(os.path.join(toolPath, '_lib', 'nkFiles', 'framing.nk'))


class Framing(framingOpt.FramingOptions):

    def __init__(self, args):
        super(Framing, self).__init__()
        self.nuke = nkFile.NkFile(nkFileName)
        if args:
            self.setOptions(args)
        self.setRead()

    def setRead(self):
        if self._checkOptions:
            node = self.nuke.getNode('Read1')
            node.printAttrs()
            node.set('file', pFile.conformPath(self.options['in']))
            size = '"%s %s 0 0 %s %s 1 HD"' % (self.options['sizeIn'][0], self.options['sizeIn'][1],
                                               self.options['sizeIn'][0], self.options['sizeIn'][1])
            node.set('format', size)
            node.printAttrs()

    @property
    def _checkOptions(self):
        print "[Framing] | Info | Checking framing options ..."
        optList = {'in': self.options['in'],
                   'out': self.options['out'],
                   'sizeIn': self.options['sizeIn']}
        for k, v in optList.iteritems():
            if v is None:
                raise KeyError, "[Framing] | Error | Framing option %r not setted." % k
        print "[Framing] | Info | Check framing options successfully."
        return True


if __name__ == '__main__':
    opts = ['--in', 'toto.%03d.png', '--out', 'titi.001.png', '--sizeIn', '1920', '1080']
    fr = Framing(opts)
    fr.printOptions()