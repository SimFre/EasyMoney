
import re, datetime
class ImportTransactionsDiners:
   def __init__(self, inputFilename):
      self.accounts = []
      self.records = {}

      # Start Diners Club parsing
      cardId = "Diners Club"
      self.accounts.append(cardId)

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
               amount = float(amount) * -1
               description = parts[6]
               description = replace.sub(" ", description)
               description = description.strip()

               row = {
                  "date": date,
                  "amount": amount,
                  "description": description
               }

               if self.records.get(cardId) == None:
                  self.records[cardId] = []
               
               self.records[cardId].append(row)

   def getRecords(self, accountName):
      return self.records.get(accountName)
