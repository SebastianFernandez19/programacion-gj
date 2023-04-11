import os
from flask import Flask
from dotenv import load_dotenv

# Importamos nuevas librerias clase 3
from flask_restful import Api  # Agrego la clase API

# Importo dir de recursos
import main.resources as resources

# Inicio Restful
api = Api()
# metodo que inicializa la app y todos los modulos


def create_app():

    # inicio de flask
    app = Flask(__name__)

# variables de entono
    load_dotenv()
    # cargar a la API el recurso y especificar la ruta

    api.add_resource(resources.UsuariosResource, "/usuarios")

    api.add_resource(resources.UsuarioResource, "/usuario/<id>")

    api.add_resource(resources.UsuarioAlumnoResource, "/usuario_alumno/<id>")

    api.add_resource(resources.UsuarioProfesorResource, "/usuario_profesor/<id>")

    api.add_resource(resources.UsuariosAlumnosResource, "/usuarios_alumnos")

    api.add_resource(resources.PlanificacionAlumnoResource, "/planificacion_alumno/<id>")

    api.add_resource(resources.PlanificacionProfesorResource, "/planificaciones_profesores/<id>")

    api.add_resource(resources.PlanificacionesProfesoresResource, "/planificacion_profesor")

    api.add_resource(resources.ProfesorClasesResource, "/profesor_clases")

    api.add_resource(resources.PagoResource, "/pago/<id>")

    api.add_resource(resources.LoginResource, "/login")

    # Cargar la aplicacion en la API de Flask Restful
    # es para que la aplicacion de flask funcione como API
    api.init_app(app)
    # Por ultimo retornamos la aplicacion iniializada
    return app
