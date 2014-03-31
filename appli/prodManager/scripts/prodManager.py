import os
from appli import prodManager
from lib.system.scripts import procFile as pFile
from appli.prodManager.scripts import core as pmCore
from appli.prodManager.scripts import template as pmTemplate


class ProdManager(object):
    """ Class containing all prodManager's commands for creation, loading,
        editing and writing datas in or from tool dataBase """

    def __init__(self):
        self.project = None

    def newProject(self, projectName, projectAlias):
        """ Create new project in dataBase
            @param projectName: (str) : New project name
            @param projectAlias: (str) : New project alias
            @return: (str) : New project creation result, (list) : Result message """
        print "#----- Create New Project -----#"
        result = pmCore.createNewProject(projectName, projectAlias)
        if result == "error code 1":
            mess = ["#!!! Error !!!#", "Project Name or Project Alias not valid !!!",
                    "Don't use special caracter or one in the list behind :", "., -, #, ', \", space"]
        elif result == "error code 2":
            mess = ["#!!! Error !!!#", "Project already exists in dataBase !!!"]
        elif result == "error code 3":
            mess = ["#!!! Error !!!#", "Can't create folder in dataBase !!!"]
        elif result == "error code 4":
            mess = ["#!!! Error !!!#", "Can't create project file in dataBase !!!"]
        else:
            mess = ["#%s#" % ('-'*60),
                    "Project successfully created in dataBase: %s" % result,
                    "#%s#" % ('-'*60)]
        print '\n'.join(mess)
        if result == '%s--%s' % (projectName, projectAlias):
            self.loadProject(projectName, projectAlias)
        return result, mess

    def loadProject(self, projectName, projectAlias):
        """ Load project from dataBase
            @param projectName: (str) : New project name
            @param projectAlias: (str) : New project alias """
        print "#----- Load Project -----#"
        projectPath = os.path.join(prodManager.binPath, 'project', '%s--%s' % (projectName, projectAlias))
        projectFile = os.path.join(projectPath, '%s--%s.py' % (projectName, projectAlias))
        if os.path.exists(projectFile):
            print "Loading '%s--%s' ..." % (projectName, projectAlias)
            #-- Project Params --#
            params = pFile.readPyFile(projectFile)
            self.project = pmTemplate.ProjectTemplate(self)
            self.project._projectPath = projectPath
            self.project._projectFile = projectFile
            self.project.addProjectParams(**params)
            #-- Project Trees --#
            trees = getattr(self.project, 'projectTrees')
            for tree in trees:
                newTree = self.project.addTree(tree)
                newTree.buildTreeFromFile()
        else:
            print "Error: Project doesn't exists (%s--%s) !!!" % (projectName, projectAlias)

    def printParams(self):
        print '#' * 100
        print "#----- PROD MANAGER PARAMS -----#"
        for k, v in self.__dict__.iteritems():
            print k, '=', v
        print '#' * 100
