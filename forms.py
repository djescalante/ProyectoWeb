from flask import Flask
from flask import flash, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField,validators
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, email, length
from wtforms.fields.html5 import EmailField, DateField
import os
from datetime import datetime
from wtforms.fields.html5 import EmailField, DateField


class flogin(FlaskForm):
    usuario = StringField('Usuario', validators =[
        DataRequired(),
        length(max=30, min=1)
    ])
    password = PasswordField('Contraseña', validators =[
        DataRequired(),
        length(max=30, min=1)
    ])
    perfil = SelectField("perfil  ",choices=[("1","Empleado"),("2","Administrador"),("3","SuperAdmin")])

    submit = SubmitField('Iniciar sesion')
    
class fempleado(FlaskForm):
    id = StringField('Cedula')
    nombre = StringField('Nombre')
    apellidos = StringField('Apellidos')
    correo = StringField('Correo')
    identificacion = StringField('Identificacion')
    direccion = StringField('Direccion')
    telefono = StringField('Telefono')
    fechaingreso = StringField('Fecha de Ingreso')
    tipocontrato = StringField('Tipo de Contrato')
    fechaterminacion = StringField('Fecha de Terminacion')
    cargo = StringField('Cargo')
    dependencia = StringField('Dependencia')
    salario = StringField('Salario')
    retroalimentacion = TextAreaField('Retroalimentacion')
    puntaje = StringField('Puntaje')
    submit = SubmitField('Cerrar sesion')

class feditar(FlaskForm):
    id = StringField('id')
    nombre = StringField('nombre')
    apellidos = StringField('apellidos')
    correo = StringField('correo')
    direccion = StringField('direccion')
    telefono = StringField('celular')
    fechaingreso = DateField('Fecha_ingreso',[validators.Required()], format='%d/%m/%Y')
    fechaterminacion = DateField('fecha_termino',[validators.Required()], format='%d/%m/%Y')
    salario = StringField('Salario')
    password =PasswordField('Password')
    cargo = SelectField("Cargo ",choices=[("1","Gerente"),("2","Analista"),("3","Profesional")])
    perfil = SelectField("perfil ",choices=[("1","Empleado")])
    dependencia = SelectField("Dependencia ",choices=[("1","Contabilidad"),("2","Administrativo"),("3","Comercial")])
    tipocontrato = SelectField("contrato ",choices=[("1","Termino Fijo"),("2","Indefinido"),("3","Prestacion de Servicios"),("4","Obra Labor")])
    retroalimentacion = TextAreaField('retroalimentacion')
    puntuacion = StringField('puntuacion')
    foto = FileField('Fotografia')
    gsubmit = SubmitField('Guardar')
    csubmit = SubmitField('Regresar')


class feditarsa(FlaskForm):
    id = StringField('id')
    nombre = StringField('nombre')
    apellidos = StringField('apellidos')
    correo = StringField('correo')
    direccion = StringField('direccion')
    telefono = StringField('celular')
    fechaingreso = DateField('Fecha_ingreso',[validators.Required()], format='%d/%m/%Y')
    fechaterminacion = DateField('fecha_termino',[validators.Required()], format='%d/%m/%Y')
    salario = StringField('Salario')
    password =PasswordField('Password')
    cargo = SelectField("Cargo ",choices=[("1","Gerente"),("2","Analista"),("3","Profesional")])
    perfil = SelectField("perfil ",choices=[("1","Empleado"), ("1","administrador"), ("1","superadministrador")])
    dependencia = SelectField("Dependencia ",choices=[("1","Contabilidad"),("2","Administrativo"),("3","Comercial")])
    tipocontrato = SelectField("contrato ",choices=[("1","Termino Fijo"),("2","Indefinido"),("3","Prestacion de Servicios"),("4","Obra Labor")])
    retroalimentacion = TextAreaField('retroalimentacion')
    puntuacion = StringField('puntuacion')
    foto = FileField('Fotografia')
    gsubmit = SubmitField('Guardar')
    csubmit = SubmitField('Regresar')



class fcrear(FlaskForm):
    id = StringField('Cedula')
    nombre = StringField('Nombre')
    apellidos = StringField('Apellidos')
    correo = StringField('Correo')
    direccion = StringField('Direccion')
    telefono = StringField('Telefono')
    fechaingreso = DateField('Fecha de Ingreso',[validators.Required()], format='%d/%m/%Y')
    fechaterminacion = DateField('Fecha de Terminacion',[validators.Required()], format='%d/%m/%Y')
    tipocontrato = SelectField("Cargo ",choices=[("1","Termino Fijo"),("2","Indefinido"),("3","Prestacion de Servicios"),("4","Obra Labor")])
    cargo = SelectField("Cargo ",choices=[("1","Gerente"),("2","Analista"),("3","Profesional")])
    dependencia = SelectField("Dependencia ",choices=[("1","Contabilidad"),("2","Administrativo"),("3","Comercial")])
    perfil = SelectField("perfil ",choices=[("1","Empleado")])
    password =PasswordField('Password')
    salario = StringField('Salario')
    foto = FileField('Fotografia')
    gsubmit = SubmitField('Guardar')
    csubmit = SubmitField('Cancelar')
    vsubmit = SubmitField('Volver')

class fcrearsa(FlaskForm):
    id = StringField('Cedula')
    nombre = StringField('Nombre')
    apellidos = StringField('Apellidos')
    correo = StringField('Correo')
    direccion = StringField('Direccion')
    telefono = StringField('Telefono')
    fechaingreso = DateField('Fecha de Ingreso',[validators.Required()], format='%d/%m/%Y')
    fechaterminacion = DateField('Fecha de Terminacion',[validators.Required()], format='%d/%m/%Y')
    tipocontrato = SelectField("Cargo ",choices=[("1","Termino Fijo"),("2","Indefinido"),("3","Prestacion de Servicios"),("4","Obra Labor")])
    cargo = SelectField("Cargo ",choices=[("1","Gerente"),("2","Analista"),("3","Profesional")])
    dependencia = SelectField("Dependencia ",choices=[("1","Contabilidad"),("2","Administrativo"),("3","Comercial")])
    perfil = SelectField("perfil ",choices=[("1","Empleado"),("2","Administrador"),("3","SuperAdmin")])
    password =PasswordField('Password')
    salario = StringField('Salario')
    foto = FileField('Fotografia')
    gsubmit = SubmitField('Guardar')
    csubmit = SubmitField('Cancelar')
    vsubmit = SubmitField('Volver')
