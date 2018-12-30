from flask import Flask

from myapp import config

__version__ = '0.1'
app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
