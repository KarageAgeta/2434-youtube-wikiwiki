import datetime
import re

from myapp.api.youtube import Youtube
from myapp.csv import Csv


class Base:
    def __init__(self, app):
        self.app = app
        self.csv = Csv()
        self.youtube = Youtube(app)

        self.date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.filename_template = '{name}_' + self.date + '.csv'
        self.members = self.csv.init_members()
        self.tag_template = '[[{tag}]]'

    def generate_youtube_wikiwiki(self, date: str, names: list) -> list:
        channel_template_list = self.csv.read_youtube_template_list()

        channel_id_list = self.csv.read_youtube_channel_list()
        # channel_ids = self.__format_channel_ids(channel_id_list['names'], channel_id_list['channels'], names)

        for i in range(len(channel_id_list['names'])):
            self.__generate_youtube_video_url(channel_id_list['channels'][i], channel_id_list['names'][i])

        for name in names:
            videos = []
            for i in range(len(channel_id_list['names'])):
                filename = self.filename_template.format(name=channel_id_list['names'][i])
                videos = self.csv.read_video_from_name(filename, name)

                self.__format_wikiwiki_statement(
                    channel_ids,
                    channel_template_list['templates'],
                    channel_template_list['caption_templates'],
                    channel_template_list['delimiters'],
                    channel_template_list['names'],
                    date
                )

        return result

    # private

    def __format_channel_ids(self, youtube_names: list, youtube_channels: list, names: list) -> list:
        channel_ids = []
        for i in range(len(youtube_names)):
            # TODO : fix
            if names:
                for name in names:
                    if youtube_names[i] == name:
                        channel_ids.append(youtube_channels)
            else:
                channel_ids.append(youtube_channels[i])

        return channel_ids

    def __generate_youtube_video_url(self, channel_id: str, name: str):
        youtube_list = self.youtube.fetch_video_list(channel_id)
        filename = self.filename_template.format(name=name)

        for item in youtube_list:
            # Generate caption if the video has any collaborators
            collaborators = []
            for tag in item['tags']:
                # Search collaborators from description
                for member in self.members:
                    if re.match(member, item['description']):
                        collaborators.append(tag)
                # Search collaborators from tags
                if self.members.count(tag) != 0 and tag != name and collaborators.count(tag) == 0:
                    collaborators.append(tag)

            self.csv.write_video(
                filename,
                item['id'],
                '', # item['name'],
                item['title'],
                item['url'],
                item['published_at'],
                ','.join(collaborators)
            )

    # TODO : fix
    def __format_wikiwiki_statement(
            self,
            video_list: list,
            templates: list,
            caption_templates: list,
            delimiters: list,
            names: list,
            date: str = None
    ) -> list:
        wikiwiki = []
        for item in video_list:
            if date and item['published_at'] < date:
                continue
            wikiwiki.insert(0, self.__generate_youtube_wikiwiki_statement(
                templates[i],
                caption_templates[i],
                delimiters[i],
                names[i],
                item['title'],
                item['description'],
                item['url'],
                item['published_at'],
                item['title'],
            ))

        return wikiwiki

    def __generate_youtube_wikiwiki_statement(
            self, template: str,
            caption_template: str,
            delimiter: str,
            name: str,
            title: str,
            description: str,
            url: str,
            published_at: str,
            tags: list,
    ) -> str:
        video_str = template.format(
            title=title,
            published_at=published_at,
            url=url
        )

        # Generate caption if the video has any collaborators
        csv = Csv()
        members = csv.init_members()
        collaborators = []
        for tag in tags:
            if members.count(tag) != 0 and tag != name:
                collaborators.append(self.tag_template.format(tag=tag))
            else:
                for member in members:
                    if re.match(member, description):
                        collaborators.append(self.tag_template.format(tag=member))

        collaborator_str = ''
        if len(collaborators) != 0:
            collaborator_str = '\n' + caption_template.format(collaborators=delimiter.join(collaborators))

        return video_str + collaborator_str
