# services/cert_server/project/__init__.py


import os

from flask import Flask


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions

    # register blueprints
    from project.api.cert_server import cert_server_blueprint
    app.register_blueprint(cert_server_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
        }

    return app
