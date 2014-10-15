import os, sys, optparse


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)


#-- Options --#
usage = "userManager -v [Verbose Index]"
parser = optparse.OptionParser(usage=usage)
parser.add_option('-v', '--verbose', type='choice', default='info',
                  choices=['critical', 'error', 'warning', 'info', 'debug'],
                  help=''.join(["[choice=['critical', 'error', 'warning', 'info', 'debug']] ",
                                "Log level (default='info')"]))


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    from appli.userManager import userManagerUi
    userManagerUi.launch(logLvl=options['verbose'])