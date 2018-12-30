import os

from dotenv import load_dotenv, find_dotenv
from flask.cli import with_appcontext

from myapp import app, create_app


@app.cli.command(help='Generate WIKIWIKI.jp statement from Youtube API')
@with_appcontext
def generate_youtube_wikiwiki():
    pass


# private

if __name__ == 'run' or __name__ == 'main':
    load_dotenv(find_dotenv())
    config_name = os.getenv('FLASK_CONFIG', 'default')
    create_app(config_name)
