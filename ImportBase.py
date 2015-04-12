
import re, datetime, os, sys
from ImportBase import *
from ImportTransactionsDiners import ImportTransactionsDiners
from ImportTransactionsSEBKort import ImportTransactionsSEBKort
from ImportTransactionsSwedbank import ImportTransactionsSwedbank

class ImportBase:
    def __init__(self, db):
        self.db = db
    
    def commit(self):
        self.db.connection.commit()
            
    def importFile(self, inputFilename, card, codepage = None):
            inputPath, inputName = os.path.split(inputFilename)
            accountId, service = self.getService(card)
            importId = self.createImport(inputName)
            print("Filename:", inputName, "Directory:", inputPath, "Card:", card, "Service:", service, "Account:", accountId, "Import:", importId)

            im = None
            if service == "Eurobonus":
                im = ImportTransactionsSEBKort(inputFilename)
            elif service == "Diners":
                im = ImportTransactionsDiners(inputFilename)
            elif service == "Swedbank":
                im = ImportTransactionsSwedbank(inputFilename, codepage)
            else:
                print("Unknown service:", service)
                sys.exit(2)
    
            records = im.getRecords(card)
            print(records)
            self.importRecords(importId, accountId, records)
            #self.printImportedRecords(importId)
        

    def getService(self, cardId):
        result = self.db.cursor.execute("""
            select
                acId, acName, acCard, acService
            from accounts
            where
                acCard=?
            limit 1
        """, [cardId])
        for row in result:
            return row.get("acId"), row.get("acService")

    def createImport(self, comment):
        self.db.cursor.execute("""
            insert into imports (
                imTimestamp, imComment
            ) values (
                datetime(), ?
            )
        """, [comment])
        return self.db.cursor.lastrowid

    def importRecords(self, importId, accountId, dataDictionary):
        counter = 0;
        for dd in dataDictionary:
            insertData = [
                importId,
                accountId,
                dd.get("date"),
                dd.get("amount"),
                dd.get("description")
            ]
            self.db.cursor.execute("""
                insert into transactions (trImport, trAccount, trDate, trAmount, trDescription)
                values (?, ?, ?, ?, ?)
            """, insertData)
            counter += 1
            
        self.db.cursor.execute(
            "update imports set imAccount=?, imLines=? where imId=?",
            [accountId, counter, importId]
        )
        return counter

    def printTransactions(self, importId):
        t = self.getTransactions(importId)
        print("Select Data:", t)
    
    def getTransactions(self, importId):
        result = self.db.cursor.execute("""
            select
                trId,
                trDate,
                trAccount,
                trDescription,
                trAmount,
                trCategory,
                caName,
                trIgnore
            from transactions
            left join categories on caId=trCategory
            where
                trImport=?
            order by trDate
        """, [importId])
        
        records = []
        for row in result:
            records.append(row)
        return records
    
    def getAccounts(self):
        result = self.db.cursor.execute("""
            select
                acId,
                acName,
                acCard,
                acService
            from accounts
            order by acName asc
        """)
        
        records = []
        for row in result:
            records.append(row)
        return records

    def getImports(self):
        result = self.db.cursor.execute("""
            select
                imId,
                imTimestamp,
                imAccount,
                imComment,
                imLines
            from imports
            order by imTimestamp asc
        """)
        
        records = []
        for row in result:
            records.append(row)
        return records

    def getCategories(self):
        result = self.db.cursor.execute("""
            select
                caId,
                caName
            from categories
            where caParent > 0
            order by caName asc
        """)
        
        records = []
        for row in result:
            records.append(row)
        return records
    
    def setAccount(self, importId, accountId):
        self.db.connection.cursor().execute("""
            update imports set
                imAccount=?
            where imId=?
        """, [accountId, importId])

        self.db.connection.cursor().execute("""
            update transactions set
                trAccount=?
            where trImport=?
        """, [accountId, importId])
    
    def setImportComment(self, importId, comment):
        self.db.connection.cursor().execute("""
            update imports set
                imComment=?
            where imId=?
        """, [comment, importId])
    
    def setTransactionValue(self, transactionId, fieldName, newValue):
        sql = None

        if (fieldName in ['trDate', 'trAccount', 'trAmount', 'trDestination', 'trIgnore']):
            sql = """
                update transactions set
                    "{0}"=?
                where trId=?
            """.format(fieldName)
            
        elif (fieldName == "trDescription"):
            sql = """
                update transactions set
                    trOriginalDescription=case when trOriginalDescription is null then trDescription else trOriginalDescription end,
                    trDescription=?
                where trId=?
            """
            
        elif (fieldName == "trCategory"):
            sql = """
                update transactions set
                    trOriginalCategory=case when trOriginalCategory is null then trCategory else trOriginalCategory end,
                    trCategory=?
                where trId=?
            """
        
        if (sql != None):
            self.db.connection.cursor().execute(sql, [newValue, transactionId])

    def updateBadDescriptions(self, importId):
        cur = self.db.connection.cursor()
        cur.execute("""
            update transactions
            set
                trOriginalDescription=trDescription,
                trDescription=(select clTo from cleanup where clFrom=trDescription)
            where
                trOriginalDescription is null
                and trDescription in(select clFrom from cleanup)
                and trImport=?
        """, [importId])
        return cur.rowcount
            
    def updateMissingCategories(self, importId):
        result = self.db.cursor.execute("""
            select
                trId,
                coalesce(a1.aiCategory, a2.aiCategory) as category,
                coalesce(a1.aiDestination, a2.aiDestination) as destination
            from transactions
            left join autoinfo a1 on a1.aiType='string' and trDescription = a1.aiPattern
            left join autoinfo a2 on a2.aiType='regexp' and trDescription REGEXP a2.aiPattern
            where
                (a1.aiCategory is not null or a2.aiPattern is not null)
                and trCategory is null
                and trImport=?
        """, [importId])
        
        counter = 0
        for row in result:
            self.setTransactionValue(row.get("trId"), "trCategory", row.get("category"))
            #print("ID:", row.get("trId"), "Cat:", row.get("category"), "Destination", row.get("destination"))
            #self.db.connection.cursor().execute("""
            #    update transactions set
            #        trCategory=?,
            #        trDestination=?
            #    where trID=?
            #""", [row.get("category"), row.get("destination"), row.get("trId")])
            counter += 1
        return counter
    
