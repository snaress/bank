from PyQt4 import QtGui


def styleSheet(styleType, color, rgb=None):
    """ Return color styleSheet string. If rgb is not None, color key will not be evaluated
        @param styleType: (str) : Style attribute
        @param color: (str) : Background color ('black', 'darkGrey', 'grey', 'lightGrey')
        @param rgb: (tuple) : Background color (int, int, int)
        @return: (str) : Background color style sheet """
    if rgb is None:
        colors = ['black', 'darkGrey', 'grey', 'lightGrey']
        if color in colors:
            if color == 'black':
                return "%s: rgb(0, 0, 0)" % styleType
            elif color == 'darkGrey':
                return "%s: rgb(62, 62, 62)" % styleType
            elif color == 'grey':
                return "%s: rgb(127, 127, 127)" % styleType
            elif color == 'lightGrey':
                return "%s: rgb(192, 192, 192)" % styleType
        else:
            raise KeyError, "Unknown color: %s. Should be in %s" % (color, colors)
    else:
        return "%s: rgb(%s, %s, %s)" % (styleType, rgb[0], rgb[1], rgb[2])

def qtColor(color, rgb=None):
    """ Return QColor object. If rgb is not None, color key will not be evaluated
        @param color: (str) : Background color ('black', 'darkGrey', 'grey', 'lightGrey')
        @param rgb: (tuple) : Background color (int, int, int)
        @return: (object) : QColor """
    if rgb is None:
        colors = ['black', 'darkGrey', 'grey', 'lightGrey']
        if color in colors:
            if color == 'black':
                return QtGui.QColor(0, 0, 0)
            if color == 'darkGrey':
                return QtGui.QColor(62, 62, 62)
            if color == 'grey':
                return QtGui.QColor(127, 127, 127)
            if color == 'lightGrey':
                return QtGui.QColor(192, 192, 192)
        else:
            raise KeyError, "Unknown color: %s. Should be in %s" % (color, colors)
    else:
        return QtGui.QColor(rgb[0], rgb[1], rgb[2])
