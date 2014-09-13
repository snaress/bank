import os
from lib.nuke import framingOpt, nkFile
from lib.system import procFile as pFile

toolPath = os.path.normpath(os.path.dirname(__file__))
nkFileName = pFile.conformPath(os.path.join(toolPath, '_lib', 'framing.nk'))


class Framing(framingOpt.FramingOptions):
    """ Framing class
        @param args: (list) : Options list
        @param lvl: (str) : Log level 'critical', 'error', 'warning', 'info', 'debug')
        Usage: opts = ['--in', imaIn, '--out', imaOut, '-s', '300', '305', '1',
                       '--sizeIn', '1920', '1080', '-F', '--title', '"CFX | cloth_dlv | v003"',
                       '--prod', '"Le Voeu"', '--file', compSrc, '--sizeOut', '960', '540']
               fr = Framing(opts, lvl='debug') """

    def __init__(self, args=None, lvl='info'):
        self.log = pFile.Logger(title='Framing', level=lvl)
        super(Framing, self).__init__()
        self.nuke = nkFile.NkFile(nkFileName)
        if args:
            self.setOptions(args)
        if lvl == 'debug':
            self.printOptions()
        self.setRoot()
        self.setRead()
        self.setFraming()
        self.setResize()
        self.setWrite()
        self.launchFraming()

    def setRoot(self):
        """ Edit rootNode """
        if self._checkOptions:
            self.log.debug("Setting root node ...")
            node = self.nuke.getNode('Root')
            node.set('frame', self._range[0])
            node.set('first_frame', self._range[0])
            node.set('last_frame', self._range[1])
            node.set('format', self._format(self.options['sizeIn']))

    def setRead(self):
        """ Edit readNode """
        self.log.debug("Setting read node ...")
        node = self.nuke.getNode('Read1')
        node.set('file', pFile.conformPath(self.options['in']))
        node.set('format', self._format(self.options['sizeIn']))
        node.set('first', self._range[0])
        node.set('last', self._range[1])

    def setFraming(self):
        """ Edit framing nodes """
        self.log.debug("Setting framing nodes ...")
        if self.options['framing']:
            self.log.info("Framing enabled.")
            self._setBandeSize()
            nodes = self.nuke.listNodes(nodeType='Text')
            for nodeName in nodes:
                self.log.debug("\tSetting text node: %s" % nodeName)
                node = self.nuke.getNode(nodeName)
                node.set('size', self.options['fontSize'])
                if nodeName == 'txtTitle':
                    self._setTitleNode(node)
                elif nodeName == 'txtProd':
                    self._setProdNode(node)
                elif nodeName == 'txtDate':
                    self._setDateNode(node)
                elif nodeName == 'txtFile':
                    self._setFileNode(node)
                elif nodeName == 'txtFrame':
                    self._setFrameNode(node)
                elif nodeName == 'txtUser':
                    self._setUserNode(node)
            #-- KeyMix --#
            node = self.nuke.getNode('addFraming')
            node.set('mix', self.options['framingOpacity'])
            node.set('disable', 'false')
            self.log.debug("Framing nodes setted.")
        else:
            self.log.info("Framing disabled.")
            #-- KeyMix --#
            node = self.nuke.getNode('addFraming')
            node.set('disable', 'true')

    def _setBandeSize(self):
        """ Edit rectangleNode for bande size"""
        self.log.debug("\tSetting framing bande size: %s" % self.options['bandeSize'])
        #-- Up --#
        node = self.nuke.getNode('bandeUp')
        area = "{0 %s %s %s}" % (self.options['sizeIn'][1]-self.options['bandeSize'],
                                 self.options['sizeIn'][0], self.options['sizeIn'][1])
        node.set('area', area)
        self.log.debug("\t\tSet bande Up: %s" % area)
        #-- Down --#
        node = self.nuke.getNode('bandeDn')
        area = "{0 0 %s %s}" % (self.options['sizeIn'][0], self.options['bandeSize'])
        node.set('area', area)
        self.log.debug("\t\tSet bande Dn: %s" % area)

    def _setTitleNode(self, node):
        """ Edit textNode 'txtTitle'
            @param node: (object) : Text node """
        node.set('message', self.options['title'])
        x = self.options['fontSize']
        y = int(self.options['sizeIn'][1] - (self.options['bandeSize'] / 2))
        node.set('translate', "{%s %s}" % (x, y))
        self.log.debug("\t\t%s setted: %s" % (node.get('name'), self.options['title']))

    def _setProdNode(self, node):
        """ Edit textNode 'txtProd'
            @param node: (object) : Text node """
        node.set('message', self.options['prod'])
        x = int(self.options['sizeIn'][0] / 2)
        y = int(self.options['sizeIn'][1] - (self.options['bandeSize'] / 2))
        node.set('translate', "{%s %s}" % (x, y))
        self.log.debug("\t\t%s setted: %s" % (node.get('name'), self.options['prod']))

    def _setDateNode(self, node):
        """ Edit textNode 'txtDate'
            @param node: (object) : Text node """
        x = int(self.options['sizeIn'][0] - self.options['fontSize'])
        y = int(self.options['sizeIn'][1] - (self.options['bandeSize'] / 2))
        node.set('translate', "{%s %s}" % (x, y))
        self.log.debug("\t\t%s setted" % node.get('name'))

    def _setFileNode(self, node):
        """ Edit textNode 'txtFile'
            @param node: (object) : Text node """
        node.set('message', self.options['file'])
        x = self.options['fontSize']
        y = int(self.options['bandeSize'] / 2)
        node.set('translate', "{%s %s}" % (x, y))
        self.log.debug("\t\t%s setted: %s" % (node.get('name'), self.options['file']))

    def _setFrameNode(self, node):
        """ Edit textNode 'txtFrame'
            @param node: (object) : Text node """
        x = int(self.options['sizeIn'][0] / 2)
        y = int(self.options['bandeSize'] / 2)
        node.set('translate', "{%s %s}" % (x, y))
        self.log.debug("\t\t%s setted" % node.get('name'))

    def _setUserNode(self, node):
        """ Edit textNode 'txtUser'
            @param node: (object) : Text node """
        node.set('message', '"User: %s"' % self.options['user'])
        x = int(self.options['sizeIn'][0] - self.options['fontSize'])
        y = int(self.options['bandeSize'] / 2)
        node.set('translate', "{%s %s}" % (x, y))
        self.log.debug("\t\t%s setted: %s" % (node.get('name'), self.options['user']))

    def setResize(self):
        """ Edit resize node """
        self.log.debug("Setting resize node ...")
        node = self.nuke.getNode('resize')
        if self.options['sizeOut']:
            self.log.info("Resize enabled.")
            node.set('disable', 'false')
            node.set('box_width', self.options['sizeOut'][0])
            node.set('box_height', self.options['sizeOut'][1])
            self.log.debug("Resize nodes setted.")
        else:
            self.log.info("Resize disabled.")
            node.set('disable', 'true')

    def setWrite(self):
        """ Edit write node """
        self.log.debug("Setting write node ...")
        imaType = self.options['out'].split('.')[-1]
        if imaType in ['png', 'jpg', 'dpx', 'exr', 'mov']:
            node = self.nuke.getNode('save_%s' % imaType)
            node.set('file', pFile.conformPath(self.options['out']))
            self.log.debug("\tImage type detected: %s" % imaType)
            if imaType == 'png':
                if self.options['dataType'] in ['8 bit', '16 bit']:
                    node.set('datatype', '"%s"' % self.options['dataType'])
                else:
                    node.set('datatype', '"8 bit"')
                    self.log.warning(' '.join(["Data type %r not supported," % self.options['dataType'],
                                               "Use default data type: '8 bit'"]))
            elif imaType == 'jpg':
                node.set('file_type', 'jpeg')
                if self.options['jpgQuality'] <= 1.0 and self.options['jpgQuality'] >= 0.0:
                    node.set('_jpeg_quality', self.options['jpgQuality'])
                else:
                    node.set('_jpeg_quality', '1')
                    self.log.warning(' '.join(["Quality %r not supported," % self.options['jpgQuality'],
                                               "Use default quality: '1.0'"]))
            elif imaType == 'dpx':
                if self.options['dataType'] in ['8 bit', '10 bit', '12 bit', '16 bit']:
                    node.set('datatype', '"%s"' % self.options['dataType'])
                else:
                    node.set('datatype', '"10 bit"')
                    self.log.warning(' '.join(["Data type %r not supported," % self.options['dataType'],
                                               "Use default data type: '10 bit'"]))
            elif imaType == 'exr':
                if self.options['detaType'] in ['16 bit float', '32 bit float']:
                    node.set('datatype', '"%s"' % self.options['dataType'])
                else:
                    node.set('datatype', '"16 bit float"')
                    self.log.warning(' '.join(["Data type %r not supported," % self.options['dataType'],
                                               "Use default data type: '16 bit float'"]))
            elif imaType == 'mov':
                if self.options['codec'] in  ['h261', 'h263', 'avc1', '"png "', 'mp4v']:
                    node.set('codec', self.options['codec'])
                else:
                    node.set('codec', 'avc1')
                    self.log.warning(' '.join(["Data type %r not supported," % self.options['codec'],
                                               "Use default codec: 'mp4v'"]))
                node.set('fps', self.options['fps'])
                node.set('quality', self.options['movQuality'])
            self._enableWriteNode('save_%s' % imaType)
        else:
            self.log.error(' '.join(["Image extention %r unknown," % imaType,
                                     "should be in ['jpg', 'png', 'dpx', 'exr', 'mov']"]))

    def _enableWriteNode(self, saveNode):
        """ Enable given Write node
            @param saveNode: (str) : Write node name to enable """
        for nodeName in self.nuke.listNodes(nodeType='Write'):
            if nodeName == saveNode:
                self.log.debug("\tEnable Write node: %s" % nodeName)
                self.nuke.setAttr(nodeName, 'disable', 'false')
            else:
                self.nuke.setAttr(nodeName, 'disable', 'true')

    def launchFraming(self):
        """ Launch framing with given options """
        print '\n'
        self.log.info("Launch framing ...")
        #-- Save TmpFile --#
        if self.options['tmpPath'] is None:
            tmpPath = os.path.dirname(self.options['out'])
        else:
            tmpPath = self.options['tmpPath']
        tmpName = '.'.join(os.path.basename(self.options['in']).split('.')[:-1])
        tmpFile = pFile.conformPath(os.path.join(tmpPath, 'framing__%s.nk' % tmpName))
        self.log.debug("Saving tmp file: %s" % tmpFile)
        self.nuke.writeNkFile(tmpFile)
        #-- Render Framing --#
        print '\n'
        self.log.info("Launching %s" % tmpFile)
        os.system("nuke5.0.exe -x %s %s,%s,%s" % (tmpFile, self._range[0], self._range[1], self._range[2]))
        #-- Clean Tmp File --#
        if not self.options['keepNkFile']:
            if os.path.exists(tmpFile):
                print '\n'
                self.log.info("Clean tmp file.")
                os.remove(tmpFile)

    @property
    def _checkOptions(self):
        """ Check global options. raise error if not setted
            @return: (bool) : True if success """
        self.log.info("Checking global options ...")
        optList = {'in': self.options['in'], 'out': self.options['out'],
                   'range': self.options['range'], 'sizeIn': self.options['sizeIn']}
        for k, v in optList.iteritems():
            if v is None:
                self.log.error("Global option %r is not setted." % k)
                raise KeyError, "[Framing] | Error | Global option %r is not setted." % k
        self.log.info("Check global options successfully.")
        return True

    @property
    def _range(self):
        """ Convert range options to tuple
            @return: (tuple) : Converted frame range """
        if isinstance(self.options['range'], bool):
            return (1, 1, 1)
        elif isinstance(self.options['range'], tuple):
            return self.options['range']

    def _format(self, size):
        """ Convert size options to string
            @param size: (str) : Image size
            @return: (str) : Converted image size """
        return '"%s %s 0 0 %s %s 1 framing"' % (size[0], size[1], size[0], size[1])
