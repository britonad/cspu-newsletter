import os
from flask import Flask
from flask_basicauth import BasicAuth

from core import settings

app = Flask(__name__)
env = os.environ.get('ENV', 'dev')
if env == 'prod':
    app.config.from_object(settings.Prod)
    app.template_folder = settings.Prod.TEMPLATE_DIR
    app.static_folder = settings.Prod.STATIC_DIR
elif env == 'dev':
    app.config.from_object(settings.Dev)
    app.template_folder = settings.Dev.TEMPLATE_DIR
    app.static_folder = settings.Dev.STATIC_DIR
else:
    raise EnvironmentError(
        'ENV variable not specified or specified wrong value.'
    )

basic_auth = BasicAuth(app)

from app import newsletter_bp

app.register_blueprint(newsletter_bp)
