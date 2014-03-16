import os
import time
from tools.apps import prodManager
from lib.system.scripts import procFile as pFile
from tools.apps.prodManager.scripts import template as pmTemplate

#============================================ PROJECT =============================================#

def createNewProject(projectName, projectAlias):
    """ Create new project in dataBase
        @param projectName: (str) : Project Name
        @param projectAlias: (str) : Project Alias """
    print "Creating New Project In DataBase ..."
    if checkProjectName(projectName, projectAlias):
        if not checkProjectPath(projectName, projectAlias):
            prodBinPath = createProjectPath(projectName, projectAlias)
            if prodBinPath is not None:
                prodFile = createProjectFile(prodBinPath, projectName, projectAlias)
                if prodFile is not None:
                    return "%s--%s" % (projectName, projectAlias)
                else:
                    return "error code 4"
            else:
                return "error code 3"
        else:
            return "error code 2"
    else:
        return "error code 1"

def checkProjectName(projectName, projectAlias):
    """ Check is project's name and alias are valide
        @param projectName: (str) : Project Name
        @param projectAlias: (str) : Project Alias
        @return: (bool) : True if project's name and alias are valide, else False """
    print "Checking Project Name ..."
    checkList = [' ', '.', '-', '#', "'", '#']
    check = False
    for key in checkList:
        if key in projectName or key in projectAlias:
            check = True
    if not check:
        print "\tProject name is valide !"
        return True
    else:
        print "\tProject name is not valide !"
        return False

def checkProjectPath(projectName, projectAlias):
    """ Check if project exists in dataBase
        @param projectName: (str) : Project Name
        @param projectAlias: (str) : Project Alias
        @return: (bool) : True if project already exists, else False """
    print "Checking Project Path ..."
    projectFld = "%s--%s" % (projectName, projectAlias)
    prodPath = os.path.join(prodManager.binPath, 'project', projectFld)
    if os.path.exists(prodPath) and os.path.isdir(prodPath):
        print "\tProject exists !!!"
        return True
    else:
        print "\tProject doesn't exists !!!"
        return False

def createProjectPath(projectName, projectAlias):
    """ Create new project path in dataBase
        @param projectName: (str) : Project Name
        @param projectAlias: (str) : Project Alias
        @return: (str) : ProdPath if success, else None """
    projectFld = "%s--%s" % (projectName, projectAlias)
    prodPath = os.path.join(prodManager.binPath, 'project', projectFld)
    try:
        #-- Project Folder --#
        print "Create folder %s in %s ..." % (projectFld, os.path.join(prodManager.binPath, 'project'))
        os.mkdir(prodPath)
        #-- project dependance --#
        print "\tCreate 'data' folder in %s" % prodPath
        os.mkdir(os.path.join(prodPath, 'data'))
        print "\tCreate 'tree' folder in %s" % prodPath
        os.mkdir(os.path.join(prodPath, 'tree'))
        return prodPath
    except:
        return None

def createProjectFile(projectBinPath, projectName, projectAlias):
    """ Create new project file in dataBase
        @param projectBinPath: (str) : New project file path
        @param projectName: (str) : Project Name
        @param projectAlias: (str) : Project Alias
        @return: (str) : ProdFile if success, else None """
    txt = ["projectName = %r" % projectName,
           "projectAlias = %r" % projectAlias,
           "projectStart = %r" % time.strftime("%Y/%m/%d", time.localtime()),
           "projectEnd = %r" % time.strftime("%Y/%m/%d", time.localtime()),
           "projectWorkDir = ''",
           "projectAssetSteps = %s" % pmTemplate.DefaultTemplate().assetSteps,
           "projectShotSteps = %s" % pmTemplate.DefaultTemplate().shotSteps]
    projectFile = os.path.join(projectBinPath, '%s--%s.py' % (projectName, projectAlias))
    try:
        print "Create project file in dataBase ..."
        pFile.writeFile(projectFile, '\n'.join(txt))
        return projectFile
    except:
        return None

#============================================= DATA ===============================================#

def createDataPath(dataFile):
    """ Create folders in data bdd
        @param dataFile: (str) : Data node file absolut path
        @return: (bool) : True is success, False if failed """
    print "Create node data folders ..."
    dataPath = os.sep.join(dataFile.split(os.sep)[:-1])
    if not os.path.exists(dataPath):
        try:
            os.makedirs(dataPath)
            print "Data path folders successfully created:\n%s" % dataPath
            return True
        except:
            print "!!! Error: Data path folders creation failed !!!\n!!! %s !!!" % dataPath
            return False
    else:
        return True
