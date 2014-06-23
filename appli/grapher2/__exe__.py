import os, sys


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)


#-- Launch Tool --#
from appli.grapher2.scripts import grapherUi
if __name__ == '__main__':
    grapherUi.launch()

