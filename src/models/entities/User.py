from werkzeug.security import check_password_hash  # para verificar la contraseña hasheada
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada"""
        return check_password_hash(self.password, password)

    
    #print(generate_password_hash("1234567891"))
