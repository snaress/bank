import os, sys


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)


#-- Launch --#
from PyQt4 import QtGui
from lib.qt import textEditor
app = QtGui.QApplication(sys.argv)
window = textEditor.TextEditor()
window.show()
sys.exit(app.exec_())
