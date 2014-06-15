import os
from lib.system.scripts import procFile as pFile


class Grapher(object):
    """ Class containing all grapher's commands for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self._path = None
        self._file = None
        self._absPath = None
        self.commentHtml = ""
        self.commentTxt = ""
        self.variables = {'order': []}
        self.graphTree = {'order': []}
        self._graphTree = []

    def __repr__(self):
        txt = []
        for k, v in sorted(self.__dict__.iteritems()):
            if not k.startswith('_'):
                if isinstance(v, str):
                    txt.append("%s = %r" % (k, v))
                else:
                    txt.append("%s = %s" % (k, v))
        return '\n'.join(txt)

    def __str__(self):
        txt = ["", "========== GRAPHER =========="]
        #-- General --#
        txt.append("\n#-- General --#")
        for k, v in sorted(self.__dict__.iteritems()):
            if k.startswith('_'):
                if isinstance(v, str):
                    txt.append("%s = %r" % (k, v))
                else:
                    txt.append("%s = %s" % (k, v))
        #-- Comment --#
        txt.append("#-- Comment --#")
        txt.append(self.commentTxt)
        # txt.extend(pFile.dictToList(self.__dict__))
        return '\n'.join(txt)

    def loadGraph(self, fileName):
        """ Load given grapher file
            @param fileName: (str) : Grapher absolut path """
        print "\n#-- Loading Graph: %s --#" % fileName
        params = pFile.readPyFile(fileName)
        self._path = os.path.dirname(fileName)
        self._file = os.path.basename(fileName)
        self._absPath = fileName
        for k in sorted(self.__dict__.keys()):
            if k in params:
                print "\tUpdating %s ..." % k
                setattr(self, k, params[k])
        print "Graph successfully loaded."

    def ud_commentFromUi(self, mainUi):
        """ Update comment from mainUi
            @param mainUi: (object) : QMainWindow """
        print "\n#-- Update Comment From Ui --#"
        self.commentHtml = str(mainUi.wgComment.teText.toHtml())
        self.commentTxt = str(mainUi.wgComment.teText.toPlainText())
        print self.commentTxt

    def writeToFile(self):
        """ Write grapher to file """
        if self._absPath is not None:
            if os.path.exists(self._path):
                print "\n#-- Writing Graph --#"
                try:
                    pFile.writeFile(self._absPath, self.__repr__())
                    print "Result: %s" % self._absPath
                except:
                    raise IOError, "Result: Failed to write file %s" % self._absPath
            else:
                raise IOError, "Path not found: %s" % self._path
        else:
            raise ValueError, "Grapher._absPath = %s" % self._absPath

    def reset(self):
        """ Reset all params """
        self._path = None
        self._file = None
        self._absPath = None
        self.commentHtml = ""
        self.commentTxt = ""
        self.variables = {'order': []}
        self.graphTree = {'order': []}
        self._graphTree = []


class GraphNode(object):

    def __init__(self, nodeName, nodeType, parent=None):
        self.parent = parent
        self.children = []
        self.nodeName = nodeName
        self.nodeType = nodeType
        self.nodeComment = ""
        self.nodeVariables = []
