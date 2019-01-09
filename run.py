import os

import click
from dotenv import load_dotenv, find_dotenv
from flask.cli import with_appcontext

from myapp import app, create_app
from myapp.base import Base
from myapp.csv import Csv
from myapp.api.youtube import Youtube


@app.cli.command(help='Generate WIKIWIKI.jp statement from Youtube API')
@click.option('--date')
@click.option('--names')
@with_appcontext
def generate_youtube_wikiwiki(date: str, names: str):
    base = Base(app)
    name_list = names.split(',') if names else []
    result = base.generate_youtube_wikiwiki(date, name_list)

    for item in result:
        print(item)
        # with open('tmp.txt', mode='a') as f:
        #     f.write(item + '\n')


@app.cli.command(help='Generate Channel ID')
@with_appcontext
def generate_youtube_channel_id():
    youtube = Youtube(app)
    csv = Csv()
    members = csv.init_members()

    for member in members:
        channel = youtube.fetch_channel_list(member)
        csv.write_channel_id(channel['name'], channel['channel_name'], channel['channel_id'])


if __name__ == 'run' or __name__ == 'main':
    load_dotenv(find_dotenv())
    config_name = os.getenv('FLASK_CONFIG', 'default')
    create_app(config_name)
