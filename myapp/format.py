import re

from myapp.csv import Csv


class Format:
    def __init__(self):
        self.tag_template = '[[{tag}]]'

    def generate_youtube_wikiwiki_statement(
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

        # Generate caption if the video has collaborators
        csv = Csv()
        members = csv.init_members()
        collaborators = []

        for tag in tags:
            if members.count(tag) != 0 and tag != name \
                    and self.tag_template.format(tag=tag) not in collaborators:
                collaborators.append(self.tag_template.format(tag=tag))
        for member in members:
            if re.match(member, description) \
                    and self.tag_template.format(tag=member) not in collaborators:
                collaborators.append(self.tag_template.format(tag=member))

        collaborator_str = ''

        if len(collaborators) != 0 and caption_template:
            collaborator_str = '\n' + caption_template.format(collaborators=delimiter.join(collaborators))

        return video_str + collaborator_str
