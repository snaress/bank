from lib.system.scripts import procFile as pFile


class NkFile(object):
    """ Nuke file parser
        @param nkFile: (str) : Nuke file absolute path """

    def __init__(self, nkFile):
        self.nkFile = nkFile
        self.nkLines = pFile.readFile(nkFile)
        self.graph = {'_order': []}
        self._parseFile()

    @property
    def listNodes(self):
        """ List all nuke nodes
            @return: (list) : List of nodes (str) """
        return self.graph['_order']

    def getNode(self, nodeName):
        """ get nodeObject from nodeName
            @param nodeName: (str) : Node name
            @return: (object) : Node """
        return self.graph[nodeName]

    def getAttr(self, nodeName, attr):
        """ Get value of given node and attribute
            @param nodeName: (str) : Node name
            @param attr: (str) : Attribute name
            @return: (str) : Value """
        node = self.graph[nodeName]
        return getattr(node, attr)

    def _parseFile(self):
        """ Parse given nuke file """
        print "[NkFile] | Parsing file", self.nkFile
        for n, line in enumerate(self.nkLines):
            if line.endswith(' {\n'):
                nodeType = line.strip(' {\n')
                if not nodeType == 'Viewer':
                    attrDict = self._nodeToDict(n, nodeType)
                    if nodeType == 'Root':
                        self.graph['_order'].append('Root')
                        self.graph['Root'] = NkNode(**attrDict)
                    else:
                        self.graph['_order'].append(attrDict['name'])
                        self.graph[attrDict['name']] = NkNode(**attrDict)
        print "[NkFile] | Parsing Done"

    def _nodeToDict(self, n, nodeType):
        """ Convert text lines to dict
            @param n: (int) : Iteration
            @param nodeType: (str) : Node type
            @return: (dict) : Node dict """
        inNode = True
        attrDict = {'_order': [], 'nodeType': nodeType}
        nn = n
        while inNode:
            nn += 1
            if self.nkLines[nn] == '}\n':
                inNode = False
            else:
                lineOpt = self.nkLines[nn].strip().split(' ')
                attrDict['_order'].append(lineOpt[0])
                attrDict[lineOpt[0]] = ' '.join(lineOpt[1:])
        return attrDict


class NkNode(object):
    """ NkFile node object
        @param kwargs: Nuke node attributes and values """

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def listAttrs(self):
        """ List all node's attributes
            @return: (list) : Node attributes (str) """
        attrs = []
        for attr in getattr(self, '_order'):
            attrs.append(attr)
        return attrs


if __name__ == '__main__':
    nk = NkFile("F:/rnd/workspace/bank/lib/nuke/_lib/nkFiles/resizeImage.nk")
    print nk.listNodes
    node = nk.getNode('Reformat1')
    print node.listAttrs()
    print nk.getAttr('Reformat1', 'box_width')