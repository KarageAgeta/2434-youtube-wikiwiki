import os

from dotenv import load_dotenv, find_dotenv
from flask.cli import with_appcontext

from myapp import app, create_app
from myapp.format import Format
from myapp.youtube import Youtube


@app.cli.command(help='Generate WIKIWIKI.jp statement from Youtube API')
@with_appcontext
def generate_youtube_wikiwiki():
    format = Format()
    channel_template_list = format.generate_youtube_template_list()
    channel_ids = channel_template_list['channel_ids']
    youtube = Youtube(app)

    result = []
    for i in range(len(channel_ids)):
        youtube_list = youtube.fetch_video_list(channel_ids[i])

        for item in youtube_list:
            result.insert(0, format.generate_youtube_wikiwiki_statement(channel_template_list['templates'][i], item))

        for item in result:
            print(item)
            # with open('tmp.txt', mode='a') as f:
            #     f.write(item + '\n')


if __name__ == 'run' or __name__ == 'main':
    load_dotenv(find_dotenv())
    config_name = os.getenv('FLASK_CONFIG', 'default')
    create_app(config_name)
