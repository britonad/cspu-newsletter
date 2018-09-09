import os
from flask import Flask
from flask_basicauth import BasicAuth

try:
    from core import local_settings as settings
except ImportError:
    from core import settings

basic_auth = BasicAuth()


def create_app():
    """
    This function creates application with predefined settings that depends on
    environment variable of a system.
    :return: Flask application instance.
    """

    application = Flask(
        __name__,
        template_folder=settings.TEMPLATE_DIR,
        static_folder=settings.STATIC_DIR
    )
    environment = os.environ.get('APP_ENV', 'dev')
    environments = {
        'dev': settings.Dev,
        'prod': settings.Prod
    }
    if environment in environments:
        application.config.from_object(environments[environment])
    else:
        raise EnvironmentError('Application variable has not been specified.')

    # Init of third-party libs.
    basic_auth.init_app(application)

    # Register blueprints
    from app.views import newsletter_bp
    application.register_blueprint(newsletter_bp)

    return application
