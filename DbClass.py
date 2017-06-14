
class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "169.254.10.1",
            "user": "root",
            "passwd": "root",
            "db": "db_BlindBerry"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getDataFromDatabase(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM tablename"
        
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getAutomaisaties(self):
        # Query zonder parameters
        sqlQuery = "SELECT naam_automatisatie, uur_start, uur_stop, beschrijving FROM tblautomatisaties;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        # self.__cursor.close()
        return result

    def getLogs(self):
        # Query zonder parameters
        sqlQuery = "SELECT uur, datum, reden  FROM tbllog;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        # self.__cursor.close()
        return result

    def getUsername(self, username):
        # Query met parameters
        sqlQuery = "SELECT Persoon, Wachtwoord FROM tblpersonen WHERE Persoon = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=username)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result


    def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
        # Query met parameters
        sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=voorwaarde)
        
        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setDataToDatabase(self,value1):
        # Query met parameters
        sqlQuery = "INSERT INTO tablename (columnname) VALUES ('{param1}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=value1)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setDataToLog(self,datum, uur, reden):
        # Query met parameters
        sqlQuery = "INSERT INTO tbllog (datum, uur, reden) VALUES ('{datum}', '{uur}', '{reden}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(datum=datum, uur= uur, reden= reden)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()
