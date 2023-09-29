import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        # в 15 строке я вообще не поняла, что произошлo, метод научного "пальцем в глаз")
        self.info = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.info['items'][0]['snippet']['title']
        self.description = self.info['items'][0]['snippet']['description']
        self.url = self.info['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriberCount = self.info['items'][0]['statistics']['subscriberCount']
        self.videoCount = self.info['items'][0]['statistics']['videoCount']
        self.viewCount = self.info['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.info, indent=2, ensure_ascii=False))
