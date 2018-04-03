from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from .models import *

DEVELOPER_KEY="AIzaSyBSmdXifs5uNzT9W9WjyybvMfEe2m0u730"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def video_search_and_accumulate(keywords, number_of_items):
    #turn on youtube data collector
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
    collected_videos_num = 0
    next_page_tokens = []
    for keyword in keywords:
        next_page_tokens.append(None)

    while collected_videos_num < number_of_items:
        for idx in range(0, len(keywords)):
            if next_page_tokens[idx] == None:
                search_response = youtube.search().list(
                    q = keywords[idx],
                    maxResults = 10,
                    part = "id, snippet",
                    order = "relevance",
                    videoEmbeddable = 'true',
                    type = "video",
                    relevanceLanguage = 'eng',
                    ).execute()
            else:
                search_response = youtube.search().list(
                    q = keywords[idx],
                    maxResults = 10,
                    part = "id, snippet",
                    order = "relevance",
                    videoEmbeddable = 'true',
                    type = "video",
                    pageToken = next_page_tokens[idx],
                    relevanceLanguage = 'eng',
                    ).execute()
            next_page_tokens[idx] = search_response.get("nextPageToken")
            for search_result in search_response.get("items", []):
                vtitle = search_result['snippet']['title']
                vid = search_result['id']['videoId']
                if Video.objects.filter(video_title = vtitle, video_url = vid).count() == 0:
                    new_video = Video(video_title = vtitle, video_url = vid)
                    new_video.save()
                    collected_videos_num += 1
                    print(vtitle, vid)

    return collected_videos_num
