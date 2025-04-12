# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, DecimalField, IntegerField, validators
from werkzeug.security import check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


from config import config
from models.ModelUser import ModelUser
from wtforms.validators import InputRequired
from models.entities.User import User
from clases import ClienteModel
from clases import CategoriaModel 
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['MYSQL_DB'] = 'flask_login'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306

csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'login'

cliente_model = ClienteModel(db)  # instancias
categoria_model = CategoriaModel(db)

# Formulario de login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Sign in')

@login_manager_app.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(db, user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for('home'))
        else:
            flash("Usuario o contraseña incorrectos")
    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()  # Cierra la sesión del usuario
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('session')  # Borra la cookie de sesión
    return response

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# Cliente Form
class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    cedula = StringField('Cédula', validators=[validators.DataRequired()])
    telefono = StringField('Teléfono', validators=[validators.DataRequired()])
    submit = SubmitField('Guardar')

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    if request.method == 'POST' and form.validate_on_submit():
        cliente_model.insert(form.nombre.data, form.email.data, form.cedula.data, form.telefono.data)
        flash('Cliente agregado exitosamente')
        return redirect(url_for('clientes'))

    clientes = cliente_model.get_all()
    return render_template('clientes.html', clientes=clientes, form=form)



@app.route('/edit_cliente/<int:id>', methods=['POST'])
@login_required
def edit_cliente(id):
    nombre = request.form['nombre']
    email = request.form['email']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    cliente_model.update(id, nombre, email, cedula, telefono)
    flash('Cliente actualizado exitosamente')
    return redirect(url_for('clientes'))

@app.route('/delete_cliente/<int:id>', methods=['POST'])
@login_required
def delete_cliente(id):
    cliente_model.delete(id)

    # Verifica si la tabla está vacía
    cur = db.connection.cursor()  # ← CORRECTO
    cur.execute("SELECT COUNT(*) FROM clientes")
    total = cur.fetchone()[0]

    # Si no quedan clientes, reinicia el contador
    if total == 0:
        cur.execute("ALTER TABLE clientes AUTO_INCREMENT = 1")
        db.connection.commit()

    cur.close()
    flash('Cliente eliminado exitosamente')
    return redirect(url_for('clientes'))


@app.route('/search_clientes', methods=['GET'])
def search_clientes():
    form = ClienteForm()
    query = request.args.get('query', '')
    clientes = cliente_model.search(query)
    return render_template('clientes.html', clientes=clientes, form=form)

# categoria Form
class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', [InputRequired()])
    descripcion = TextAreaField('Descripción', [InputRequired()])
    categoria = StringField('Categoría', [InputRequired()])
    submit = SubmitField('Agregar Categoría')


@app.route('/gestion_categorias', methods=['GET', 'POST'])
def gestion_categorias():
    form = CategoriaForm()
    if request.method == 'POST' and form.validate_on_submit():
        categoria_model.insert(
            form.nombre.data,
            form.descripcion.data,
            form.categoria.data
        )
        flash('Categoría agregada correctamente')
        print("Datos traídos desde SQL:", categorias)
        return redirect(url_for('gestion_categorias'))

    categorias = categoria_model.get_all()
    return render_template('gestion_categorias.html', form=form, categorias=categorias)

@app.route('/edit_categoria/<int:id>', methods=['POST'])
def edit_categoria(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    
    categoria_model.update(id, nombre, descripcion, categoria)
    flash('Categoría actualizada correctamente')
    return redirect(url_for('gestion_categorias'))

@app.route('/delete_categoria/<int:id>')
def delete_categoria(id):
    categoria_model.delete(id)
    flash('Categoría eliminada correctamente')
    return redirect(url_for('gestion_categorias'))



@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida</h1>"

@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run(debug=True)
