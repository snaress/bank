import maya.cmds as mc
from lib.system.scripts import procMath as pMath


def getSelAnimCurves():
    """ Get selcted curves from graphEditor
        @return: (list) : Selected curves name """
    return mc.keyframe(q=True, n=True, sl=True) or []

def getCurveInfo(animCurves):
    """ store info from selected curves
        @param animCurves: (list) : Selected curves name
        @return: (dict) : Selected curves info """
    curveInfo = {}
    for curve in animCurves:
        #-- Get Connections --#
        nodes = None
        if mc.listConnections(curve, p=True) is not None:
            nodes = mc.listConnections(curve, p=True)
        #-- Get Frame Info --#
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

def addAttrOnCurves(curveInfo):
    """ Add and set curve attributes
        @param curveInfo: (dict) : Selected curves info """
    for curve in curveInfo.keys():
        if not mc.objExists('%s.nac_initState' % curve):
            mc.addAttr(curve, ln='nac_initState', dt='string')
        if not mc.objExists('%s.nac_storedState' % curve):
            mc.addAttr(curve, ln='nac_storedState', dt='string')
        curveState = {}
        for n, f in enumerate(curveInfo[curve]['nf']):
            curveState[str(f)] = curveInfo[curve]['val'][n]
        mc.setAttr('%s.nac_initState' % curve, curveState, type='string')

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
    #-- Create Random Sequence --#
    r = pMath.RandomSequence(kwargs['randType'], kwargs['min'], kwargs['max'], kwargs['octaves'],
                             kwargs['frequence'], bias=kwargs['bias'], biasMin=kwargs['biasMin'],
                             biasMax=kwargs['biasMax'])
    randSeq = r.generate()
    #-- Create Random Frequence --#
    rOctaves = randSeq
    for m in range(kwargs['frequence']-1):
        randSeq.extend(rOctaves)
    #-- Return Random List --#
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
