from sqlite3.dbapi2 import Cursor
from types import MethodType
from flask import Flask, flash, request, redirect, url_for
from flask import render_template as render
from flask_wtf import form
from werkzeug.utils import redirect
from wtforms.form import Form # importamos el render para poder utilijar jinja y plantillas html
from forms import fcrearsa, flogin, fempleado, feditar,fcrear
import os
from flask import send_from_directory
import sqlite3 as sql
from werkzeug.exceptions import RequestTimeout
from db import get_db, close_db
from flask import g
from datetime import datetime, time
from flask import send_file
from flask import make_response
import functools
from flask import session




app = Flask(__name__)


app.secret_key = os.urandom(24)
rutafotos = os.path.join('uploads')
app.config['rutafotos']=rutafotos

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['rutafotos'],nombreFoto )

@app.route('/logout')
def logout():
    session.clear()
    return redirect (url_for('inicio'))



@app.route('/', methods=["GET", "POST"])
def inicio():
    form = flogin(request.form)
    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']
        perfil = request.form['perfil']

        error = None
        db = get_db()
        
        if not usuario:
            error = "Usuario requerido."
            flash( error )
        if not password:
            error = "Contraseña requerida."
            flash( error )

        if error is not None:
            # SI HAY ERROR:
            return render("inicioSesion.html", form=form, titulo='Inicio de sesión')
        else:
            # No hay error:
            user = db.execute(
                'SELECT * FROM usuarios WHERE id_cedula= ? AND password= ? AND id_perfil= ?'
                ,
                (usuario,password,perfil)
            ).fetchone()            
            if user is None:
                error = "Usuario y contraseña no son correctos."
                flash( error )                
                return render ("inicioSesion.html", form=form, titulo='Inicio de sesión')
            else: 
                 
                if perfil == '1':
                    session.clear()
                    session['id_usuario'] = user[0] # con esto estoy guardando el id_usuario logueado
                    session['id_perfil'] = user[11] 


                    #Modifica la función login para que cuando confirme la sesión, cree una cookie
                    #del tipo ‘username’ y almacene el usuario.
                    response = make_response(redirect( url_for('empleado')))
                    response.set_cookie('username', usuario) # nombre de la cookie y su valor
                    return response
                    

                elif perfil == '2':
                    session.clear()
                    session['id_usuario'] = user[0] # con esto estoy guardando el id_usuario logueado
                    session['id_perfil'] = user[11] 
                    response = make_response(redirect( url_for('administrador')))
                    response.set_cookie('username', usuario) # nombre de la cookie y su valor
                    return response

                else:
                    session.clear()
                    session['id_usuario'] = user[0] # con esto estoy guardando el id_usuario logueado
                    session['id_perfil'] = user[11] 
                    response = make_response(redirect( url_for('superadministrador')))
                    response.set_cookie('username', usuario) # nombre de la cookie y su valor
                    return response

    # GET:
    return render ("inicioSesion.html", form=form, titulo='Inicio de sesión')

       
@app.route('/empleado', methods=["GET" , "POST"])
def empleado():
    print("Entró en before_request.")
    #g.user = con los datos de la base de datos, basados en la session.
    usuario = str(session.get('id_usuario'))
    perfil = str(session.get('id_perfil'))
    print("id_usuario", usuario)
  
   
    print("id_perfil", perfil)

    con = sql.connect("empleados.db")
    
    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute('SELECT id_cedula, nombre, apellido, direccion,correo, celular, salario, nombre_cargo, nombre_dependencia, nombre_tipo_contrato, fecha_ingreso,fecha_termino FROM usuarios JOIN cargo on cargo.id_cargo = usuarios.id_cargo JOIN dependencia on dependencia.id_dependencia = usuarios.id_dependencia JOIN tipo_contrato on tipo_contrato.id_tipo_contrato = usuarios.id_tipo_contrato JOIN perfil on perfil.id_perfil = usuarios.id_perfil WHERE id_cedula= ?',(usuario,) )
    
    rows = cur.fetchall()
    return render ("empleado.html", rows=rows)
         


