from flask_restful import Resource
from flask import request

PLANIFICACIONES ={
    1:{'ejercicio':'Press de Banca' , 'series':'4' , 'repeticiones':'10',
        'ejercicio':'Press de Banca inclinado con mancuerna' , 'series':'4' , 'repeticiones':'10',
        'ejercicio':'Press de Banca declinado' , 'series':'4' , 'repeticiones':'10'},
    2:{'ejercicio':'Prensa en Maquina' , 'series':'3' , 'repeticiones':'15',
        'ejercicio':'Sentadillas' , 'series':'3' , 'repeticiones':'15',
        'ejercicio':'Peso Muerto' , 'series':'3' , 'repeticiones':'20'},
    3:{'ejercicio':'Curl de barra' , 'series':'3' , 'repeticiones':'20',
        'ejercicio':'Dominadas' , 'series':'2' , 'repeticiones':'10',
        'ejercicio':'Dominadas de agarre invertido' , 'series':'2' , 'repeticiones':'10',}
}

PLANIFICACION_ALUMNO = {
    1:{"id":"1","id_plan":"1"},
    2:{"id":"2","id_plan":"2"}
}

class PlanificacionAlumno(Resource):
    def get(self,id):
        if int(id) in PLANIFICACION_ALUMNO:
            return PLANIFICACION_ALUMNO[int(id)]
        return "", 404
    
class PlanificacionesProfesores(Resource):
    def get(self):
        return PLANIFICACIONES

    def post(self):
        planificacion = request.get_json()
        id = int(max(PLANIFICACIONES.keys()))+1
        PLANIFICACIONES[id] = planificacion
        return PLANIFICACIONES[id], 201
    
class PlanificacionProfesor(Resource):
    def get(self,id):
        if int(id) in PLANIFICACIONES:
            return PLANIFICACIONES[int(id)]
        return "", 404
    
    def put(self,id):
        if int(id) in PLANIFICACIONES:
            planificacion = PLANIFICACIONES[int(id)]
            data = request.get_json()
            planificacion.update(data)
            return "", 201
        return "", 404
    
    def delete(self,id):
        if int(id) in PLANIFICACIONES:
            del PLANIFICACIONES[int(id)]
            return "", 204
        return "", 404