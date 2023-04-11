from flask_restful import Resource

PROFESORES = {
    1: {"nombre":"Sebastian","apellido":"Fernandez","Clases":"Crossfit",}
}

class ProfesorClases(Resource):
     def get(self):
        return PROFESORES