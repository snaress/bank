import os, sys


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)


#-- Launch Tool --#
from PyQt4 import QtGui
from appli.prodManager.scripts import prodManagerUi


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = prodManagerUi.ProdManagerUi()
    window.show()
    sys.exit(app.exec_())
