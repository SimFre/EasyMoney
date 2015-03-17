
import os, sys, sqlite3
#from DbConnection import *

class ImportTransactionsRaw:
   def __init__(self, inputFilename, dbFile):
      self.accounts = []
      self.records = {}
      self.lines = []

      db = sqlite3.connect(dbFile)
      #connection.create_function("REGEXP", 2, self.sqliteRegexp)
      #connection.row_factory = self.sqliteRowFactory
      cursor = db.cursor()


      # Start raw parsing
      #2012-10-31;DINERS CLUB NORD;LOUNGE;-125,00 kr;Restaurangbesök;Mat & Förbrukning;Ja;Tärande;2012-10;;

      with open(inputFilename, encoding="utf8") as fp:
         for line in fp:
            parts = line.split(";")
            date = parts[0]
            cardName = parts[1]
            description = parts[2]

            amount = parts[3]
            amount = amount.replace(" kr", "")
            amount = amount.replace(",", ".")
            amount = amount.replace(" ", "")
            amount = amount.replace(" ", "") # Some 0xA0 / 0xC2?
            amount = amount.replace("Â", "") # Some 0xA0 / 0xC2?
            amount = float(amount)
            
            category = parts[4]
            direction = parts[7]
            
            cardId = 0
            if cardName == "Privatkonto":
               cardId = 1
            elif cardName == "First Card":
               cardId = 2
            elif cardName == "DINERS CLUB NORD":
               cardId = 3
            elif cardName == "SAS Eurobonus Ma":
               cardId = 4
            else:
               print("Card:", cardName)
   
            insertData = [1, cardId, date, amount, description, direction, category]
            try:
               cursor.execute("""
                  insert into transactions (trImport, trAccount, trDate, trAmount, trDescription, trDestination, trDummy)
                  values (?, ?, ?, ?, ?, ?, ?)
               """, insertData)
               db.commit()
               #db.cursor.commit()
               #print(insertData)
            except sqlite3.Error as e:
               print ('DB Error', e)

      #result = db.cursor.execute("""
      #   select
      #      trId, trImport, trAccount, trDate, trAmount, trDescription,
      #      coalesce(a1.aiPattern, a2.aiPattern) as pattern,
      #      coalesce(a1.aiCategory, a2.aiCategory) as category
      #   from transactions
      #   left join autoinfo a1 on a1.aiType='string' and trDescription = a1.aiPattern
      #   left join autoinfo a2 on a2.aiType='regexp' and trDescription REGEXP a2.aiPattern
      #   where
      #      trImport=?
      #""", [1])
      #for row in result:
      #   #if row != None:
      #   print("Select Data:", row)
  
      #db.commit()
      db.close()
         
accountId = 1
dbFile = "/Users/laban/Documents/Ekonomi/Transactions.db"
inputFilename = "/Users/laban/Documents/Ekonomi/DB/rawImport.txt"

inputPath, inputName = os.path.split(inputFilename)
print("Filename:", inputName)
print("Directory:", inputPath)
print("Database:", dbFile)

#with DbConnection(dbFile) as db:
#   try:
itr = ImportTransactionsRaw(inputFilename, dbFile)
#      db.close()
#      
#   except E as e:
#      print ("General Error", e)
#      sys.exit(1)

