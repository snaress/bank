from appli import grapher
from PyQt4 import uic
from functools import partial
from lib.qt.scripts import procQt as pQt
from appli.grapher.scripts import widgets


nodeEditorClass, nodeEditorUiClass = uic.loadUiType(grapher.uiList['nodeEditor'])
class NodeEditor(nodeEditorClass, nodeEditorUiClass):
    """ Class used for graph nodes edition
        @param mainUi: (object) : QMainWindow """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.grapher = self.mainUi.grapher
        self.graphNode = None
        super(NodeEditor, self).__init__()
        self._setupUi()
        self.initUi()

    def _setupUi(self):
        self.setupUi(self)
        self._setupMain()

    def _setupMain(self):
        #-- Node Version --#
        self.leVersionTitle.returnPressed.connect(self.on_versionTitle)
        self.cbNodeVersion.currentIndexChanged.connect(self.on_version)
        self.bNewVersion.clicked.connect(self.on_newVersion)
        self.bDelVersion.clicked.connect(self.on_delVersion)
        #-- Comment --#
        self.wgComment = widgets.Comment(self)
        self.vlComment.insertWidget(-1, self.wgComment)
        self.cbComment.clicked.connect(partial(self.mainUi.rf_commentVis, self))
        #-- Variables --#
        self.wgVariables = widgets.VarEditor(self.mainUi, self)
        self.vlVariables.insertWidget(-1, self.wgVariables)
        self.cbVariables.clicked.connect(partial(self.mainUi.rf_variablesVis, self))

    def initUi(self):
        """ Initialize ui """
        self.mainUi.rf_commentVis(self)
        self.mainUi.rf_variablesVis(self)

    def resetUi(self):
        """ Reset NodeEditor ui """
        self.graphNode = None
        self.leNodeName.clear()
        self.cbNodeType.setCurrentIndex(self.cbNodeType.findText('modul'))
        self.leVersionTitle.clear()
        self.cbNodeVersion.clear()
        self.wgComment.resetComment()
        self.wgVariables.resetTree()

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.mainUi.flNodeEditor.setVisible(self.mainUi.miNodeEditor.isChecked())

    def rf_versionTitle(self):
        """ Refresh node version title """
        if not self.currentVersion == '':
            title = self.graphNode._data.versionTitle[self.currentVersion]
            self.leVersionTitle.setText(title)

    def rf_versionList(self, versions):
        """ Refresh node version list
            @param versions: (list) : Version list """
        self.cbNodeVersion.clear()
        self.cbNodeVersion.addItems(versions)

    def rf_nodeComment(self):
        """ Refresh nodeEditor comment """
        if self.graphNode is not None:
            nodeDict = self.graphNode.__repr__()
            if self.currentVersion in nodeDict['nodeComment'].keys():
                if nodeDict['nodeComment'][self.currentVersion]['html'] == "":
                    self.wgComment.teText.setText(nodeDict['nodeComment'][self.currentVersion]['txt'])
                else:
                    self.wgComment.rf_comment(nodeDict['nodeComment'][self.currentVersion]['html'])
            else:
                self.wgComment.teText.setText("Add Comment")

    def ud_nodeComment(self):
        """ Update graphNode comment """
        data = self.graphNode._data
        data.nodeComment[self.currentVersion]['txt'] = self.wgComment.teText.toPlainText()
        data.nodeComment[self.currentVersion]['html'] = self.wgComment.teText.toPlainText()

    def connectGraphNode(self, graphNode):
        """ Update nodeEditor with given graphNode
            @param graphNode: (object) : QTreeWidgetItem """
        self.graphNode = graphNode
        nodeDict = self.graphNode.__repr__()
        self.leNodeName.setText(nodeDict['nodeName'])
        self.cbNodeType.setCurrentIndex(self.cbNodeType.findText(nodeDict['nodeType']))
        self.leVersionTitle.setText(nodeDict['versionTitle'][nodeDict['currentVersion']])
        self.rf_versionList(sorted(nodeDict['versionTitle'].keys()))
        self.cbNodeVersion.setCurrentIndex(self.cbNodeVersion.findText(nodeDict['currentVersion']))
        self.rf_nodeComment()

    def on_versionTitle(self):
        """ Command launch when leVersionTitle has changed """
        self.graphNode._data.versionTitle[self.currentVersion] = str(self.leVersionTitle.text())

    def on_version(self):
        """ Command launch when cbNodeVersion has changed """
        if not self.currentVersion == '':
            self.graphNode._data.currentVersion = self.currentVersion
            self.rf_versionTitle()
            self.rf_nodeComment()

    def on_newVersion(self):
        """ Command launch when bAddVersion is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            items = pQt.getComboBoxItems(self.cbNodeVersion)
            newVersion = str(int(max(items)) + 1).zfill(3)
            self._newVersion(newVersion)
            self.graphNode._data.currentVersion = newVersion
            self.cbNodeVersion.addItem(newVersion)
            self.cbNodeVersion.setCurrentIndex(self.cbNodeVersion.findText(newVersion))
            self.rf_nodeComment()

    def _newVersion(self, newVersion):
        """ Add new version to data
            @param newVersion: (str) : New version """
        self.graphNode._data.versionTitle[newVersion] = "New Version"
        self.graphNode._data.nodeComment[newVersion] = {'txt': "Add Comment", 'html': ""}

    def on_delVersion(self):
        """ Command launch when bDelVersion is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            if len(self.graphNode._data.versionTitle.keys()) > 1:
                self._delVersion(self.currentVersion)
                self.rf_versionList(self.graphNode._data.versionTitle.keys())
                self.rf_nodeComment()

    def _delVersion(self, version):
        """ Remove version from data
            @param version: (str) : Current version """
        self.graphNode._data.versionTitle.pop(version)
        self.graphNode._data.nodeComment.pop(version)

    @property
    def currentVersion(self):
        """ Get current version from ui
            @return: (str) : Current version """
        return str(self.cbNodeVersion.itemText(self.cbNodeVersion.currentIndex()))
