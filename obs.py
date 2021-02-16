import sys
import time

import logging
logging.basicConfig(level=logging.INFO)

from obswebsocket import obsws, requests  # noqa: E402


host = "ssnj-streaming.duckdns.org"
port = 4444
password = "kaur"

ws = obsws(host, port, password)
ws.connect()
baseRequest = ws.call(requests.GetStreamSettings())

print(baseRequest)

ws.call(requests.SetStreamSettings('rtmp_custom', {'bwtest': False, 'key': '417399328?s_bl=1&s_psm=1&s_sc=4173993372615613&s_sw=0&s_vt=api-s&a=Abw6vccFNpU5EITH', 'server': 'rtmps://live-api-s.facebook.com:443/rtmp', 'use_auth': False}, True))
baseRequest = ws.call(requests.GetStreamSettings())
print(baseRequest)

print(ws.call(requests.GetStreamingStatus()))
ws.call(requests.StartStreaming())
print(ws.call(requests.GetStreamingStatus()))

ws.disconnect()