import os

import click
from dotenv import load_dotenv, find_dotenv
from flask.cli import with_appcontext

from myapp import app, create_app
from myapp.csv import Csv
from myapp.format import Format
from myapp.youtube import Youtube


@app.cli.command(help='Generate WIKIWIKI.jp statement from Youtube API')
@click.option('--date')
@click.option('--names')
@with_appcontext
def generate_youtube_wikiwiki(date: str, names: str):
    format = Format()
    csv = Csv()
    youtube = Youtube(app)

    channel_template_list = csv.read_youtube_template_list()
    channel_id_list = csv.read_youtube_channel_list()

    channel_ids = []
    for i in range(len(channel_id_list['names'])):
        if names:
            for name in names.split(','):
                if channel_id_list['names'][i] == name:
                    channel_ids.append(channel_id_list['channels'][i])
        else:
            channel_ids.append(channel_id_list['channels'][i])

    result = []
    for i in range(len(channel_ids)):
        youtube_list = youtube.fetch_video_list(channel_ids[i], date)

        for item in youtube_list:
            result.insert(0, format.generate_youtube_wikiwiki_statement(
                channel_template_list['templates'][i],
                channel_template_list['caption_templates'][i],
                channel_template_list['delimiters'][i],
                channel_template_list['names'][i],
                item['title'],
                item['description'],
                item['url'],
                item['published_at'],
                item['title'],
            ))

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
        name = channel['name'] if 'name' in channel else ''
        channel_name = channel['channel_name'] if 'channel_name' in channel else ''
        channel_id = channel['channel_id'] if 'channel_id' in channel else ''
        csv.generate_channel_ids(name, channel_name, channel_id)


if __name__ == 'run' or __name__ == 'main':
    load_dotenv(find_dotenv())
    config_name = os.getenv('FLASK_CONFIG', 'default')
    create_app(config_name)
