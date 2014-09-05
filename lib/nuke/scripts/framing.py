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
        self.setRoot()
        self.setRead()

    def setRoot(self):
        if self._checkOptions:
            node = self.nuke.getNode('Root')
            node.printAttrs()
            node.set('frame', self._range[0])
            node.set('first_frame', self._range[0])
            node.set('last_frame', self._range[1])
            node.set('format', self._format(self.options['sizeIn']))
            node.printAttrs()

    def setRead(self):
        if self._checkOptions:
            node = self.nuke.getNode('Read1')
            node.printAttrs()
            node.set('file', pFile.conformPath(self.options['in']))
            node.set('format', self._format(self.options['sizeIn']))
            node.set('first', self._range[0])
            node.set('last', self._range[1])
            node.printAttrs()

    @property
    def _checkOptions(self):
        print "[Framing] | Info | Checking framing options ..."
        optList = {'in': self.options['in'], 'out': self.options['out'],
                   'range': self.options['range'], 'sizeIn': self.options['sizeIn']}
        for k, v in optList.iteritems():
            if v is None:
                raise KeyError, "[Framing] | Error | Framing option %r is not setted." % k
        print "[Framing] | Info | Check framing options successfully."
        return True

    @property
    def _range(self):
        if isinstance(self.options['range'], bool):
            return (1, 1, 1)
        elif isinstance(self.options['range'], tuple):
            return self.options['range']

    def _format(self, size):
        return "%s %s 0 0 %s %s 1 framing" % (size[0], size[1], size[0], size[1])



if __name__ == '__main__':
    imaIn = "F:/devZone/leVoeu/shots/s0020/p0010/compo/tracking/s0020_p0010_verifTrack.0000300.png"
    imaOut = "F:/devZone/leVoeu/shots/s0020/p0010/compo/tracking/test.0000300.png"
    opts = ['--in', imaIn, '--out', imaOut, '-s', '300', '305', '1', '--sizeIn', '1920', '1080']
    fr = Framing(opts)
    fr.printOptions()