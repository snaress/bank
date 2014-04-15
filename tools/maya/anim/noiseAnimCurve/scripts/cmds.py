import maya.cmds as mc
from lib.system.scripts import procMath as pMath


def getSelAnimCurves():
    """ Get selcted curves from graphEditor
        @return: (list) : Selected curves name """
    return mc.keyframe(q=True, n=True, sl=True) or []

def getCurveLinks(curve):
    """ Get curve output connections
        @param curve: (str) : Curve node name
        @return: (list) : Connected node list """
    nodes = None
    if mc.listConnections(curve, p=True) is not None:
        nodes = mc.listConnections(curve, p=True)
    return nodes

def getNacCurves():
    nacCurves = []
    for curve in mc.ls(type='animCurveTL'):
        if mc.objExists('%s.nac_links' % curve):
            nacCurves.append(curve)
    return nacCurves

def getCurveInfo(animCurves):
    """ store info from selected curves
        @param animCurves: (list) : Selected curves name
        @return: (dict) : Selected curves info """
    curveInfo = {}
    for curve in animCurves:
        nodes = getCurveLinks(curve)
        nk = mc.keyframe(curve, q=True, kc=True)
        nf = []
        vals = []
        for k in range(nk):
            f = mc.keyframe(curve, q=True, index=(k,k))[0]
            nf.append(f)
            vals.append(mc.keyframe(curve, q=True, t=(f, f), ev=True)[0])
        #-- Create dict --#
        curveInfo[curve] = {}
        curveInfo[curve]['nodes'] = nodes
        curveInfo[curve]['nk'] = nk
        curveInfo[curve]['nf'] = nf
        curveInfo[curve]['val'] = vals
        curveInfo[curve]['duree'] = (nf[nk-1] - nf[0]) + 1
    return curveInfo

def getRandomSeq(**kwargs):
    """ Create random sequence from params
        @param kwargs: (dict) : Noise Params
            @keyword randType: (str) : 'uniform' or 'sinusoidal'
            @keyword min: (float) : Amplitude Minimum
            @keyword max: (float) : Amplitude Maximum
            @keyword octaves: (int) : Number of random value to create
            @keyword frequence: (int) : Octaves repetition
            @keyword bias: (bool) : Amplitude Bias on or off
            @keyword biasMin: (float) : Bias Minimum
            @keyword biasMax: (float) : Bias Maximum
        @return: (list) : Random sequence """
    r = pMath.RandomSequence(kwargs['randType'], kwargs['min'], kwargs['max'], kwargs['octaves'],
                             kwargs['frequence'], bias=kwargs['bias'], biasMin=kwargs['biasMin'],
                             biasMax=kwargs['biasMax'])
    randSeq = r.generate()
    r.printRandParams()
    return randSeq

def getNewCurves(curveInfo, randSeq):
    """ Create new curves with noise params
        @param curveInfo: (dict) : Selected curves info
        @param randSeq: (list) : Random sequence
        @return: (dict) : New curves info """
    newCurves = {}
    for curve in curveInfo.keys():
        newCurves[curve] = {}
        step = curveInfo[curve]['duree'] / len(randSeq)
        newCurves[curve]['step'] = step
        for n, rand in enumerate(randSeq):
            ind = curveInfo[curve]['nf'][0] + (step * (n+1))
            if not ind >= curveInfo[curve]['nf'][-1]:
                val = mc.keyframe(curve, q=True, t=(ind, ind), ev=True)
                if val is not None:
                    newCurves[curve][ind] = {}
                    newCurves[curve][ind]['rand'] = rand
                    newCurves[curve][ind]['val'] = val[0]+rand
    return newCurves

def applyOnCurves(newCurves):
    """ Apply new curves params on selected curves
        @param newCurves: (dict) : New curves info """
    printNewCurvesInfo(newCurves)
    for curve in newCurves.keys():
        for k, v in newCurves[curve].iteritems():
            if not k == 'step':
                mc.setKeyframe(curve, t=k, v=v['val'])

def printNewCurvesInfo(newCurves):
    """ Print new curves info
        @param newCurves: (dict) : New curves info """
    print "\n", "#" * 60
    print "#-- New Curves Info --#"
    for curve in newCurves.keys():
        print "%s :" % curve
        print "\tStep = %s" % newCurves[curve]['step']
        frames = []
        for ind in newCurves[curve].keys():
            if not ind == 'step':
                frames.append(ind)
        frames.sort()
        for f in frames:
            print "\tFrame %s = %s" % (f, newCurves[curve][f])
    print "#" * 60

def checkCurveStatus(curve):
    """ Check curve status
        @param curve: (str): Curve name
        @return: (str) : Curve status ('init' or 'choice' or 'blend') """
    if not mc.objExists('%s.nac_links' % curve):
        mc.addAttr(curve, ln='nac_links', dt='string')
        mc.addAttr(curve, ln='nac_choice', dt='string')
        mc.addAttr(curve, ln='nac_blend', dt='string')
        mc.setAttr('%s.nac_links' % curve, getCurveLinks(curve), type='string')
        return 'init'
    nodeType = mc.nodeType(eval(mc.getAttr('%s.nac_links' % curve))[0])
    print nodeType
    if not nodeType in ['choice', 'blend']:
        mc.setAttr('%s.nac_links' % curve, getCurveLinks(curve), type='string')
        return 'init'
    if nodeType == 'choice':
        return 'choice'
    if nodeType == 'blend':
        return 'blend'

def convertToChoice(curve, status):
    if status == 'init':
        curveLinks = getCurveLinks(curve)
        mc.setAttr('%s.nac_links' % curve, curveLinks, type='string')
        newChoice = mc.createNode('choice', n='nac_choice_1')
        mc.connectAttr('%s.output' % curve, '%s.input[0]' % newChoice, f=True)
        for link in curveLinks:
            mc.disconnectAttr('%s.output' % curve, link)
            mc.connectAttr('%s.output' % newChoice, link)
