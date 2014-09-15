import os, sys, optparse


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)

#-- Options --#
usage = "prodManager -o [prodId]"
parser = optparse.OptionParser(usage=usage)
parser.add_option('-o', '--open', type='string', help="[str] Prod id (ex:'lv--Le Voeu')")
parser.add_option('-v', '--verbose', type='choice', default='info',
                  choices=['critical', 'error', 'warning', 'info', 'debug'],
                  help=''.join(["[choice=['critical', 'error', 'warning', 'info', 'debug']] ",
                                "Log level (default='info')"]))


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    #-- Launch Tool --#
    from appli.prodManager import prodManagerUi as pmUi
    if options['open'] is None:
        pmUi.launch('loader', logLvl=options['verbose'])
    else:
        pmUi.launch('manager', prodId=options['open'], logLvl=options['verbose'])
