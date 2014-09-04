from lib.system.scripts import procFile as pFile


class NkFile(object):
    """ Nuke file parser
        @param nkFile: (str) : Nuke file absolute path
        Usage:  nk = NkFile(fileName)
                node = nk.getNode('Reformat1')
                node.set('box_width', 333)
                nk.setAttr('Reformat1', 'box_height', 111)
                node.printAttrs()
                nk.writeNkFile(fileName) """

    def __init__(self, nkFile):
        self.nkFile = nkFile
        self.nkLines = pFile.readFile(nkFile)
        self.graph = {'_order': []}
        self._parseFile()

    def listNodes(self, nodeType=None):
        """ List all nuke nodes
            @param nodeType: (str) : Node type
            @return: (list) : List of nodes (str) """
        if nodeType is None:
            return self.graph['_order']
        else:
            nodes = []
            for nodeName in self.graph['_order']:
                node = self.getNode(nodeName)
                if node.nodeType == nodeType:
                    nodes.append(nodeName)
            return nodes

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
        return node.get(attr)

    def setAttr(self, nodeName, attr, val):
        """ Set value of given node and attribute
            @param nodeName: (str) : Node name
            @param attr: (str) : Attribute name
            @param val: (instance) : Attribute value """
        node = self.graph[nodeName]
        node.set(attr, val)

    def writeNkFile(self, fileName):
        """ Write graph into given fileName
            @param fileName: (str) : Nuke file name absolute path
            @return: (bool) : True if succes, False if failed """
        for nodeName in self.listNodes():
            node = self.getNode(nodeName)
            for n, attr in enumerate(node.listAttrs()):
                ind = node._index[n]
                self.nkLines.pop(ind-1)
                self.nkLines.insert(ind-1, " %s %s\n" % (attr, node.get(attr)))
        try:
            pFile.writeFile(fileName, ''.join(self.nkLines))
            print "[nkFile] | Info | Graph saved: %s" % fileName
            return True
        except:
            print "[nkFile] | Error | Can not save graph: %s" % fileName
            return False

    def _parseFile(self):
        """ Parse given nuke file """
        print "[NkFile] | Info | Parsing file", self.nkFile
        for n, line in enumerate(self.nkLines):
            if line.endswith(' {\n'):
                nodeType = line.strip(' {\n')
                if not nodeType in ['Viewer', 'Dot']:
                    attrDict = self._nodeToDict(n, nodeType)
                    if nodeType == 'Root':
                        self.graph['_order'].append('Root')
                        self.graph['Root'] = NkNode(**attrDict)
                    else:
                        self.graph['_order'].append(attrDict['name'])
                        self.graph[attrDict['name']] = NkNode(**attrDict)
        print "[NkFile] | Info | Parsing Done"

    def _nodeToDict(self, n, nodeType):
        """ Convert text lines to dict
            @param n: (int) : Iteration
            @param nodeType: (str) : Node type
            @return: (dict) : Node dict """
        inNode = True
        attrDict = {'_order': [], '_index': [], '_nodeType': nodeType}
        nn = n
        while inNode:
            nn += 1
            if self.nkLines[nn] == '}\n':
                inNode = False
            else:
                lineOpt = self.nkLines[nn].strip().split(' ')
                if not lineOpt[0] in ['xpos', 'ypos']:
                    attrDict['_order'].append(lineOpt[0])
                    attrDict['_index'].append(nn+1)
                    attrDict[lineOpt[0]] = ' '.join(lineOpt[1:])
        return attrDict


class NkNode(object):
    """ NkFile node object
        @param kwargs: Nuke node attributes and values """

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get(self, attr):
        """ Get given attribute value
            @param attr: (str) : Attribute name
            @return: (str) : Attribute value """
        if not attr in getattr(self, '_order'):
            if self.nodeType == 'Root':
                raise KeyError, "[NkFile] | Error | %r not found on 'Root'" % attr
            else:
                raise KeyError, "[NkFile] | Error | %r not found on %r" % (attr, getattr(self, 'name'))
        else:
            return getattr(self, attr)

    def set(self, attr, val):
        """ Set given attribute value
            @param attr: (str) : Attribute name
            @param val: (instance) : Attribute value
            @return: (str) : Attribute value """
        if not attr in getattr(self, '_order'):
            if self.nodeType == 'Root':
                raise KeyError, "[NkFile] | Error | %r not found on 'Root'" % attr
            else:
                raise KeyError, "[NkFile] | Error | %r not found on %r" % (attr, getattr(self, 'name'))
        else:
            setattr(self, attr, val)

    def listAttrs(self):
        """ List all node's attributes
            @return: (list) : Node attributes (str) """
        attrs = []
        for attr in getattr(self, '_order'):
            attrs.append(attr)
        return attrs

    def printAttrs(self):
        """ Print node line index, attribute and value """
        print "-" * 80
        if self.nodeType == 'Root':
            print "Node Name: Root"
        else:
            print "Node Name:", getattr(self, 'name'), "(%s)" % self.nodeType
        for n, attr in enumerate(self.listAttrs()):
            print "\t[%s] | %s = %s" % (getattr(self, '_index')[n], attr, getattr(self, attr))
        print "-" * 80

    @property
    def nodeType(self):
        """ Get node type
            @return: (str) : Node type """
        return getattr(self, '_nodeType')
