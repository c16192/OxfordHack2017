#!/usr/bin/python
# -*- coding: utf-8 -*-

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAEOu3ZZ0vXNjeY5Tq7135KWERE2u4zLTo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def youtube_search(options):
  try:
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      maxResults=options.max_results
    ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        video = {}
        video["title"] = removeNonAscii(search_result["snippet"]["title"])
        video["id"] = removeNonAscii(search_result["id"]["videoId"])
        video["image"] = removeNonAscii(search_result["snippet"]["thumbnails"]["default"]["url"])
        videos.append(video)
    return json.dumps(videos)
  except():
    return json.dumps([])

def youtube(keyword, maxResults=25):
  args = argparser.parse_args([])
  if not hasattr(args, 'q'):
    argparser.add_argument("--q", help="Search term", default='')
  if not hasattr(args, 'max_results'):
    argparser.add_argument("--max-results", help="Max results", default=25)
  argparser.set_defaults(q=keyword)
  argparser.set_defaults(max_results=maxResults)
  args = argparser.parse_args([])
  print(args)
  string = youtube_search(args)
  print(string[0:200])
  return string

if __name__ == "__main__":
  youtube("Google")