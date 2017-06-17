
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

    def updateToestandBlind(self,toestand):
        # Query met parameters
        sqlQuery = "UPDATE tbltoestand SET toestand = '{toestand}' WHERE idtoestand = 0"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(toestand=toestand)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def updateToestandLicht(self,toestand):
        # Query met parameters
        sqlQuery = "UPDATE tbltoestand SET toestand = '{toestand}' WHERE  idtoestand = 1"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(toestand=toestand)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def updateToestandGeenLicht(self,toestand):
        # Query met parameters
        sqlQuery = "UPDATE tbltoestand SET toestand = '{toestand}' WHERE  idtoestand = 2"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(toestand=toestand)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def updateToestandWelLicht(self,toestand):
        # Query met parameters
        sqlQuery = "UPDATE tbltoestand SET toestand = '{toestand}' WHERE  idtoestand = 3"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(toestand=toestand)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def getToestandBlind(self):
        sqlQuery = "SELECT toestand  FROM tbltoestand WHERE idtoestand = 0;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        return result
    def getToestandLicht(self):
        sqlQuery = "SELECT toestand  FROM tbltoestand WHERE idtoestand = 1;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        return result

    def getToestandBlindGeenLicht(self):
        sqlQuery = "SELECT toestand  FROM tbltoestand WHERE idtoestand = 2;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
        return result

    def getToestandBlindWelLicht(self):
        sqlQuery = "SELECT toestand  FROM tbltoestand WHERE idtoestand = 3;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchone()
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

    def getLaatsteTemperatuur(self):
        # Query zonder parameters
        sqlQuery = "SELECT idtbldata, temperatuur FROM db_BlindBerry.tbldata order by idtbldata desc limit 1;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        # self.__cursor.close()
        return result

    def getLaatste10Temperaturen(self):
        # Query zonder parameters
        sqlQuery = "SELECT idtbldata, temperatuur FROM db_BlindBerry.tbldata order by idtbldata desc limit 10;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        # self.__cursor.close()
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

    def setDataToData(self, temperatuur, licht):
        # Query met parameters
        sqlQuery = "INSERT INTO tbldata (temperatuur,licht) VALUES ('{temperatuur}', '{licht}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(temperatuur=temperatuur, licht=licht)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()


    def deleteDataLog(self):
        sqlQuery = "DELETE FROM tbllog;"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format()
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