@app.route('/administrador', methods=["GET", "POST"])
def administrador():
    con = sql.connect("empleados.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    #cur.execute("SELECT id_cedula, nombre, apellido, direccion,correo, celular, salario, nombre_cargo, nombre_dependencia, nombre_tipo_contrato, nombre_perfil,password, fecha_ingreso,fecha_termino FROM usuarios JOIN cargo on cargo.id_cargo = usuarios.id_cargo JOIN dependencia on dependencia.id_dependencia = usuarios.id_dependencia JOIN tipo_contrato on tipo_contrato.id_tipo_contrato = usuarios.id_tipo_contrato JOIN perfil on perfil.id_perfil = usuarios.id_perfil")
    cur.execute("SELECT id_cedula,nombre,apellido,correo,direccion, celular,fecha_ingreso,fecha_termino, salario, password,nombre_cargo,nombre_perfil,nombre_dependencia,nombre_tipo_contrato,retroalimentacion,puntuacion,foto FROM usuarios JOIN cargo on usuarios.id_cargo = cargo.id_cargo JOIN dependencia on dependencia.id_dependencia = usuarios.id_dependencia JOIN perfil on usuarios.id_perfil = perfil.id_perfil JOIN tipo_contrato on usuarios.id_tipo_contrato = tipo_contrato.id_tipo_contrato")
    usuarios = cur.fetchall()
    con.close()
    return render ("administrador.html",usuarios=usuarios)



@app.route('/superadministrador', methods=["GET", "POST"])
def superadministrador():
    con = sql.connect("empleados.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT id_cedula,nombre,apellido,correo,direccion, celular,fecha_ingreso,fecha_termino, salario, password,nombre_cargo,nombre_perfil,nombre_dependencia,nombre_tipo_contrato,retroalimentacion,puntuacion,foto FROM usuarios JOIN cargo on usuarios.id_cargo = cargo.id_cargo JOIN dependencia on dependencia.id_dependencia = usuarios.id_dependencia JOIN perfil on usuarios.id_perfil = perfil.id_perfil JOIN tipo_contrato on usuarios.id_tipo_contrato = tipo_contrato.id_tipo_contrato")
    usuarios = cur.fetchall()
    con.close()
    return render ("superadministrador.html",usuarios=usuarios)
    

@app.route('/retornar')
def retornar():
    rol = str(session.get('id_perfil'))
    print("ROL", rol)

    if rol == '3':
        return redirect(url_for('superadministrador'))
    else:
        return redirect(url_for('administrador'))





@app.route('/CrearEmpleado', methods=["GET","POST"])
def CrearEmpleado():
   
    rol = str(session.get('id_perfil'))
    
    if rol == '2':
         form = fcrear(request.form)

    else:
        form = fcrearsa(request.form)

    if request.method == 'POST':  
        id=request.form['id']      
        nombre=request.form['nombre']  
        apellidos=request.form['apellidos']
        correo=request.form['correo']
        direccion=request.form['direccion']
        telefono=request.form['telefono'] 
        fechaingreso=request.form['fechaingreso']
        fechaterminacion=request.form['fechaterminacion']
        salario=request.form['salario']
        password=request.form['password']
        cargo=request.form['cargo']
        perfil=request.form['perfil']
        tipocontrato=request.form['tipocontrato']
        dependencia=request.form['dependencia']
        foto=request.files['foto']
        now = datetime.now()
        tiempo = now.strftime("%Y%M%H%S")
        if nombre=='' or apellidos=='' or correo=='' or direccion =='' or telefono=='' or fechaingreso =='' or salario=='' or password=='' or foto=='':
            flash('Debes diligenciar todos los datos')
            return redirect(url_for('crear'))
        if foto.filename !='':
            nuevonombrefoto=tiempo+foto.filename
            foto.save("uploads/"+nuevonombrefoto)
            
        query="INSERT INTO usuarios (id_cedula, nombre, apellido, correo, direccion, celular, fecha_ingreso,fecha_termino, salario, password, id_cargo, id_perfil, id_tipo_contrato,id_dependencia,foto ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?)"
        values=(id,nombre,apellidos,correo,direccion,telefono,fechaingreso,fechaterminacion,salario,password,cargo,perfil,tipocontrato, dependencia,nuevonombrefoto)
        cursor = get_db()
        cursor.execute(query,values)
        cursor.commit()
        cursor.close()  
        return render ("/CrearEmpleado.html", form=form)     
       
    return render ("/CrearEmpleado.html", form=form)  




@app.route('/guardar', methods=['POST'])
def almacenado():
    identificacion = request.form['identificacion']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    direccion = request.form['direccion']
    correo = request.form['correo']
    telefono = request.form['telefono']
    salario = request.form['salario']
    cargo = request.form['cargo']
    dependencia = request.form['dependencia']
    tipo_Contrato = request.form['Tipo_Contrato']
    fec_Ingreso = request.form['fec_Ingreso']
    fec_Termino = request.form['fec_Termino']
    perfil = request.form['perfil']
    password = request.form['password']
    foto = request.files['foto']

    now=datetime.now()
    time=now.strftime("%Y%H%M%S")
    if foto.filename!="":
        nombrefoto = time+foto.filename
        foto.save("uploads/"+nombrefoto)
     
        
    mysql= "INSERT INTO 'usuarios'('id_cedula','nombre','apellido','correo','direccion','celular','fecha_ingreso','fecha_termino','salario','password','id_cargo', 'id_perfil', 'id_dependencia', 'id_tipo_contrato', 'foto') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    datos=(identificacion,nombre,apellidos,correo,direccion,telefono,fec_Ingreso,fec_Termino,salario,password,cargo,perfil,dependencia,tipo_Contrato,foto.filename)
    con = sql.connect("empleados.db")
    cur = con.cursor()
    cur.execute(mysql,datos)    
    con.commit()
    
    return render("CrearEmpleado.html")


@app.route('/delete/<int:id_cedula>')#no se muestra hace la operacion y vuelve y carga el listado
def delete(id_cedula):
    cursor = get_db()
    select_borrar=cursor.execute("SELECT foto FROM usuarios WHERE id_cedula=?",(id_cedula,))  
    fila_borrar=select_borrar.fetchall()
    os.remove(os.path.join(app.config["rutafotos"],fila_borrar[0][0]))    
    print("validar porque esta entrando aqui quien te esta llamando ")
    print(type(id_cedula))
    cursor.execute("DELETE FROM usuarios WHERE id_cedula=?", (id_cedula,))
    cursor.commit()
    cursor.close() 
    return redirect('/administrador')




@app.route('/editar/<int:id>')
def edit(id):
    rol = str(session.get('id_perfil'))
    if rol == '2':
        db =get_db()
        cursor = get_db().execute("SELECT id_cedula,nombre,apellido,correo,direccion, celular,fecha_ingreso,fecha_termino, salario, password,nombre_cargo,nombre_dependencia,nombre_tipo_contrato,retroalimentacion,puntuacion,foto FROM usuarios left JOIN cargo on usuarios.id_cargo = cargo.id_cargo left JOIN dependencia on dependencia.id_dependencia = usuarios.id_dependencia left JOIN perfil on usuarios.id_perfil = perfil.id_perfil left JOIN tipo_contrato on usuarios.id_tipo_contrato = tipo_contrato.id_tipo_contrato WHERE id_cedula = ?",(id,))
        editado=cursor.fetchone()
        print(editado)
        db.commit()
        cursor.close() 
        return render('/editar.html',editado=editado)
    else:
        db =get_db()
        cursor = get_db().execute("SELECT id_cedula,nombre,apellido,correo,direccion, celular,fecha_ingreso,fecha_termino, salario, password,nombre_cargo,nombre_perfil,nombre_dependencia,nombre_tipo_contrato,retroalimentacion,puntuacion,foto FROM usuarios left JOIN cargo on usuarios.id_cargo = cargo.id_cargo left JOIN dependencia on dependencia.id_dependencia = usuarios.id_dependencia left JOIN perfil on usuarios.id_perfil = perfil.id_perfil left JOIN tipo_contrato on usuarios.id_tipo_contrato = tipo_contrato.id_tipo_contrato WHERE id_cedula = ?",(id,))
        editado=cursor.fetchone()
        print(editado)
        db.commit()
        cursor.close() 
        return render('/editarSa.html',editado=editado)


   
 
@app.route('/update', methods=['POST'])
def update():
    rol = str(session.get('id_perfil'))

    print("PERFIL UPDATE", rol)

    form = feditar(request.form) 
        
    if request.method == 'POST':  
        id=request.form['id']      
        nombre=request.form['nombre']  
        apellidos=request.form['apellidos']
        correo=request.form['correo']
        direccion=request.form['direccion']
        telefono=request.form['celular'] 
        fechaingreso=request.form['fecha_ingreso']
        fechaterminacion=request.form['fecha_termino']
        salario=request.form['salario']
        password=request.form['password']
        cargo=request.form['cargo']
        tipocontrato=request.form['contrato']
        dependencia=request.form['dependencia']
        retroalimentacion=request.form['retroalimentacion']
        puntuacion=request.form['puntuacion']
        foto=request.files['foto']
        now = datetime.now()
        tiempo = now.strftime("%Y%M%H%S")
        
        if rol == '3':
            perfil=request.form['perfil']

            query_update="UPDATE usuarios  SET nombre= ?, apellido= ?, correo= ?, direccion= ?, celular= ?, fecha_ingreso= ?,fecha_termino= ?, salario= ?, password= ?, id_cargo= ?, id_perfil= ?, id_tipo_contrato= ?,id_dependencia= ?, retroalimentacion=?, puntuacion=? WHERE id_cedula =?"
            values_update=(nombre,apellidos,correo,direccion,telefono,fechaingreso,fechaterminacion,salario,password,cargo,perfil,tipocontrato, dependencia, retroalimentacion, puntuacion, (id))
            cursor_update = get_db()
        
        else:
            query_update="UPDATE usuarios  SET nombre= ?, apellido= ?, correo= ?, direccion= ?, celular= ?, fecha_ingreso= ?,fecha_termino= ?, salario= ?, password= ?, id_cargo= ?, id_tipo_contrato= ?,id_dependencia= ?, retroalimentacion=?, puntuacion=? WHERE id_cedula =?"
            values_update=(nombre,apellidos,correo,direccion,telefono,fechaingreso,fechaterminacion,salario,password,cargo,tipocontrato, dependencia, retroalimentacion, puntuacion, (id))
            cursor_update = get_db()

        
        if foto.filename !='': 
            nuevonombrefoto=tiempo+foto.filename
            foto.save("uploads/"+nuevonombrefoto)
            #buscamos la foto y guadamos el id donde esta

            ejecutado=cursor_update.execute("SELECT foto FROM usuarios WHERE id_cedula=?",(id,))  
            fila=ejecutado.fetchall()
            os.remove(os.path.join(app.config["rutafotos"],fila[0][0]))
            cursor_update.execute("UPDATE usuarios SET foto=? WHERE id_cedula=? ",(nuevonombrefoto,id,))
            cursor_update.commit()   
        cursor_update.execute(query_update,values_update)
        cursor_update.commit()
        cursor_update.close()  
    return redirect(url_for('retornar'))






            
@app.route('/retroalimentacion', methods=["GET", "POST"]) #podria varias si solo es de consulta o si puede actulizar sus datos
def perfil():

    return render("/retroalimentacion.html")






if __name__ == "__main__":
    app.run(debug = True)
    
