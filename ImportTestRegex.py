#!/usr/local/bin/python3
from ImportBase import ImportBase
from DbConnection import DbConnection

if  __name__ =='__main__':   
   dbFile = "/Users/laban/Documents/Ekonomi/Transactions.db"
   with DbConnection(dbFile) as db:
      print("Database:", dbFile)
      ib = ImportBase(db)
      i = 0
      i += ib.updateMissingCategories(28)
      i += ib.updateMissingCategories(29)
      i += ib.updateMissingCategories(30)
      i += ib.updateMissingCategories(31)
      i += ib.updateMissingCategories(32)
      i += ib.updateMissingCategories(33)
      i += ib.updateMissingCategories(34)
      i += ib.updateMissingCategories(35)
      i += ib.updateMissingCategories(36)
      i += ib.updateMissingCategories(37)
      i += ib.updateMissingCategories(38)
      i += ib.updateMissingCategories(39)
      i += ib.updateMissingCategories(40)
      i += ib.updateMissingCategories(41)
      i += ib.updateMissingCategories(42)
      i += ib.updateMissingCategories(43)
      i += ib.updateMissingCategories(44)
      i += ib.updateMissingCategories(45)
      i += ib.updateMissingCategories(46)
      #ib.printImportedRecords(38)
      print("Updated:", i)
