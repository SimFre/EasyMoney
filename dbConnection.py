
import sqlite3, re
class DbConnection:
   connection = None
   cursor = None
   fileName = None

   def __init__(self, dbFile):
      try:
         self.fileName = dbFile
         connection = sqlite3.connect(self.fileName)
         connection.create_function("REGEXP", 2, self.sqliteRegexp)
         connection.row_factory = self.sqliteRowFactory
         self.cursor = connection.cursor()
      except sqlite3.Error as e:
         print ('DB Error', e)
         return False
      except E as e:
         print ('General Error', e)
         return False
      finally:
         if self.connection:
            connection.close()

   def __enter__(self):
      return self

   def __exit__(self, type, value, traceback):
      if self.connection:
         self.connection.commit()
         self.connection.close()

   def sqliteRegexp(self, pattern, subject):
      rx = re.compile(pattern)
      match = rx.search(subject)
      if match:
         #print("RE:", match.group(0))
         #return match.group(0)
         return True
      else:
         return None

   def sqliteRowFactory(self, cursor, row):
      dictionary = {}
      for index, field in enumerate(cursor.description):
         dictionary[field[0]] = row[index]
      return dictionary

