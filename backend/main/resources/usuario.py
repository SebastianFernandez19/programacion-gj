from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel, ProfesorModel, PlanificacionModel
import regex
from datetime import datetime
from sqlalchemy import func, desc

# Datos de prueba en JSON
#USUARIOS ={
#     1: {"nombre":"Sebastian","apellido":"Fernandez"},
#     2: {"nombre":"Marcos","apellido":"Diaz"},
#     3: {"nombre":"Natalio","apellido":"Hercovich"}
# }

# USUARIO_PROFESOR ={
#     1: {"nombre":"Sebastian","apellido":"Fernandez"}
# }

# usuarios_alumnosLUMNO ={
#     1:{"nombre":"Marcos","apellido":"Diaz"},
#     2:{"nombre":"Natalio","apellido":"Hercovich"}
# }

class Usuario(Resource):
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()

    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key.lower(), value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class Usuarios(Resource):
    def get(self):
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify([usuario.to_json() for usuario in usuarios])

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            return 'Formato Incorrecto', 400
        return usuario.to_json(), 201
    
class UsuarioAlumno(Resource):
    def get(self, id):
        usuario_alumno = db.session.query(UsuarioModel).get_or_404(id)
        return usuario_alumno.to_json()

    def put(self, id):
        usuario_alumno = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario_alumno, key.lower(), value)
        db.session.add(usuario_alumno)
        db.session.commit()
        return usuario_alumno.to_json(), 201
    
class UsuariosAlumnos(Resource):
    def get(self):
            page = 1
            per_page = 10
            
            usuarios_alumnos = db.session.query(UsuarioModel)
            
            if request.args.get('page'):
                page = int(request.args.get('page'))
            if request.args.get('per_page'):
                per_page = int(request.args.get('per_page'))
            
            if request.args.get('apellido'):
                usuarios_alumnos=usuarios_alumnos.filter(UsuarioModel.apellido.like("%"+request.args.get('apellido')+"%"))
            
            if request.args.get('sortby_apellido'):
                usuarios_alumnos=usuarios_alumnos.order_by(desc(UsuarioModel.apellido))


            if request.args.get('nombre'):
                usuarios_alumnos=usuarios_alumnos.filter(UsuarioModel.nombre.like("%"+request.args.get('nombre')+"%"))
            
            if request.args.get('sortby_nombre'):
                usuarios_alumnos=usuarios_alumnos.order_by(desc(UsuarioModel.nombre))


            if request.args.get('nrPlanificaciones'):
                usuarios_alumnos=usuarios_alumnos.outerjoin(UsuarioModel.planificaciones).group_by(UsuarioModel.id).having(func.count(PlanificacionModel.id) >= int(request.args.get('nrPlanificaciones')))

            if request.args.get('sortby_nrPlanificaciones'):
                usuarios_alumnos=usuarios_alumnos.outerjoin(UsuarioModel.Planificaciones).group_by(UsuarioModel.id).order_by(func.count(PlanificacionModel.id).desc())
            
            
            usuarios_alumnos = usuarios_alumnos.paginate(page=page, per_page=per_page, error_out=True, max_per_page=30)

            return jsonify({'usuarios': [usuario_a.to_json() for usuario_a in usuarios_alumnos],
                    'total': usuarios_alumnos.total,
                    'pages': usuarios_alumnos.pages,
                    'page': page
                    })

    def post(self):
        usuarios_alumnos = UsuarioModel.from_json(request.get_json())
        db.session.add(usuarios_alumnos)
        db.session.commit()
        return usuarios_alumnos.to_json(), 201
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
            page = 1
            per_page = 10
            
            usuario_profesores = db.session.query(ProfesorModel)
            
            if request.args.get('page'):
                page = int(request.args.get('page'))
            if request.args.get('per_page'):
                per_page = int(request.args.get('per_page'))
            
            if request.args.get('apellido'):
                usuario_profesores=usuario_profesores.filter(ProfesorModel.apellido.like("%"+request.args.get('apellido')+"%"))
            
            if request.args.get('sortby_apellido'):
                usuario_profesores=usuario_profesores.order_by(desc(ProfesorModel.apellido))


            if request.args.get('nombre'):
                usuario_profesores=usuario_profesores.filter(ProfesorModel.nombre.like("%"+request.args.get('nombre')+"%"))
            
            if request.args.get('sortby_nombre'):
                usuario_profesores=usuario_profesores.order_by(desc(ProfesorModel.nombre))


            if request.args.get('nrPlanificaciones'):
                usuario_profesores=usuario_profesores.outerjoin(ProfesorModel.planificaciones).group_by(ProfesorModel.id).having(func.count(PlanificacionModel.id) >= int(request.args.get('nrPlanificaciones')))
            
            if request.args.get('sortby_nrPlanificaciones'):
                usuario_profesores=usuario_profesores.outerjoin(ProfesorModel.Planificaciones).group_by(ProfesorModel.id).order_by(func.count(PlanificacionModel.id).desc())
            
            
            usuario_profesores = usuario_profesores.paginate(page=page, per_page=per_page, error_out=True, max_per_page=30)

            return jsonify({'usuarios': [usuario_p.to_json() for usuario_p in usuario_profesores],
                    'total': usuario_profesores.total,
                    'pages': usuario_profesores.pages,
                    'page': page
                    })

    def post(self):
        usuario_profesores = ProfesorModel.from_json(request.get_json())
        db.session.add(usuario_profesores)
        db.session.commit()
        return usuario_profesores.to_json(), 201