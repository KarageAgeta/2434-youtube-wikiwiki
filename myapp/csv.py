import csv


class Csv:
    def __init__(self):
        self.tag_template = '[[{tag}]]'

    def init_members(self) -> list:
        with open('static/members.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # remove header

            members = []
            for row in reader:
                members.append(row[0])

        return members

    def read_youtube_template_list(self) -> dict:
        with open('static/youtube_template.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # remove header

            names = []
            templates = []
            caption_templates = []
            delimiters = []
            for row in reader:
                names.append(row[0])
                templates.append(row[1])
                caption_templates.append(row[2])
                delimiters.append(row[3])

        return {
            'names': names,
            'templates': templates,
            'caption_templates': caption_templates,
            'delimiters': delimiters
        }

    def read_youtube_channel_list(self) -> list:
        with open('static/youtube_channel.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # remove header

            channels = []
            for row in reader:
                channels.append(row[2])

        return channels

    def generate_channel_ids(self, name, title, id):
        with open('static/youtube_channel.csv', mode='a') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator='\n')
            writer.writerow([name, title, id])
