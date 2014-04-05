from appli.prodManager.scripts import prodManager


pm = prodManager.ProdManager()
# pm.newProject('asterix', 'ddd')
pm.loadProject('asterix', 'ddd')
# pm.project.projectEnd = '2015/03/29'
# pm.project.projectTrees.append('asset')
# pm.project.writeProjectFile()
# print tree.treeNodes
# params = {'nodeType': 'assetCtnr', 'nodeLabel': 'main',
#           'nodeName': 'main', 'nodePath': 'chars/main'}
# tree.addNode(**params)
# print tree.treeNodes
# tree.writeTreeToFile()
pm.printTreeParams('shot')
