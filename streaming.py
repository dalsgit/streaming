access_token = "EAADMZBhiQHmEBAMoxflbDpbkWrHZAGo8RXJ812ZA8Hd5A1mWvEdVsDxW7nZBKjGq8kOEswiqPCrZBsgmjbipwZCD0xLo5efyMy8diTiqwsc1vZA0bfA5XKRZBXRvYPEPOqKJp2FPNlQ9DrCZBpaSPzgf9hknBCzhpmHCfZBXy5UyZCUu0BoxDLhRxrc7sJBXNeelwAZD"

import requests, datetime, json2html
from obswebsocket import obsws
from obswebsocket import requests as obs_requests
from flask import Flask
app = Flask(__name__)

facebook_persistent_stream_key = "3439972949350996?s_bl=1&s_ps=1&s_psm=1&s_sw=0&s_vt=api-s&a=AbzGvRYtQHVKAwyC"
obs_host = "ssnj-streaming.duckdns.org"
obs_port = 4444
obs_password = "kaur"

def getLabelBasedOnTime():
    if(datetime.datetime.now().time().hour < 12):
        return "Morning Programme"
    else:
        return "Evening Programme"
params = (
    ('status', 'LIVE_NOW'),
    ('title', getLabelBasedOnTime()),
    ('access_token', access_token),
)

def getStreamInfo():
    response = requests.post('https://graph.facebook.com/v9.0/610250765656576/live_videos', params=params)
    print(response.json())
    stream_url = response.json()['stream_url'].split("/rtmp/")
    url = stream_url[0] + "/rtmp/"
    key = stream_url[1]
    return [url, key]

@app.route('/startOBSStreaming')
def startOBS(url='', key=''):
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    if(url):
        ws.call(obs_requests.StopStreaming())
        ws.call(obs_requests.SetStreamSettings('rtmp_custom', {'bwtest': False, 'key': key, 'server': url, 'use_auth': False}, True))
    ws.call(obs_requests.StartStreaming())
    ws.disconnect()
    return getStreamingStatus()

# python -c "from streaming import *; startStreaming()"
@app.route('/startFacebookStreaming')
def startStreaming():
    [url, key] = getStreamInfo()
    return startOBS(url, key)

# python -c "from streaming import *; stopStreaming()"
@app.route('/stopStreaming')
def stopStreaming():
    ws = obsws(obs_host, obs_port, obs_password)
    ws.connect()
    ws.call(obs_requests.StopStreaming())
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
    return html

from waitress import serve
def serveWeb():
    serve(app, host='0.0.0.0', port=8000, threads=1)  # WAITRESS!

if __name__ == "__main__":
    #startStreaming()
    #getStreamingStatus()
    serveWeb()
    #setOBSSettingsWithPersistentKey()
    #getStreamingStatus()
