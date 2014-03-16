import os
import time
import shutil
from PyQt4 import QtGui
from tools.apps import archiver
from lib.system.scripts import procFile as pFile


def getItemByAbsPath(absPath, twTree):
    """ Get QTreeWidgetItem with absPath
        @param absPath: Item absolut path
        @type absPath: str
        @param twTree: QTreeWidget object
        @type twTree: object
        @return: QTreeWidgetItem object
        @rtype: object """
    allItems = QtGui.QTreeWidgetItemIterator(twTree, QtGui.QTreeWidgetItemIterator.All) or None
    if allItems is not None:
        while allItems.value():
            item = allItems.value()
            if item.absPath == absPath:
                return item
            allItems += 1

class Archivage(object):

    def __init__(self, mainUi):
        """ @param mainUi: Archiver ui object (QMainWindow)
            @type mainUi: object """
        print "\n##### Launch Archivage #####"
        self.mainUi = mainUi
        self.bankPath = archiver.bankPath
        self.archPath = archiver.archPath

    def archive(self, selItems, comm):
        """ Archive selected tools
            @param selItems: Selected QTreeWidgetItems
            @type selItems: list
            @param comm: User comment
            @type comm: str """
        for item in selItems:
            toolRelPath = item.relPath
            toolAbsPath = item.absPath
            archPath = self.createRelPath(toolRelPath)
            self.createFileInfo(item, archPath, comm)
            self.copyTool(toolAbsPath, archPath)
        print "\n##### Archivage Done #####"

    def createRelPath(self, relPath):
        """ Create Relative path
            @param relPath: Tool relative path
            @type relPath: str
            @return: Tool archive relative path
            @rtype: str """
        print "#-- Check Relative Path --#"
        archPath = self.archPath
        #-- Relative Path --#
        for fld in relPath.split(os.sep):
            archPath = os.path.join(archPath, fld)
            if not os.path.exists(archPath):
                print "Create:", archPath
                os.mkdir(archPath)
        #-- Date Folder --#
        fullDate = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())
        archPath = os.path.join(archPath, fullDate)
        if not os.path.exists(archPath):
            print "Create:", archPath
            os.mkdir(archPath)
        #-- Return Tool Archive Path --#
        print "Tool Archive Path:", archPath
        return archPath

    def createFileInfo(self, item, dst, comm):
        """ Create file 'archInfo.txt'
            @param item: Selected QTreeWidgetItem
            @type item: str
            @param dst: Destination absolut path
            @type dst: str
            @param comm: User comment
            @type comm: str """
        print "#-- Create File Info --#"
        #-- Create Texte --#
        txt = ["%s ARCHIVAGE INFO %s#" % ('#'*20, '#'*20),
               "Tool Name: %s" % str(item.text(0)),
               "User Name: %s" % archiver.user,
               "Archive Date: %s" % dst.split(os.sep)[-1].split('__')[0].replace('_', '/'),
               "Archive Time: %s" % dst.split(os.sep)[-1].split('__')[1].replace('_', ':'),
               "Source Path: %s" % item.absPath,
               "Destin Path: %s" % dst,
               "%s" % '#'*56, " ", " ", "Comment:", "%s" % '-'*8]
        txt.append(comm)
        #-- Create File --#
        fileInfo = os.path.join(dst, 'archInfo.txt')
        pFile.writeFile(fileInfo, '\n'.join(txt))
        print "FileInfo created in", fileInfo

    def copyTool(self, src, dst):
        """ Copy tool from 'bank' to 'archive'
            @param src: Source absolut path
            @type src: str
            @param dst: Destination absolut path
            @type dst: str """
        print "#-- Copy Tool --#"
        toolDict = pFile.PathToDict(src).getPathDict
        for n, root in enumerate(toolDict['root']):
            print "Checking %s ..." % root
            #-- Create Folders --#
            for fld in toolDict['flds'][n]:
                absPath = os.path.join(root, fld)
                relPath = absPath.replace("%s%s" % (src, os.sep), '')
                archPath = os.path.join(dst, relPath)
                print "\tCreate:", archPath
                os.mkdir(archPath)
            #-- Copy Files --#
            for f in toolDict['files'][n]:
                if not f.endswith('.pyc'):
                    absPath = os.path.join(root, f)
                    relPath = absPath.replace("%s%s" % (src, os.sep), '')
                    archFile = os.path.join(dst, relPath)
                    print "\tCopy:", relPath
                    shutil.copy(absPath, archFile)

