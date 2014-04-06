#-- Modul Import --#
from appli.prodManager.scripts import prodManager

#-- ProdManager Istanciate --#
pm = prodManager.ProdManager()

#-- Projects Listing --#
pm.printProjects()

#-- New Project --#
# pm.newProject('test', 'dev')

#-- Load Project --#
pm.loadProject('asterix', 'ddd')

#-- Get ProdManager Params --#
pmDict = pm.getParams
print '*' * 100
print "#----- Get ProdManager Params -----#"
print pmDict
print '*' * 100

#-- Print ProdManager Params --#
pm.printProdManagerParams()

#-- Get Project Params --#
projectDict = pm.project.getParams
print '*' * 100
print "#----- Get Project Params -----#"
print projectDict
print '*' * 100

#-- Print Project Params --#
pm.printProjectParams()

#-- Edit ProdManager Project Params --#
# pm.project.projectEnd = '2015/03/29'
# pm.project.addTree('treeName', new=True)
# pm.project.writeProjectFile()

#-- Get Tree Params --#
assetTree = getattr(pm, 'assetTree')
treeDict = assetTree.getParams
print '*' * 100
print "#----- Get Tree Params -----#"
print treeDict
print '*' * 100

#-- Print Tree Params --#
pm.printTreeParams('asset')

#-- Add Project Tree Node --#
nodeParams1 = {'nodeType': 'assetCtnr', 'nodeLabel': 'chars',
               'nodeName': 'chars', 'nodePath': 'chars'}
assetTree.addNode(**nodeParams1)
nodeParams2 = {'nodeType': 'assetCtnr', 'nodeLabel': 'main',
               'nodeName': 'main', 'nodePath': 'chars/main'}
assetTree.addNode(**nodeParams2)
nodeParams3 = {'nodeType': 'asset', 'nodeLabel': 'asterix',
               'nodeName': 'asterix', 'nodePath': 'chars/main/asterix'}
assetTree.addNode(**nodeParams3)
pm.printTreeParams('asset')
# assetTree.writeTreeToFile()
