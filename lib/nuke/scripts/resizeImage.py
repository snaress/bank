import os
from lib.system.scripts import procFile as pFile


class NukeResize(object):
    """ Class used for image resizing
        @param imaIn: (str) : Image absolut path to resize
        @param imaOut: (str) : New resized image absolut path
        @param imaX: (int) : Image Width
        @param imaY: (int) : Image Height
        @param rszX: (int) : New image width
        @param rszY: (int) : New image height """

    def __init__(self, imaIn, imaOut, imaX, imaY, rszX, rszY):
        self.imaIn = os.path.normpath(imaIn)
        self.imaOut = os.path.normpath(imaOut)
        self.imaX = imaX
        self.imaY = imaY
        self.rszX = rszX
        self.rszY = rszY
        self.nkFile = self.getNkFile()
        self.nkData = pFile.readFile(self.nkFile)
        self.rszData = self.getRszData()

    @staticmethod
    def getNkFile():
        """ Get resizeImage nuke file path
            @return: (str) : resizeImage nuke file path """
        toolPath = os.sep.join(os.path.normpath(os.path.dirname(__file__)).split(os.sep)[0:-1])
        return os.path.join(toolPath, '_lib', 'nkFiles', 'resizeImage.nk')

    def getRszData(self):
        """ Get resizeImage nuke file data
            @return: (list) : Nuke resizeImage data """
        rszData = []
        lOffset = 0
        for l in range(0, len(self.nkData), 1):
            l = l + lOffset
            if l <= len(self.nkData)-1:
                if (self.nkData[l].startswith('Read') or self.nkData[l].startswith('Reformat')
                    or self.nkData[l].startswith('Write')):
                    #-- Load --#
                    if self.nkData[l].startswith('Read'):
                        rszData.extend([self.nkData[l], self.nkData[l+1],
                                        ' file %s\n' % self.imaIn.replace('\\', '/'),
                                        ' format "%s %s 0 0 %s %s 1 "\n' % (self.imaX, self.imaY,
                                                                            self.imaX, self.imaY)])
                        lOffset += 3
                    #-- Reformat --#
                    if self.nkData[l].startswith('Reformat'):
                        rszData.extend([self.nkData[l], self.nkData[l+1],
                                        ' box_width %s\n' % self.rszX,
                                        ' box_height %s\n' % self.rszY])
                        lOffset += 3
                    #-- Write --#
                    if self.nkData[l].startswith('Write'):
                        rszData.extend([self.nkData[l],
                                        ' file %s\n' % self.imaOut.replace('\\', '/')])
                        lOffset += 1
                else:
                    rszData.extend([self.nkData[l]])
        return rszData

    def resize(self):
        """ Launch resize process """
        tmpFile = self.saveTmpFile()
        if tmpFile is not None:
            os.system("nuke5.0.exe -x %s 1" % tmpFile)

    def saveTmpFile(self):
        """ Save resizeData nuke tmp file
            @return: (str) : TmpFile absolut path """
        tmpPath = os.sep.join(self.imaIn.split(os.sep)[:-1])
        tmpName = '.'.join(self.imaIn.split(os.sep)[-1].split('.')[:-1])
        tmpFile = os.path.join(tmpPath, 'ri__%s.nk' % tmpName)
        try:
            pFile.writeFile(tmpFile, self.rszData)
            print "[RI] Writing tmpFile: %s" % tmpFile
            return tmpFile
        except:
            print "[RI] ERROR: Can't Write tmpFile: %s" % tmpFile
            return None
