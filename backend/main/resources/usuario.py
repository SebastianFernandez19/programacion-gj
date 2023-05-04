from flask_restful import Resource
from flask import request
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuariosModel, ProfesorModel, AlumnoModel
import regex
from datetime import datetime

# Datos de prueba en JSON
#USUARIOS ={
#     1: {"nombre":"Sebastian","apellido":"Fernandez"},
#     2: {"nombre":"Marcos","apellido":"Diaz"},
#     3: {"nombre":"Natalio","apellido":"Hercovich"}
# }

# USUARIO_PROFESOR ={
#     1: {"nombre":"Sebastian","apellido":"Fernandez"}
# }

# USUARIOS_ALUMNO ={
#     1:{"nombre":"Marcos","apellido":"Diaz"},
#     2:{"nombre":"Natalio","apellido":"Hercovich"}
# }

class Usuario(Resource):
    def get(self, id):
        usuario = db.session.query(UsuariosModel).get_or_404(id)
        return usuario.to_json()

    def put(self, id):
        usuario = db.session.query(UsuariosModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key.lower(), value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

    def delete(self, id):
        usuario = db.session.query(UsuariosModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class Usuarios(Resource):
    def get(self):
        usuarios = db.session.query(UsuariosModel).all()
        return jsonify([usuario.to_json() for usuario in usuarios])

    def post(self):
        usuario = UsuariosModel.from_json(request.get_json())
        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            return 'Formato Incorrecto', 400
        return usuario.to_json(), 201
    
class UsuarioAlumno(Resource):
    def get(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        return alumno.to_json()

    def put(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(alumno, key.lower(), value)
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json(), 201
    
class UsuariosAlumnos(Resource):
    def get(self):
        alumnos = db.session.query(AlumnoModel).all()
        return jsonify([alumno.to_json() for alumno in alumnos])

    def post(self):
        alumno = AlumnoModel.from_json(request.get_json())
        exist = db.session.query(UsuariosModel).get_or_404(alumno.id)
        try:
            db.session.add(alumno)
            db.session.commit()
        except:
            return 'Formato Incorrecto', 400
        return alumno.to_json(), 201

class UsuarioProfesor(Resource):
    def get(self, id):
        profesor = db.session.query(ProfesorModel).get_or_404(id)
        return profesor.to_json()

    def put(self, id):
        profesor = db.session.query(ProfesorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            if regex.match(r"\d{2}/\d{2}/\d{4}", str(value)) != None:
                setattr(profesor, key.lower(), datetime.strptime(value, "%d/%M/%Y"))
            else: setattr(profesor, key.lower(), value)
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json() , 201

class UsuarioProfesores(Resource):
    def get(self):
        profesores = db.session.query(ProfesorModel).all()
        return jsonify([profesor.to_json() for profesor in profesores])

    def post(self):
        try:
            profesor = ProfesorModel.from_json(request.get_json())
        except:
            return 'Formato Incorrecto', 400
        exist = db.session.query(UsuariosModel).get_or_404(profesor.id)
        db.session.add(profesor)
        db.session.commit()
        return profesor.to_json(), 201
