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
@with_appcontext
def generate_youtube_wikiwiki(date):
    format = Format()
    csv = Csv()
    channel_template_list = csv.read_youtube_template_list()
    channel_ids = csv.read_youtube_channel_list()
    youtube = Youtube(app)

    result = []
    for i in range(len(channel_ids)):
        youtube_list = youtube.fetch_video_list(channel_ids[i])

        for item in youtube_list:
            if date and item['published_at'] < date:
                continue
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
        break


@app.cli.command(help='Generate Channel ID')
@with_appcontext
def generate_youtube_channel_id():
    youtube = Youtube(app)
    csv = Csv()
    members = csv.init_members()

    for member in members:
        channel = youtube.fetch_channel_list(member)
        csv.generate_channel_ids(channel['name'], channel['channel_name'], channel['channel_id'])


if __name__ == 'run' or __name__ == 'main':
    load_dotenv(find_dotenv())
    config_name = os.getenv('FLASK_CONFIG', 'default')
    create_app(config_name)