class PopulateArchivage(object):

    def __init__(self, rootPath, twTree):
        """ @param rootPath: Absolut path
            @type rootPath: str
            @param twTree: Archivage QTree object (QTreeWidget)
            @type twTree: object """
        self.rootPath = rootPath
        self.twTree = twTree

    def populate(self):
        """ Populate Archivage QTreeWidget """
        tools = []
        topItems = []
        pathDict = pFile.PathToDict(self.rootPath).getPathDict
        for n, root in enumerate(pathDict['root']):
            #-- Add Top Level Items --#
            if n == 0:
                for fld in pathDict['flds'][n]:
                    newItem = self.newArchItem('folder', fld)
                    newItem.absPath = os.path.join(root, fld)
                    newItem.relPath = newItem.absPath.replace("%s%s" % (self.rootPath, os.sep), '')
                    self.twTree.addTopLevelItem(newItem)
                    topItems.append(newItem.absPath)
            #-- Add Child Items --#
            else:
                if self._verifTool(tools, root, topItems):
                    if 'scripts' in pathDict['flds'][n]:
                        mode = 'tool'
                        tools.append(pathDict['root'][n].split(os.sep)[-1])
                    else:
                        mode = 'folder'
                    newItem = self.newArchItem(mode, pathDict['root'][n].split(os.sep)[-1])
                    newItem.absPath = root
                    newItem.relPath = newItem.absPath.replace("%s%s" % (self.rootPath, os.sep), '')
                    parentPath = os.sep.join(pathDict['root'][n].split(os.sep)[:-1])
                    parent = getItemByAbsPath(parentPath, self.twTree)
                    if parent is not None:
                        parent.addChild(newItem)
                        #-- Add Check Box --#
                        if mode == 'tool':
                            newCb = self.newCheckBox(newItem)
                            self.twTree.setItemWidget(newItem, 1, newCb)
                            newItem.Active = newCb

    def newArchItem(self, mode, txt):
        """ Create new archivage QTreeWidgetItem
            @param mode: 'folder' or 'tool'
            @type mode: str
            @param txt: New item text
            @type txt: str
            @return: QTreeWidgetItem object
            @rtype: object """
        newItem = QtGui.QTreeWidgetItem()
        if mode == 'folder':
            newItem.setText(0, txt.upper())
        elif mode == 'tool':
            newItem.setText(0, txt.capitalize())
            newItem.setTextColor(0, QtGui.QColor(50, 100, 255))
            newFont = QtGui.QFont()
            newFont.setBold(True)
            newItem.setFont(0, newFont)
        newItem.type = mode
        return newItem

    def newCheckBox(self, parent):
        """ Add QChecBox to new QTreeWidgetItem
            @param parent: Parent object (QTreeWidgetItem)
            @type parent: object
            @return: New QCheckBox (QCheckBox)
            @rtype: object"""
        newCb = QtGui.QCheckBox()
        newCb.parent = parent
        return newCb

    def _verifTool(self, tools, root, topItems):
        """ Tool detection
            @param tools: Detected tools list
            @type tools: list
            @param root: Root absolut path
            @type root: str
            @param topItems: Top level QTreeWidgetItems
            @type topItems: list
            @return: True if valid, else False
            @rtype: bool """
        for tool in tools:
            if tool in root:
                return False
            if root in topItems:
                return False
        return True

