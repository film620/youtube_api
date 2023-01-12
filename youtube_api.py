#!/usr/bin/python
import httplib2
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Variable
video_id = "bwvK9F8Ones"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# 계정 oauth
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

# 상태 수정
def update_video(youtube, options):
  videos_list_response = youtube.videos().list(
    id=video_id,
    part='status'
  ).execute()

  if not videos_list_response["items"]:
    print("Video '%s' was not found." % options.video_id)
    sys.exit(1)

  videos_list_status = videos_list_response["items"][0]["status"]

  if "privacyStatus" not in  videos_list_status:
    videos_list_status["privacyStatus"] = []

  videos_list_status["privacyStatus"] = 'private'

  videos_update_response = youtube.videos().update(
    part='status',
    body=dict(
      status=videos_list_status,
      id=video_id
    )).execute()


if __name__ == "__main__":
  argparser.add_argument("--video-id", help="ID of video to update.", required=True)
  argparser.add_argument("--privacyStatus")
  args = argparser.parse_args()

  youtube = get_authenticated_service(args)
  
  try:
    update_video(youtube, args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("Tag '%s' was added to video id '%s'." % (args.privacyStatus, args.video_id))


'''
   1. 유투브 계정 로그인 패스워드 넣기
   2. 수정할 영상 링크 넣기 
   3. 상태변경 시간 넣기
   4. 예약 걸기
   5. 예약 리스트(추가 삭제 수정))
'''