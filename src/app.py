from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user:
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            flash("Usuario o contraseña incorrectos...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    cedula = StringField('Cédula', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Guardar')

CLIENTES_POR_PAGINA = 6

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    if request.method == 'POST' and form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        cedula = form.cedula.data
        telefono = form.telefono.data
        
        cliente = Cliente(nombre=nombre, email=email, cedula=cedula, telefono=telefono)
        db.session.add(cliente)
        db.session.commit()
        
        flash('Cliente agregado exitosamente')
        return redirect(url_for('clientes'))
    
    page = request.args.get('page', 1, type=int)
    clientes = Cliente.query.paginate(page, per_page=CLIENTES_POR_PAGINA)
    
    return render_template('clientes.html', clientes=clientes, form=form)

@app.route('/edit_cliente/<int:id>', methods=['POST'])
@login_required
def edit_cliente(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        
        cur = db.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET nombre = %s,
                email = %s,
                cedula = %s,
                telefono = %s
            WHERE id = %s
        """, (nombre, email, cedula, telefono, id))
        db.connection.commit()
        flash('Cliente actualizado exitosamente')
        return redirect(url_for('clientes'))
        
    else:
        return jsonify({'error': 'Método no permitido'}), 405

@app.route('/delete_cliente/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_cliente(id):
    cur = db.connection.cursor()

    cur.execute('DELETE FROM clientes WHERE id = %s', (id,))
    db.connection.commit()

    cur.execute('SET @count = 0')
    cur.execute('UPDATE clientes SET id = @count:= @count + 1')
    db.connection.commit()

    cur.execute('ALTER TABLE clientes AUTO_INCREMENT = 1')
    db.connection.commit()

    flash('Cliente eliminado exitosamente')
    return redirect(url_for('clientes'))

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
