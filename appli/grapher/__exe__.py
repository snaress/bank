import os, sys, optparse


#-- SysPath --#
wsPath = os.path.join('F:', os.sep, 'rnd', 'workspace')
bankPath = os.path.join(wsPath, 'bank')
sys.path.insert(0, bankPath)

#-- Options --#
usage = "Grapher launcher usage ..."
parser = optparse.OptionParser(usage=usage)

parser.add_option('-o', '--open', type='string', help="[str] Open given graphFile.")


if __name__ == '__main__':
    options, args = parser.parse_args()
    options = eval(str(options))

    #-- Launch Tool --#
    from appli.grapher import grapherUi
    if options['open'] is None:
        grapherUi.launch()
    else:
        print options['open']
        grapherUi.launch(graph=options['open'])
