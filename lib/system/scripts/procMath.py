import math


def secondsToStr(seconds):
    """ Convert number of seconds into humanized string
        @param seconds: (int) : Number of seconds
        @return: (str) : Humanized string """
    S = int(seconds)
    hours = S / 3600
    S = S - (hours * 3600)
    minutes = S / 60
    seconds = S - (minutes * 60)
    return "%s:%s:%s" % (hours, minutes, seconds)

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
