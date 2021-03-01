#!/usr/bin/python
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json, configparser, os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
api_key=config['youtube']['api_key']
refresh_token=config['youtube']['refresh_token']
client_secret=config['youtube']['client_secret']

SCOPES = ['https://www.googleapis.com/auth/youtube']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# store this value if the refresh token has expired
def get_refresh_token():
    #flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow = InstalledAppFlow.from_client_secrets(client_secret, SCOPES)
    credentials = flow.run_console()

def get_authenticated_service():
    cs = json.loads(client_secret)['installed']
    credentials = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri=cs['token_uri'],
        client_id=cs['client_id'],
        client_secret=cs['client_secret']
    )
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

def insert_broadcast(youtube, options):
  insert_broadcast_response = youtube.liveBroadcasts().insert(
    part="snippet,status,contentDetails",
    body=dict(
      kind='youtube#liveBroadcast',
      snippet=dict(
        title=options.broadcast_title,
        scheduledStartTime=options.start_time,
        #scheduledEndTime=options.end_time
        ),
      status=dict(
        privacyStatus=options.privacy_status,
        selfDeclaredMadeForKids=False
      ),
      contentDetails=dict(
          enableAutoStart=True,
          enableAutoStop=True
      )
    )).execute()

  snippet = insert_broadcast_response["snippet"]
  print("Broadcast '%s' with title '%s' was published at '%s'" % (insert_broadcast_response["id"], snippet["title"], snippet["publishedAt"]))
  return insert_broadcast_response["id"]

def get_broadcast(youtube, broadcast_id):
    broadcast_response = youtube.liveBroadcasts().list(
        part="status", id=broadcast_id).execute()
    broadcast_response = broadcast_response["items"][0]
    print("Broadcast '%s' was retrieved" % (broadcast_id))
    return broadcast_response

def get_stream(youtube, stream_id):
    stream_response = youtube.liveStreams().list(
        part="status", id=stream_id).execute()
    stream_response = stream_response["items"][0]
    print("Stream '%s' was retrieved" % (stream_response["id"]))
    return stream_response

def insert_stream(youtube, options):
  insert_stream_response = youtube.liveStreams().insert(
    part="snippet,cdn",
    body=dict(
      kind='youtube#liveStream',
      snippet=dict(
        title=options.stream_title
        ),
      cdn=dict(
       format="1080p",
       ingestionType="rtmp",
       resolution="variable",
       frameRate="variable"
    ))).execute()
  snippet = insert_stream_response["snippet"]
  cdn = insert_stream_response["cdn"]["ingestionInfo"]
  print("Stream '%s' with title '%s' was inserted" % (insert_stream_response["id"], snippet["title"]))
  return [insert_stream_response["id"],cdn["rtmpsIngestionAddress"],cdn["streamName"]]


def bind_broadcast(youtube, broadcast_id, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id).execute()

  print("Broadcast '%s' was bound to stream '%s'." % (bind_broadcast_response["id"], bind_broadcast_response["contentDetails"]["boundStreamId"]))

def broadcast_transition(youtube, broadcast_id, status):
    transition_state_response = youtube.liveBroadcasts().transition(
        part="status",
        id=broadcast_id,
        broadcastStatus=status
    ).execute()