class PopulateArchives(object):

    def __init__(self, selTool, twTree):
        """ @param selTool: Selected archivage QTreeWidgetItem
            @type selTool: object
            @param twTree: Archive QTreeWidget
            @type twTree: object """
        self.tool = selTool
        self.twTree = twTree
        self.archPath = archiver.archPath

    def populate(self):
        """ Populate Archives QTreeWidget """
        archives = self.getArchives
        archives.reverse()
        for arch in archives:
            user, archDate, archTime, comment = self.getArchivesInfo(arch)
            newItem = QtGui.QTreeWidgetItem()
            newItem.setText(0, user)
            newItem.setText(1, archDate)
            newItem.setText(2, archTime)
            newItem.comment = comment
            self.twTree.addTopLevelItem(newItem)

    @property
    def getArchives(self):
        """ Get archives
            @return: Archives info list
            @rtype: list """
        archives = []
        archPath = os.path.join(self.archPath, self.tool.relPath)
        if os.path.exists(archPath):
            archFlds = os.listdir(archPath) or []
            for fld in archFlds:
                if not fld.startswith('.') and not fld.startswith('_'):
                    fileInfo = os.path.join(archPath, fld, 'archInfo.txt')
                    if os.path.exists(fileInfo):
                        archives.append(fileInfo)
        return archives

    def getArchivesInfo(self, fileInfo):
        """ Get Archive info from fileInfo
            @param fileInfo: Archive file info absolut path
            @type fileInfo: str
            @return: UserName, ArchDate, ArchTime, Comment
            @rtype: str """
        info = pFile.readFile(fileInfo)
        for n, line in enumerate(info):
            if line.startswith('User Name'):
                userName = line.split(': ')[1].replace('\n', '')
            elif line.startswith('Archive Date'):
                archDate = line.split(': ')[1].replace('\n', '')
            elif line.startswith('Archive Time'):
                archTime = line.split(': ')[1].replace('\n', '')
            elif line.startswith('Comment'):
                comment = ''.join(info[n+2:])
        return userName, archDate, archTime, comment

