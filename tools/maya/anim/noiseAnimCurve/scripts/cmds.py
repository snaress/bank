import random
import maya.cmds as mc


def getSelAnimCurves():
    """ Get selcted curves from graphEditor
        @return: (list) : Selected curves name """
    return mc.keyframe(q=True, n=True)

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
        for k in range(nk):
            nf.append(mc.keyframe(curve, q=True, index=(k,k))[0])
        #-- Create dict --#
        curveInfo[curve] = {}
        curveInfo[curve]['nodes'] = nodes
        curveInfo[curve]['nk'] = nk
        curveInfo[curve]['nf'] = nf
        curveInfo[curve]['duree'] = (nf[nk-1] - nf[0]) + 1
    return curveInfo

def getRandomSeq(**kwargs):
    """ Create random sequence from params
        @param kwargs: (dict) : Noise Params
            @keyword noiseType: (str) : 'random' or sinRandom'
            @keyword min: (float) : Amplitude Minimum
            @keyword max: (float) : Amplitude Maximum
            @keyword bias: (bool) : Amplitude Bias on or off
            @keyword biasMin: (float) : Bias Minimum
            @keyword biasMax: (float) : Bias Maximum
            @keyword octaves: (int) : Number of random value to create
            @keyword frequence: (int) : Octaves repetition
        @return: (list) : Random sequence """
    #-- Create Random Sequence --#
    randSeq = []
    for n in range(kwargs['octaves']):
        rand = random.uniform(kwargs['min'], kwargs['max'])
        if kwargs['bias']:
            if not rand > kwargs['biasMax'] and not rand < kwargs['biasMin']:
                if rand > (kwargs['min'] + kwargs['max'])/2:
                    rand = random.uniform(kwargs['biasMax'], kwargs['max'])
                else:
                    rand = random.uniform(kwargs['biasMin'], kwargs['min'])
        randSeq.append(rand)
    #-- Create Random Frequence --#
    rOctaves = randSeq
    for m in range(kwargs['frequence']-1):
        randSeq.extend(rOctaves)
    #-- Return Random List --#
    printNoiseParams(**kwargs)
    return randSeq

def createCurves(curveInfo, randSeq):
    """ Create new curves with noise params
        @param curveInfo: (dict) : Selected curves info
        @param randSeq: (list) : Random sequence
        @return: (dict) : New curves info """
    newCurves = {}
    for curve in curveInfo.keys():
        newCurves[curve] = {}
        step = curveInfo[curve]['duree'] / len(randSeq)-1
        newCurves[curve]['step'] = step
        for n, rand in enumerate(randSeq):
            ind = curveInfo[curve]['nf'][0] + (step * (n+1))
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

def printNoiseParams(**kwargs):
    """ Print noise params
        @param kwargs: (dict) : Noise Params """
    print "\n", "#" * 60
    print "#-- Noise Params --#"
    for k, v in kwargs.iteritems():
        print k, ' = ', v
    print "#" * 60

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
