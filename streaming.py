facebook_access_token = "EAADMZBhiQHmEBAAcr8eJJVUYoMx8sZBwDFY2zA8nV8srPQP7am8AYbR5GElbHsTGpFfq6oUxP59mEzSZAZAHf4dCkvp4EWdjaJwolpiFxnwYf3DvUeluq1p0BLQFOHZCW8pmhxQqlqttGe9sNZCdrNrDV3O1noywWfaxpCoa9vnrnSOJr2RErngKi224W7IGEZD"

import requests, datetime, json2html
from obswebsocket import obsws
from obswebsocket import requests as obs_requests
from flask import Flask, render_template
import youtube_streaming as yts
from optparse import OptionParser
import time, datetime, pytz
import os, random, shutil

app = Flask(__name__)

facebook_persistent_stream_key = "3439972949350996?s_bl=1&s_ps=1&s_psm=1&s_sw=0&s_vt=api-s&a=AbzGvRYtQHVKAwyC"
obs_host = "ssnj-streaming.duckdns.org"
obs_port = 4444
obs_password = "kaur"
SCENE_MAIN_NAME="Main"
SCENE_PRERECORDED_NAME='Pre-recorded'

def getLabelBasedOnTime():
    if(datetime.datetime.now().time().hour < 12):
        return "Morning Programme"
    else:
        return "Evening Programme"
params = (
    ('status', 'LIVE_NOW'),
    ('title', getLabelBasedOnTime()),
    ('access_token', facebook_access_token),
)

def getStreamInfo():
    response = requests.post('https://graph.facebook.com/v9.0/610250765656576/live_videos', params=params)
    print(response.json())
    stream_url = response.json()['stream_url'].split("/rtmp/")
    url = stream_url[0] + "/rtmp/"
    key = stream_url[1]
    return [url, key]

@app.route('/startOBSStreaming')
def startOBS(url='', key='', scene=SCENE_MAIN_NAME):
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    if(url):
        ws.call(obs_requests.StopStreaming())
        ws.call(obs_requests.SetCurrentScene(scene))
        ws.call(obs_requests.SetStreamSettings('rtmp_custom', {'bwtest': False, 'key': key, 'server': url, 'use_auth': False}, True))
    ws.call(obs_requests.StartStreaming())
    ws.disconnect()
    return getStreamingStatus()

@app.route('/startStreaming')
def startStreaming():
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    ws.call(obs_requests.StartStreaming())
    ws.disconnect()
    return getStreamingStatus()

@app.route('/startYoutubeStreaming')
def startYoutubeSteaming():
    parser = OptionParser()
    parser.add_option("--broadcast-title", dest="broadcast_title", help="Broadcast title",
                      default=getLabelBasedOnTime())
    parser.add_option("--privacy-status", dest="privacy_status",
                      help="Broadcast privacy status", default="public")
    parser.add_option("--start-time", dest="start_time",
                      help="Scheduled start time",
                      default=(datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(seconds=5)).isoformat())
    # parser.add_option("--end-time", dest="end_time",
    #  help="Scheduled end time", default='2021-03-31T00:00:00.000Z')
    parser.add_option("--stream-title", dest="stream_title", help="Stream title",
                      default="SSNJ: " + getLabelBasedOnTime())
    (options, args) = parser.parse_args()

    youtube = yts.get_authenticated_service()
    broadcast_id = yts.insert_broadcast(youtube, options)
    [stream_id, url, key] = yts.insert_stream(youtube, options)
    print("Stream url is '%s' and key is '%s'" % (url, key))
    yts.bind_broadcast(youtube, broadcast_id, stream_id)
    time.sleep(10)
    startOBS(url, key)
    startStreaming()
    # yts.broadcast_transition(youtube, broadcast_id, "live")
    return getStreamingStatus()

