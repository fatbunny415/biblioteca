from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bibliotecas"
mongo = PyMongo(app)

# Ruta principal
@app.route('/')
def index():
    total_usuarios = mongo.db.usuarios.count_documents({})
    total_libros = mongo.db.Libros.count_documents({})
    total_prestamos = mongo.db.Prestamos.count_documents({})
    total_reservas = mongo.db.Reservas.count_documents({})
    
    return render_template('index.html', 
                           total_usuarios=total_usuarios, 
                           total_libros=total_libros, 
                           total_prestamos=total_prestamos, 
                           total_reservas=total_reservas)

# Rutas para Usuarios
@app.route('/usuarios')
def usuarios():
    usuarios = mongo.db.usuarios.find()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    edad = request.form.get('edad')
    contraseña = request.form.get('contraseña')
    email = request.form.get('email')
    if nombre and apellido and email:
        mongo.db.usuarios.insert_one({
            'nombre': nombre,
            'apellido': apellido,
            'edad': int(edad),
            'contraseña': contraseña,
            'email': email
        })
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<id>', methods=['POST'])
def editar_usuario(id):
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    edad = request.form.get('edad')
    contraseña = request.form.get('contraseña')
    email = request.form.get('email')
    if nombre and apellido and email:
        mongo.db.usuarios.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'nombre': nombre,
                'apellido': apellido,
                'edad': int(edad),
                'contraseña': contraseña,
                'email': email
            }
        })
    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<id>')
def eliminar_usuario(id):
    mongo.db.usuarios.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('usuarios'))

# Rutas para Libros
@app.route('/libros')
def libros():
    libros = mongo.db.Libros.find()
    return render_template('libros.html', libros=libros)

@app.route('/libros/agregar', methods=['POST'])
def agregar_libro():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    ejemplares = request.form.get('ejemplares')
    prestados = request.form.get('prestados')
    if titulo and autor:
        mongo.db.Libros.insert_one({
            'titulo': titulo,
            'autor': autor,
            'ejemplares': int(ejemplares),
            'prestados': int(prestados)
        })
    return redirect(url_for('libros'))

@app.route('/libros/editar/<id>', methods=['POST'])
def editar_libro(id):
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    ejemplares = request.form.get('ejemplares')
    prestados = request.form.get('prestados')
    if titulo and autor:
        mongo.db.Libros.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'titulo': titulo,
                'autor': autor,
                'ejemplares': int(ejemplares),
                'prestados': int(prestados)
            }
        })
    return redirect(url_for('libros'))

@app.route('/libros/eliminar/<id>')
def eliminar_libro(id):
    mongo.db.Libros.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('libros'))

# Rutas para Préstamos
@app.route('/prestamos')
def prestamos():
    prestamos = mongo.db.Prestamos.find()
    usuarios = mongo.db.usuarios.find()
    libros = mongo.db.Libros.find()
    return render_template('prestamos.html', prestamos=prestamos, usuarios=usuarios, libros=libros)

@app.route('/prestamos/agregar', methods=['POST'])
def agregar_prestamo():
    usuario_id = request.form.get('usuario_id')
    libro_id = request.form.get('libro_id')
    fecha = request.form.get('fecha')
    fecha_devolucion = request.form.get('fecha_devolucion')
    if usuario_id and libro_id:
        mongo.db.Prestamos.insert_one({
            'usuario_id': usuario_id,
            'libro_id': libro_id,
            'fecha': fecha,
            'fecha_devolucion': fecha_devolucion
        })
    return redirect(url_for('prestamos'))

# Rutas para Reservas
@app.route('/reservas')
def reservas():
    reservas = mongo.db.Reservas.find()
    usuarios = mongo.db.usuarios.find()
    libros = mongo.db.Libros.find()
    return render_template('reservas.html', reservas=reservas, usuarios=usuarios, libros=libros)

@app.route('/reservas/agregar', methods=['POST'])
def agregar_reserva():
    usuario_id = request.form.get('usuario_id')
    libro_id = request.form.get('libro_id')
    fecha_reserva = request.form.get('fecha_reserva')
    if usuario_id and libro_id:
        mongo.db.Reservas.insert_one({
            'usuario_id': usuario_id,
            'libro_id': libro_id,
            'fecha_reserva': fecha_reserva
        })
    return redirect(url_for('reservas'))

if __name__ == '__main__':
    app.run(debug=True)