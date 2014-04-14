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


class RandomSequence(object):
    """ Create random sequence from given params
        @param randType: (str) : 'uniform' or 'sinusoidal'
        @param ampMin: (float) : Amplitude Minimum
        @param ampMax: (float) : Amplitude Maximum
        @param octaves: (int) : Number of random value to create
        @param frequence: (int) : Octaves repetition
        @param bias: (bool) : Amplitude Bias on or off
        @param biasMin: (float) : Bias Minimum
        @param biasMax: (float) : Bias Maximum """

    def __init__(self, randType, ampMin, ampMax, octaves, frequence, bias=False, biasMin=0, biasMax=0):
        self.randType = randType
        self.ampMin = ampMin
        self.ampMax = ampMax
        self.octaves = octaves
        self.frequence = frequence
        self.bias = bias
        self.biasMin = biasMin
        self.biasMax = biasMax

    def generate(self):
        """ Generate random sequence
            @return: (list) : Random sequence """
        if self.randType == 'uniform':
            return self.getUniformRand
        elif self.randType == 'sinusoidal':
            return self.getSinusoidalRand

    @property
    def getUniformRand(self):
        """ Create uniform random sequence from params
            @return: (list) : Uniform random sequence """
        #-- Create Random Sequence --#
        randSeq = []
        for n in range(self.octaves):
            rand = random.uniform(self.ampMin, self.ampMax)
            if self.bias:
                if not rand > self.biasMax and not rand < self.biasMin:
                    if rand > (self.ampMin + self.ampMax)/2:
                        rand = random.uniform(self.biasMax, self.ampMax)
                    else:
                        rand = random.uniform(self.biasMin, self.ampMin)
            randSeq.append(rand)
        #-- Create Random Frequence --#
        rOctaves = randSeq
        for m in range(self.frequence-1):
            randSeq.extend(rOctaves)
        return randSeq

    @property
    def getSinusoidalRand(self):
        """ Create sinusoidal random sequence from params
            @return: (list) : Sinusoidal random sequence """
        #-- Create Sinusoidal Random Sequence --#
        randSeq = []
        rand = 0
        sign = ''
        for n in range(self.octaves):
            #-- Random Init --#
            if sign == '':
                rand = random.uniform(self.ampMin, self.ampMax)
                if rand > (self.ampMin + self.ampMax)/2:
                    if self.bias:
                        rand = self.getSinBiasValue(rand, '-')
                    sign = '+'
                else:
                    if self.bias:
                        rand = self.getSinBiasValue(rand, '+')
                    sign = '-'
            #-- Random Lo --#
            elif sign == '+':
                rand = random.uniform(self.ampMin, (self.ampMin + self.ampMax)/2)
                if self.bias:
                    rand = self.getSinBiasValue(rand, sign)
                sign = '-'
            #-- Random Hi --#
            elif sign == '-':
                rand = random.uniform((self.ampMin + self.ampMax)/2, self.ampMax)
                if self.bias:
                    rand = self.getSinBiasValue(rand, sign)
                sign = '+'
            randSeq.append(rand)
        #-- Create Random Frequence --#
        rOctaves = randSeq
        for m in range(self.frequence-1):
            randSeq.extend(rOctaves)
        return randSeq

    def getSinBiasValue(self, rand, sign):
        """ Get bias value from given params
            @param rand: (float) : Random value
            @param sign: (str) : '-' or '+'
            @return: (float) : Bias value """
        if not rand > self.biasMax and not rand < self.biasMin:
            if sign == '+':
                rand = random.uniform(self.ampMin, self.biasMin)
            else:
                rand = random.uniform(self.biasMax, self.ampMax)
        return rand

    def printRandParams(self):
        """ Print noise params
            @param kwargs: (dict) : Noise Params """
        print "\n", "#" * 60
        print "#-- Random Params --#"
        for k, v in self.__dict__.iteritems():
            print k, ' = ', v
        print "#" * 60


if __name__ == '__main__':
    r = RandomSequence('sinusoidal', -5, 5, 10, 2, bias=True, biasMin=-3, biasMax=3)
    r.printRandParams()
    rand = r.generate()
    for val in rand:
        print val
