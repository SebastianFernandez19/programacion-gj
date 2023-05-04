from flask_restful import Resource
from flask import request
from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import PlanificacionModel

# Datos de prueba en JSON
#
# PLANIFICACIONES ={
#     1:{'ejercicio':'Press de Banca' , 'series':'4' , 'repeticiones':'10',
#         'ejercicio':'Press de Banca inclinado con mancuerna' , 'series':'4' , 'repeticiones':'10',
#         'ejercicio':'Press de Banca declinado' , 'series':'4' , 'repeticiones':'10'},
#     2:{'ejercicio':'Prensa en Maquina' , 'series':'3' , 'repeticiones':'15',
#         'ejercicio':'Sentadillas' , 'series':'3' , 'repeticiones':'15',
#         'ejercicio':'Peso Muerto' , 'series':'3' , 'repeticiones':'20'},
#     3:{'ejercicio':'Curl de barra' , 'series':'3' , 'repeticiones':'20',
#         'ejercicio':'Dominadas' , 'series':'2' , 'repeticiones':'10',
#         'ejercicio':'Dominadas de agarre invertido' , 'series':'2' , 'repeticiones':'10',}
# }

# PLANIFICACION_ALUMNO = {
#     1:{"id":"1","id_plan":"1"},
#     2:{"id":"2","id_plan":"2"}
# }

class PlanificacionAlumno(Resource):
    def get(self,id):
        planificacion_a=db.session.query(PlanificacionModel).get_or_404(id)
        return planificacion_a.to_json()
    
class PlanificacionesProfesores(Resource):
    def get(self,id):
        id_profesor = request.args.get("id_profesor")
        planificaciones = db.session.query(PlanificacionModel)
        if id_profesor:
            planificaciones = planificaciones.filter(PlanificacionModel.id_profesor == id_profesor)
        planificaciones = planificaciones.all()
        return jsonify({"planificaciones": [planificacion.to_json() for planificacion in planificaciones]})

    def post(self):
        planificacion = PlanificacionModel.from_json(request.get_json())
        print(planificacion)
        try:
            db.session.add(planificacion)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return planificacion.to_json(), 201
    
class PlanificacionProfesor(Resource):
    def get(self,id):
        planificacion_p=db.session.query(PlanificacionModel).get_or_404(id)
        return planificacion_p.to_json()
    
    def put(self,id):
        planificacion_p=db.session.query(PlanificacionModel).get_or_404(id)
        data=request.get_json().items
        for key, value in data:
            setattr(planificacion_p, key, value)
        db.session.add(planificacion_p)
        db.session.commit()
        return planificacion_p.to_json(), 201
    
    def delete(self,id):
        planificacion_p=db.session.query(PlanificacionModel).get_or_404(id)
        db.session.delete(planificacion_p)
        db.session.commit()
        return "", 204
    