import os
from lib.system.scripts import procFile as pFile


class Grapher(object):
    """ Class containing all grapher's commands for creation, loading,
        editing and writing datas in or from tool """

    def __init__(self):
        self._path = None
        self._file = None
        self._absPath = None
        self._lock = False
        self.commentHtml = ""
        self.commentTxt = ""
        self.variables = []
        self.graphTree = []

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
        txt = ["", "#" * 80, "========== GRAPHER =========="]
        txt.extend(pFile.dictToList(self.__dict__))
        return '\n'.join(txt)

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
                print "\n#-- Writing File --#"
                try:
                    pFile.writeFile(self._absPath, self.__repr__())
                    print "Result: %s" % self._absPath
                except:
                    raise IOError, "Result: Failed to write file %s" % self._absPath
            else:
                raise IOError, "Path not found: %s" % self._path
        else:
            raise ValueError, "Grapher._absPath = %s" % self._absPath


class GraphNode(object):

    def __init__(self, nodeName, nodeType, parent=None):
        self.parent = parent
        self.children = []
        self.nodeName = nodeName
        self.nodeType = nodeType
        self.nodeComment = ""
        self.nodeVariables = []
