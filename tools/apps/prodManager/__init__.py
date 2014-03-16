import os


#-- Packager Var --#
toolPath = os.path.normpath(os.path.dirname(__file__))
toolName = toolPath.split(os.sep)[-1]
toolPack = __package__

#-- Global Var --#
user = os.environ.get('username')
station = os.environ.get('computername')
rootDisk = os.path.join('F:', os.sep)
libPath = os.path.join(toolPath, '_lib')
binPath = os.path.join('G:', os.sep, 'rndBin', toolName)

#-- UI Files --#
uiL = os.listdir(os.path.join(toolPath, 'ui')) or []
uiList = {}
for ui in uiL:
    if ui.endswith('.ui') and not ui.startswith('.'):
        uiList[ui.replace('.ui', '')] = os.path.join(toolPath, 'ui', ui)

#-- Ima Files --#
imaL =  os.listdir(os.path.join(libPath, 'ima')) or []
imaList = {}
for ima in imaL:
    if not ima.startswith('.') and os.path.isfile(os.path.join(libPath, 'ima', ima)):
        imaList[ima] = os.path.join(libPath, 'ima', ima)

#-- Show Info --#
print '########## %s ##########' % toolName.upper()
print 'Tool Path : ', toolPath
print 'Tool Package : ', toolPack
print '#%s#' % ('-'*(22+len(toolName)))
print 'User : ', user
print 'Station : ', station
print 'Lib Path : ', libPath
print 'Bin Path : ', binPath
print '#%s#' % ('-'*(22+len(toolName)))
for ui in sorted(uiList):
    print '%s : %s' % (ui, uiList[ui])
print '#%s#' % ('-'*(22+len(toolName)))
for ima in sorted(imaList):
    print '%s : %s' % (ima, imaList[ima])
print '%s\n' % ('#'*(22+len(toolName)))
