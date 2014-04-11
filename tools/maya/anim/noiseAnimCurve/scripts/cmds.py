import random
import maya.cmds as mc


def getSelAnimCurves():
    return mc.keyframe(q=True, n=True)

def getCurveInfo(animCurves):
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

def createRandomSeq(**kwargs):
    randSeq = []
    for n in range(kwargs['octaves']):
        randSeq.append(random.uniform(kwargs['min'], kwargs['max']))
    rOctaves = randSeq
    for m in range(kwargs['frequence']-1):
        randSeq.extend(rOctaves)
    return randSeq

def createCurves(curveInfo, randSeq):
    print curveInfo
    for curve in curveInfo.keys():
        step = curveInfo[curve]['duree'] / len(randSeq)
        for n, rand in enumerate(randSeq):
            ind = curveInfo[curve]['nf'][0] + (step * n)
            val = mc.keyframe(curve, q=True, t=(ind, ind), ev=True)
            if val is not None:
                mc.setKeyframe(curve, t=[ind], v=val[0]+rand)
