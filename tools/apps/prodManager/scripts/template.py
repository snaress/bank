class DefaultTemplate(object):
    """ Class containing all prodManager defaut attributes and params """

    @staticmethod
    def previewMaxSize():
        """ Give preview image default max size
            @return: (int) : maxWidth, (int) : maxHeight """
        return 300, 150

    @staticmethod
    def projectTreeNodeAttr(nodeType, nodeLabel, nodeName, nodePath):
        """ Get default project tree node attributes
            @param nodeType: (str) : 'assetFld' or 'asset' or 'shotFld' or 'shot'
            @param nodeLabel: (str) : Display node name
            @param nodeName: (str) : Id node name
            @param nodePath: (str) : Node tree path
            @return: (dict) : QTreeWidgetItem attributes """
        return {'nodeType': nodeType, 'nodeLabel': nodeLabel,
                'nodeName': nodeName, 'nodePath': nodePath}

    @staticmethod
    def projectStepNodeAttr(stepType, stepLabel, stepParent):
        """ Get default project step node attributes
            @param stepType: (str) : 'step' or 'substep'
            @param stepLabel: (str) : Display node name
            @param stepParent: (str) : Parent node label
            @return: (dict) QTreeWidgetItem attributes """
        return {'stepType': stepType, 'stepLabel': stepLabel, 'stepParent': stepParent}

    @staticmethod
    def shotNodeAttr(shotWorkDir, shotIn, shotOut, shotFocal, shotHdlIn, shotHdlOut):
        """ Get default shot node attributes
            @param shotWorkDir: (str) : Shot work directory
            @param shotIn: (int) : Shot start frame
            @param shotOut: (int) : Shot end frame
            @param shotFocal: (int) : Shot camera focal
            @param shotHdlIn: (int) : Number of frames for handle in
            @param shotHdlOut: (int) : Number of frames for handle out
            @return: (dict) : QTreeWidgetItem attributes """
        return {'shotWorkDir': shotWorkDir, 'shotIn': shotIn, 'shotOut': shotOut,
                'shotFocal': shotFocal, 'shotHandleIn': shotHdlIn, 'shotHandleOut': shotHdlOut}

    @staticmethod
    def _assetSteps():
        """ Get default asset steps
            @return: (dict) : Project asset steps and subSteps """
        return {'stepOrder': ['design', 'modeling', 'mapping', 'rigg', 'cloth', 'hair', 'actor'],
                'design': ['turn', 'color', 'light'],
                'modeling': ['nude', 'cloth', 'hair', 'shape', 'tech', 'split'],
                'mapping': ['shader', 'texture'],
                'rigg': ['skin', 'shape', 'dynamic'],
                'cloth': ['rigg', 'clothToSkin', 'setup'],
                'hair': ['rigg', 'dynamic', 'setup'],
                'actor': ['previz', 'anim', 'render', 'tech']}

    @property
    def assetSteps(self):
        return self._assetSteps()

    @staticmethod
    def _shotSteps():
        """ Get default shot steps
            @return: (dict) : Project shot steps and subSteps """
        return {'stepOrder': ['storyBord', 'animatic', 'anim', 'lighting', 'cloth', 'fx', 'compo'],
                'storyBord': ['layout', 'color'],
                'animatic': ['layout', 'posing', 'deliver'],
                'anim': ['block', 'spline', 'refine', 'fixing', 'deliver'],
                'lighting': ['preLight', 'light', 'deliver'],
                'cloth': ['confo', 'simu', 'fixing', 'deliver'],
                'fx': ['confo', 'simu', 'fixing', 'deliver'],
                'compo': ['bd', 'hd', 'deliver']}

    @property
    def shotSteps(self):
        return self._shotSteps()
