import os, sys


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)

from lib.qt import textEditor
from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)
window = textEditor.TextEditor()
window.show()
sys.exit(app.exec_())