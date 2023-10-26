import os
from googleapiclient.discovery import build
from isodate import parse_duration


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_info()['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + f"{playlist_id}"
        self.video_properties = self.get_video_properties()

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def get_playlist_info(self):
        """Метод возвращает словарь с данными о плейлисте по его ID"""
        dict_playlist_info = self.get_service().playlists().list(id=self.playlist_id,
                                                                 part='snippet',
                                                                 maxResults=50).execute()
        return dict_playlist_info

    def get_playlist_items(self):
        """Метод возвращает словарь с данными о видеороликах плейлиста по его ID"""
        playlist_response = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                    part='contentDetails',
                                                                    maxResults=50).execute()
        return playlist_response

    def get_id_videos(self):
        """Метод для построения списка из videoID"""
        id_videos = []
        for video in self.get_playlist_items()['items']:
            id_videos.append(video['contentDetails']['videoId'])
        return id_videos

    def get_video_descriptions(self):
        """Метод возвращает описание каждого видео"""
        video_description = self.get_service().videos().list(id=','.join(self.get_id_videos()),
                                                             part='contentDetails,statistics',
                                                             maxResults=50).execute()
        return video_description

    def get_video_properties(self):
        """Метод для сбора данных о длительности видео и количестве лайков"""
        video_properties = []
        for video in self.get_video_descriptions()['items']:
            dict_properties = {
                'duration': parse_duration(video['contentDetails']['duration']),
                'like_count': int(video['statistics']['likeCount']),
                'video_url': 'https://youtu.be/' + video['id'],
            }
            video_properties.append(dict_properties)
        return video_properties

    @property
    def total_duration(self):
        """Метод возвращает суммарную длительность всех видео из плейлиста"""
        total_duration = parse_duration('PT0S')
        for item in self.video_properties:
            total_duration += item['duration']
        return total_duration

    def show_best_video(self):
        """Метод возвращает ссылку на самое популярное видео из плейлиста"""
        best_video = max(self.video_properties, key=lambda item: item['like_count'])
        return best_video['video_url']


# pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
# print(pl.get_playlist_info())
# print(pl.title)
# print(pl.url)
# print(pl.get_playlist_items())
# print(pl.get_id_videos())
# print(pl.get_video_descriptions())
# print(pl.get_video_properties())
# print(pl.total_duration)
# duration = pl.total_duration
# print(duration.total_seconds())
# print(pl.show_best_video())
