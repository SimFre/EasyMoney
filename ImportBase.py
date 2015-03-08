
import sqlite3

class ImportBase:
   '''
   def __enter__(self):
      return self
   
   def __init__(self, dbFile):
      try:
         self.fileName = dbFile
      except E as e:
         print ('General Error', e)
         return False
      finally:
         if self.connection:
            connection.close()

   def __exit__(self, type, value, traceback):
      pass
   '''

   def createImport(self, cursor, comment):
      cursor.execute("""
         insert into imports (
            imTimestamp, imComment
         ) values (
            datetime(), ?
         )
      """, [comment])
      return cursor.lastrowid

   def importRecord(self, cursor, importId, accountId, transactionDate, amount, description):
      insertData = [importId, accountId, transactionDate, amount, description]
      cursor.execute("""
         insert into transactions (trImport, trAccount, trDate, trAmount, trDescription)
         values (?, ?, ?, ?, ?)
      """, insertData)
      #insertData.insert(0, cur.lastrowid)
      return cursor.lastrowid

   def printImportedRecords(self, cursor, importId):
      result = cursor.execute("""
         select
            trId, trImport, trAccount, trDate, trAmount, trDescription,
            coalesce(a1.aiPattern, a2.aiPattern) as pattern,
            coalesce(a1.aiCategory, a2.aiCategory) as category
         from transactions
         left join autoinfo a1 on a1.aiType='string' and trDescription = a1.aiPattern
         left join autoinfo a2 on a2.aiType='regexp' and trDescription REGEXP a2.aiPattern
         where
            trImport=?
      """, [importId])
      for row in result:
         if row != None:
            print("Select Data:", row)

