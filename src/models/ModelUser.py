from models.entities.User import User
from flask_mysqldb import MySQL

class ModelUser():

 from models.entities.User import User

class ModelUser():

    @classmethod
    def login(cls, db, user):
        cursor = None  # Inicializamos cursor fuera del bloque try
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, password, fullname FROM user WHERE username = %s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            
            if row is not None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
