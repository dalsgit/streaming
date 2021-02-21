1.Get code: 
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=306115041451-pprkk87q52jt7cfn7paq137i3blb4ri5.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube&access_type=offline

Code: [copy from browser and replace in the curl command below]: 4/1AY0e-g6Eo0SfkfXLKXTO-A1KZg0g1EC7oYrtiQbGidIlLcviZpl78TziTys 

2. Get access_token and refresh_token
curl --request POST --data "code=4/1AY0e-g6Eo0SfkfXLKXTO-A1KZg0g1EC7oYrtiQbGidIlLcviZpl78TziTys&client_id=306115041451-pprkk87q52jt7cfn7paq137i3blb4ri5.apps.googleusercontent.com&client_secret=ZiTezQR_tRxCYvXsXJQGYeng&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&grant_type=authorization_code" https://accounts.google.com/o/oauth2/token

{
  "access_token": "ya29.A0AfH6SMCdzbnNPvlIgMlmFQFkXfSOhxn6lJ82fZkNM1j0_R3FtaFp5rMxfNy6UZJfZ9lP6yImgjnKkS_V_vjFvJ-E076Dfy2mSWs730jQHmGnA4bxFiYbOKQFr1aAyv8ptk2mRjoGMu_fV9kURKDiriL38XLZ",
  "expires_in": 3599,
  "refresh_token": "1//0dp4stKKErTTpCgYIARAAGA0SNwF-L9IrJglQ9IYCfB1dnK15REgaHx7f3HRX8zqfgvqS_-oeVDg9tXsgPWsGRc_cY4qQKx0p1mk",
  "scope": "https://www.googleapis.com/auth/youtube",
  "token_type": "Bearer"
}

Refresh Token:[copy from curl response and replace in the curl command below]:
1//0dSH4X8ZeWH7QCgYIARAAGA0SNwF-L9Iratt9Gw7Exl9nvS82VlO2_Q_vA2AmGqoEJlkI54tt99T56egGENpN-oB6pVp80grMQS8

3.Get new access_token using refresh_token
curl --request POST --data "client_id=306115041451-pprkk87q52jt7cfn7paq137i3blb4ri5.apps.googleusercontent.com&client_secret=ZiTezQR_tRxCYvXsXJQGYeng&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&refresh_token=1//0dSH4X8ZeWH7QCgYIARAAGA0SNwF-L9Iratt9Gw7Exl9nvS82VlO2_Q_vA2AmGqoEJlkI54tt99T56egGENpN-oB6pVp80grMQS8&grant_type=refresh_token" https://accounts.google.com/o/oauth2/token​


curl --request POST https://youtube.googleapis.com/youtube/v3/videos?part=snippet&access_token=ya29.a0AfH6SMAe1t3LaNzezsL08FLIqY_d-bwvTjinqAK_zbCn4INDt8Rq4Wl8TCe1Mgzu69TdTJEUhS4_uBRSS7Gb8yrVsJzqhQpLBUI4B2GYhC3U3cJw_iWdtC0vorTsYd22McebH6bQFGAf7WFNkt6ZnJfsnCuiPO9vUQmwNCvXo_4&key=AIzaSyC2maF-9v1KW2Z9KMd9CX3Rj1NhqXpdOYM


curl --request POST \
  'https://youtube.googleapis.com/youtube/v3/liveBroadcasts?part=snippet&part=status&key=[YOUR_API_KEY]' \
  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{"snippet":{"title":"test","scheduledStartTime":"2021-02-17T23:48:46.46Z","description":"Test"},"status":{"privacyStatus":"private"}}' \
  --compressed


{
  "kind": "youtube#liveBroadcast",
  "etag": "OPdCPl5wRJNGLbHKpDKeKOW6az0",
  "id": "iUPe56GsxVk",
  "snippet": {
    "publishedAt": "2021-02-17T01:04:47Z",
    "channelId": "UCYO6niUZFQf_--K1Hfb0Cvg",
    "title": "test",
    "description": "Test",
    "thumbnails": {
      "default": {
        "url": "https://i9.ytimg.com/vi/iUPe56GsxVk/default_live.jpg?sqp=CJDVsYEG&rs=AOn4CLAwcEEdkowKYFlksLvype3ccRglGQ",
        "width": 120,
        "height": 90
      },
      "medium": {
        "url": "https://i9.ytimg.com/vi/iUPe56GsxVk/mqdefault_live.jpg?sqp=CJDVsYEG&rs=AOn4CLA9IYMjq8wGDGJK4klCvRwO_KQoRQ",
        "width": 320,
        "height": 180
      },
      "high": {
        "url": "https://i9.ytimg.com/vi/iUPe56GsxVk/hqdefault_live.jpg?sqp=CJDVsYEG&rs=AOn4CLBNItc5_F9Cwgk6Ur674tGLmA3BHg",
        "width": 480,
        "height": 360
      }
    },
    "scheduledStartTime": "2021-02-17T23:48:46Z",
    "isDefaultBroadcast": false,
    "liveChatId": "Cg0KC2lVUGU1NkdzeFZrKicKGFVDWU82bmlVWkZRZl8tLUsxSGZiMEN2ZxILaVVQZTU2R3N4Vms"
  },
  "status": {
    "lifeCycleStatus": "created",
    "privacyStatus": "private",
    "recordingStatus": "notRecording",
    "madeForKids": false,
    "selfDeclaredMadeForKids": false
  }
}