# python -c "from streaming import *; startFacebookStreaming()"
@app.route('/startFacebookStreaming')
def startFacebookStreaming():
    [url, key] = getStreamInfo()
    return startOBS(url, key)

# python -c "from streaming import *; stopStreaming()"
@app.route('/stopStreaming')
def stopStreaming():
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    ws.call(obs_requests.StopStreaming())
    # go to the main scene when done
    ws.call(obs_requests.SetCurrentScene(SCENE_MAIN_NAME))
    ws.disconnect()
    return getStreamingStatus()

@app.route('/obs')
def getStreamingStatus():
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    retVal = str(ws.call(obs_requests.GetStreamSettings()))
    retVal += str(ws.call(obs_requests.GetStreamingStatus()))
    ws.disconnect()
    return json2html.html_escape(retVal)

@app.route('/setOBSSettingsWithPersistentKey')
def setOBSSettingsWithPersistentKey():
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    ws.call(obs_requests.StopStreaming())
    ws.call(obs_requests.SetStreamSettings('rtmp_common', {'bwtest': False,
               'key': facebook_persistent_stream_key,
               'server': 'rtmps://rtmp-api.facebook.com:443/rtmp/',
               'service': 'Facebook Live'}, True))
    ws.disconnect()
    return getStreamingStatus()

### Pre-recorded sessions
@app.route('/streamPreRecordedAsaDiWarToFacebook')
def streamPreRecordedAsaDiWar():
    return streamPreRecorded(folder='adw')

PRE_RECORDED_BASE_FOLDER = "D:/daljeet/videos"
SELECTED_VIDEO_FULL_FILE = "D:/daljeet/videos/selected_video.mp4"
def streamPreRecorded(folder):
    currentSessionSelectedFile = PRE_RECORDED_BASE_FOLDER+'/'+folder +'/'+ random.choice(os.listdir(PRE_RECORDED_BASE_FOLDER+'/'+folder))
    shutil.copy(currentSessionSelectedFile, SELECTED_VIDEO_FULL_FILE)
    [url, key] = getStreamInfo()
    return startOBS(url, key, SCENE_PRERECORDED_NAME)

### Web functions ###
@app.route('/')
def links():
    html = "OBS Commands</br>"
    html += "<a href='/obs'>OBS Info</a></br>"
    html += "<a href='/setOBSSettingsWithPersistentKey'>Set OBS persistent key</a></br>"
    html += "<a href='/startOBSStreaming'>Start OBS streaming (settings are not changed)</a></br>"

    html += "<br/><br/><br/><br/>"
    html += "Facebook Commands</br>"
    html += "<b>Be careful with the commands below</b><br/>"
    html += "<a href='/startFacebookStreaming'>Start Facebook Streaming</a></br>"
    html += "<a href='/stopStreaming'>Stop Streaming</a></br>"

    html += "<br/><br/><br/><br/>"
    html += "Youtube Commands</br>"
    html += "<b>Be careful with the commands below</b><br/>"
    html += "<a href='/startYoutubeStreaming'>Start Youtube Streaming</a></br>"
    html += "<a href='/stopStreaming'>Stop Streaming</a></br>"

    html += "<br/><br/><br/><br/>"
    html += "Pre-recorded Commands</br>"
    html += "<a href='/streamPreRecordedAsaDiWarToFacebook'>Pre-recorded Asa Di War to Facebook</a></br>"

    html += "<br/><br/><br/><br/>"
    html += "<a href='/privacy'>Privacy</a></br>"
    html += "<a href='/about'>About</a></br>"
    return html

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', message="Privacy Policy")

from waitress import serve
def serveWeb():
    serve(app, host='0.0.0.0', port=8000, threads=1)  # WAITRESS!

if __name__ == "__main__":
    #startStreaming()
    #getStreamingStatus()
    serveWeb()
    #setOBSSettingsWithPersistentKey()
    #getStreamingStatus()
    #streamPreRecordedAsaDiWar()
