
import re, datetime
import openpyxl as xl

class ImportTransactionsSEBKort:

    def __init__(self, inputFilename):
        self.accounts = []
        self.records = {}

        # Start SEB Kort (Eurobonus, Diners Club, SJ Prio) parsing
        wb = xl.load_workbook(inputFilename, use_iterators=True)
        ws = wb[wb.get_sheet_names()[0]]

        cardId = None
        for row in ws.iter_rows():
            fields = []
            for cell in row:
                fields.append(cell.value)

            if isinstance(fields[0], str) and fields[0].startswith("Kortnummer"):
                cardId = fields[2] + " (" + fields[0][11:] + ")"

            elif isinstance(fields[0], datetime.datetime) and cardId != None:
                row = {
                    "date": fields[0].strftime("%Y-%m-%d"),
                    "amount": float(fields[6]) * -1,
                    "description": fields[2]
                }

                if self.records.get(cardId) == None:
                    self.records[cardId] = []

                self.records[cardId].append(row)

    def getRecords(self, accountName):
        return self.records[accountName]
