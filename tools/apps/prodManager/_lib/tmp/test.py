import os
from tools.apps.prodManager.scripts import prodManager


pm = prodManager.ProdManager()
pm.loadProject('asterix', 'ddd')
# pm.shotTreeObj.printTree()
node = pm.shotTreeObj.getNodeByName('s001_p001')
# print node.ltTreeObj.__dict__
ltTree = node.ltTreeObj
# print ltTree.__dict__
dataLtFile = os.path.join(node._dataLtPath, 'lt-%s.py' % (node.nodeName))
params = {'ltTitle': 'Test', 'ltUser': 'kheops', 'ltDate': '2014/03/22', 'ltTime': '16:10:15',
          'ltWorkDir': node.shotWorkDir, 'ltDataFile': dataLtFile, 'ltStep': 'anim',
          'ltStepList': pm.projectShotSteps.keys()}
ltTree.newLineTest(**params)
# params2 = {'ltTitle': 'Test', 'ltUser': 'kheops', 'ltDate': '2014/03/22', 'ltTime': '16:10:15',
#           'ltWorkDir': node.shotWorkDir, 'ltDataFile': node._dataLtFile, 'ltStep': 'lighting',
#           'ltStepList': pm.projectShotSteps.keys()}
# ltTree.newLineTest(**params2)
# ltTree.writeLineTest()
# treeNode = pm.shotTreeObj.getNodeByName('s001_p001')
# print treeNode.shotIn
# treeNode.shotIn = 1
# print treeNode.shotIn
# treeNode.writeNode()

# node = pm.shotTreeObj.getNodeByName('s001_p001')
# print node.nodeName
# d = pm.shotTreeObj.getNodeParams('s001_p001')
# print d
# pm.printDict()
# pm.writeTree('shotTree')
# params1 = {'nodeType': 'assetFld', 'nodeName': 'char', 'nodeLabel': 'char', 'nodePath': 'char'}
# params2 = {'nodeType': 'assetFld', 'nodeName': 'toto', 'nodeLabel': 'toto', 'nodePath': 'test/toto'}
# params3 = {'nodeType': 'assetFld', 'nodeName': 'test2', 'nodeLabel': 'test2', 'nodePath': 'test2'}
# if pm.assetTreeObj.addNode(**params1):
#     pm.writeTree('assetTree')
# pm.assetTreeObj.addNode(**params2)
# pm.assetTreeObj.addNode(**params3)
# pm.printTreeObj('assetTree')

