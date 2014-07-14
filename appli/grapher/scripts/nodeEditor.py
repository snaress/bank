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
        #-- Node Type --#
        self.cbNodeType.currentIndexChanged.connect(self.rf_scriptVis)
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
        #-- Loop --#
        self.rbLoopRange.clicked.connect(self.on_loopType)
        self.rbLoopList.clicked.connect(self.on_loopType)
        self.rbLoopSingle.clicked.connect(self.on_loopType)
        #-- Trash --#
        self.cbTrash.clicked.connect(self.rf_trashVis)
        #-- Edit --#
        self.bSave.clicked.connect(self.on_save)
        self.bCancel.clicked.connect(self.on_cancel)

    def initUi(self):
        """ Initialize ui """
        self.mainUi.rf_commentVis(self)
        self.mainUi.rf_variablesVis(self)
        self.rf_scriptVis()
        self.rf_trashVis()

    def resetUi(self):
        """ Reset NodeEditor ui """
        self.graphNode = None
        self.leNodeName.clear()
        self.cbNodeType.setCurrentIndex(self.cbNodeType.findText('modul'))
        self.leVersionTitle.clear()
        self.cbNodeVersion.clear()
        self.wgComment.resetComment()
        self.wgVariables.resetTree()
        self.teScript.clear()
        self.teTrash.clear()

    def rf_nodeEditorVis(self):
        """ Refresh Grapher NodeEditor visibility """
        self.mainUi.flNodeEditor.setVisible(self.mainUi.miNodeEditor.isChecked())

    def rf_nodeBgc(self):
        """ Refresh node background color """
        self.graphNode.setStyleSheet(self.graphNode.graphNodeBgc(self.currentType))

    def ud_nodeType(self):
        """ Update graphNode type """
        self.graphNode._data.nodeType = self.currentType

    def rf_versionTitle(self):
        """ Refresh node version title """
        if self.graphNode is not None:
            if not self.currentVersion == '':
                title = self.graphNode._data.versionTitle[self.currentVersion]
                self.leVersionTitle.setText(title)

    def rf_versionList(self, versions):
        """ Refresh node version list
            @param versions: (list) : Version list """
        if self.graphNode is not None:
            self.cbNodeVersion.clear()
            self.cbNodeVersion.addItems(versions)

    def ud_version(self):
        """ Update graphNode version """
        self.graphNode._data.currentVersion = self.currentVersion

    def rf_comment(self):
        """ Refresh nodeEditor comment """
        if self.graphNode is not None:
            nodeDict = self.graphNode.__repr2__()
            self.wgComment.resetComment()
            if self.currentVersion in nodeDict['nodeComment'].keys():
                if nodeDict['nodeComment'][self.currentVersion]['html'] == "":
                    self.wgComment.teText.setText(nodeDict['nodeComment'][self.currentVersion]['txt'])
                else:
                    self.wgComment.rf_comment(nodeDict['nodeComment'][self.currentVersion]['html'])
            else:
                self.wgComment.teText.setText("Add Comment")

    def ud_comment(self):
        """ Update graphNode comment """
        data = self.graphNode._data
        data.nodeComment[self.currentVersion] = {}
        data.nodeComment[self.currentVersion]['txt'] = str(self.wgComment.teText.toPlainText())
        data.nodeComment[self.currentVersion]['html'] = str(self.wgComment.teText.toHtml())

    def rf_variables(self):
        """ Refresh node variables """
        if self.graphNode is not None:
            if self.currentVersion in self.graphNode._data.nodeVariables:
                params = self.graphNode._data.nodeVariables[self.currentVersion]
                self.wgVariables.rf_variables(**params)
            else:
                self.wgVariables.twVariables.clear()

    def ud_variables(self):
        """ Update graphNode variables """
        data = self.graphNode._data
        data.nodeVariables[self.currentVersion] = {}
        data.nodeVariables[self.currentVersion] = self.wgVariables.__repr2__()

    def rf_scriptVis(self):
        """ Refresh node script visibility """
        if self.currentType in ['sysData', 'cmdData', 'purData']:
            self.qfLoop.setVisible(False)
            self.qfScript.setVisible(True)
            self.qfScriptSpacer.setVisible(False)
        elif self.currentType == 'loop':
            self.qfLoop.setVisible(True)
            self.qfScript.setVisible(False)
            self.qfScriptSpacer.setVisible(True)
            self.on_loopType()
        elif self.currentType == 'modul':
            self.qfLoop.setVisible(False)
            self.qfScript.setVisible(False)
            self.qfScriptSpacer.setVisible(True)

    def rf_loop(self):
        """ Refresh node Loop """
        if self.graphNode is not None:
            if self.currentVersion in self.graphNode._data.nodeLoop:
                loopDict = self.graphNode._data.nodeLoop[self.currentVersion]
                self.leLoopIter.setText(loopDict['iter'])
                self.leLoopCheckFile.setText(loopDict['checkFile'])
                self.rbLoopRange.setChecked(True)
                self.leRangeStart.setText(loopDict['start'])
                self.leRangeStop.setText(loopDict['stop'])
                self.leRangeStep.setText(loopDict['step'])
                self.rbLoopList.setChecked(True)
                self.leLoopList.setText(loopDict['list'])
                self.rbLoopSingle.setChecked(True)
                self.leLoopSingle.setText(loopDict['single'])

    def ud_loop(self):
        """ Update graphNode loop """
        data = self.graphNode._data
        data.nodeLoop[self.currentVersion] = {}
        #TODO

    def rf_script(self):
        """ Refresh node script """
        if self.graphNode is not None:
            self.teScript.clear()
            if self.currentVersion in self.graphNode._data.nodeScript:
                self.teScript.setText(self.graphNode._data.nodeScript[self.currentVersion])

    def ud_script(self):
        """ Update graphNode script """
        data = self.graphNode._data
        data.nodeScript[self.currentVersion] = str(self.teScript.toPlainText())

    def rf_trashVis(self):
        """ Refresh node trash visibility """
        self.mainUi.rf_zoneVisibility(self.cbTrash, [self.teTrash], self.flTrash)

    def rf_trash(self):
        """ Refresh node trash text """
        if self.graphNode is not None:
            self.teTrash.clear()
            if self.currentVersion in self.graphNode._data.nodeTrash:
                self.teTrash.setText(self.graphNode._data.nodeTrash[self.currentVersion])

    def ud_trash(self):
        """ Update graphNode trash """
        data = self.graphNode._data
        data.nodeTrash[self.currentVersion] = str(self.teTrash.toPlainText())

    def rf_editor(self):
        """ Refresh node editor """
        self.rf_nodeBgc()
        self.rf_scriptVis()
        self.rf_comment()
        self.rf_variables()
        self.rf_loop()
        self.rf_script()
        self.rf_trash()

    def connectGraphNode(self, graphNode):
        """ Update nodeEditor with given graphNode
            @param graphNode: (object) : QTreeWidgetItem """
        self.graphNode = graphNode
        nodeDict = self.graphNode.__repr2__()
        self.leNodeName.setText(nodeDict['nodeName'])
        self.cbNodeType.setCurrentIndex(self.cbNodeType.findText(nodeDict['nodeType']))
        self.leVersionTitle.setText(nodeDict['versionTitle'][nodeDict['currentVersion']])
        self.rf_versionList(sorted(nodeDict['versionTitle'].keys()))
        self.cbNodeVersion.setCurrentIndex(self.cbNodeVersion.findText(nodeDict['currentVersion']))
        self.rf_editor()

    def on_versionTitle(self):
        """ Command launch when leVersionTitle has changed """
        self.graphNode._data.versionTitle[self.currentVersion] = str(self.leVersionTitle.text())

    def on_version(self):
        """ Command launch when cbNodeVersion has changed """
        if not self.currentVersion == '':
            self.rf_versionTitle()
            self.rf_editor()

    def on_newVersion(self):
        """ Command launch when bAddVersion is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            items = pQt.getComboBoxItems(self.cbNodeVersion)
            newVersion = str(int(max(items)) + 1).zfill(3)
            self._newVersion(newVersion)
            self.cbNodeVersion.addItem(newVersion)
            self.cbNodeVersion.setCurrentIndex(self.cbNodeVersion.findText(newVersion))
            self.ud_version()
            self.rf_editor()

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
                self.rf_editor()

    def _delVersion(self, version):
        """ Remove version from data
            @param version: (str) : Current version """
        self.graphNode._data.versionTitle.pop(version)
        self.graphNode._data.nodeComment.pop(version)
        self.graphNode._data.nodeVariables.pop(version)
        self.graphNode._data.nodeScript.pop(version)
        self.graphNode._data.nodeTrash.pop(version)

    def on_loopType(self):
        """ Command launch when bgLoopType is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            if self.currentLoopType == 'range':
                self.qfLoopRange.setVisible(True)
                self.qfLoopList.setVisible(False)
                self.qfLoopSingle.setVisible(False)
            elif self.currentLoopType == 'list':
                self.qfLoopRange.setVisible(False)
                self.qfLoopList.setVisible(True)
                self.qfLoopSingle.setVisible(False)
            if self.currentLoopType == 'single':
                self.qfLoopRange.setVisible(False)
                self.qfLoopList.setVisible(False)
                self.qfLoopSingle.setVisible(True)

    def on_save(self):
        """ Command launch when bSave is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            print "[grapherUi] : Saving node %s" % str(self.leNodeName.text())
            self.ud_nodeType()
            self.ud_version()
            self.rf_nodeBgc()
            self.ud_comment()
            self.ud_variables()
            self.ud_script()
            self.ud_trash()

    def on_cancel(self):
        """ Command launch when bCancel is clicked """
        if self.graphNode is None:
            mess = "!!! Warning: Node editor is not connected !!!"
            self.mainUi._defaultErrorDialog(mess, self.mainUi)
        else:
            self.connectGraphNode(self.graphNode)

    @property
    def currentType(self):
        """ Get current node type from ui
            @return: (str) : Current node type """
        return str(self.cbNodeType.itemText(self.cbNodeType.currentIndex()))

    @property
    def currentVersion(self):
        """ Get current version from ui
            @return: (str) : Current version """
        return str(self.cbNodeVersion.itemText(self.cbNodeVersion.currentIndex()))

    @property
    def currentLoopType(self):
        """ Get current loop type from ui
            @return: (str) : Current loop type """
        if self.rbLoopRange.isChecked():
            return 'range'
        elif self.rbLoopList.isChecked():
            return 'list'
        elif self.rbLoopSingle.isChecked():
            return 'single'
