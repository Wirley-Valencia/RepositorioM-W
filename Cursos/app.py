from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'cursos'

# Se crea una instancia de MySQL
mysql = MySQL(app)

# Ruta para la página principal
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        password = request.form['password']
        
        if validar_credenciales(nombre_usuario, password):
            return redirect(url_for('curso'))
        else:
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."
            return render_template('login.html', error_message=error_message)

    
    return render_template('login.html')

def validar_credenciales(username, password):
    if username == 'usuario' and password == 'contraseña':
        return True
    else:
        return False
    
    
# Ruta para la página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
       
        nombre_usuario = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

     
        if password != confirm_password:
            error_message = "Las contraseñas no coinciden. Inténtalo de nuevo."
            return render_template('registro.html', error_message=error_message)

      
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE username = %s', (nombre_usuario,))
        usuario_existente = cur.fetchone()
        cur.close()
        if usuario_existente:
            error_message = "El usuario ya existe. Por favor, elige otro nombre de usuario."
            return render_template('registro.html', error_message=error_message)

   
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (nombre_usuario, password))
        mysql.connection.commit()
        cur.close()

       
        return redirect(url_for('login'))

   
    return render_template('registro.html')

# Ruta para mostrar todos los cursos
@app.route('/curso')
def curso():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM curso')
    data = cur.fetchall()
    cur.close()  # Cierra el cursor
    return render_template('curso.html', cursos=data)

# Ruta para agregar cursos
@app.route('/add_cursos', methods=['POST'])
def add_cursos():
    if request.method == "POST":
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        horas = request.form['horas']
        area = request.form['area']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO curso (codigo, nombre, horas, area) VALUES (%s, %s, %s, %s)', (codigo, nombre, horas, area))
        mysql.connection.commit()
        cur.close()  # Cierra el cursor
        return redirect(url_for('curso'))
    else:
        return render_template('curso.html')

# Ruta para obtener un curso por su ID
@app.route('/edit/<int:id>')
def get_curso(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM curso WHERE id = %s', (id,))
    data = cur.fetchone()  # Obtiene solo un registro
    cur.close()  # Cierra el cursor
    return render_template('edit_curso.html', c=data)

# Ruta para actualizar un curso
@app.route('/update/<int:id>', methods=['POST'])
def update_curso(id):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        horas = request.form['horas']
        area = request.form['area']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE curso SET codigo = %s, nombre = %s, horas = %s, area = %s WHERE id = %s', (codigo, nombre, horas, area, id))
        mysql.connection.commit()
        cur.close()  # Cierra el cursor
    return redirect(url_for('curso'))

# Ruta para eliminar un curso
@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM curso WHERE ID = %s', (id,))
    mysql.connection.commit()
    cur.close()  # Cierra el cursor
    return redirect(url_for('curso'))

# Manejador de error para página no encontrada
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
