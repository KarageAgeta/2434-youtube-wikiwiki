import dateutil.parser
import requests
import json

# TODO : Move to models
from myapp.util import chunks


class Youtube:
    base_api_url = 'https://www.googleapis.com/youtube/v3/'
    key_page_info = 'pageInfo'
    key_total_results = 'totalResults'
    key_items = 'items'
    key_next_page_token = 'nextPageToken'

    def __init__(self, app):
        self.config = app.config
        self.search_url = self.base_api_url + 'search?part=snippet&order=date&type=video&videoSyndicated=true' \
                                              '&channelId={channel_name}&key={api_key}'
        self.video_url = self.base_api_url + 'videos?part=snippet&id={video_ids}&key={api_key}'
        self.next_token = None

    def fetch_video_list(self, channel_name: str) -> list:
        search_url = self.search_url.format(api_key=self.config['YOUTUBE_API_KEY'], channel_name=channel_name)
        data = json.loads(requests.get(search_url).text)

        if not data.get(self.key_page_info) or data.get(self.key_page_info).get(self.key_total_results) == 0:
            return []

        ids = []
        for item in data[self.key_items]:
            ids.append(item['id']['videoId'])
        self.next_token = data.get(self.key_next_page_token)

        while True:
            if not self.next_token or len(self.next_token) == 0:
                break

            data = json.loads(requests.get(search_url + '&pageToken=' + self.next_token).text)
            self.next_token = data.get(self.key_next_page_token)
            for item in data[self.key_items]:
                ids.append(item['id']['videoId'])

        return self.__fetch_video_detail(ids)

    # private

    def __fetch_video_detail(self, ids: list) -> list:
        result = []
        for id_list in list(chunks(ids, 5)):
            url = self.video_url.format(api_key=self.config['YOUTUBE_API_KEY'], video_ids=','.join(id_list))
            data = json.loads(requests.get(url).text)
            if not data.get(self.key_page_info) or data.get(self.key_page_info).get(self.key_total_results) == 0:
                return []

            for item in data[self.key_items]:
                result.append({
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': 'https://www.youtube.com/watch?v=' + item['id'],
                    'published_at': dateutil.parser.parse(item['snippet']['publishedAt']).strftime('%Y/%m/%d'),
                    'tags': item['snippet']['tags']
                })

        return result
