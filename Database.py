import psycopg2


class Database:
    """
    Class is used to update 
    postgreSQL database
    """
    __conn = None
    __cursor = None

    def connection(self, user):
        # connect to the database
        self.__conn = psycopg2.connect(user)
        # cursor = conn.cursor()

    def cursor(self):
        # opens cursor
        self.__cursor = self.__conn.cursor()

    def insert(self, cType, regName, cName, dateFiled, add1, city1, state1, zipCode1,):
        # add each element to the database and map to correct field
        insertCommand = 'INSERT INTO scrappack_businessprofile ("companyType", "registeredName", "companyName", ' + \
                        '"dateFiled", "address", "city", "state", "zipCode")' + \
                        ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        data = (cType, regName, cName, dateFiled, add1, city1, state1, zipCode1,)
        self.__cursor.execute(insertCommand, data)

    def commit(self):
        self.__conn.commit()

    def close(self):
        self.__conn.close()
