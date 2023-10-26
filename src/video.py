import os
from googleapiclient.discovery import build


class Video:
    """Класс инициализируется по 'id видео'"""
    def __init__(self, video_id):
        self.video_id = video_id

        try:
            self.dict_info = self.get_video_info(video_id)
            self.title = self.dict_info['items'][0]['snippet']['title']
            self.video_url = 'https://www.youtube.com/watch?v=' + self.video_id
            self.view_count = self.dict_info['items'][0]['statistics']['viewCount']
            self.like_count = self.dict_info['items'][0]['statistics']['likeCount']
        except IndexError:
            self.dict_info = None
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def get_video_info(cls, video_id):
        dict_video_info = cls.get_service().videos().list(part='snippet,statistics,topicDetails', id=video_id).execute()
        return dict_video_info


class PLVideo(Video):
    """Класс инициализируется по 'id видео' и 'id плейлиста'"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
