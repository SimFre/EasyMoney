
import sqlite3, re
class DbConnection:

    def __init__(self, dbFile, commitOnClose = True):
        try:
            self.commitOnClose = commitOnClose
            self.fileName = dbFile
            self.connection = sqlite3.connect(self.fileName)
            self.connection.create_function("REGEXP", 2, self.sqliteRegexp)
            self.connection.row_factory = self.sqliteRowFactory
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print ('DB Error', e)
            return False
        except Exception as e:
            print ('General Error', e)
            return False
        #finally:
        #    if self.connection:
        #        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exitType, exitValue, exitTraceback):
        self.close(self.commitOnClose)

    def close(self, commit = True):
        if self.connection:
            if (commit):
                self.connection.commit()
            self.connection.close()
            self.connection = None
    
    def sqliteRegexp(self, pattern, subject):
        rx = re.compile(pattern)
        match = rx.search(subject)
        #print("Pattern:", pattern, "Subject:", subject, "Match:", match)
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

