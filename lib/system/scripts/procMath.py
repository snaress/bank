import math
import random


def getDistance(p1, p2):
    """ Get distance between two 3d points
        @param p1: (list) : First point coord (list[float(x), float(y), float(z)])
        @param p2: (list) : Second point coord (list[float(x), float(y), float(z)])
        @return: (float) : Distance between p1 and p2 """
    dist = math.sqrt(math.pow((p1[0]-p2[0]), 2) +
                     math.pow((p1[1]-p2[1]), 2) +
                     math.pow((p1[2]-p2[2]), 2))
    return dist

def coordOp(p1, p2, operation):
    """ Coord operations
        @param p1: (list) : First point coord (list[float(x), float(y), float(z)])
        @param p2: (list) : Second point coord (list[float(x), float(y), float(z)])
        @param operation: (str) : 'plus', 'minus', 'mult', 'divide' or 'average'
        @return: (list) : New coord (list[float(x), float(y), float(z)]) """
    operations = ('plus', 'minus', 'mult', 'divide', 'average')
    if not operation in operations:
        raise NotImplementedError("The operation must be in %s" % ", ".join(operations))
    newCoord = []
    if operation == 'plus':
        for x, y in zip(p1, p2):
            newCoord.append(x + y)
    elif operation == 'minus':
        for x, y in zip(p1, p2):
            newCoord.append(x - y)
    elif operation == 'mult':
        for x, y in zip(p1, p2):
            newCoord.append(x * y)
    elif operation == 'divide':
        for x, y in zip(p1, p2):
            newCoord.append(x / y)
    elif operation == 'average':
        for x, y in zip(p1, p2):
            newCoord.append((x + y) / 2)

def getRandomSeq(ampMin=-5, ampMax=5, bias=False, biasMin=-3, biasMax=3, octaves=4, frequence=2):
    """ Create random sequence from params
        @param ampMin: (float) : Amplitude Minimum
        @param ampMax: (float) : Amplitude Maximum
        @param bias: (bool) : Amplitude Bias on or off
        @param biasMin: (float) : Bias Minimum
        @param biasMax: (float) : Bias Maximum
        @param octaves: (int) : Number of random value to create
        @param frequence: (int) : Octaves repetition
        @return: (list) : Random sequence """
    #-- Create Random Sequence --#
    randSeq = []
    for n in range(octaves):
        rand = random.uniform(ampMin, ampMax)
        if bias:
            if not rand > biasMax and not rand < biasMin:
                if rand > (ampMin + ampMax)/2:
                    rand = random.uniform(biasMax, ampMax)
                else:
                    rand = random.uniform(biasMin, ampMin)
        randSeq.append(rand)
    #-- Create Random Frequence --#
    rOctaves = randSeq
    for m in range(frequence-1):
        randSeq.extend(rOctaves)
    return randSeq

def getSinRandomSeq(ampMin=-5, ampMax=5, bias=False, biasMin=-3, biasMax=3, octaves=4, frequence=2):
    """ Create sinusoidal random sequence from params
        @param ampMin: (float) : Amplitude Minimum
        @param ampMax: (float) : Amplitude Maximum
        @param bias: (bool) : Amplitude Bias on or off
        @param biasMin: (float) : Bias Minimum
        @param biasMax: (float) : Bias Maximum
        @param octaves: (int) : Number of random value to create
        @param frequence: (int) : Octaves repetition
        @return: (list) : Random sequence """
    #-- Create Sinusoidal Random Sequence --#
    randSeq = []
    rand = 0
    sign = ''
    for n in range(octaves):
        #-- Random Init --#
        if sign == '':
            rand = random.uniform(ampMin, ampMax)
            if rand > (ampMin + ampMax)/2:
                sign = '+'
                if bias:
                    if not rand > biasMax and not rand < biasMin:
                        rand = random.uniform(biasMax, ampMax)
            else:
                sign = '-'
                if bias:
                    if not rand > biasMax and not rand < biasMin:
                        rand = random.uniform(ampMin, biasMin)
        #-- Random Lo --#
        elif sign == '+':
            rand = random.uniform(ampMin, (ampMin + ampMax)/2)
            if bias:
                if not rand > biasMax and not rand < biasMin:
                    rand = random.uniform(ampMin, biasMin)
            sign = '-'
        #-- Random Hi --#
        elif sign == '-':
            rand = random.uniform((ampMin + ampMax)/2, ampMax)
            if bias:
                if not rand > biasMax and not rand < biasMin:
                    rand = random.uniform(biasMax, ampMax)
            sign = '+'
        randSeq.append(rand)
    #-- Create Random Frequence --#
    rOctaves = randSeq
    for m in range(frequence-1):
        randSeq.extend(rOctaves)
    return randSeq
