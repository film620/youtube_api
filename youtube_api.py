#!/usr/bin/python
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from datetime import datetime, timedelta

import os
import sys
sys.path.append(
  os.path.join(os.path.dirname(__file__), 'mysite')
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from django.conf import settings
from youtubeOnOff.models import OnOff

CLIENT_SECRETS_FILE = "/Users/yo_mac/youtube/client_secrets.json"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# 계정 oauth
def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE, message='MISSING_CLIENT_SECRETS_MESSAGE')
  storage = Storage("%s-oauth2.json" % '/Users/yo_mac/youtube/youtube_api.py')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    print('Error (args)')
    #credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

# 상태 수정
def update_video(youtube, video_id, privacy_status):
  videos_list_response = youtube.videos().list(
    id=video_id,
    part='status'
  ).execute()

  if not videos_list_response["items"]:
    print("Video '%s' was not found." % video_id)
    sys.exit(1)

  videos_list_status = videos_list_response["items"][0]["status"]

  if "privacyStatus" not in  videos_list_status:
    videos_list_status["privacyStatus"] = []

  videos_list_status["privacyStatus"] = privacy_status

  videos_update_response = youtube.videos().update(
    part='status',
    body=dict(
      status=videos_list_status,
      id=video_id
    )).execute()

def get_onoff_list(youtube):
  onoff_list = OnOff.objects.all()
  now = datetime.now()

  seoul_time = now + timedelta(hours=9)
  print('#### ' + seoul_time.strftime('%Y-%m-%d %H:%M') + ' ####')

  for onoff in onoff_list:
    if is_same_time(now, onoff.work_time):
      try:
        update_video(youtube, onoff.video_id, onoff.privacy_status)
      except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      else:
        print("Tag '%s' was added to video id '%s'." % (onoff.privacy_status, onoff.video_id))

  print(" ")

def is_same_time(time1: datetime, time2: datetime):
  return time1.year == time2.year and time1.month == time2.month and time1.day == time2.day and time1.hour == time2.hour and time1.minute == time2.minute

if __name__ == "__main__":
  youtube = get_authenticated_service()
  get_onoff_list(youtube)