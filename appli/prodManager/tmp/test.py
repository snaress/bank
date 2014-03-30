from appli.prodManager.scripts import prodManager

pm = prodManager.ProdManager()
# pm.newProject('asterix', 'ddd')
pm.loadProject('asterix', 'ddd')
# pm.project.projectEnd = '2015/03/29'
# pm.project.projectTrees.append('asset')
# pm.project.writeProjectFile()
pm.project.printParams()