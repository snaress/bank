import os
import sys

#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
libPath = os.path.join('F:', os.sep, 'rnd', 'lib')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, libPath)
sys.path.insert(0, bankPath)

#-- Launch Tool --#
from PyQt4 import QtGui
from tools.apps.grapher.scripts import grapher

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = grapher.MainWindow()
    window.show()
    sys.exit(app.exec_())