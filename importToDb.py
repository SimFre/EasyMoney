
import sqlite3 as db
import sys

dbFile = '/Users/laban/Documents/Ekonomi/Transactions.db'

con = None

try:
   con = db.connect(dbFile)
   
   cur = con.cursor()
   cur.execute('select sqlite_version()')
   data = cur.fetchone()
   
   print ('DB Version:', data)

except db.Error as e:
   print ('DB Error', e)
   sys.exit(1)
   
finally:
   if con:
      con.close()



