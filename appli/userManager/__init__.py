import os
from lib.qt import procQt as pQt


#-- Packager Var --#
toolPath = os.path.normpath(os.path.dirname(__file__))
toolName = toolPath.split(os.sep)[-1]
toolPack = __package__


#-- Global Var --#
user = os.environ.get('username')
binPath = os.path.join('G:', os.sep, 'rndBin', 'userManager')
wsPath = "F:/rnd/workspace/bank"
defaultIcone = os.path.join(toolPath, '_lib', 'ima', 'noImage.png')
nConvert = os.path.normpath(os.path.join(wsPath, "lib/system/_lib/nConvert/nconvert.exe"))


#-- Show Info --#
print '########## %s ##########' % toolName.upper()
print 'Tool Path : ', toolPath
print 'Tool Package : ', toolPack
print '#%s#' % ('-'*(22+len(toolName)))
print 'User : ', user
print 'Bin Path : ', binPath
pQt.CompileUi(uiDir=os.path.join(toolPath, 'ui'))
print '%s\n' % ('#'*(22+len(toolName)))
