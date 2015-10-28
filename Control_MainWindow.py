
import locale, copy, functools
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication

class Control_MainWindow:
    # Getting UI and ImportBase
        
    def accountChanged(self, index):
        data = self.accountsLists[index]
        self.accountChangedToId = data['acId']
        print("Account changed:", index, data)
        #if (data != None):
        #    self.populateTable(data.get("imId"))
    
    def importChanged(self, index):
        ui = self.ui
        data = self.importsList[index]
        print("New import:", index, data)
        if (data != None):
            self.currentImportIndex = index
            self.currentImportId = data.get("imId")
            self.populateTable(data.get("imId"))
            ui.txt_Comment.setText(data.get("imComment"))
            self.importComment = data.get("imComment")
            
            # Populate accounts dropdown
            try:
                ui.sel_Accounts.currentIndexChanged.disconnect()
            except Exception as e:
                pass
            ui.sel_Accounts.clear()
            index = 0
            for entry in self.accountsLists:
                #print(entry)
                value = data.get("imAccount")
                account = entry.get("acId")
                ui.sel_Accounts.addItem("")
                ui.sel_Accounts.setItemText(index, entry.get("acName"))
                if (account == value):
                    ui.sel_Accounts.setCurrentIndex(index)
                index += 1
            ui.sel_Accounts.currentIndexChanged.connect(self.accountChanged)


    def tableValueChanged(self, row, cell, newValue = None, obj = None):
        entryType = self.tableData[row][cell]['type']

        if (entryType == "trIgnore"):
            if newValue == 2:
                newValue = "Y"
            else:
                newValue = "N"
        
        elif (entryType == "trDate"):
            newValue = newValue.toString('yyyy-MM-dd')
        
        elif (entryType == "trCategory"):
            obj = newValue
            i = obj.currentIndex()
            if (i < len(self.categoryList)):
                newValue = self.categoryList[i].get("caId")
            else:
                newValue = None

            print("Row:", row, "Cell", cell, "Value:", newValue, "Obj:", obj, "Index:", i)
            #pass
        
        elif (entryType == "trAmount"):
            item = self.ui.tableWidget.item(row, cell)
            newValue = item.text()

        elif (entryType == "trDescription"):
            item = self.ui.tableWidget.item(row, cell)
            newValue = item.text()

        recordId = self.tableData[row]['trId']
        oldValue = self.tableData[row][cell]['originalValue']
        #print("Old Value:", self.tableData[row][cell]['originalValue'])
        #print("New Value:", newValue)
        #print("entryType:", entryType)
        #print("recordId:", recordId)
        #uniq = str(recordId) + "_" + entryType
        updatedRecord = {'id':recordId, 'type':entryType, 'value':newValue, 'old':oldValue}
        self.actionHistory.append(updatedRecord)
        
    def populateTable(self, importId):
        ib = self.ib
        ui = self.ui
        
        try:
            ui.tableWidget.cellChanged.disconnect()
        except Exception as e:
            pass

        transactions = ib.getTransactions(importId)
        ui.tableWidget.clearContents()
        ui.tableWidget.setRowCount(len(transactions))
        ui.tableWidget.setSortingEnabled(False)
        self.tableData = {}
        rowNum = 0

        for row in transactions:
            cellNum = 0
            rowId = row.get('trId')
            self.tableData[rowNum] = {'trId':rowId}
            
            tr = QtWidgets.QTableWidgetItem(str(rowNum +1))
            tr.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            ui.tableWidget.setVerticalHeaderItem(rowNum, tr)

            fieldName = "trDate"
            td = self.createDateBox(row.get(fieldName))
            self.tableData[rowNum][cellNum] = {'type':fieldName, 'originalValue': row.get(fieldName)}
            ui.tableWidget.setCellWidget(rowNum, cellNum, td)
            td.dateChanged.connect(functools.partial(self.tableValueChanged, rowNum, cellNum))
            cellNum += 1

            fieldName = "trCategory"
            td = self.createCategoryDropdown(row.get('caName'))
            self.tableData[rowNum][cellNum] = {'type':fieldName, 'originalValue': row.get(fieldName)}
            ui.tableWidget.setCellWidget(rowNum, cellNum, td)
            td.currentIndexChanged.connect(functools.partial(self.tableValueChanged, rowNum, cellNum, td))
            cellNum += 1

            fieldName = "trAmount"
            td = QtWidgets.QTableWidgetItem()
            td.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            td.setText(locale.currency(row.get(fieldName), 0, 1))
            self.tableData[rowNum][cellNum] = {'type':fieldName, 'originalValue': row.get(fieldName)}
            ui.tableWidget.setItem(rowNum, cellNum, td)
            cellNum += 1

            fieldName = "trIgnore"
            td = QtWidgets.QCheckBox()
            if (row.get(fieldName) == "Y"):
                td.setChecked(True)
            self.tableData[rowNum][cellNum] = {'type':fieldName, 'originalValue': row.get(fieldName)}
            ui.tableWidget.setCellWidget(rowNum, cellNum, td)
            td.stateChanged.connect(functools.partial(self.tableValueChanged, rowNum, cellNum))
            cellNum += 1

            fieldName = "trDescription"
            td = QtWidgets.QTableWidgetItem()
            td.setText(str(row.get(fieldName)))
            self.tableData[rowNum][cellNum] = {'type':fieldName, 'originalValue': row.get(fieldName)}
            ui.tableWidget.setItem(rowNum, cellNum, td)
            cellNum += 1
            
            rowNum += 1
        
        #print("Transactions:", transactions)
        #print("TableData:", self.tableData)
        ui.tableWidget.setSortingEnabled(True)
        ui.tableWidget.cellChanged.connect(self.tableValueChanged)

    def createDateBox(self, dateValue):
        dw = QtWidgets.QDateEdit(self.ui.centralWidget)
        dw.setDate(QtCore.QDate.fromString(dateValue, 'yyyy-MM-dd'))
        #dw.setDateTime(QtCore.QDateTime(QtCore.QDate(2012, 12, 1), QtCore.QTime(0, 0, 0)))
        dw.setCalendarPopup(True)
        #self.horizontalLayout.addWidget(dw)
        return dw

    def createCategoryDropdown(self, categoryValue):
        sel = QtWidgets.QComboBox(self.ui.centralWidget)
        index = 0
        for entry in self.categoryList:
            sel.addItem("")
            value = entry.get("caName")
            sel.setItemText(index, value)
            if (categoryValue == value):
                sel.setCurrentIndex(index)
            index += 1
        
        if (categoryValue == None):
            sel.addItem("Undefined")
            sel.setCurrentIndex(index)

        return sel
        
    def saveTable(self):
        for data in self.actionHistory:
            transactionId = data['id']
            fieldName = data['type']
            newValue = data['value']
            self.ib.setTransactionValue(transactionId, fieldName, newValue)
            print(data)
        
        if (self.accountChangedToId and self.currentImportId):
            self.ib.setAccount(self.currentImportId, self.accountChangedToId)
            self.accountChangedToId = None
            print("Saved account.")

        if (self.ui.txt_Comment.text() != self.importComment):
            self.importComment = self.ui.txt_Comment.text()
            self.ib.setImportComment(self.currentImportId, self.importComment)
            print("Saved comment.")

        self.ib.commit()
        print("Saved data!")
        print(self.actionHistory)
        self.actionHistory = []

    def setCategories(self):
        title = "Change categories?"
        msgtext = "This will attempt to change category of all entries in this list that are currently undefined, and reload the current set. This will undo any unsaved changes!\n\nWould you like to do this?"
        buttons = QMessageBox.Yes | QMessageBox.No
        defaultButton = QMessageBox.Yes
        reply = QMessageBox.question(None, title, msgtext, buttons, defaultButton)
        print("Reply:", reply)
        if (reply == QMessageBox.Yes):
            self.ib.updateBadDescriptions(self.currentImportId)
            self.ib.updateMissingCategories(self.currentImportId)
            self.importChanged(self.currentImportIndex)
            
        #QtGui.QMessageBox.information(self, 'Message Title', 'The Bosy Text', QtGui.MessageBox.No | QtGui.MessageBox.Yes | QtGui.MessageBox.Cancel)

    def __init__(self, ui, ib):
        #locale.setlocale(locale.LC_ALL, 'sv_SE')
        #_translate = QtCore.QCoreApplication.translate
        self.ui = ui
        self.ib = ib
        self.categoryList = self.ib.getCategories()
        self.accountsLists = self.ib.getAccounts()
        self.actionHistory = []
        self.accountChangedToId = None
        self.currentImportId = None

        ui.btn_Save.clicked.connect(self.saveTable)
        ui.btn_AutoInfo.clicked.connect(self.setCategories)

        # Populate imports dropdown and flll the table with the last import
        ui.sel_Import.clear()
        index = 0
        self.importsList = ib.getImports()
        for entry in self.importsList:
            ui.sel_Import.addItem("")
            ui.sel_Import.setItemText(index, entry.get("imComment"))
            index += 1

        ui.sel_Import.currentIndexChanged.connect(self.importChanged)
        ui.sel_Import.setCurrentIndex(index -1)
        # This will execute self.importChanged(index -1)
