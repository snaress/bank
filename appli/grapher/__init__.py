import os
from lib.maya import mayaEnv


#-- Packager Var --#
toolPath = os.path.normpath(os.path.dirname(__file__))
toolName = toolPath.split(os.sep)[-1]
toolPack = __package__


#-- Global Var --#
rootDir = os.path.join('G:', os.sep)
binPath = os.path.join('G:', os.sep, 'rndBin', toolName)
envFile = os.path.join(os.path.dirname(mayaEnv.__file__), 'mayaEnv.py').replace('\\', '/')
user = os.environ.get('username')
station = os.environ.get('computername')

#-- UI Files --#
uiL = os.listdir(os.path.join(toolPath, 'ui')) or []
uiList = {}
for ui in uiL:
    if ui.endswith('.ui') and not ui.startswith('.'):
        uiList[ui.replace('.ui', '')] = os.path.join(toolPath, 'ui', ui)


#-- Show Info --#
print '########## %s ##########' % toolName.upper()
print 'Tool Path : ', toolPath
print 'Tool Package : ', toolPack
print '#%s#' % ('-'*(22+len(toolName)))
print 'User : ', user
print 'Station : ', station
print '#%s#' % ('-'*(22+len(toolName)))
for ui in sorted(uiList):
    print '%s : %s' % (ui, uiList[ui])
print '%s\n' % ('#'*(22+len(toolName)))
