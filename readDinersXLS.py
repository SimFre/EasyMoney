#!/usr/local/bin/python3

accountId = 3
dbFile = "/Users/laban/Documents/Ekonomi/Transactions.db"
inputFilename = "/Users/laban/Documents/Ekonomi/Diners Club/Diners20150217.xls"

#     0                     1                  2              3         4       5        6                 7             8
# Transaktionsdatum	Bokföringsdatum	Utlän dskt belopp	Belopp SEK	Valuta	Kurs	Inköpsställe	Biljettnummer	Passagerarer	
# 20.01.2015	21.01.2015	420,00	420,00	SEK	0,0000	A HEREFORD BEEFSTONW          			


import re, datetime, os, sys
from DbConnection import *
from ImportBase import *

inputPath, inputName = os.path.split(inputFilename)
print("Filename:", inputName)
print("Directory:", inputPath)
print("Database:", dbFile)

ib = ImportBase()
with DbConnection(dbFile) as db:
   try:
      importId = ib.createImport(db.cursor, inputName)

      # Start Diners Club parsing
      with open(inputFilename, encoding="cp1252") as fp:
         pattern = re.compile(r"^(\d\d\.){2}\d{4}")
         replace = re.compile(r"\s+")
         for line in fp:
            if pattern.match(line):
               parts = line.split("\t")
               
               date = parts[0]
               date = datetime.datetime.strptime(date, "%d.%m.%Y")
               date = date.strftime("%Y-%m-%d")
               amount = parts[3].replace(",", ".")
               amount = float(amount)
               amount = amount * -1
               description = parts[6]
               description = replace.sub(" ", description)
               description = description.strip()

               ib.importRecord(db.cursor, importId, accountId, date, amount, description)
      # Parsing done
      ib.printImportedRecords(db.cursor, importId)
   except E as e:
      print ("General Error", e)
      sys.exit(1)


