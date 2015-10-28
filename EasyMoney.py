#!/usr/local/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ImportBase import ImportBase
from DbConnection import DbConnection
from Ui_MainWindow import Ui_MainWindow
from Control_MainWindow import Control_MainWindow

if  __name__ == '__main__':
    #dbFile = "/Users/laban/Documents/Ekonomi/Transactions.db"
    dbFile = "/home/laban/Documents/Ekonomi/Transactions.db"
    with DbConnection(dbFile, False) as db:
        print("Database:", dbFile)

        # Initiate data class
        ib = ImportBase(db)
        
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        ctl = Control_MainWindow(ui, ib)       
        
        window.show()
        app.exec_()

        # SAS Eurobonus Mastercard
        # inputFilename = "/Users/laban/Documents/Ekonomi/SAS Eurobonus Mastercard/"
        # card = "Fredriksson Simon (nnnnnn******nnnn)"
        # ib.importFile(inputFilename + "Kontoutdrag-201405.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201406.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201407.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201408.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201409.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201410.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201411.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201412.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201501.xlsx", card)
        # ib.importFile(inputFilename + "Kontoutdrag-201502.xlsx", card)

        # Diners
        # inputFilename = "/Users/laban/Documents/Ekonomi/Diners Club/"
        # card = "Diners Club"
        # ib.importFile(inputFilename + "Diners20140618.xls", card)
        # ib.importFile(inputFilename + "Diners20140721.xls", card)
        # ib.importFile(inputFilename + "Diners20140819.xls", card)
        # ib.importFile(inputFilename + "Diners20140918.xls", card)
        # ib.importFile(inputFilename + "Diners20141021.xls", card)
        # ib.importFile(inputFilename + "Diners20141118.xls", card)
        # ib.importFile(inputFilename + "Diners20141218.xls", card)
        # ib.importFile(inputFilename + "Diners20150120.xls", card)
        # ib.importFile(inputFilename + "Diners20150217.xls", card)

        # Swedbank
        # inputFilename = "/Users/laban/Documents/Ekonomi/Swedbank/Swedbank_20140530-20150304.txt"
        # card = "Privatkonto (nnnnn.nnnnnnnnnn)"
        # codepage = "utf8"
        # ib.importFile(inputFilename, card, codepage)