class PopulateStat(object):

    def __init__(self, mainUi, twTree):
        """ @param mainUi: Archiver ui object (QMainWindow)
            @type mainUi: object
            @param twTree: Archive QTreeWidget
            @type twTree: object """
        self.mainUi = mainUi
        self.twTree = twTree
        self.bankPath = archiver.bankPath

    def populate(self):
        """ Populate Archives QTreeWidget """
        pathDict = pFile.PathToDict(self.bankPath).getPathDict
        for n, root in enumerate(pathDict['root']):
            #-- Add Folders --#
            for fld in pathDict['flds'][n]:
                newItem = self.newStatItem('folder', fld)
                newItem.absPath = os.path.join(root, fld)
                newItem.relPath = newItem.absPath.replace("%s%s" % (self.bankPath, os.sep), '')
                newItem.lines = 0
                newItem.size = 0
                if n == 0:
                    newItem.parent = None
                    self.twTree.addTopLevelItem(newItem)
                else:
                    parent = getItemByAbsPath(root, self.twTree)
                    newItem.parent = parent
                    parent.addChild(newItem)
                    parent.children.append(newItem)
            #-- Add Files --#
            for f in pathDict['files'][n]:
                if not f.endswith('.pyc'):
                    if f.split('.')[1] in self.getActiveExt:
                        newItem = self.newStatItem('file', f)
                        newItem.absPath = os.path.join(root, f)
                        newItem.relPath = newItem.absPath.replace("%s%s" % (self.bankPath, os.sep), '')
                        NL = len(pFile.readFile(newItem.absPath))
                        S = os.path.getsize(newItem.absPath)
                        newItem.setText(1, str(NL))
                        newItem.lines = NL
                        newItem.setText(2, pFile.fileSizeFormat(S))
                        newItem.size = S
                        if n == 0:
                            newItem.parent = None
                            self.twTree.addTopLevelItem(newItem)
                        else:
                            parent = getItemByAbsPath(root, self.twTree)
                            newItem.parent = parent
                            parent.addChild(newItem)
                            parent.children.append(newItem)
        self.countLines(pathDict)
        self.totalStatItem()

    def countLines(self, pathDict):
        """ Count total lines and total size
            @param pathDict: Root path contents
            @type pathDict: dict """
        pathDict['root'].reverse()
        for root in pathDict['root']:
            item = getItemByAbsPath(root, self.twTree)
            if hasattr(item, 'children'):
                NL = 0
                S = 0
                for child in item.children:
                    NL += child.lines
                    S += child.size
                item.lines = NL
                item.size = S
                item.setText(1, str(NL))
                item.setText(2, pFile.fileSizeFormat(S))

    def totalStatItem(self):
        """ Add total stat QTreeWidgetItem """
        totalLine = 0
        totalSize = 0
        for n in range(self.twTree.topLevelItemCount()):
            item = self.twTree.topLevelItem(n)
            totalLine += item.lines
            totalSize += item.size
        newItem = self.newStatItem('folder', 'Total')
        newItem.setText(1, str(totalLine))
        newItem.setText(2, pFile.fileSizeFormat(totalSize))
        newFont = QtGui.QFont()
        newFont.setBold(True)
        newItem.setFont(0, newFont)
        newItem.setFont(1, newFont)
        newItem.setFont(2, newFont)
        self.twTree.addTopLevelItem(newItem)

    def newStatItem(self, mode, txt):
        """ Create new archivage QTreeWidgetItem
            @param mode: 'folder' or 'file'
            @type mode: str
            @param txt: New item text
            @type txt: str
            @return: QTreeWidgetItem object
            @rtype: object """
        newItem = QtGui.QTreeWidgetItem()
        if mode == 'folder':
            newItem.setText(0, txt)
            newItem.children = []
        elif mode == 'file':
            newItem.setText(0, txt)
            newFont = QtGui.QFont()
            newFont.setBold(True)
            newItem.setFont(1, newFont)
            newItem.setFont(2, newFont)
            if txt.endswith('.py'):
                newItem.setTextColor(0, QtGui.QColor(0, 0, 255))
                newItem.setTextColor(1, QtGui.QColor(0, 0, 255))
                newItem.setTextColor(2, QtGui.QColor(0, 0, 255))
            elif txt.endswith('.ui'):
                newItem.setTextColor(0, QtGui.QColor(0, 175, 0))
                newItem.setTextColor(1, QtGui.QColor(0, 175, 0))
                newItem.setTextColor(2, QtGui.QColor(0, 175, 0))
            elif txt.endswith('.xml'):
                newItem.setTextColor(0, QtGui.QColor(255, 0, 255))
                newItem.setTextColor(1, QtGui.QColor(255, 0, 255))
                newItem.setTextColor(2, QtGui.QColor(255, 0, 255))
            elif txt.endswith('.txt'):
                newItem.setTextColor(0, QtGui.QColor(127, 0, 0))
                newItem.setTextColor(1, QtGui.QColor(127, 0, 0))
                newItem.setTextColor(2, QtGui.QColor(127, 0, 0))
            elif txt.endswith('.mel'):
                newItem.setTextColor(0, QtGui.QColor(255, 0, 0))
                newItem.setTextColor(1, QtGui.QColor(255, 0, 0))
                newItem.setTextColor(2, QtGui.QColor(255, 0, 0))
            elif txt.endswith('.ma'):
                newItem.setTextColor(0, QtGui.QColor(255, 145, 0))
                newItem.setTextColor(1, QtGui.QColor(255, 145, 0))
                newItem.setTextColor(2, QtGui.QColor(255, 145, 0))
            elif txt.endswith('.nk'):
                newItem.setTextColor(0, QtGui.QColor(140, 0, 255))
                newItem.setTextColor(1, QtGui.QColor(140, 0, 255))
                newItem.setTextColor(2, QtGui.QColor(140, 0, 255))
            else:
                newItem.setTextColor(0, QtGui.QColor(0, 0, 0))
                newItem.setTextColor(1, QtGui.QColor(0, 0, 0))
                newItem.setTextColor(2, QtGui.QColor(0, 0, 0))
        newItem.mode = mode
        return newItem

    @property
    def getActiveExt(self):
        """ Get checked QRadioButtons
            @return: Active extension
            @rtype: list """
        extL = ['py']
        if self.mainUi.rbUi.isChecked():
            extL.append('ui')
        if self.mainUi.rbXml.isChecked():
            extL.append('xml')
        if self.mainUi.rbTxt.isChecked():
            extL.append('txt')
        if self.mainUi.rbMel.isChecked():
            extL.append('mel')
        if self.mainUi.rbMa.isChecked():
            extL.append('ma')
        if self.mainUi.rbNk.isChecked():
            extL.append('nk')
        return extL
