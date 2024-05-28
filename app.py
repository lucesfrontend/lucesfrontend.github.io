import pymysql
from flask import Flask, render_template, request, redirect, url_for
import _mysql_connector 
from werkzeug.utils import secure_filename 
import os

app= Flask(__name__)

db = pymysql.connect(
     host="localhost",
     user="root",
     password="",
     database="r&o_eco"
)
cursor=db.cursor()

app.config['UPLOAD_FOLDER']= os.path.join('static','img')
app.config['ALLOMED_EXTENSIONS'] = {'png','jpg','jpeg','gif'}

def archivopermitido(filename):
    return '.' in filename and  filename.rsplit('.',1)[1].lower() in app.config['ALLOMED_EXTENSIONS']

#rutas
@app.route('/')
def principal(): 
    return render_template('index.html')

@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method=='POST': 
        codigo=request.form['codigo']
        nombre=request.form['nombre']
        precio=request.form['precio']
        cantidad=request.form['cantidad']
        descripcion=request.form['descripcion']
        marca=request.form['marca']
        foto=request.files['foto']
        categoria=request.form['categoria']
        if foto and archivopermitido(foto.filename):
            filename= secure_filename(foto.filename) 
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql= "INSERT INTO productos (Codigo_Productos,Nombre,Precio,Cantidad,Descripcion,Marca,Imagen,Categoria) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val= (codigo,nombre,precio,cantidad,descripcion,marca,filename,categoria)
            cursor.execute(sql,val)
            db.commit()
            return redirect(url_for('principal'))
    return render_template('registrar.html')

@app.route('/mostrar')
def mostrar(): 
    cursor.execute("SELECT * FROM productos")
    productos= cursor.fetchall()
    return render_template('garden-producto.html', productos=productos)

@app.route('/categoria')
def categoria(): 
    return render_template('garden-category.html') 

@app.route('/contactos')
def contactos(): 
    return render_template('garden-contact.html') 

@app.route('/galeria')
def galeria(): 
    return render_template('garden-galeria.html') 

@app.route('/puntoverde')
def puntoverde(): 
    return render_template('garden-punto_verde.html')

if __name__ == '__main__':
    app.run(debug=True)