import os


#-- Packager Var --#
toolPath = os.path.normpath(os.path.dirname(__file__))
toolName = toolPath.split(os.sep)[-1]
toolPack = __package__


#-- Global Var --#
mayaToolsPath = os.sep.join(toolPath.split(os.sep)[:-2])


#-- UI Files --#
uiL = os.listdir(os.path.join(toolPath, 'ui')) or []
uiList = {}
for ui in uiL:
    if ui.endswith('.ui') and not ui.startswith('.'):
        uiList[ui.replace('.ui', '')] = os.path.join(toolPath, 'ui', ui)


#-- Show Info --#
def printToolInfo():
    print '########## %s ##########' % toolName.upper()
    print 'Tool Path : ', toolPath
    print 'Tool Package : ', toolPack
    print '#%s#' % ('-'*(22+len(toolName)))
    print 'mayaToolsPath : ', mayaToolsPath
    print '#%s#' % ('-'*(22+len(toolName)))
    for ui in sorted(uiList):
        print '%s : %s' % (ui, uiList[ui])
    print '%s\n' % ('#'*(22+len(toolName)))
