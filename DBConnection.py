import mysql.connector
class IDatabaseConnection:
    def connect(self):
        raise NotImplementedError

    def get_cursor(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class DatabaseConnection(IDatabaseConnection):
    def __init__(self):
        self.mydb = None
        self.mycursor = None

    def connect(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sampathdb",
            port="3306"
        )
        self.mycursor = self.mydb.cursor()

    def get_cursor(self):
        return self.mycursor

    def commit(self):
        self.mydb.commit()

    def close(self):
        self.mycursor.close()
        self.mydb.close()


class IAuthenticationService:
    def authenticate(self, username, password):
        raise NotImplementedError


class AuthenticationService(IAuthenticationService):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate(self, username, password):
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
        return cursor.fetchall()