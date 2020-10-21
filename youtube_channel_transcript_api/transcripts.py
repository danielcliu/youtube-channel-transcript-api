import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
import googleapiclient.errors
import json

yt_api_url = 'https://www.googleapis.com/youtube/v3/'

class YoutubePlaylistTranscripts():
    def __init__(self, name, pid, key):
        self.name = name
        self.video = self._get_playlist_videos(pid, key)

    def _get_playlist_videos(self, pid, key):
        video_ids = []
        params = {
                'part': 'snippet',
                'maxResults': 50,
                'playlistId': pid,
                'key': key,
                'pageToken': ''
                }
        while True:
            response = requests.get(f'{yt_api_url}playlistItems', params = params)
            response.raise_for_status()
            playlists = response.json()
            video_ids += [ [item['snippet']['title'], item['snippet']['resourceId']['videoId']] for item in playlists['items']]
            page_token = playlists.get('nextPageToken')
            
            if page_token:
                params.update({'pageToken':  page_token})
            else:
                break
        return video_ids

    def get_transcripts(self, languages=['en'], proxies=None, cookies=None, just_text=False):
        videos_that_erred = []
        video_data = {}
        for video in self.video:
            transcript = self._get_transcript(video, videos_that_erred, languages, proxies, cookies, just_text) 
            if transcript: 
                video_data.update(transcript)
        return video_data, videos_that_erred

    def write_transcripts(self, file_path, languages=['en'], proxies=None, cookies=None, just_text=False):
        videos_that_erred = []
        for video in self.video:
            transcript = self._get_transcript(video, videos_that_erred, languages, proxies, cookies, just_text) 
            filepath=f'{file_path}{video[0].replace(" ", "_")}.json'
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(transcript, f, indent=4)

        return videos_that_erred

    def _get_transcript(self, video, videos_that_erred, languages, proxies, cookies, just_text):
        transcript_json = None
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video[1], languages=languages, proxies=proxies, cookies=cookies)
            if just_text:
                transcript_json = {video[1]: {'title': video[0], 'captions': ' '.join([item['text'] for item in transcript])}}
            else: 
                transcript_json = {video[1]: {'title': video[0], 'captions': transcript}}
        except Exception as exception:
            videos_that_erred.append(video)
        return transcript_json


class YoutubeChannelTranscripts(YoutubePlaylistTranscripts):
    def __init__(self, name, key):
        self.channel_name, self.pid = self._get_channel_playlist(name, key)
        super().__init__(self.channel_name, self.pid, key)

    def _get_channel_playlist(self, name, key):
        channel_id = self._get_channel_id(name, key)
        return self._get_channel_playlist_id(channel_id, key)

    def _get_channel_id(self, name, key):
        params = {
                'part': 'snippet',
                'q': name,
                'type': 'channel',
                'key': key,
                }
        
        response = requests.get(f'{yt_api_url}search', params = params)
        response.raise_for_status()
        channel_search = response.json()
        for item in channel_search['items']:
            if item['snippet']['title'] == name:
                return item['snippet']['channelId']
        return channel_search['items'][0]['snippet']['channelId']

    def _get_channel_playlist_id(self, channel_id, key):
        params = {
                'part': 'snippet,contentDetails',
                'id': channel_id,
                'key': key,
                }
        
        response = requests.get(f'{yt_api_url}channels', params = params)
        response.raise_for_status()
        channel = response.json()['items'][0]
        return channel['snippet']['title'], channel['contentDetails']['relatedPlaylists']['uploads']
