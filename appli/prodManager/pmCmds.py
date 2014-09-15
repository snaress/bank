import os
from PyQt4 import QtGui, QtCore
from lib.qt import procQt as pQt
from lib.system import procFile as pFile


class LoaderCmds(object):

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.rootPath = os.path.join(self.mainUi._binPath, 'pref')
        self.prefFile = os.path.join(self.rootPath, "%s.py" % self.mainUi._user)

    def rf_allProds(self):
        """ Refresh 'All Prods' treeWidget """
        self.mainUi.twAll.clear()
        prods = os.listdir(self.mainUi._prodsPath) or []
        items = []
        for prod in sorted(prods):
            newItem = self._newItem(prod.split('--')[0], prod.split('--')[1])
            items.append(newItem)
        self.mainUi.twAll.addTopLevelItems(items)
        self.mainUi.twAll.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)

    def rf_prefProds(self):
        """ Refresh 'User Prods' treeWidget """
        self.mainUi.twPref.clear()
        self._checkPrefPath()
        bookMarks = pFile.readPyFile(self.prefFile)['prodBookMarks']
        items = []
        for prod in sorted(bookMarks):
            newItem = self._newItem(prod.split('--')[0], prod.split('--')[1])
            items.append(newItem)
        self.mainUi.twPref.addTopLevelItems(items)
        self.mainUi.twPref.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)

    def rf_itemStyle(self, twTree):
        """ Refresh items font color
            @param twTree: (object) : QTreeWidget """
        pQt.rf_selTreeItemTextColor(twTree, color1='black', color2='lightGrey')

    def on_createNewProd(self):
        """ Command launched when 'Create New Prod' pushButton is clicked """
        mess = "Create New Prod:\nLine 1: Prod Alias\nLine 2: Prod Name"
        self.newProdDialog = pQt.PromptDialog(mess, self.createNewProd, Nlines=2)
        self.newProdDialog.exec_()

    def createNewProd(self):
        """ Create new prod """
        prodAlias = self.newProdDialog.result()['result_1']
        prodName = self.newProdDialog.result()['result_2']
        if prodAlias == '' or prodName == '':
            error = "Prod Alias and Prod Name must be edited !!!"
            pQt.errorDialog(error, self.newProdDialog)
        else:
            result = self.mainUi.createNewProd(self.mainUi._prodsPath, prodAlias, prodName)
            if not isinstance(result, bool):
                error = result.replace('error__', '')
                pQt.errorDialog(error, self.newProdDialog)
            else:
                self.mainUi.log.info("New prod successfully created: %s--%s." % (prodAlias, prodName))
                self.newProdDialog.close()
                self.rf_allProds()

    def on_includeToPref(self):
        """ Include selected prods into user prodBokkMarks """
        prefDict = pFile.readPyFile(self.prefFile)
        selItems = self.mainUi.twAll.selectedItems() or []
        for item in selItems:
            if not item.prodId in prefDict['prodBookMarks']:
                prefDict['prodBookMarks'].append(item.prodId)
        txt = []
        for k, v in prefDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        pFile.writeFile(self.prefFile, '\n'.join(txt))
        self.mainUi.log.info("Pref file saved: %s" % self.mainUi._user)
        self.rf_prefProds()

    def on_removeFromPref(self):
        """ Remove Selected prods from user prodBookMarks """
        prefDict = pFile.readPyFile(self.prefFile)
        selItems = self.mainUi.twPref.selectedItems() or []
        for item in selItems:
            if item.prodId in prefDict['prodBookMarks']:
                prefDict['prodBookMarks'].pop(prefDict['prodBookMarks'].index(item.prodId))
        txt = []
        for k, v in prefDict.iteritems():
            if isinstance(v, str):
                txt.append("%s = %r" % (k, v))
            else:
                txt.append("%s = %s" % (k, v))
        pFile.writeFile(self.prefFile, '\n'.join(txt))
        self.mainUi.log.info("Pref file saved: %s" % self.mainUi._user)
        self.rf_prefProds()

    def _checkPrefPath(self):
        """ Check if pref path exists """
        if not os.path.exists(self.prefFile):
            result = self.mainUi.createPrefFile(self.prefFile)
            if not isinstance(result, bool):
                error = result.replace('error__', '')
                pQt.errorDialog(error, self.newProdDialog)
            else:
                self.mainUi.log.info("New user pref file successfully created: %s" % self.mainUi._user)

    def _newItem(self, prodAlias, prodName):
        """ Create new QTreeWidgetItem
            @param prodAlias: (str) : Prod alias
            @param prodName: (str) : Prod name
            @return: (object) : QTreeWidgetItem """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, prodAlias)
        newItem.setText(1, " -- ")
        newItem.setText(2, prodName)
        newItem.prodAlias = prodAlias
        newItem.prodName = prodName
        newItem.prodId = "%s--%s" % (prodAlias, prodName)
        newItem.prodPath = os.path.join(self.mainUi._prodsPath, newItem.prodId, '%s.py' % newItem.prodId)
        return newItem


class ManagerCmds(object):

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.pm = self.mainUi.pm
