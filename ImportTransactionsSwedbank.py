#81562  9933661754  Privatkonto          SEK     14-02-24         14-02-25           2618690051785079                    L?n                          29 742,90
import re, datetime
class ImportTransactionsSwedbank:
   def __init__(self, inputFilename, codepage):
      self.accounts = []
      self.records = {}
      self.lines = []

      # Start Swedbank parsing
      cardId = None
      with open(inputFilename, encoding=codepage) as fp:
         pattern = re.compile(r"^\d{5}")
         for line in fp:
            if pattern.match(line):
               self.lines.append(line.strip())

         slices = self.scanForSlices()
         for line in self.lines:      
            fields = self.splitLineBySlice(slices, line)
            fields = self.reformat(fields)
            cardId = fields["cardId"]
            del(fields["cardId"])

            if self.records.get(cardId) == None:
               self.accounts.append(cardId)
               self.records[cardId] = []
            
            self.records[cardId].append(fields)

   def reformat(self, fields):
      date = fields[5]
      date = datetime.datetime.strptime(date, "%y-%m-%d")
      date = date.strftime("%Y-%m-%d")
      
      amount = fields[8]
      amount = amount.replace(",", ".")
      amount = amount.replace(" ", "")
      amount = float(amount)
      #amount = amount * -1
      
      description = fields[6]
      description = description.strip()

      clearing = fields[0].strip()
      account = fields[1].strip()
      name = fields[2].strip()
      cardId = name + " (" + clearing + "." + account + ")"
      
      export = {
         "cardId": cardId,
         "date": date,
         "amount": amount,
         "description": description
      }
      return export
   
   def getRecords(self, accountName):
      return self.records.get(accountName)
      
   # Scan through all lines to find what the columns look like.
   def scanForSlices(self):
      slices = []
      lineNum = 0
      start = 0
      wordStart = -1
      wordEnd = -1
      longestLine = 0
      allCellsAreBlank = True
      rowCellIsBlank = True
      lastLine = len(self.lines)-1
      resetLoop = False
      loopCounter = 0

      while lineNum <= lastLine:
         loopCounter += 1
         end = start + 1
         resetLoop = False

         if lineNum == 0:
            allCellsAreBlank = True

         lineData = self.lines[lineNum].strip()
         char = lineData[start:end]
         if len(lineData) > longestLine:
            longestLine = len(lineData)

         if char == " " or len(char) == 0:
            rowCellIsBlank = True
         else:
            rowCellIsBlank = False
            allCellsAreBlank = False
            resetLoop = True
            if wordStart == -1:
               wordStart = start
               wordEnd = end
            else:
               wordEnd = end
               
         #print("Line", lineNum, "of", lastLine, "Longest:", longestLine, "[", start, ":", end, "] = ", char, "(", lineData[wordStart:wordEnd], ")")
         
         # Create a slice
         if lineNum == lastLine and allCellsAreBlank and wordStart > -1:
            #print("SliceA", wordStart, ":", wordEnd)
            slices.append((wordStart, wordEnd))
            wordStart = -1
                  
         # Shift caret right one step
         if lineNum == lastLine and allCellsAreBlank:
            resetLoop = True

         if resetLoop:
            start += 1
         
         # End the loop if caret is beyond the end
         if lineNum == lastLine and start > longestLine:
            lineNum += lastLine
            resetLoop = False
         
         # Restart the loop if the cell is not blank
         if (lineNum <= lastLine and rowCellIsBlank == False) or resetLoop:
            lineNum = 0

         # Advance by one line if the cell is indeed blank.
         if rowCellIsBlank == True and resetLoop == False:
            lineNum += 1
      return slices
      
   # Split a raw text line by supplying an array of touples of start/stop coordinates.
   def splitLineBySlice(self, slices, line):
      cells = []
      for s in slices:
         x, y = s
         data = line[x:y]
         data = data.strip()
         cells.append(data)
      return cells
         
         
   
   
   
# accountId = 1
# dbFile = "/Users/laban/Documents/Ekonomi/Transactions.db"
# inputFilename = "/Users/laban/Documents/Ekonomi/Swedbank/Swebank_20140204-20150303.txt"
# card = "Privatkonto (81562.9933661754)"
# service = "Swedbank"
# 
# it = ImportTransactionsSwedbank(inputFilename)
# print(it.getRecords(card))
