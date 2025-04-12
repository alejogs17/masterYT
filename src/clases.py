
class ClienteModel:
    """
    Clase que maneja las operaciones CRUD de la entidad Cliente en la base de datos.
    """

    def __init__(self, db):
        """
        Constructor que recibe la instancia de la base de datos.
        :param db: Conexión a MySQL proporcionada por Flask-MySQLdb
        """
        self.db = db

    def get_all(self):
        """
        Obtiene todos los clientes de la base de datos.
        :return: Lista de tuplas con todos los clientes
        """
        cur = self.db.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        cur.close()
        return clientes

    def insert(self, nombre, email, cedula, telefono):
        """
        Inserta un nuevo cliente en la base de datos.
        :param nombre: Nombre del cliente
        :param email: Email del cliente
        :param cedula: Cédula del cliente
        :param telefono: Teléfono del cliente
        """
        cur = self.db.connection.cursor()
        cur.execute("""
            INSERT INTO clientes (nombre, email, cedula, telefono) 
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, cedula, telefono))
        self.db.connection.commit()

    def update(self, id, nombre, email, cedula, telefono):
        """
        Actualiza los datos de un cliente existente.
        :param id: ID del cliente
        :param nombre: Nuevo nombre
        :param email: Nuevo email
        :param cedula: Nueva cédula
        :param telefono: Nuevo teléfono
        """
        cur = self.db.connection.cursor()
        cur.execute("""
            UPDATE clientes 
            SET nombre = %s, email = %s, cedula = %s, telefono = %s 
            WHERE id = %s
        """, (nombre, email, cedula, telefono, id))
        self.db.connection.commit()

    def delete(self, id):
        """
        Elimina un cliente por su ID.
        :param id: ID del cliente a eliminar
        """
        cur = self.db.connection.cursor()
        cur.execute("DELETE FROM clientes WHERE id = %s", (id,))
        self.db.connection.commit()

    def search(self, query):
        """
        Busca clientes por nombre, email o cédula.
        :param query: Texto a buscar
        :return: Lista de clientes que coincidan con la búsqueda
        """
        cur = self.db.connection.cursor()
        cur.execute("""
            SELECT * FROM clientes 
            WHERE nombre LIKE %s OR email LIKE %s OR cedula LIKE %s
        """, ('%' + query + '%',) * 3)
        clientes = cur.fetchall()
        cur.close()
        return clientes

class CategoriaModel:
    """
    Clase que maneja las operaciones CRUD de la entidad Categoría en la base de datos.
    """

    def __init__(self, db):
        self.db = db

    def get_all(self):
        cur = self.db.connection.cursor()
        cur.execute("SELECT * FROM categorias")
        categorias = cur.fetchall()
        cur.close()
        return categorias

    def insert(self, nombre, descripcion, categoria):
        cur = self.db.connection.cursor()
        cur.execute("""
            INSERT INTO categorias (nombre, descripcion, categoria) 
            VALUES (%s, %s, %s)
        """, (nombre, descripcion, categoria))
        self.db.connection.commit()
        cur.close()

    def delete(self, id):
        cur = self.db.connection.cursor()
        cur.execute("DELETE FROM categorias WHERE id = %s", (id,))
        self.db.connection.commit()
        cur.close()

    def update(self, id, nombre, descripcion, categoria):
        cur = self.db.connection.cursor()
        cur.execute("""
            UPDATE categorias 
            SET nombre = %s, descripcion = %s, categoria = %s
            WHERE id = %s
        """, (nombre, descripcion, categoria, id))
        self.db.connection.commit()
        cur.close()

