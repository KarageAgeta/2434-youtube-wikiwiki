import csv
import re


class Format:
    def __init__(self):
        self.tag_template = '[[{tag}]]'
        self.members = self.__init_members()

    def generate_youtube_template_list(self) -> dict:
        with open('static/youtube_template.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # remove header

            names = []
            channel_ids = []
            templates = []
            caption_templates = []
            delimiters = []
            for row in reader:
                names.append(row[0])
                channel_ids.append(row[1])
                templates.append(row[2])
                caption_templates.append(row[3])
                delimiters.append(row[4])

        return {
            'names': names,
            'channel_ids': channel_ids,
            'templates': templates,
            'caption_templates': caption_templates,
            'delimiters': delimiters
        }

    def generate_youtube_wikiwiki_statement(
            self,
            template: str,
            caption_template: str,
            delimiter: str,
            name: str,
            item: dict
    ) -> str:
        video_str = template.format(
            title=item['title'],
            published_at=item['published_at'],
            url=item['url']
        )

        # Generate caption if the video has any collaborators
        collaborators = []
        for tag in item['tags']:
            if self.members.count(tag) != 0 and tag != name:
                collaborators.append(self.tag_template.format(tag=tag))
            else:
                for member in self.members:
                    if re.match(member, item['description']):
                        collaborators.append(self.tag_template.format(tag=member))

        collaborator_str = ''
        if len(collaborators) != 0:
            collaborator_str = '\n' + caption_template.format(collaborators=delimiter.join(collaborators))

        return video_str + collaborator_str

    # private

    def __init_members(self) -> list:
        with open('static/members.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # remove header

            members = []
            for row in reader:
                members.append(row[0])

        return members
